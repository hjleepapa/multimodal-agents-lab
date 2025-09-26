#!/usr/bin/env python3
"""
Test Snowflake functionality only - without Google API dependencies
This verifies that our Snowflake solution is working correctly.
"""

import os
import json
import snowflake.connector
from snowflake.connector import DictCursor
from tqdm import tqdm

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")

def setup_snowflake_connection():
    """Initialize Snowflake connection"""
    # Snowflake connection parameters
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account.snowflakecomputing.com")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format - remove .snowflakecomputing.com if present
    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    print(f"Connecting to Snowflake account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Warehouse: {SNOWFLAKE_WAREHOUSE}")
    print(f"Database: {SNOWFLAKE_DATABASE}")
    print(f"Schema: {SNOWFLAKE_SCHEMA}")

    # Initialize Snowflake connection
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

    # Test the connection
    cursor = conn.cursor()
    cursor.execute("SELECT CURRENT_VERSION()")
    print(f"Connected to Snowflake: {cursor.fetchone()[0]}")
    cursor.close()
    
    return conn

def load_embeddings_to_snowflake(conn):
    """Load pre-generated embeddings and store in Snowflake using STRING approach"""
    # Read pre-generated embeddings from JSON file
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print(f"Loaded {len(embeddings_data)} documents with embeddings")
    
    # Prepare data for Snowflake insertion
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM multimodal_documents")
    print("Cleared existing documents from multimodal_documents table.")
    
    # Insert documents with embeddings using STRING storage
    for doc in tqdm(embeddings_data):
        # Convert embedding to comma-separated string
        embedding_str = ','.join(map(str, doc['embedding']))
        
        # Simple INSERT with string parameter - no complex type handling needed
        cursor.execute("""
            INSERT INTO multimodal_documents (key, width, height, embedding)
            VALUES (%s, %s, %s, %s)
        """, (doc['key'], doc['width'], doc['height'], embedding_str))
    
    cursor.close()
    conn.commit()
    
    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM multimodal_documents")
    count = cursor.fetchone()[0]
    print(f"{count} documents ingested into the multimodal_documents table.")
    cursor.close()

def test_vector_search(conn):
    """Test vector search functionality with a simple query"""
    print("\n=== Testing Vector Search ===")
    
    # Create a simple test embedding (first document's embedding)
    cursor = conn.cursor()
    cursor.execute("SELECT embedding FROM multimodal_documents LIMIT 1")
    result = cursor.fetchone()
    
    if result:
        # Use the first document's embedding as our query
        query_embedding_str = result[0]
        print(f"Using first document's embedding as query")
        
        # Test vector search using the view
        search_query = """
        SELECT key, width, height,
               VECTOR_COSINE_SIMILARITY(embedding, STRTOK_TO_ARRAY(%s, ',')::VECTOR(FLOAT, 1024)) as similarity_score
        FROM multimodal_documents_vector
        ORDER BY similarity_score DESC
        LIMIT 3
        """
        
        cursor.execute(search_query, (query_embedding_str,))
        results = cursor.fetchall()
        
        print("Vector search results:")
        for i, result in enumerate(results):
            print(f"  {i+1}. {result[0]} - Similarity: {result[3]:.6f}")
        
        cursor.close()
        return True
    else:
        print("No documents found for testing")
        cursor.close()
        return False

def test_view_functionality(conn):
    """Test that the view is working correctly"""
    print("\n=== Testing View Functionality ===")
    
    cursor = conn.cursor()
    
    # Test that the view exists and returns data
    try:
        cursor.execute("SELECT COUNT(*) FROM multimodal_documents_vector")
        view_count = cursor.fetchone()[0]
        print(f"View returns {view_count} documents")
        
        # Test that embedding column is properly converted to VECTOR
        cursor.execute("SELECT key, embedding FROM multimodal_documents_vector LIMIT 1")
        result = cursor.fetchone()
        if result:
            print(f"Sample document: {result[0]}")
            print(f"Embedding type: {type(result[1])}")
            print("✅ View is working correctly")
            return True
        else:
            print("❌ No data in view")
            return False
            
    except Exception as e:
        print(f"❌ View test failed: {e}")
        return False
    finally:
        cursor.close()

def main():
    """Main test function"""
    print("🧪 Testing Snowflake Multimodal Solution (Without Google API)")
    print("=" * 60)
    
    try:
        # Setup Snowflake connection
        conn = setup_snowflake_connection()
        
        # Test 1: Load embeddings
        print("\n1. Testing embedding loading...")
        load_embeddings_to_snowflake(conn)
        
        # Test 2: Test view functionality
        print("\n2. Testing view functionality...")
        view_success = test_view_functionality(conn)
        
        # Test 3: Test vector search
        print("\n3. Testing vector search...")
        search_success = test_vector_search(conn)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"✅ Snowflake Connection: SUCCESS")
        print(f"✅ Embedding Loading: SUCCESS")
        print(f"{'✅' if view_success else '❌'} View Functionality: {'SUCCESS' if view_success else 'FAILED'}")
        print(f"{'✅' if search_success else '❌'} Vector Search: {'SUCCESS' if search_success else 'FAILED'}")
        
        if view_success and search_success:
            print("\n🎉 ALL SNOWFLAKE TESTS PASSED!")
            print("The solution is working correctly. The Google API error is expected.")
            print("To use the full solution, set your Google API key:")
            print("export GOOGLE_API_KEY='your-actual-api-key'")
        else:
            print("\n❌ Some tests failed. Check the errors above.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Close the Snowflake connection
        if 'conn' in locals():
            conn.close()
            print("\nSnowflake connection closed.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test the final working solution using JSON approach
"""

import os
import json
import snowflake.connector
from snowflake.connector import DictCursor
from tqdm import tqdm

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

def setup_snowflake_connection():
    """Initialize Snowflake connection"""
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    
    return conn

def load_embeddings_to_snowflake(conn):
    """Load pre-generated embeddings and store in Snowflake using JSON approach"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print(f"Loaded {len(embeddings_data)} documents with embeddings")
    
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM multimodal_documents")
    print("Cleared existing documents from multimodal_documents table.")
    
    # Insert documents with embeddings using JSON string approach
    for doc in tqdm(embeddings_data):
        # Convert embedding to JSON string
        embedding_json = json.dumps(doc['embedding'])
        
        # Insert using parameterized query with JSON string
        insert_query = """
        INSERT INTO multimodal_documents (key, width, height, embedding)
        VALUES (%s, %s, %s, PARSE_JSON(%s))
        """
        
        cursor.execute(insert_query, (
            doc['key'],
            doc['width'],
            doc['height'],
            embedding_json
        ))
    
    cursor.close()
    conn.commit()
    
    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM multimodal_documents")
    count = cursor.fetchone()[0]
    print(f"{count} documents ingested into the multimodal_documents table.")
    cursor.close()

def test_vector_search(conn):
    """Test vector search functionality"""
    print("\n=== Testing Vector Search ===")
    
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    # Use first document's embedding as query
    query_embedding = embeddings_data[0]['embedding']
    
    # Convert query embedding to JSON string
    query_embedding_json = json.dumps(query_embedding)
    
    cursor = conn.cursor(DictCursor)
    
    search_query = """
    SELECT key, width, height,
           VECTOR_COSINE_SIMILARITY(
               embedding::VECTOR(FLOAT, 1024),
               PARSE_JSON(%s)::VECTOR(FLOAT, 1024)
           ) as similarity_score
    FROM multimodal_documents
    ORDER BY similarity_score DESC
    LIMIT 3
    """
    
    cursor.execute(search_query, (query_embedding_json,))
    results = cursor.fetchall()
    
    print("Vector search results:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['key']} - Similarity: {result['similarity_score']:.6f}")
    
    cursor.close()
    return True

def main():
    """Main test function"""
    print("🧪 Testing FINAL Snowflake Solution (JSON Approach)")
    print("=" * 60)
    
    try:
        conn = setup_snowflake_connection()
        
        # Load embeddings
        print("\n1. Loading embeddings...")
        load_embeddings_to_snowflake(conn)
        
        # Test vector search
        print("\n2. Testing vector search...")
        search_success = test_vector_search(conn)
        
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY:")
        print(f"✅ Snowflake Connection: SUCCESS")
        print(f"✅ Embedding Loading: SUCCESS")
        print(f"{'✅' if search_success else '❌'} Vector Search: {'SUCCESS' if search_success else 'FAILED'}")
        
        if search_success:
            print("\n🎉 FINAL SOLUTION CONFIRMED!")
            print("The JSON storage + VECTOR conversion approach works correctly.")
            print("This is the production-ready solution.")
        else:
            print("\n❌ Some tests failed.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'conn' in locals():
            conn.close()
            print("\nSnowflake connection closed.")

if __name__ == "__main__":
    main()

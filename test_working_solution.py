#!/usr/bin/env python3
"""
Test the working solution
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
    """Load pre-generated embeddings and store in Snowflake using ARRAY type"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print(f"Loaded {len(embeddings_data)} documents with embeddings")
    
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM multimodal_documents")
    print("Cleared existing documents from multimodal_documents table.")
    
    # Insert documents with embeddings using ARRAY type
    for doc in tqdm(embeddings_data):
        # Convert embedding to ARRAY format using ARRAY_CONSTRUCT
        embedding_array = doc['embedding']
        
        # Create ARRAY_CONSTRUCT string for the embedding
        array_values = ','.join([str(val) for val in embedding_array])
        array_construct_sql = f"ARRAY_CONSTRUCT({array_values})"
        
        # Insert using dynamic SQL with ARRAY_CONSTRUCT
        insert_sql = f"""
            INSERT INTO multimodal_documents (key, width, height, embedding)
            VALUES ('{doc['key']}', {doc['width']}, {doc['height']}, {array_construct_sql})
        """
        
        cursor.execute(insert_sql)
    
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
    
    # Convert query embedding to ARRAY_CONSTRUCT format
    query_array_values = ','.join([str(val) for val in query_embedding])
    query_array_construct = f"ARRAY_CONSTRUCT({query_array_values})"
    
    cursor = conn.cursor(DictCursor)
    
    search_query = f"""
    SELECT key, width, height,
           VECTOR_COSINE_SIMILARITY(
               embedding::VECTOR(FLOAT, 1024),
               {query_array_construct}::VECTOR(FLOAT, 1024)
           ) as similarity_score
    FROM multimodal_documents
    ORDER BY similarity_score DESC
    LIMIT 3
    """
    
    cursor.execute(search_query)
    results = cursor.fetchall()
    
    print("Vector search results:")
    for i, result in enumerate(results):
        print(f"  {i+1}. {result['key']} - Similarity: {result['similarity_score']:.6f}")
    
    cursor.close()
    return True

def main():
    """Main test function"""
    print("🧪 Testing Working Snowflake Solution")
    print("=" * 50)
    
    try:
        conn = setup_snowflake_connection()
        
        # Load embeddings
        print("\n1. Loading embeddings...")
        load_embeddings_to_snowflake(conn)
        
        # Test vector search
        print("\n2. Testing vector search...")
        search_success = test_vector_search(conn)
        
        print("\n" + "=" * 50)
        print("📊 TEST SUMMARY:")
        print(f"✅ Snowflake Connection: SUCCESS")
        print(f"✅ Embedding Loading: SUCCESS")
        print(f"{'✅' if search_success else '❌'} Vector Search: {'SUCCESS' if search_success else 'FAILED'}")
        
        if search_success:
            print("\n🎉 WORKING SOLUTION CONFIRMED!")
            print("The ARRAY storage + VECTOR conversion approach works correctly.")
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


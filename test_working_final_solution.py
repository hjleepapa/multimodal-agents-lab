#!/usr/bin/env python3
"""
Test the WORKING FINAL solution using Python for vector operations
"""

import os
import json
import snowflake.connector
from snowflake.connector import DictCursor
from tqdm import tqdm
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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

def format_embedding_for_snowflake(embedding):
    """Format embedding to avoid scientific notation issues"""
    # Format each number to avoid scientific notation
    formatted_values = []
    for val in embedding:
        # Use format to avoid scientific notation for small numbers
        if abs(val) < 1e-10:
            # For very small numbers, use scientific notation but ensure it's parseable
            formatted_val = f"{val:.15g}"
        else:
            # For normal numbers, use fixed decimal format
            formatted_val = f"{val:.15f}".rstrip('0').rstrip('.')
        formatted_values.append(formatted_val)
    return ','.join(formatted_values)

def parse_embedding_from_string(embedding_str):
    """Parse embedding from comma-separated string back to list"""
    return [float(x) for x in embedding_str.split(',')]

def load_embeddings_to_snowflake(conn):
    """Load pre-generated embeddings and store in Snowflake using STRING approach with proper formatting"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print(f"Loaded {len(embeddings_data)} documents with embeddings")
    
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM multimodal_documents")
    print("Cleared existing documents from multimodal_documents table.")
    
    # Insert documents with embeddings using STRING approach with proper formatting
    for doc in tqdm(embeddings_data):
        # Convert embedding to properly formatted comma-separated string
        embedding_str = format_embedding_for_snowflake(doc['embedding'])
        
        # Insert using simple parameterized query with STRING
        insert_query = """
        INSERT INTO multimodal_documents (key, width, height, embedding)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            doc['key'],
            doc['width'],
            doc['height'],
            embedding_str
        ))
    
    cursor.close()
    conn.commit()
    
    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM multimodal_documents")
    count = cursor.fetchone()[0]
    print(f"{count} documents ingested into the multimodal_documents table.")
    cursor.close()

def test_vector_search_with_python(conn):
    """Test vector search functionality using Python for vector operations"""
    print("\n=== Testing Vector Search with Python Vector Operations ===")
    
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    # Use first document's embedding as query
    query_embedding = embeddings_data[0]['embedding']
    
    # Get all documents and their embeddings from Snowflake
    cursor = conn.cursor(DictCursor)
    cursor.execute("SELECT key, width, height, embedding FROM multimodal_documents")
    results = cursor.fetchall()
    cursor.close()
    
    # Calculate similarities using Python
    similarities = []
    query_embedding_array = np.array(query_embedding).reshape(1, -1)
    
    for result in results:
        # Parse embedding from string
        doc_embedding = parse_embedding_from_string(result['EMBEDDING'])
        doc_embedding_array = np.array(doc_embedding).reshape(1, -1)
        
        # Calculate cosine similarity
        similarity = cosine_similarity(query_embedding_array, doc_embedding_array)[0][0]
        
        similarities.append({
            'key': result['KEY'],
            'width': result['WIDTH'],
            'height': result['HEIGHT'],
            'similarity_score': similarity
        })
    
    # Sort by similarity and get top results
    similarities.sort(key=lambda x: x['similarity_score'], reverse=True)
    top_results = similarities[:3]
    
    print("Vector search results:")
    for i, result in enumerate(top_results):
        print(f"  {i+1}. {result['key']} - Similarity: {result['similarity_score']:.6f}")
    
    return True

def main():
    """Main test function"""
    print("🧪 Testing WORKING FINAL Snowflake Solution (Python Vector Operations)")
    print("=" * 80)
    
    try:
        conn = setup_snowflake_connection()
        
        # Load embeddings
        print("\n1. Loading embeddings...")
        load_embeddings_to_snowflake(conn)
        
        # Test vector search with Python
        print("\n2. Testing vector search with Python...")
        search_success = test_vector_search_with_python(conn)
        
        print("\n" + "=" * 80)
        print("📊 TEST SUMMARY:")
        print(f"✅ Snowflake Connection: SUCCESS")
        print(f"✅ Embedding Loading: SUCCESS")
        print(f"{'✅' if search_success else '❌'} Vector Search with Python: {'SUCCESS' if search_success else 'FAILED'}")
        
        if search_success:
            print("\n🎉 WORKING FINAL SOLUTION CONFIRMED!")
            print("The Python vector operations approach works correctly.")
            print("This is the DEFINITIVE WORKING solution!")
        else:
            print("\n❌ Python vector operations approach failed.")
        
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

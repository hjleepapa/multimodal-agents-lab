#!/usr/bin/env python3
"""
Test simple vector operations with Snowflake
"""

import os
import json
import snowflake.connector
from snowflake.connector import DictCursor

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

def test_simple_vector_operations():
    """Test simple vector operations"""
    print("🧪 Testing Simple Vector Operations")
    print("=" * 40)
    
    conn = setup_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        # Create a simple test table
        print("1. Creating test table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE test_simple_vectors (
                id INTEGER,
                name STRING,
                embedding STRING
            )
        """)
        print("   ✅ Test table created")
        
        # Test with simple vectors
        print("\n2. Testing with simple vectors...")
        
        # Simple 3-dimensional vectors
        test_vectors = [
            (1, "vector1", "1.0,2.0,3.0"),
            (2, "vector2", "4.0,5.0,6.0"),
            (3, "vector3", "7.0,8.0,9.0")
        ]
        
        for id_val, name, vector_str in test_vectors:
            cursor.execute("""
                INSERT INTO test_simple_vectors (id, name, embedding)
                VALUES (%s, %s, %s)
            """, (id_val, name, vector_str))
        
        print("   ✅ Simple vectors inserted")
        
        # Test vector similarity
        print("\n3. Testing vector similarity...")
        cursor.execute("""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(
                       STRTOK_TO_ARRAY(embedding, ',')::VECTOR(FLOAT, 3),
                       STRTOK_TO_ARRAY('1.0,2.0,3.0', ',')::VECTOR(FLOAT, 3)
                   ) as similarity
            FROM test_simple_vectors
            ORDER BY similarity DESC
        """)
        
        results = cursor.fetchall()
        for row in results:
            print(f"   {row[0]}: {row[1]} - similarity: {row[2]:.6f}")
        
        print("\n   ✅ Vector similarity test passed")
        
        # Test with real embedding data (first 10 dimensions)
        print("\n4. Testing with real embedding data (first 10 dimensions)...")
        
        with open("data/embeddings.json", "r") as f:
            embeddings_data = json.load(f)
        
        # Take first 10 dimensions of first embedding
        first_embedding = embeddings_data[0]['embedding'][:10]
        embedding_str = ','.join([f"{val:.10f}" for val in first_embedding])
        
        print(f"   Using embedding: {embedding_str[:100]}...")
        
        # Insert test data
        cursor.execute("""
            INSERT INTO test_simple_vectors (id, name, embedding)
            VALUES (%s, %s, %s)
        """, (4, "real_embedding_10d", embedding_str))
        
        # Test similarity
        cursor.execute("""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(
                       STRTOK_TO_ARRAY(embedding, ',')::VECTOR(FLOAT, 10),
                       STRTOK_TO_ARRAY(%s, ',')::VECTOR(FLOAT, 10)
                   ) as similarity
            FROM test_simple_vectors
            WHERE id = 4
        """, (embedding_str,))
        
        result = cursor.fetchone()
        print(f"   Real embedding similarity: {result[2]:.6f}")
        
        print("\n   ✅ Real embedding test passed")
        
        # Test with full 1024-dimensional embedding
        print("\n5. Testing with full 1024-dimensional embedding...")
        
        full_embedding = embeddings_data[0]['embedding']
        # Format with more precision and no scientific notation
        embedding_str_full = ','.join([f"{val:.15f}".rstrip('0').rstrip('.') for val in full_embedding])
        
        print(f"   Embedding length: {len(full_embedding)} dimensions")
        print(f"   String length: {len(embedding_str_full)} characters")
        
        # Insert test data
        cursor.execute("""
            INSERT INTO test_simple_vectors (id, name, embedding)
            VALUES (%s, %s, %s)
        """, (5, "real_embedding_1024d", embedding_str_full))
        
        print("   ✅ Full embedding inserted")
        
        # Test similarity with itself
        cursor.execute("""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(
                       STRTOK_TO_ARRAY(embedding, ',')::VECTOR(FLOAT, 1024),
                       STRTOK_TO_ARRAY(%s, ',')::VECTOR(FLOAT, 1024)
                   ) as similarity
            FROM test_simple_vectors
            WHERE id = 5
        """, (embedding_str_full,))
        
        result = cursor.fetchone()
        print(f"   Full embedding similarity: {result[2]:.6f}")
        
        print("\n   ✅ Full embedding test passed")
        
        # Clean up
        cursor.execute("DROP TABLE test_simple_vectors")
        print("\n   ✅ Test table cleaned up")
        
        print("\n🎉 All tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    finally:
        cursor.close()
        conn.close()

def main():
    """Main function"""
    success = test_simple_vector_operations()
    
    if success:
        print("\n✅ All vector operations working correctly!")
        print("The issue might be in the specific formatting or the view definition.")
    else:
        print("\n❌ Vector operations failed.")

if __name__ == "__main__":
    main()

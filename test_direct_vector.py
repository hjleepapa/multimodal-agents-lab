#!/usr/bin/env python3
"""
Test direct VECTOR creation without string conversion
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

def test_direct_vector_creation():
    """Test direct VECTOR creation"""
    print("🧪 Testing Direct VECTOR Creation")
    print("=" * 40)
    
    conn = setup_snowflake_connection()
    cursor = conn.cursor()
    
    try:
        # Create a test table with VECTOR column
        print("1. Creating test table with VECTOR column...")
        cursor.execute("""
            CREATE OR REPLACE TABLE test_direct_vectors (
                id INTEGER,
                name STRING,
                embedding VECTOR(FLOAT, 3)
            )
        """)
        print("   ✅ Test table created")
        
        # Test direct VECTOR creation using ARRAY_CONSTRUCT
        print("\n2. Testing direct VECTOR creation...")
        
        # Method 1: Using ARRAY_CONSTRUCT with individual values
        cursor.execute("""
            INSERT INTO test_direct_vectors (id, name, embedding)
            VALUES (1, 'vector1', ARRAY_CONSTRUCT(1.0, 2.0, 3.0)::VECTOR(FLOAT, 3))
        """)
        
        cursor.execute("""
            INSERT INTO test_direct_vectors (id, name, embedding)
            VALUES (2, 'vector2', ARRAY_CONSTRUCT(4.0, 5.0, 6.0)::VECTOR(FLOAT, 3))
        """)
        
        cursor.execute("""
            INSERT INTO test_direct_vectors (id, name, embedding)
            VALUES (3, 'vector3', ARRAY_CONSTRUCT(7.0, 8.0, 9.0)::VECTOR(FLOAT, 3))
        """)
        
        print("   ✅ Direct VECTOR insertion successful")
        
        # Test vector similarity
        print("\n3. Testing vector similarity...")
        cursor.execute("""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(embedding, ARRAY_CONSTRUCT(1.0, 2.0, 3.0)::VECTOR(FLOAT, 3)) as similarity
            FROM test_direct_vectors
            ORDER BY similarity DESC
        """)
        
        results = cursor.fetchall()
        for row in results:
            print(f"   {row[0]}: {row[1]} - similarity: {row[2]:.6f}")
        
        print("\n   ✅ Vector similarity test passed")
        
        # Test with real embedding data (first 3 dimensions)
        print("\n4. Testing with real embedding data (first 3 dimensions)...")
        
        with open("data/embeddings.json", "r") as f:
            embeddings_data = json.load(f)
        
        # Take first 3 dimensions of first embedding
        first_embedding = embeddings_data[0]['embedding'][:3]
        
        # Create ARRAY_CONSTRUCT string
        array_construct_str = 'ARRAY_CONSTRUCT(' + ','.join([str(val) for val in first_embedding]) + ')'
        
        print(f"   Using embedding: {first_embedding}")
        
        # Insert test data using dynamic SQL
        insert_sql = f"""
            INSERT INTO test_direct_vectors (id, name, embedding)
            VALUES (4, 'real_embedding_3d', {array_construct_str}::VECTOR(FLOAT, 3))
        """
        
        cursor.execute(insert_sql)
        print("   ✅ Real embedding inserted")
        
        # Test similarity
        similarity_sql = f"""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(embedding, {array_construct_str}::VECTOR(FLOAT, 3)) as similarity
            FROM test_direct_vectors
            WHERE id = 4
        """
        
        cursor.execute(similarity_sql)
        result = cursor.fetchone()
        print(f"   Real embedding similarity: {result[2]:.6f}")
        
        print("\n   ✅ Real embedding test passed")
        
        # Test with larger embedding (first 10 dimensions)
        print("\n5. Testing with 10-dimensional embedding...")
        
        ten_dim_embedding = embeddings_data[0]['embedding'][:10]
        array_construct_str_10 = 'ARRAY_CONSTRUCT(' + ','.join([str(val) for val in ten_dim_embedding]) + ')'
        
        # Create new table for 10D vectors
        cursor.execute("""
            CREATE OR REPLACE TABLE test_direct_vectors_10d (
                id INTEGER,
                name STRING,
                embedding VECTOR(FLOAT, 10)
            )
        """)
        
        insert_sql_10 = f"""
            INSERT INTO test_direct_vectors_10d (id, name, embedding)
            VALUES (1, 'real_embedding_10d', {array_construct_str_10}::VECTOR(FLOAT, 10))
        """
        
        cursor.execute(insert_sql_10)
        print("   ✅ 10D embedding inserted")
        
        # Test similarity
        similarity_sql_10 = f"""
            SELECT id, name,
                   VECTOR_COSINE_SIMILARITY(embedding, {array_construct_str_10}::VECTOR(FLOAT, 10)) as similarity
            FROM test_direct_vectors_10d
            WHERE id = 1
        """
        
        cursor.execute(similarity_sql_10)
        result = cursor.fetchone()
        print(f"   10D embedding similarity: {result[2]:.6f}")
        
        print("\n   ✅ 10D embedding test passed")
        
        # Clean up
        cursor.execute("DROP TABLE test_direct_vectors")
        cursor.execute("DROP TABLE test_direct_vectors_10d")
        print("\n   ✅ Test tables cleaned up")
        
        print("\n🎉 All direct VECTOR tests passed!")
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
    success = test_direct_vector_creation()
    
    if success:
        print("\n✅ Direct VECTOR creation works correctly!")
        print("We should use ARRAY_CONSTRUCT with dynamic SQL for our solution")
    else:
        print("\n❌ Direct VECTOR creation failed.")

if __name__ == "__main__":
    main()

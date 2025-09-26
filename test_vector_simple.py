#!/usr/bin/env python3
"""
Simple test script for VECTOR functionality using environment variables
"""

import os
import snowflake.connector
from snowflake.connector import DictCursor

def test_vector_simple():
    """Test VECTOR functionality with environment variables"""
    
    # Get connection parameters from environment
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format
    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    print("🧪 Testing VECTOR Data Type (Simple)")
    print("=" * 40)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Warehouse: {SNOWFLAKE_WAREHOUSE}")
    print(f"Database: {SNOWFLAKE_DATABASE}")
    print(f"Schema: {SNOWFLAKE_SCHEMA}")
    
    # Check if credentials are set
    if (SNOWFLAKE_ACCOUNT == "your-account" or 
        SNOWFLAKE_USER == "your-username" or 
        SNOWFLAKE_PASSWORD == "your-password"):
        print("\n❌ Please set your Snowflake credentials in environment variables:")
        print("export SNOWFLAKE_ACCOUNT='your-account'")
        print("export SNOWFLAKE_USER='your-username'")
        print("export SNOWFLAKE_PASSWORD='your-password'")
        print("export SNOWFLAKE_WAREHOUSE='COMPUTE_WH'")
        print("export SNOWFLAKE_DATABASE='multimodal_agents_db'")
        print("export SNOWFLAKE_SCHEMA='multimodal_schema'")
        return False
    
    try:
        # Connect to Snowflake
        print("\n1. Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        print("   ✅ Connected successfully!")
        
        cursor = conn.cursor()
        
        # Test VECTOR functions
        print("\n2. Testing VECTOR functions...")
        try:
            cursor.execute("SELECT VECTOR_COSINE_SIMILARITY([1.0, 2.0], [1.0, 2.0])")
            result = cursor.fetchone()
            print(f"   ✅ VECTOR_COSINE_SIMILARITY works: {result[0]}")
        except Exception as e:
            print(f"   ❌ VECTOR functions error: {e}")
            return False
        
        # Test table creation and VECTOR insertion
        print("\n3. Testing VECTOR table operations...")
        cursor.execute("""
            CREATE OR REPLACE TABLE test_vectors (
                id STRING,
                test_vector VECTOR(FLOAT, 1024)
            )
        """)
        print("   ✅ VECTOR table created")
        
        # Test insertion using ARRAY_CONSTRUCT
        test_embedding = [0.1, 0.2, 0.3] + [0.0] * 1021  # 1024 dimensions
        embedding_values = ','.join(map(str, test_embedding))
        
        cursor.execute("""
            INSERT INTO test_vectors (id, test_vector)
            VALUES (%s, ARRAY_CONSTRUCT(%s)::VECTOR(FLOAT, 1024))
        """, ("test_1", embedding_values))
        print("   ✅ VECTOR insertion successful")
        
        # Test query using ARRAY_CONSTRUCT with explicit cast
        cursor.execute("""
            SELECT id, VECTOR_COSINE_SIMILARITY(test_vector, ARRAY_CONSTRUCT(%s)::VECTOR(FLOAT, 1024)) as similarity
            FROM test_vectors
            WHERE id = 'test_1'
        """, (embedding_values,))
        
        result = cursor.fetchone()
        print(f"   ✅ VECTOR query successful: similarity = {result[1]}")
        
        # Clean up
        cursor.execute("DROP TABLE test_vectors")
        print("   ✅ Test table cleaned up")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All VECTOR tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    success = test_vector_simple()
    
    if success:
        print("\n✅ VECTOR data type is working correctly!")
        print("You can now run the full solution:")
        print("python3 snowflake_solution.py")
    else:
        print("\n❌ VECTOR data type issues detected.")
        print("Please check:")
        print("1. Your Snowflake region supports VECTOR data type")
        print("2. Your Snowflake version is up to date")
        print("3. You have the necessary permissions")
        print("4. Your environment variables are set correctly")

if __name__ == "__main__":
    main()

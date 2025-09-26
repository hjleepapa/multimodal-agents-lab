#!/usr/bin/env python3
"""
Test script to verify VECTOR data type handling in Snowflake
"""

import os
import snowflake.connector
from snowflake.connector import DictCursor

def test_vector_insertion():
    """Test inserting VECTOR data into Snowflake"""
    
    # Get connection parameters
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account.snowflakecomputing.com")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format
    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    print("🧪 Testing VECTOR Data Type in Snowflake")
    print("=" * 40)
    
    try:
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )
        
        cursor = conn.cursor()
        
        # Test 1: Check if VECTOR data type is supported
        print("1. Testing VECTOR data type support...")
        try:
            cursor.execute("SELECT VECTOR_COSINE_SIMILARITY([1.0, 2.0], [1.0, 2.0])")
            result = cursor.fetchone()
            print(f"   ✅ VECTOR functions work: {result[0]}")
        except Exception as e:
            print(f"   ❌ VECTOR functions not supported: {e}")
            return False
        
        # Test 2: Create a test table with VECTOR column
        print("2. Creating test table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE test_vectors (
                id STRING,
                test_vector VECTOR(FLOAT, 1024)
            )
        """)
        print("   ✅ Test table created")
        
        # Test 3: Insert test vector data
        print("3. Testing vector insertion...")
        test_embedding = [0.1, 0.2, 0.3] + [0.0] * 1021  # 1024 dimensions
        
        insert_query = """
        INSERT INTO test_vectors (id, test_vector)
        VALUES (%s, %s)
        """
        
        cursor.execute(insert_query, ("test_1", test_embedding))
        print("   ✅ Vector insertion successful")
        
        # Test 4: Query the vector data
        print("4. Testing vector query...")
        cursor.execute("""
            SELECT id, test_vector, 
                   VECTOR_COSINE_SIMILARITY(test_vector, %s) as similarity
            FROM test_vectors
            WHERE id = 'test_1'
        """, (test_embedding,))
        
        result = cursor.fetchone()
        print(f"   ✅ Vector query successful: similarity = {result[2]}")
        
        # Test 5: Clean up
        print("5. Cleaning up...")
        cursor.execute("DROP TABLE test_vectors")
        print("   ✅ Test table dropped")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 All VECTOR tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ VECTOR test failed: {e}")
        return False

def main():
    """Main test function"""
    success = test_vector_insertion()
    
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

if __name__ == "__main__":
    main()

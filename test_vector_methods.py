#!/usr/bin/env python3
"""
Test different methods for inserting VECTOR data into Snowflake
"""

import os
import snowflake.connector

def test_vector_insertion_methods():
    """Test different approaches for VECTOR insertion"""
    
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
    
    print("🧪 Testing VECTOR Insertion Methods")
    print("=" * 40)
    
    # Check if credentials are set
    if (SNOWFLAKE_ACCOUNT == "your-account" or 
        SNOWFLAKE_USER == "your-username" or 
        SNOWFLAKE_PASSWORD == "your-password"):
        print("❌ Please set your Snowflake credentials first")
        return False
    
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
        
        # Create test table
        print("1. Creating test table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE test_vector_methods (
                id STRING,
                method STRING,
                test_vector VECTOR(FLOAT, 1024)
            )
        """)
        print("   ✅ Test table created")
        
        # Test data
        test_embedding = [0.1, 0.2, 0.3] + [0.0] * 1021  # 1024 dimensions
        
        # Method 1: Direct array insertion
        print("\n2. Testing Method 1: Direct array insertion...")
        try:
            cursor.execute("""
                INSERT INTO test_vector_methods (id, method, test_vector)
                VALUES (%s, %s, %s)
            """, ("test_1", "direct_array", test_embedding))
            print("   ✅ Method 1 successful")
        except Exception as e:
            print(f"   ❌ Method 1 failed: {e}")
        
        # Method 2: Using ARRAY_CONSTRUCT
        print("\n3. Testing Method 2: ARRAY_CONSTRUCT...")
        try:
            embedding_values = ','.join(map(str, test_embedding))
            cursor.execute("""
                INSERT INTO test_vector_methods (id, method, test_vector)
                VALUES (%s, %s, ARRAY_CONSTRUCT(%s))
            """, ("test_2", "array_construct", embedding_values))
            print("   ✅ Method 2 successful")
        except Exception as e:
            print(f"   ❌ Method 2 failed: {e}")
        
        # Method 3: Using PARSE_JSON
        print("\n4. Testing Method 3: PARSE_JSON...")
        try:
            import json
            embedding_json = json.dumps(test_embedding)
            cursor.execute("""
                INSERT INTO test_vector_methods (id, method, test_vector)
                VALUES (%s, %s, PARSE_JSON(%s))
            """, ("test_3", "parse_json", embedding_json))
            print("   ✅ Method 3 successful")
        except Exception as e:
            print(f"   ❌ Method 3 failed: {e}")
        
        # Method 4: Using STRTOK_TO_ARRAY
        print("\n5. Testing Method 4: STRTOK_TO_ARRAY...")
        try:
            embedding_str = ','.join(map(str, test_embedding))
            cursor.execute("""
                INSERT INTO test_vector_methods (id, method, test_vector)
                VALUES (%s, %s, STRTOK_TO_ARRAY(%s, ','))
            """, ("test_4", "strtok_to_array", embedding_str))
            print("   ✅ Method 4 successful")
        except Exception as e:
            print(f"   ❌ Method 4 failed: {e}")
        
        # Check what was inserted
        print("\n6. Checking inserted data...")
        cursor.execute("SELECT id, method FROM test_vector_methods")
        results = cursor.fetchall()
        for row in results:
            print(f"   ✅ {row[0]}: {row[1]}")
        
        # Test vector similarity
        print("\n7. Testing vector similarity...")
        cursor.execute("""
            SELECT id, method, 
                   VECTOR_COSINE_SIMILARITY(test_vector, %s) as similarity
            FROM test_vector_methods
            WHERE method IS NOT NULL
        """, (test_embedding,))
        
        similarity_results = cursor.fetchall()
        for row in similarity_results:
            print(f"   ✅ {row[0]} ({row[1]}): similarity = {row[2]}")
        
        # Clean up
        cursor.execute("DROP TABLE test_vector_methods")
        print("\n   ✅ Test table cleaned up")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 VECTOR method testing complete!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        return False

def main():
    """Main function"""
    success = test_vector_insertion_methods()
    
    if success:
        print("\n✅ VECTOR method testing completed successfully!")
    else:
        print("\n❌ VECTOR method testing failed.")

if __name__ == "__main__":
    main()

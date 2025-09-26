#!/usr/bin/env python3
"""
Test script that prompts for credentials and tests VECTOR functionality
"""

import os
import snowflake.connector
from snowflake.connector import DictCursor

def get_credentials():
    """Get credentials from user input"""
    print("🔐 Snowflake Credentials Setup")
    print("=" * 30)
    
    account = input("Snowflake Account (e.g., CSWRMBD-HUB94431): ").strip()
    if not account:
        account = "CSWRMBD-HUB94431"
    
    user = input("Username: ").strip()
    if not user:
        print("❌ Username is required")
        return None
    
    password = input("Password: ").strip()
    if not password:
        print("❌ Password is required")
        return None
    
    warehouse = input("Warehouse [COMPUTE_WH]: ").strip()
    if not warehouse:
        warehouse = "COMPUTE_WH"
    
    database = input("Database [multimodal_agents_db]: ").strip()
    if not database:
        database = "multimodal_agents_db"
    
    schema = input("Schema [multimodal_schema]: ").strip()
    if not schema:
        schema = "multimodal_schema"
    
    return {
        'account': account,
        'user': user,
        'password': password,
        'warehouse': warehouse,
        'database': database,
        'schema': schema
    }

def test_vector_functionality(creds):
    """Test VECTOR functionality with provided credentials"""
    
    print(f"\n🧪 Testing VECTOR Data Type")
    print("=" * 30)
    print(f"Account: {creds['account']}")
    print(f"User: {creds['user']}")
    print(f"Warehouse: {creds['warehouse']}")
    print(f"Database: {creds['database']}")
    print(f"Schema: {creds['schema']}")
    
    try:
        # Connect to Snowflake
        print("\n1. Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            account=creds['account'],
            user=creds['user'],
            password=creds['password'],
            warehouse=creds['warehouse'],
            database=creds['database'],
            schema=creds['schema']
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
            VALUES (%s, ARRAY_CONSTRUCT(%s))
        """, ("test_1", embedding_values))
        print("   ✅ VECTOR insertion successful")
        
        # Test query using ARRAY_CONSTRUCT
        cursor.execute("""
            SELECT id, VECTOR_COSINE_SIMILARITY(test_vector, ARRAY_CONSTRUCT(%s)) as similarity
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
    print("🚀 Snowflake VECTOR Data Type Test")
    print("=" * 40)
    
    # Get credentials
    creds = get_credentials()
    if not creds:
        return
    
    # Test VECTOR functionality
    success = test_vector_functionality(creds)
    
    if success:
        print("\n✅ VECTOR data type is working correctly!")
        print("\nTo run the full solution, set these environment variables:")
        print(f"export SNOWFLAKE_ACCOUNT='{creds['account']}'")
        print(f"export SNOWFLAKE_USER='{creds['user']}'")
        print(f"export SNOWFLAKE_PASSWORD='{creds['password']}'")
        print(f"export SNOWFLAKE_WAREHOUSE='{creds['warehouse']}'")
        print(f"export SNOWFLAKE_DATABASE='{creds['database']}'")
        print(f"export SNOWFLAKE_SCHEMA='{creds['schema']}'")
        print("\nThen run: python3 snowflake_solution.py")
    else:
        print("\n❌ VECTOR data type issues detected.")
        print("Please check:")
        print("1. Your Snowflake region supports VECTOR data type")
        print("2. Your Snowflake version is up to date")
        print("3. You have the necessary permissions")

if __name__ == "__main__":
    main()

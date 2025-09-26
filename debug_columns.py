#!/usr/bin/env python3
"""
Debug script to check column names
"""

import os
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

def main():
    """Debug column names"""
    print("🔍 Debugging column names...")
    
    try:
        conn = setup_snowflake_connection()
        
        # Check table structure
        cursor = conn.cursor()
        cursor.execute("DESCRIBE TABLE multimodal_documents")
        columns = cursor.fetchall()
        
        print("Table structure:")
        for col in columns:
            print(f"  {col}")
        
        # Check actual data
        cursor = conn.cursor(DictCursor)
        cursor.execute("SELECT * FROM multimodal_documents LIMIT 1")
        result = cursor.fetchone()
        
        if result:
            print(f"\nSample record keys: {list(result.keys())}")
            print(f"Sample record: {result}")
        else:
            print("No records found")
        
        cursor.close()
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    main()


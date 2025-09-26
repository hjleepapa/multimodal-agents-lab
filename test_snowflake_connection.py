#!/usr/bin/env python3
"""
Test Snowflake connection with proper error handling
"""

import os
import snowflake.connector

def test_snowflake_connection():
    """Test Snowflake connection with detailed error information"""
    
    # Get connection parameters
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account.snowflakecomputing.com")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format - remove .snowflakecomputing.com if present
    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    print("🧪 Testing Snowflake Connection")
    print("=" * 40)
    print(f"Account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Warehouse: {SNOWFLAKE_WAREHOUSE}")
    print(f"Database: {SNOWFLAKE_DATABASE}")
    print(f"Schema: {SNOWFLAKE_SCHEMA}")
    print()

    # Check if credentials are set
    if SNOWFLAKE_ACCOUNT == "your-account.snowflakecomputing.com" or SNOWFLAKE_USER == "your-username":
        print("❌ Please set your Snowflake credentials in environment variables:")
        print("export SNOWFLAKE_ACCOUNT='your-account'")
        print("export SNOWFLAKE_USER='your-username'")
        print("export SNOWFLAKE_PASSWORD='your-password'")
        print("export SNOWFLAKE_WAREHOUSE='COMPUTE_WH'")
        print("export SNOWFLAKE_DATABASE='multimodal_agents_db'")
        print("export SNOWFLAKE_SCHEMA='multimodal_schema'")
        return False

    try:
        print("Attempting to connect...")
        
        # Initialize Snowflake connection
        conn = snowflake.connector.connect(
            account=SNOWFLAKE_ACCOUNT,
            user=SNOWFLAKE_USER,
            password=SNOWFLAKE_PASSWORD,
            warehouse=SNOWFLAKE_WAREHOUSE,
            database=SNOWFLAKE_DATABASE,
            schema=SNOWFLAKE_SCHEMA
        )

        # Test the connection
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        print(f"✅ Connected to Snowflake: {version}")
        
        # Test database access
        cursor.execute("SELECT CURRENT_DATABASE(), CURRENT_SCHEMA()")
        db_info = cursor.fetchone()
        print(f"✅ Database: {db_info[0]}, Schema: {db_info[1]}")
        
        # Test warehouse
        cursor.execute("SELECT CURRENT_WAREHOUSE()")
        warehouse = cursor.fetchone()[0]
        print(f"✅ Warehouse: {warehouse}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Snowflake connection test successful!")
        return True
        
    except snowflake.connector.errors.HttpError as e:
        print(f"❌ HTTP Error: {e}")
        print("\nPossible issues:")
        print("1. Incorrect account identifier")
        print("2. Account doesn't exist or is suspended")
        print("3. Network connectivity issues")
        print("4. Account format should be just the account name (e.g., 'CSWRMBD-HUB94431')")
        return False
        
    except snowflake.connector.errors.ProgrammingError as e:
        print(f"❌ Programming Error: {e}")
        print("\nPossible issues:")
        print("1. Incorrect username or password")
        print("2. User doesn't have access to the specified warehouse/database/schema")
        print("3. Warehouse, database, or schema doesn't exist")
        return False
        
    except snowflake.connector.errors.DatabaseError as e:
        print(f"❌ Database Error: {e}")
        print("\nPossible issues:")
        print("1. Database or schema doesn't exist")
        print("2. Insufficient privileges")
        return False
        
    except Exception as e:
        print(f"❌ Unexpected Error: {e}")
        print(f"Error type: {type(e).__name__}")
        return False

def main():
    """Main function"""
    success = test_snowflake_connection()
    
    if success:
        print("\n✅ You can now run the full solution:")
        print("python3 snowflake_solution.py")
    else:
        print("\n❌ Please fix the connection issues before running the full solution.")
        
        print("\n📋 Quick Setup Guide:")
        print("1. Make sure you have a Snowflake account")
        print("2. Set environment variables with your credentials")
        print("3. Run the snowflake_setup.sql script in your Snowflake environment")
        print("4. Test the connection again")

if __name__ == "__main__":
    main()

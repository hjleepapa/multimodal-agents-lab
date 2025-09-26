#!/usr/bin/env python3
"""
Test script to verify Snowflake setup and dependencies
"""

import sys
import os

def test_imports():
    """Test all required imports"""
    print("Testing imports...")
    
    try:
        import snowflake.connector
        print("✅ snowflake.connector imported successfully")
    except ImportError as e:
        print(f"❌ snowflake.connector import failed: {e}")
        return False
    
    try:
        from google import genai
        print("✅ google.genai imported successfully")
    except ImportError as e:
        print(f"❌ google.genai import failed: {e}")
        return False
    
    try:
        import pymupdf
        print("✅ pymupdf imported successfully")
    except ImportError as e:
        print(f"❌ pymupdf import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    try:
        import voyageai
        print("✅ voyageai imported successfully")
    except ImportError as e:
        print(f"❌ voyageai import failed: {e}")
        return False
    
    return True

def test_config():
    """Test configuration"""
    print("\nTesting configuration...")
    
    # Check if config file exists
    if os.path.exists('snowflake_config.py'):
        print("✅ snowflake_config.py found")
    else:
        print("❌ snowflake_config.py not found")
        return False
    
    # Check if requirements file exists
    if os.path.exists('snowflake_requirements.txt'):
        print("✅ snowflake_requirements.txt found")
    else:
        print("❌ snowflake_requirements.txt not found")
        return False
    
    # Check if setup SQL exists
    if os.path.exists('snowflake_setup.sql'):
        print("✅ snowflake_setup.sql found")
    else:
        print("❌ snowflake_setup.sql not found")
        return False
    
    return True

def test_solution_imports():
    """Test importing the main solution"""
    print("\nTesting solution imports...")
    
    try:
        from snowflake_solution import setup_snowflake_connection, setup_gemini
        print("✅ Main solution functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Solution import failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Snowflake Multimodal Agents Lab Setup")
    print("=" * 50)
    
    all_tests_passed = True
    
    # Test imports
    if not test_imports():
        all_tests_passed = False
    
    # Test configuration files
    if not test_config():
        all_tests_passed = False
    
    # Test solution imports
    if not test_solution_imports():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Snowflake setup is ready.")
        print("\nNext steps:")
        print("1. Run snowflake_setup.sql in your Snowflake environment")
        print("2. Set up your environment variables:")
        print("   - SNOWFLAKE_ACCOUNT")
        print("   - SNOWFLAKE_USER") 
        print("   - SNOWFLAKE_PASSWORD")
        print("   - GOOGLE_API_KEY")
        print("3. Run: python3 snowflake_solution.py")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

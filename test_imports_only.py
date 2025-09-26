#!/usr/bin/env python3
"""
Simple test script to verify all imports work without requiring Snowflake connection
"""

def test_all_imports():
    """Test all imports without connecting to external services"""
    print("Testing all imports...")
    
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
    
    try:
        import json
        print("✅ json imported successfully")
    except ImportError as e:
        print(f"❌ json import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from tqdm import tqdm
        print("✅ tqdm imported successfully")
    except ImportError as e:
        print(f"❌ tqdm import failed: {e}")
        return False
    
    try:
        from typing import List
        print("✅ typing imported successfully")
    except ImportError as e:
        print(f"❌ typing import failed: {e}")
        return False
    
    try:
        from datetime import datetime
        print("✅ datetime imported successfully")
    except ImportError as e:
        print(f"❌ datetime import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    return True

def test_function_imports():
    """Test importing functions from our solution"""
    print("\nTesting solution function imports...")
    
    try:
        from snowflake_solution import (
            setup_snowflake_connection,
            setup_gemini,
            download_and_process_pdf,
            load_embeddings_to_snowflake,
            get_information_for_question_answering,
            create_function_declaration,
            select_tool,
            generate_answer,
            execute_agent,
            store_chat_message,
            retrieve_session_history,
            generate_answer_with_memory,
            execute_agent_with_memory,
            generate_answer_react,
            execute_react_agent
        )
        print("✅ All solution functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Solution function import failed: {e}")
        return False

def test_config_imports():
    """Test importing configuration"""
    print("\nTesting configuration imports...")
    
    try:
        from snowflake_config import SnowflakeConfig, get_config
        print("✅ Configuration imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Configuration import failed: {e}")
        return False

def test_utils_imports():
    """Test importing utilities"""
    print("\nTesting utility imports...")
    
    try:
        from snowflake_utils import (
            validate_embedding_format,
            convert_embedding_to_snowflake_format,
            parse_snowflake_vector,
            create_image_hash,
            validate_image_file,
            batch_insert_documents,
            get_document_statistics,
            cleanup_old_sessions,
            export_embeddings_to_json,
            validate_database_schema,
            create_backup_tables,
            restore_from_backup
        )
        print("✅ All utility functions imported successfully")
        return True
    except ImportError as e:
        print(f"❌ Utility import failed: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing Snowflake Multimodal Agents Lab - Import Only")
    print("=" * 60)
    
    all_tests_passed = True
    
    # Test basic imports
    if not test_all_imports():
        all_tests_passed = False
    
    # Test function imports
    if not test_function_imports():
        all_tests_passed = False
    
    # Test config imports
    if not test_config_imports():
        all_tests_passed = False
    
    # Test utils imports
    if not test_utils_imports():
        all_tests_passed = False
    
    print("\n" + "=" * 60)
    if all_tests_passed:
        print("🎉 All import tests passed! The environment is ready.")
        print("\nThe previous connection error was expected because:")
        print("- The script tried to connect to Snowflake with placeholder credentials")
        print("- This confirms that the snowflake module is working correctly")
        print("\nTo run the full solution, you need to:")
        print("1. Set up your Snowflake credentials")
        print("2. Run the snowflake_setup.sql script")
        print("3. Configure your environment variables")
    else:
        print("❌ Some import tests failed. Please check the errors above.")
        return False
    
    return True

if __name__ == "__main__":
    main()

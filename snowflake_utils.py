"""
Utility functions for Snowflake Multimodal Agents Lab

This module contains helper functions for data processing, validation,
and common operations used throughout the Snowflake multimodal agent system.
"""

import json
import os
import hashlib
from typing import List, Dict, Any, Optional
import numpy as np
from PIL import Image
import snowflake.connector
from snowflake.connector import DictCursor

def validate_embedding_format(embedding: List[float], expected_dimensions: int = 1024) -> bool:
    """
    Validate that an embedding has the correct format and dimensions
    
    Args:
        embedding: List of float values representing the embedding
        expected_dimensions: Expected number of dimensions
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not isinstance(embedding, list):
        return False
    
    if len(embedding) != expected_dimensions:
        return False
    
    if not all(isinstance(x, (int, float)) for x in embedding):
        return False
    
    return True

def convert_embedding_to_snowflake_format(embedding: List[float]) -> str:
    """
    Convert embedding list to Snowflake VECTOR format string for ARRAY_CONSTRUCT
    
    Args:
        embedding: List of float values
        
    Returns:
        str: Comma-separated string for use with ARRAY_CONSTRUCT
    """
    if not validate_embedding_format(embedding):
        raise ValueError("Invalid embedding format")
    
    return ','.join(map(str, embedding))  # Return comma-separated string for ARRAY_CONSTRUCT

def parse_snowflake_vector(vector_str: str) -> List[float]:
    """
    Parse Snowflake VECTOR format string to list of floats
    
    Args:
        vector_str: String in format '[1.0,2.0,3.0,...]'
        
    Returns:
        List[float]: Parsed embedding values
    """
    # Remove brackets and split by comma
    vector_str = vector_str.strip('[]')
    values = [float(x.strip()) for x in vector_str.split(',')]
    return values

def create_image_hash(image_path: str) -> str:
    """
    Create a hash for an image file to detect duplicates
    
    Args:
        image_path: Path to the image file
        
    Returns:
        str: MD5 hash of the image file
    """
    hash_md5 = hashlib.md5()
    with open(image_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def validate_image_file(image_path: str) -> bool:
    """
    Validate that an image file exists and is readable
    
    Args:
        image_path: Path to the image file
        
    Returns:
        bool: True if valid, False otherwise
    """
    if not os.path.exists(image_path):
        return False
    
    try:
        with Image.open(image_path) as img:
            img.verify()
        return True
    except Exception:
        return False

def batch_insert_documents(cursor, documents: List[Dict[str, Any]], batch_size: int = 100) -> int:
    """
    Insert documents in batches for better performance
    
    Args:
        cursor: Snowflake cursor object
        documents: List of document dictionaries
        batch_size: Number of documents to insert per batch
        
    Returns:
        int: Number of documents inserted
    """
    insert_query = """
    INSERT INTO multimodal_documents (key, width, height, embedding)
    VALUES (%s, %s, %s, ARRAY_CONSTRUCT(%s)::VECTOR(FLOAT, 1024))
    """
    
    total_inserted = 0
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        batch_data = []
        
        for doc in batch:
            embedding_str = convert_embedding_to_snowflake_format(doc['embedding'])
            batch_data.append((
                doc['key'],
                doc['width'],
                doc['height'],
                embedding_str
            ))
        
        cursor.executemany(insert_query, batch_data)
        total_inserted += len(batch_data)
    
    return total_inserted

def get_document_statistics(conn) -> Dict[str, Any]:
    """
    Get statistics about documents in the database
    
    Args:
        conn: Snowflake connection object
        
    Returns:
        Dict containing document statistics
    """
    cursor = conn.cursor(DictCursor)
    
    # Get total count
    cursor.execute("SELECT COUNT(*) as total_docs FROM multimodal_documents")
    total_docs = cursor.fetchone()['total_docs']
    
    # Get average dimensions
    cursor.execute("""
        SELECT 
            AVG(width) as avg_width,
            AVG(height) as avg_height,
            MIN(width) as min_width,
            MIN(height) as min_height,
            MAX(width) as max_width,
            MAX(height) as max_height
        FROM multimodal_documents
    """)
    dimension_stats = cursor.fetchone()
    
    # Get recent documents
    cursor.execute("""
        SELECT key, created_at
        FROM multimodal_documents
        ORDER BY created_at DESC
        LIMIT 5
    """)
    recent_docs = cursor.fetchall()
    
    cursor.close()
    
    return {
        'total_documents': total_docs,
        'dimension_statistics': dimension_stats,
        'recent_documents': recent_docs
    }

def cleanup_old_sessions(conn, days_old: int = 30) -> int:
    """
    Clean up old chat history sessions
    
    Args:
        conn: Snowflake connection object
        days_old: Number of days to keep history
        
    Returns:
        int: Number of records deleted
    """
    cursor = conn.cursor()
    
    delete_query = """
    DELETE FROM chat_history
    WHERE timestamp < DATEADD(day, -%s, CURRENT_TIMESTAMP())
    """
    
    cursor.execute(delete_query, (days_old,))
    deleted_count = cursor.rowcount
    cursor.close()
    conn.commit()
    
    return deleted_count

def export_embeddings_to_json(conn, output_file: str) -> bool:
    """
    Export embeddings from Snowflake to JSON file
    
    Args:
        conn: Snowflake connection object
        output_file: Path to output JSON file
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor(DictCursor)
        
        query = """
        SELECT key, width, height, embedding
        FROM multimodal_documents
        ORDER BY key
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()
        
        # Convert embeddings back to list format
        documents = []
        for row in results:
            embedding_list = parse_snowflake_vector(row['embedding'])
            documents.append({
                'key': row['key'],
                'width': row['width'],
                'height': row['height'],
                'embedding': embedding_list
            })
        
        # Write to JSON file
        with open(output_file, 'w') as f:
            json.dump(documents, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"Error exporting embeddings: {e}")
        return False

def validate_database_schema(conn) -> bool:
    """
    Validate that the database schema is correctly set up
    
    Args:
        conn: Snowflake connection object
        
    Returns:
        bool: True if schema is valid, False otherwise
    """
    try:
        cursor = conn.cursor()
        
        # Check if tables exist
        tables_to_check = ['multimodal_documents', 'chat_history']
        
        for table in tables_to_check:
            cursor.execute(f"""
                SELECT COUNT(*) 
                FROM INFORMATION_SCHEMA.TABLES 
                WHERE TABLE_NAME = '{table}'
            """)
            if cursor.fetchone()[0] == 0:
                print(f"Table {table} does not exist")
                return False
        
        # Check if VECTOR data type is supported
        cursor.execute("""
            SELECT COUNT(*) 
            FROM multimodal_documents 
            WHERE embedding IS NOT NULL
            LIMIT 1
        """)
        
        cursor.close()
        return True
        
    except Exception as e:
        print(f"Schema validation error: {e}")
        return False

def create_backup_tables(conn) -> bool:
    """
    Create backup tables for the main tables
    
    Args:
        conn: Snowflake connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        
        # Create backup tables
        cursor.execute("""
            CREATE OR REPLACE TABLE multimodal_documents_backup AS
            SELECT * FROM multimodal_documents
        """)
        
        cursor.execute("""
            CREATE OR REPLACE TABLE chat_history_backup AS
            SELECT * FROM chat_history
        """)
        
        cursor.close()
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Backup creation error: {e}")
        return False

def restore_from_backup(conn) -> bool:
    """
    Restore tables from backup
    
    Args:
        conn: Snowflake connection object
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        cursor = conn.cursor()
        
        # Restore from backup tables
        cursor.execute("""
            CREATE OR REPLACE TABLE multimodal_documents AS
            SELECT * FROM multimodal_documents_backup
        """)
        
        cursor.execute("""
            CREATE OR REPLACE TABLE chat_history AS
            SELECT * FROM chat_history_backup
        """)
        
        cursor.close()
        conn.commit()
        return True
        
    except Exception as e:
        print(f"Restore error: {e}")
        return False

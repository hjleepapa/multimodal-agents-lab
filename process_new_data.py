#!/usr/bin/env python3
"""
Process New Data Files for Multimodal Agents Lab

This script helps you process new PDF, text, and image files
and integrate them into your Snowflake multimodal agents system.
"""

import os
import json
import pymupdf
import requests
from tqdm import tqdm
from PIL import Image
import snowflake.connector
from snowflake.connector import DictCursor
from dotenv import load_dotenv
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load environment variables
load_dotenv()

def setup_snowflake_connection():
    """Setup Snowflake connection"""
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format
    if SNOWFLAKE_ACCOUNT and SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
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

def format_embedding_for_snowflake(embedding):
    """Format embedding to avoid scientific notation issues"""
    formatted_values = []
    for val in embedding:
        if abs(val) < 1e-10:
            formatted_val = f"{val:.15g}"
        else:
            formatted_val = f"{val:.15f}".rstrip('0').rstrip('.')
        formatted_values.append(formatted_val)
    return ','.join(formatted_values)

def process_pdf_file(pdf_path, output_dir="data/images"):
    """Process a PDF file and extract images"""
    print(f"Processing PDF: {pdf_path}")
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open PDF
    pdf = pymupdf.Document(pdf_path)
    print(f"PDF loaded with {pdf.page_count} pages")
    
    docs = []
    zoom = 3.0
    mat = pymupdf.Matrix(zoom, zoom)
    
    # Get base filename for naming
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]
    
    # Process each page
    for n in tqdm(range(pdf.page_count)):
        temp = {}
        # Render the PDF page as a matrix of pixels
        pix = pdf[n].get_pixmap(matrix=mat)
        
        # Store image locally
        key = f"{output_dir}/{base_name}_page_{n+1}.png"
        pix.save(key)
        
        # Extract image metadata
        temp["key"] = key
        temp["width"] = pix.width
        temp["height"] = pix.height
        docs.append(temp)
    
    print(f"Processed {len(docs)} pages from {pdf_path}")
    return docs

def process_image_file(image_path):
    """Process a single image file"""
    print(f"Processing image: {image_path}")
    
    try:
        # Open image to get metadata
        with Image.open(image_path) as img:
            width, height = img.size
            
        # Create document entry
        doc = {
            "key": image_path,
            "width": width,
            "height": height
        }
        
        print(f"Processed image: {image_path} ({width}x{height})")
        return [doc]
        
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return []

def process_text_file(text_path):
    """Process a text file (placeholder for text processing)"""
    print(f"Processing text file: {text_path}")
    
    try:
        with open(text_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # For now, we'll create a placeholder entry
        # In a full implementation, you'd generate embeddings for the text
        doc = {
            "key": text_path,
            "content": content[:100] + "..." if len(content) > 100 else content,
            "type": "text"
        }
        
        print(f"Processed text file: {text_path}")
        return [doc]
        
    except Exception as e:
        print(f"Error processing text file {text_path}: {e}")
        return []

def load_embeddings_to_snowflake(conn, documents, embeddings_data=None):
    """Load documents and embeddings to Snowflake"""
    cursor = conn.cursor()
    
    # If no embeddings provided, use demo embeddings
    if embeddings_data is None:
        print("No embeddings provided, using demo embeddings...")
        # Use the first document's embedding as a template
        cursor.execute("SELECT EMBEDDING FROM multimodal_documents LIMIT 1")
        result = cursor.fetchone()
        if result:
            demo_embedding = [float(x) for x in result[0].split(',')]
        else:
            # Create a dummy embedding if no data exists
            demo_embedding = [0.1] * 1024
    
    for i, doc in enumerate(tqdm(documents)):
        # Use provided embedding or demo embedding
        if embeddings_data and i < len(embeddings_data):
            embedding = embeddings_data[i]
        else:
            embedding = demo_embedding
        
        # Format embedding for Snowflake
        embedding_str = format_embedding_for_snowflake(embedding)
        
        # Insert document
        insert_query = """
        INSERT INTO multimodal_documents (key, width, height, embedding)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            doc['key'],
            doc.get('width', 0),
            doc.get('height', 0),
            embedding_str
        ))
    
    cursor.close()
    conn.commit()
    print(f"Loaded {len(documents)} documents to Snowflake")

def process_directory(directory_path, file_type="auto"):
    """Process all files in a directory"""
    if not os.path.exists(directory_path):
        print(f"Directory not found: {directory_path}")
        return []
    
    all_docs = []
    
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        
        if os.path.isfile(file_path):
            if file_type == "auto":
                # Auto-detect file type
                if filename.lower().endswith('.pdf'):
                    docs = process_pdf_file(file_path)
                elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    docs = process_image_file(file_path)
                elif filename.lower().endswith(('.txt', '.md', '.csv')):
                    docs = process_text_file(file_path)
                else:
                    print(f"Skipping unsupported file: {filename}")
                    continue
            else:
                # Process based on specified type
                if file_type == "pdf" and filename.lower().endswith('.pdf'):
                    docs = process_pdf_file(file_path)
                elif file_type == "image" and filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    docs = process_image_file(file_path)
                elif file_type == "text" and filename.lower().endswith(('.txt', '.md', '.csv')):
                    docs = process_text_file(file_path)
                else:
                    continue
            
            all_docs.extend(docs)
    
    return all_docs

def main():
    """Main processing function"""
    print("🚀 Multimodal Data Processing Tool")
    print("=" * 50)
    
    # Setup Snowflake connection
    try:
        conn = setup_snowflake_connection()
        print("✅ Connected to Snowflake")
    except Exception as e:
        print(f"❌ Failed to connect to Snowflake: {e}")
        return
    
    # Process different types of files
    all_documents = []
    
    # Process PDFs
    pdf_dir = "data/pdfs"
    if os.path.exists(pdf_dir):
        print(f"\n📄 Processing PDFs in {pdf_dir}")
        pdf_docs = process_directory(pdf_dir, "pdf")
        all_documents.extend(pdf_docs)
    
    # Process Images
    image_dir = "data/images"
    if os.path.exists(image_dir):
        print(f"\n🖼️ Processing Images in {image_dir}")
        image_docs = process_directory(image_dir, "image")
        all_documents.extend(image_docs)
    
    # Process Text files
    text_dir = "data/text"
    if os.path.exists(text_dir):
        print(f"\n📝 Processing Text files in {text_dir}")
        text_docs = process_directory(text_dir, "text")
        all_documents.extend(text_docs)
    
    if all_documents:
        print(f"\n💾 Loading {len(all_documents)} documents to Snowflake...")
        load_embeddings_to_snowflake(conn, all_documents)
        print("✅ All documents processed and loaded to Snowflake!")
    else:
        print("ℹ️ No documents found to process")
    
    # Close connection
    conn.close()
    print("🔌 Snowflake connection closed")

if __name__ == "__main__":
    main()

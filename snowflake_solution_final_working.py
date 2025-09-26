#!/usr/bin/env python3
"""
Snowflake Multimodal Agents Lab - FINAL WORKING SOLUTION

This is the DEFINITIVE solution that works with Snowflake's current limitations.
Uses VARIANT storage with direct Python object insertion (no PARSE_JSON in INSERT).
"""

import os
import json
import snowflake.connector
from snowflake.connector import DictCursor
import pandas as pd
import numpy as np
import pymupdf
import requests
from tqdm import tqdm
from PIL import Image
from typing import List
from datetime import datetime
from google import genai
from google.genai import types
from google.genai.types import FunctionCall

# Load environment variables from .env file if it exists
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("python-dotenv not installed. Using system environment variables only.")

# Step 1: Setup Prerequisites
def setup_snowflake_connection():
    """Initialize Snowflake connection"""
    # Snowflake connection parameters
    SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT", "your-account.snowflakecomputing.com")
    SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER", "your-username")
    SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
    SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
    SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
    SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")

    # Fix account format - remove .snowflakecomputing.com if present
    if SNOWFLAKE_ACCOUNT.endswith('.snowflakecomputing.com'):
        SNOWFLAKE_ACCOUNT = SNOWFLAKE_ACCOUNT.replace('.snowflakecomputing.com', '')
    
    print(f"Connecting to Snowflake account: {SNOWFLAKE_ACCOUNT}")
    print(f"User: {SNOWFLAKE_USER}")
    print(f"Warehouse: {SNOWFLAKE_WAREHOUSE}")
    print(f"Database: {SNOWFLAKE_DATABASE}")
    print(f"Schema: {SNOWFLAKE_SCHEMA}")

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
    print(f"Connected to Snowflake: {cursor.fetchone()[0]}")
    cursor.close()
    
    return conn

def setup_gemini():
    """Setup Gemini client"""
    # Get Google API key from environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set. Please set it in your .env file or environment.")
    
    LLM = "gemini-2.0-flash"
    gemini_client = genai.Client(api_key=google_api_key)
    return gemini_client, LLM

# Step 2: PDF Processing
def download_and_process_pdf(pdf_url="https://arxiv.org/pdf/2501.12948"):
    """Download PDF and extract images"""
    # Download the PDF
    response = requests.get(pdf_url)
    if response.status_code != 200:
        raise ValueError(f"Failed to download PDF. Status code: {response.status_code}")

    pdf_stream = response.content
    pdf = pymupdf.Document(stream=pdf_stream, filetype="pdf")
    print(f"PDF loaded with {pdf.page_count} pages")
    
    # Create images directory if it doesn't exist
    os.makedirs("data/images", exist_ok=True)
    
    docs = []
    zoom = 3.0
    mat = pymupdf.Matrix(zoom, zoom)
    
    # Iterate through the pages of the PDF
    for n in tqdm(range(pdf.page_count)):
        temp = {}
        # Render the PDF page as a matrix of pixels
        pix = pdf[n].get_pixmap(matrix=mat)
        
        # Store image locally
        key = f"data/images/{n+1}.png"
        pix.save(key)
        
        # Extract image metadata
        temp["key"] = key
        temp["width"] = pix.width
        temp["height"] = pix.height
        docs.append(temp)
    
    print(f"Processed {len(docs)} pages")
    return docs

# Step 3: Load embeddings and store in Snowflake (VARIANT approach - direct insertion)
def load_embeddings_to_snowflake(conn):
    """Load pre-generated embeddings and store in Snowflake using VARIANT approach"""
    # Read pre-generated embeddings from JSON file
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print(f"Loaded {len(embeddings_data)} documents with embeddings")
    
    # Prepare data for Snowflake insertion
    cursor = conn.cursor()
    
    # Clear existing data
    cursor.execute("DELETE FROM multimodal_documents")
    print("Cleared existing documents from multimodal_documents table.")
    
    # Insert documents with embeddings using VARIANT approach - direct Python object
    for doc in tqdm(embeddings_data):
        # Insert using direct Python object (Snowflake will handle the VARIANT conversion)
        insert_query = """
        INSERT INTO multimodal_documents (key, width, height, embedding)
        VALUES (%s, %s, %s, %s)
        """
        
        cursor.execute(insert_query, (
            doc['key'],
            doc['width'],
            doc['height'],
            doc['embedding']  # Pass the Python list directly - Snowflake converts to VARIANT
        ))
    
    cursor.close()
    conn.commit()
    
    # Verify insertion
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM multimodal_documents")
    count = cursor.fetchone()[0]
    print(f"{count} documents ingested into the multimodal_documents table.")
    cursor.close()

# Step 4: Vector Search Function (using VARIANT to VECTOR conversion in SELECT)
def get_information_for_question_answering(conn, user_query: str, serverless_url: str = None) -> List[str]:
    """
    Retrieve information using vector search to answer a user query.
    Converts VARIANT to VECTOR in the SELECT query.

    Args:
    conn: Snowflake connection object
    user_query (str): The user's query string.
    serverless_url (str): URL for the serverless embedding endpoint

    Returns:
    List[str]: List of image keys that match the query.
    """
    # For demo purposes, use a simple query embedding (first document's embedding)
    # In production, you would use the serverless_url to get the actual embedding
    if serverless_url and serverless_url != "your-serverless-endpoint-url":
        # Embed the user query using serverless endpoint
        response = requests.post(
            url=serverless_url,
            json={
                "task": "get_embedding",
                "data": {"input": user_query, "input_type": "query"},
            },
        )
        
        # Extract the embedding from the response
        query_embedding = response.json()["embedding"]
    else:
        # Demo mode: use first document's embedding as query embedding
        print("Demo mode: Using first document's embedding as query embedding")
        cursor = conn.cursor()
        cursor.execute("SELECT embedding FROM multimodal_documents LIMIT 1")
        result = cursor.fetchone()
        if result:
            # The embedding is stored as VARIANT, so we can access it directly
            query_embedding = result[0]
        else:
            raise ValueError("No documents found in database")
        cursor.close()
    
    # Perform vector search converting VARIANT to VECTOR in SELECT
    cursor = conn.cursor(DictCursor)
    
    search_query = """
    SELECT key, width, height,
           VECTOR_COSINE_SIMILARITY(
               embedding::VECTOR(FLOAT, 1024),
               %s::VECTOR(FLOAT, 1024)
           ) as similarity_score
    FROM multimodal_documents
    ORDER BY similarity_score DESC
    LIMIT 2
    """
    
    cursor.execute(search_query, (query_embedding,))
    results = cursor.fetchall()
    cursor.close()
    
    # Get image keys from results
    keys = [result['key'] for result in results]
    print(f"Keys: {keys}")
    return keys

# Step 5: Function Declaration for Tool Calling
def create_function_declaration():
    """Create function declaration for the tool"""
    return {
        "name": "get_information_for_question_answering",
        "description": "Retrieve information using vector search to answer a user query.",
        "parameters": {
            "type": "object",
            "properties": {
                "user_query": {
                    "type": "string",
                    "description": "Query string to use for vector search",
                }
            },
            "required": ["user_query"],
        },
    }

def select_tool(gemini_client, LLM, tools_config, messages: List) -> FunctionCall | None:
    """Use an LLM to decide which tool to call"""
    system_prompt = [
        (
            "You're an AI assistant. Based on the given information, decide which tool to use."
            "If the user is asking to explain an image, don't call any tools unless that would help you better explain the image."
            "Here is the provided information:\n"
        )
    ]
    
    contents = system_prompt + messages
    response = gemini_client.models.generate_content(
        model=LLM, contents=contents, config=tools_config
    )
    
    return response.candidates[0].content.parts[0].function_call

def generate_answer(conn, gemini_client, LLM, user_query: str, images: List = [], serverless_url: str = "") -> str:
    """Execute any tools and generate a response"""
    # Create tools config
    function_declaration = create_function_declaration()
    tools = types.Tool(function_declarations=[function_declaration])
    tools_config = types.GenerateContentConfig(tools=[tools], temperature=0.0)
    
    # Use the select_tool function to get the tool config
    tool_call = select_tool(gemini_client, LLM, tools_config, [user_query])
    
    # If a tool call is found and the name matches
    if (
        tool_call is not None
        and tool_call.name == "get_information_for_question_answering"
    ):
        print(f"Agent: Calling tool: {tool_call.name}")
        # Call the tool with the arguments extracted by the LLM
        tool_images = get_information_for_question_answering(conn, **tool_call.args, serverless_url=serverless_url)
        # Add images returned by the tool to the list of input images
        images.extend(tool_images)

    system_prompt = f"Answer the questions based on the provided context only. If the context is not sufficient, say I DON'T KNOW. DO NOT use any other information to answer the question."
    
    # Pass the system prompt, user query, and content retrieved using vector search
    contents = [system_prompt] + [user_query] + [Image.open(image) for image in images]

    # Get the response from the LLM
    response = gemini_client.models.generate_content(
        model=LLM,
        contents=contents,
        config=types.GenerateContentConfig(temperature=0.0),
    )
    answer = response.text
    return answer

def execute_agent(conn, gemini_client, LLM, user_query: str, images: List = [], serverless_url: str = "") -> None:
    """Execute the agent."""
    response = generate_answer(conn, gemini_client, LLM, user_query, images, serverless_url)
    print("Agent:", response)

# Memory functions (simplified versions)
def store_chat_message(conn, session_id: str, role: str, message_type: str, content: str) -> None:
    """Create chat history document and store it in Snowflake"""
    cursor = conn.cursor()
    
    insert_query = """
    INSERT INTO chat_history (session_id, role, message_type, content)
    VALUES (%s, %s, %s, %s)
    """
    
    cursor.execute(insert_query, (session_id, role, message_type, content))
    cursor.close()
    conn.commit()

def retrieve_session_history(conn, session_id: str) -> List:
    """Retrieve chat history for a particular session."""
    cursor = conn.cursor(DictCursor)
    
    query = """
    SELECT role, message_type, content, timestamp
    FROM chat_history
    WHERE session_id = %s
    ORDER BY timestamp ASC
    """
    
    cursor.execute(query, (session_id,))
    results = cursor.fetchall()
    cursor.close()
    
    messages = []
    for msg in results:
        if msg['message_type'] == 'text':
            messages.append(msg['content'])
        elif msg['message_type'] == 'image':
            messages.append(Image.open(msg['content']))
    
    return messages

# Main execution function
def main():
    """Main execution function"""
    # Setup connections
    conn = setup_snowflake_connection()
    gemini_client, LLM = setup_gemini()
    
    # Get serverless URL from environment variables (optional)
    SERVERLESS_URL = os.getenv("SERVERLESS_URL", None)
    
    try:
        # Load embeddings to Snowflake
        load_embeddings_to_snowflake(conn)
        
        # Test the agent with a text input
        print("\n=== Testing basic agent ===")
        execute_agent(conn, gemini_client, LLM, 
                     "What is the Pass@1 accuracy of Deepseek R1 on the MATH500 benchmark?", 
                     serverless_url=SERVERLESS_URL)
        
        # Test the agent with an image input
        print("\n=== Testing agent with image ===")
        execute_agent(conn, gemini_client, LLM, 
                     "Explain the graph in this image:", 
                     images=["data/test.png"], 
                     serverless_url=SERVERLESS_URL)
        
    finally:
        # Close the Snowflake connection
        conn.close()
        print("Snowflake connection closed.")

if __name__ == "__main__":
    main()
#!/usr/bin/env python3
"""
Example Usage of Multimodal Agents Lab with New Data

This script demonstrates how to add new data and query the AI agent.
"""

import os
from snowflake_solution_working_final import (
    setup_snowflake_connection, 
    setup_gemini, 
    execute_agent
)
from process_new_data import process_pdf_file, process_image_file, process_text_file

def main():
    """Example usage of the multimodal agents lab"""
    print("🚀 Multimodal Agents Lab - Example Usage")
    print("=" * 50)
    
    # Setup connections
    print("🔌 Setting up connections...")
    conn = setup_snowflake_connection()
    gemini_client, LLM = setup_gemini()
    print("✅ Connections established")
    
    try:
        # Example 1: Process a PDF file
        print("\n📄 Example 1: Processing a PDF file")
        print("To add a PDF file:")
        print("1. Copy your PDF to: data/pdfs/your_document.pdf")
        print("2. Run: python process_new_data.py")
        print("3. Query the agent about the document")
        
        # Example 2: Process an image file
        print("\n🖼️ Example 2: Processing an image file")
        print("To add an image file:")
        print("1. Copy your image to: data/images/your_image.png")
        print("2. Run: python process_new_data.py")
        print("3. Query the agent about the image")
        
        # Example 3: Process a text file
        print("\n📝 Example 3: Processing a text file")
        print("To add a text file:")
        print("1. Copy your text to: data/text/your_document.txt")
        print("2. Run: python process_new_data.py")
        print("3. Query the agent about the text")
        
        # Example 4: Query the agent
        print("\n🤖 Example 4: Querying the AI agent")
        print("Available queries:")
        print("- 'What documents do you have access to?'")
        print("- 'Explain the content in the images'")
        print("- 'What are the main topics in the documents?'")
        print("- 'Compare the different documents'")
        
        # Run a sample query
        print("\n🔍 Running sample query...")
        execute_agent(conn, gemini_client, LLM, 
                     "What documents and images do you have access to?")
        
        # Example 5: Custom queries
        print("\n💡 Example 5: Custom queries")
        print("You can ask questions like:")
        print("- 'What is the main topic of the research paper?'")
        print("- 'Describe what you see in the product images'")
        print("- 'Summarize the key points from the documentation'")
        print("- 'What are the similarities between these documents?'")
        
        # Interactive mode
        print("\n🎯 Interactive Mode")
        print("Enter your questions (type 'quit' to exit):")
        
        while True:
            try:
                user_input = input("\n❓ Your question: ").strip()
                if user_input.lower() in ['quit', 'exit', 'q']:
                    break
                if user_input:
                    execute_agent(conn, gemini_client, LLM, user_input)
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    finally:
        # Close connection
        conn.close()
        print("\n🔌 Connection closed")
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()

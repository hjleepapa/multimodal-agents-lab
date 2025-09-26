# Snowflake Multimodal Agents Lab

A self-contained multimodal AI agents lab built using Snowflake as the vector database, Gemini, and Python.

This is a Snowflake-compatible version of the original MongoDB-based multimodal agents lab.

## Overview

This lab demonstrates how to build a multimodal AI agent that can:
- Process PDF documents and extract images
- Store multimodal embeddings in Snowflake using the VECTOR data type
- Perform vector similarity search using Snowflake's built-in functions
- Generate responses using Google's Gemini AI
- Maintain conversation history and memory
- Implement ReAct (Reasoning and Acting) agent patterns

## Prerequisites

1. **Snowflake Account**: You need a Snowflake account with appropriate permissions to create databases, schemas, and tables.

2. **Google AI Studio API Key**: Obtain a Gemini API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

3. **Voyage AI API Key** (Optional): For generating embeddings. You can also use the pre-generated embeddings provided in the lab.

4. **Python Environment**: Python 3.8+ with the required dependencies.

## Setup Instructions

### 1. Snowflake Database Setup

First, run the `snowflake_setup.sql` script in your Snowflake environment to create the necessary database structure:

```sql
-- This script creates:
-- - Database: multimodal_agents_db
-- - Schema: multimodal_schema
-- - Tables: multimodal_documents, chat_history
-- - Indexes for performance
-- - Stage for data loading
```

### 2. Environment Configuration

Set up your environment variables:

```bash
# Snowflake Connection
export SNOWFLAKE_ACCOUNT="your-account.snowflakecomputing.com"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_DATABASE="multimodal_agents_db"
export SNOWFLAKE_SCHEMA="multimodal_schema"

# Google AI API Key
export GOOGLE_API_KEY="your-google-api-key"

# Optional: Voyage AI API Key
export VOYAGE_API_KEY="your-voyage-api-key"
```

### 3. Install Dependencies

Install the required Python packages:

```bash
pip install -r snowflake_requirements.txt
```

### 4. Serverless Endpoint (Optional)

If you want to generate embeddings dynamically, you'll need to set up a serverless endpoint that can generate embeddings. Update the `SERVERLESS_URL` variable in the code with your endpoint URL.

## Key Differences from MongoDB Version

### Database Schema

**MongoDB (Original)**:
- Uses MongoDB collections
- Vector search via MongoDB Atlas Vector Search
- Document-based storage

**Snowflake (This Version)**:
- Uses Snowflake tables with VECTOR data type
- Vector search via `VECTOR_COSINE_SIMILARITY()` function
- Relational table structure

### Vector Search Implementation

**MongoDB**:
```python
pipeline = [
    {
        "$vectorSearch": {
            "index": VS_INDEX_NAME,
            "path": "embedding",
            "queryVector": query_embedding,
            "numCandidates": 150,
            "limit": 2,
        }
    }
]
```

**Snowflake**:
```python
search_query = """
SELECT key, width, height,
       VECTOR_COSINE_SIMILARITY(embedding, %s) as similarity_score
FROM multimodal_documents
ORDER BY similarity_score DESC
LIMIT 2
"""
```

### Data Storage

**MongoDB**:
- Stores embeddings as arrays in documents
- Uses MongoDB's native vector search capabilities

**Snowflake**:
- Stores embeddings as VECTOR data type
- Uses SQL-based vector similarity functions
- Better integration with existing SQL workflows

## Usage

### Basic Usage

```python
from snowflake_solution import *

# Setup connections
conn = setup_snowflake_connection()
gemini_client, LLM = setup_gemini()

# Load embeddings
load_embeddings_to_snowflake(conn)

# Test the agent
execute_agent(conn, gemini_client, LLM, 
             "What is the Pass@1 accuracy of Deepseek R1 on the MATH500 benchmark?")
```

### With Memory

```python
# Test agent with conversation memory
execute_agent_with_memory(conn, gemini_client, LLM, "session_1",
                         "What is the Pass@1 accuracy of Deepseek R1 on the MATH500 benchmark?")

# Follow-up question
execute_agent_with_memory(conn, gemini_client, LLM, "session_1",
                         "What did I just ask you?")
```

### ReAct Agent

```python
# Test ReAct (Reasoning and Acting) agent
execute_react_agent(conn, gemini_client, LLM,
                   "What is the Pass@1 accuracy of Deepseek R1 on the MATH500 benchmark?")
```

## File Structure

```
multimodal-agents-lab/
├── snowflake_solution.py          # Main Snowflake implementation
├── snowflake_requirements.txt     # Python dependencies
├── snowflake_setup.sql           # Database setup script
├── SNOWFLAKE_README.md           # This documentation
├── data/
│   ├── embeddings.json           # Pre-generated embeddings
│   └── images/                   # Extracted PDF images
└── [original MongoDB files]
```

## Key Features

### 1. Vector Search with Snowflake
- Uses Snowflake's native VECTOR data type
- Leverages `VECTOR_COSINE_SIMILARITY()` for similarity search
- SQL-based queries for better integration

### 2. Multimodal Processing
- PDF document processing and image extraction
- Image embedding generation and storage
- Text and image query processing

### 3. Agent Capabilities
- Function calling with Gemini
- Tool selection and execution
- Conversation memory and history
- ReAct agent pattern implementation

### 4. Scalability
- Snowflake's cloud-native architecture
- Automatic scaling and performance optimization
- Integration with existing data warehouse workflows

## Performance Considerations

### Snowflake Advantages
- **Scalability**: Automatic scaling based on workload
- **Performance**: Optimized vector operations
- **Integration**: Native SQL interface
- **Cost**: Pay-per-use pricing model

### Optimization Tips
1. Use appropriate warehouse sizes for your workload
2. Use clustering keys instead of traditional indexes (Snowflake doesn't use indexes on regular tables)
3. Consider using Snowflake's result caching
4. Monitor query performance using Snowflake's query history
5. Use the VECTOR data type for optimal vector search performance

## Troubleshooting

### Common Issues

1. **Connection Issues**:
   - Verify Snowflake account details
   - Check network connectivity
   - Ensure proper permissions

2. **Vector Search Issues**:
   - Verify VECTOR data type is supported in your Snowflake region
   - Check embedding dimensions match (1024 for Voyage AI)
   - Ensure proper vector format in queries

3. **API Issues**:
   - Verify Google AI API key is valid
   - Check API quotas and limits
   - Ensure proper authentication

4. **Index Creation Issues**:
   - Snowflake doesn't use traditional indexes on regular tables
   - Use clustering keys instead: `ALTER TABLE table_name CLUSTER BY (column_name)`
   - Indexes are only available for hybrid tables in Snowflake

### Getting Help

- Check Snowflake documentation for VECTOR data type
- Review Google AI documentation for Gemini API
- Consult the original MongoDB lab for comparison

## License

Same license as the original multimodal-agents-lab project.

## Contributing

Contributions are welcome! Please feel free to submit issues and enhancement requests.

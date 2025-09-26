-- Snowflake Multimodal Agents Lab - DEFINITIVE Setup
-- This script creates the necessary database objects for the DEFINITIVE solution

-- Create the multimodal_documents table with STRING for embeddings
CREATE OR REPLACE TABLE multimodal_documents (
    id STRING DEFAULT UUID_STRING(),
    key STRING NOT NULL,
    width INTEGER,
    height INTEGER,
    embedding STRING, -- Store as STRING
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create clustering keys for better performance (Snowflake doesn't use traditional indexes)
-- Clustering keys help optimize query performance by organizing data
ALTER TABLE multimodal_documents CLUSTER BY (key);

-- Create the chat_history table
CREATE OR REPLACE TABLE chat_history (
    id STRING DEFAULT UUID_STRING(),
    session_id STRING NOT NULL,
    role STRING NOT NULL,
    message_type STRING NOT NULL,
    content STRING,
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- For chat_history, we can cluster by session_id for better performance on session-based queries
ALTER TABLE chat_history CLUSTER BY (session_id, timestamp);

-- Create stored procedure for vector search
CREATE OR REPLACE PROCEDURE vector_search(
    query_embedding_str STRING,
    result_limit INTEGER
)
RETURNS TABLE (
    key STRING,
    width INTEGER,
    height INTEGER,
    similarity_score FLOAT
)
LANGUAGE SQL
AS
$$
DECLARE
    query_vector VECTOR(FLOAT, 1024);
BEGIN
    -- Convert query string to vector
    query_vector := STRTOK_TO_ARRAY(query_embedding_str, ',')::VECTOR(FLOAT, 1024);
    
    -- Return vector search results
    RETURN TABLE(
        SELECT 
            key,
            width,
            height,
            VECTOR_COSINE_SIMILARITY(
                STRTOK_TO_ARRAY(embedding, ',')::VECTOR(FLOAT, 1024),
                query_vector
            ) as similarity_score
        FROM multimodal_documents
        ORDER BY similarity_score DESC
        LIMIT result_limit
    );
END;
$$;

-- Verify objects were created
SELECT 'multimodal_documents table created' as status;
SELECT 'chat_history table created' as status;
SELECT 'vector_search procedure created' as status;

-- Show table structure
DESCRIBE TABLE multimodal_documents;
DESCRIBE TABLE chat_history;
DESCRIBE PROCEDURE vector_search(STRING, INTEGER);

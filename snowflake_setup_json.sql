-- Snowflake Multimodal Agents Lab - JSON Storage Setup
-- This script creates the necessary database objects for the JSON storage approach

-- Create the multimodal_documents table with VARIANT for embeddings
CREATE OR REPLACE TABLE multimodal_documents (
    id STRING DEFAULT UUID_STRING(),
    key STRING NOT NULL,
    width INTEGER,
    height INTEGER,
    embedding VARIANT, -- Store as VARIANT (JSON)
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

-- Verify tables were created
SELECT 'multimodal_documents table created' as status;
SELECT 'chat_history table created' as status;

-- Show table structure
DESCRIBE TABLE multimodal_documents;
DESCRIBE TABLE chat_history;

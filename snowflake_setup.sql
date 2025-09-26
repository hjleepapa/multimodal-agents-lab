-- Snowflake Setup Script for Multimodal Agents Lab
-- This script creates the necessary database, schema, and tables for the multimodal agent

-- Create database
CREATE DATABASE IF NOT EXISTS multimodal_agents_db;

-- Use the database
USE DATABASE multimodal_agents_db;

-- Create schema
CREATE SCHEMA IF NOT EXISTS multimodal_schema;

-- Use the schema
USE SCHEMA multimodal_schema;

-- Create table for storing multimodal documents with embeddings
CREATE OR REPLACE TABLE multimodal_documents (
    id STRING DEFAULT UUID_STRING(),
    key STRING NOT NULL,
    width INTEGER,
    height INTEGER,
    embedding VECTOR(FLOAT, 1024), -- Voyage AI multimodal-3 embeddings are 1024 dimensions
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create table for chat history
CREATE OR REPLACE TABLE chat_history (
    id STRING DEFAULT UUID_STRING(),
    session_id STRING NOT NULL,
    role STRING NOT NULL, -- 'user' or 'agent'
    message_type STRING NOT NULL, -- 'text' or 'image'
    content STRING NOT NULL,
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- Create clustering keys for better performance (Snowflake doesn't use traditional indexes)
-- Clustering keys help optimize query performance by organizing data
ALTER TABLE multimodal_documents CLUSTER BY (key);

-- For chat_history, we can cluster by session_id for better performance on session-based queries
ALTER TABLE chat_history CLUSTER BY (session_id, timestamp);

-- Create a stage for loading data from local files (if needed)
CREATE OR REPLACE STAGE multimodal_stage
    FILE_FORMAT = (TYPE = 'JSON');

-- Grant necessary permissions (adjust as needed for your environment)
-- GRANT USAGE ON DATABASE multimodal_agents_db TO ROLE your_role;
-- GRANT USAGE ON SCHEMA multimodal_schema TO ROLE your_role;
-- GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA multimodal_schema TO ROLE your_role;

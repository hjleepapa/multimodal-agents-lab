"""
Configuration file for Snowflake Multimodal Agents Lab

This file contains configuration settings and environment variable management
for the Snowflake-based multimodal agent system.
"""

import os
from typing import Optional

class SnowflakeConfig:
    """Configuration class for Snowflake connection and settings"""
    
    def __init__(self):
        # Snowflake Connection Parameters
        self.account = os.getenv("SNOWFLAKE_ACCOUNT", "your-account.snowflakecomputing.com")
        self.user = os.getenv("SNOWFLAKE_USER", "your-username")
        self.password = os.getenv("SNOWFLAKE_PASSWORD", "your-password")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
        self.database = os.getenv("SNOWFLAKE_DATABASE", "multimodal_agents_db")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA", "multimodal_schema")
        self.role = os.getenv("SNOWFLAKE_ROLE", "ACCOUNTADMIN")  # Optional
        
        # API Keys
        self.google_api_key = os.getenv("GOOGLE_API_KEY", "your-google-api-key")
        self.voyage_api_key = os.getenv("VOYAGE_API_KEY", "your-voyage-api-key")
        
        # Serverless Endpoint
        self.serverless_url = os.getenv("SERVERLESS_URL", "your-serverless-endpoint-url")
        
        # Model Settings
        self.llm_model = os.getenv("LLM_MODEL", "gemini-2.0-flash")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "voyage-multimodal-3")
        self.embedding_dimensions = int(os.getenv("EMBEDDING_DIMENSIONS", "1024"))
        
        # Vector Search Settings
        self.similarity_metric = os.getenv("SIMILARITY_METRIC", "cosine")
        self.max_results = int(os.getenv("MAX_SEARCH_RESULTS", "2"))
        self.similarity_threshold = float(os.getenv("SIMILARITY_THRESHOLD", "0.0"))
        
        # Agent Settings
        self.max_iterations = int(os.getenv("MAX_ITERATIONS", "3"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.0"))
        
        # File Paths
        self.data_dir = os.getenv("DATA_DIR", "data")
        self.images_dir = os.path.join(self.data_dir, "images")
        self.embeddings_file = os.path.join(self.data_dir, "embeddings.json")
        
        # PDF Processing Settings
        self.pdf_zoom = float(os.getenv("PDF_ZOOM", "3.0"))
        self.pdf_url = os.getenv("PDF_URL", "https://arxiv.org/pdf/2501.12948")
    
    def validate_config(self) -> bool:
        """Validate that required configuration is present"""
        required_fields = [
            "account", "user", "password", "google_api_key"
        ]
        
        missing_fields = []
        for field in required_fields:
            if not getattr(self, field) or getattr(self, field).startswith("your-"):
                missing_fields.append(field)
        
        if missing_fields:
            print(f"Missing or invalid configuration for: {', '.join(missing_fields)}")
            return False
        
        return True
    
    def get_connection_params(self) -> dict:
        """Get Snowflake connection parameters"""
        params = {
            "account": self.account,
            "user": self.user,
            "password": self.password,
            "warehouse": self.warehouse,
            "database": self.database,
            "schema": self.schema
        }
        
        if self.role:
            params["role"] = self.role
            
        return params
    
    def setup_environment(self):
        """Setup environment variables for external libraries"""
        os.environ["GOOGLE_API_KEY"] = self.google_api_key
        if self.voyage_api_key:
            os.environ["VOYAGE_API_KEY"] = self.voyage_api_key

# Global configuration instance
config = SnowflakeConfig()

def get_config() -> SnowflakeConfig:
    """Get the global configuration instance"""
    return config

def validate_and_setup() -> bool:
    """Validate configuration and setup environment"""
    if not config.validate_config():
        return False
    
    config.setup_environment()
    return True

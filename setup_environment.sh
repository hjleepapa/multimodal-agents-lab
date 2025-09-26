#!/bin/bash

# Snowflake Multimodal Agents Lab - Environment Setup Script
# This script helps you set up the environment variables needed for the lab

echo "🔧 Snowflake Multimodal Agents Lab - Environment Setup"
echo "======================================================"

# Function to prompt for input with default value
prompt_with_default() {
    local prompt="$1"
    local default="$2"
    local var_name="$3"
    
    echo -n "$prompt [$default]: "
    read input
    if [ -z "$input" ]; then
        input="$default"
    fi
    export "$var_name"="$input"
}

echo ""
echo "📋 Please provide your Snowflake connection details:"
echo ""

# Snowflake Account
prompt_with_default "Snowflake Account Identifier" "CSWRMBD-HUB94431" "SNOWFLAKE_ACCOUNT"

# Snowflake User
prompt_with_default "Snowflake Username" "your-username" "SNOWFLAKE_USER"

# Snowflake Password
echo -n "Snowflake Password: "
read -s SNOWFLAKE_PASSWORD
export SNOWFLAKE_PASSWORD="$SNOWFLAKE_PASSWORD"
echo ""

# Warehouse
prompt_with_default "Warehouse Name" "COMPUTE_WH" "SNOWFLAKE_WAREHOUSE"

# Database
prompt_with_default "Database Name" "multimodal_agents_db" "SNOWFLAKE_DATABASE"

# Schema
prompt_with_default "Schema Name" "multimodal_schema" "SNOWFLAKE_SCHEMA"

echo ""
echo "🔑 Please provide your API keys:"
echo ""

# Google API Key
prompt_with_default "Google AI API Key" "your-google-api-key" "GOOGLE_API_KEY"

# Voyage AI API Key (optional)
prompt_with_default "Voyage AI API Key (optional)" "your-voyage-api-key" "VOYAGE_API_KEY"

echo ""
echo "📊 Environment Variables Set:"
echo "============================="
echo "SNOWFLAKE_ACCOUNT=$SNOWFLAKE_ACCOUNT"
echo "SNOWFLAKE_USER=$SNOWFLAKE_USER"
echo "SNOWFLAKE_PASSWORD=***hidden***"
echo "SNOWFLAKE_WAREHOUSE=$SNOWFLAKE_WAREHOUSE"
echo "SNOWFLAKE_DATABASE=$SNOWFLAKE_DATABASE"
echo "SNOWFLAKE_SCHEMA=$SNOWFLAKE_SCHEMA"
echo "GOOGLE_API_KEY=$GOOGLE_API_KEY"
echo "VOYAGE_API_KEY=$VOYAGE_API_KEY"

echo ""
echo "🧪 Testing Snowflake Connection..."
python3 test_snowflake_connection.py

if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 Setup complete! You can now run:"
    echo "python3 snowflake_solution.py"
else
    echo ""
    echo "❌ Connection test failed. Please check your credentials and try again."
fi

# Quick Start Guide - Snowflake Multimodal Agents Lab

## 🚀 Get Started in 3 Steps

### Step 1: Set Up Environment Variables

You have two options:

#### Option A: Interactive Setup (Recommended)
```bash
./setup_environment.sh
```

#### Option B: Manual Setup
```bash
export SNOWFLAKE_ACCOUNT="CSWRMBD-HUB94431"  # Your account identifier
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_DATABASE="multimodal_agents_db"
export SNOWFLAKE_SCHEMA="multimodal_schema"
export GOOGLE_API_KEY="your-google-api-key"
```

### Step 2: Set Up Snowflake Database

Run the SQL setup script in your Snowflake environment:
```sql
-- Copy and paste the contents of snowflake_setup.sql into your Snowflake worksheet
-- Then execute it to create the database schema
```

### Step 3: Test and Run

Test your connection:
```bash
python3 test_snowflake_connection.py
```

If successful, run the full solution:
```bash
python3 snowflake_solution.py
```

## 🔧 Troubleshooting

### Connection Issues

**Error: 404 Not Found with double .snowflakecomputing.com**
- **Solution**: Make sure your `SNOWFLAKE_ACCOUNT` is just the account identifier (e.g., `CSWRMBD-HUB94431`), not the full URL

**Error: Invalid credentials**
- **Solution**: Verify your username and password are correct

**Error: Warehouse/Database not found**
- **Solution**: Make sure you've run the `snowflake_setup.sql` script first

**Error: VECTOR data type mismatch**
- **Solution**: The solution now passes arrays directly to Snowflake VECTOR columns
- Test VECTOR support: `python3 test_with_credentials.py`

### Import Issues

**Error: ModuleNotFoundError**
- **Solution**: Make sure you're in the virtual environment and dependencies are installed:
  ```bash
  pip install -r snowflake_requirements.txt
  ```

## 📁 Key Files

- `snowflake_solution.py` - Main implementation
- `snowflake_setup.sql` - Database setup script
- `test_snowflake_connection.py` - Connection test
- `setup_environment.sh` - Interactive environment setup
- `snowflake_requirements.txt` - Python dependencies

## 🎯 What This Lab Does

1. **PDF Processing**: Downloads and processes PDF documents
2. **Image Extraction**: Converts PDF pages to images
3. **Vector Embeddings**: Stores multimodal embeddings in Snowflake
4. **Vector Search**: Performs similarity search using Snowflake's VECTOR functions
5. **AI Agent**: Uses Gemini for intelligent responses
6. **Memory**: Maintains conversation history
7. **ReAct Pattern**: Implements reasoning and acting for complex queries

## 🔗 Additional Resources

- [Snowflake VECTOR Data Type Documentation](https://docs.snowflake.com/en/sql-reference/data-types-vector)
- [Google AI Studio](https://aistudio.google.com/)
- [Voyage AI Documentation](https://docs.voyageai.com/)

## 💡 Tips

1. **Account Format**: Use just the account identifier, not the full URL
2. **Permissions**: Make sure your user has CREATE and INSERT permissions
3. **Warehouse**: Ensure your warehouse is running and accessible
4. **API Keys**: Get your Google AI API key from [Google AI Studio](https://aistudio.google.com/app/apikey)

Happy coding! 🎉

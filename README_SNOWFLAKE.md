# 🚀 Multimodal Agents Lab - Snowflake Edition

A complete multimodal AI agent solution that processes PDF documents, generates embeddings, and provides intelligent querying capabilities using **Snowflake** as the data platform and **Google Gemini** for AI processing.

## 🌟 Features

- **📄 PDF Processing**: Extract images and text from PDF documents
- **🧠 Multimodal Embeddings**: Generate and store embeddings for both text and images
- **🔍 Vector Search**: Intelligent similarity search using Python-based vector operations
- **🤖 AI Agent**: Google Gemini-powered agent with function calling capabilities
- **💾 Snowflake Integration**: Robust data storage and retrieval using Snowflake
- **🔄 ReAct Pattern**: Reasoning and action-taking agent architecture
- **📊 Memory Management**: Persistent chat history and session management

## 🏗️ Architecture

```
PDF Documents → Image Extraction → Embedding Generation → Snowflake Storage
                                                                    ↓
User Query → Vector Search → AI Agent → Response Generation
```

### Key Components:
- **Data Layer**: Snowflake database with STRING-based embedding storage
- **Processing Layer**: PDF processing, embedding generation, vector operations
- **AI Layer**: Google Gemini integration for function calling and response generation
- **Agent Layer**: ReAct-style agent with tool calling capabilities
- **Memory Layer**: Chat history persistence in Snowflake

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Snowflake account
- Google API key for Gemini
- Voyage AI API key (optional, for custom embeddings)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/hjleepapa/multimodal-agents-lab.git
   cd multimodal-agents-lab
   ```

2. **Set up virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r snowflake_requirements.txt
   ```

4. **Configure environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

5. **Set up Snowflake database**:
   ```bash
   python -c "
   import snowflake.connector
   from dotenv import load_dotenv
   import os
   load_dotenv()
   
   conn = snowflake.connector.connect(
       account=os.getenv('SNOWFLAKE_ACCOUNT'),
       user=os.getenv('SNOWFLAKE_USER'),
       password=os.getenv('SNOWFLAKE_PASSWORD'),
       warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
       database=os.getenv('SNOWFLAKE_DATABASE'),
       schema=os.getenv('SNOWFLAKE_SCHEMA')
   )
   
   with open('snowflake_setup_final_working.sql', 'r') as f:
       sql = f.read()
   
   cursor = conn.cursor()
   cursor.execute(sql)
   cursor.close()
   conn.close()
   print('Snowflake setup complete!')
   "
   ```

6. **Run the solution**:
   ```bash
   python snowflake_solution_working_final.py
   ```

## 📁 Project Structure

```
multimodal-agents-lab/
├── 📄 snowflake_solution_working_final.py    # Main working solution
├── 🗄️ snowflake_setup_final_working.sql     # Database schema
├── 📋 snowflake_requirements.txt             # Python dependencies
├── 🔧 setup_environment.sh                   # Environment setup script
├── 📚 Documentation/
│   ├── SNOWFLAKE_README.md                   # Comprehensive guide
│   ├── QUICK_START.md                        # Quick start guide
│   ├── migration_guide.md                    # MongoDB to Snowflake migration
│   └── FINAL_WORKING_SOLUTION.md             # Technical details
├── 🧪 Test Scripts/
│   ├── test_working_final_solution.py        # Main test script
│   ├── test_snowflake_connection.py          # Connection testing
│   └── debug_*.py                            # Debug utilities
└── 📊 data/
    ├── embeddings.json                       # Pre-generated embeddings
    └── images/                               # Extracted PDF images
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Snowflake Configuration
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=multimodal_agents_db
SNOWFLAKE_SCHEMA=multimodal_schema

# Google API Configuration
GOOGLE_API_KEY=your-google-api-key

# Optional: Voyage AI for custom embeddings
VOYAGE_API_KEY=your-voyage-api-key
SERVERLESS_URL=your-serverless-endpoint-url
```

## 🎯 Usage Examples

### Basic Text Query
```python
from snowflake_solution_working_final import execute_agent, setup_snowflake_connection, setup_gemini

# Setup
conn = setup_snowflake_connection()
gemini_client, LLM = setup_gemini()

# Query
execute_agent(conn, gemini_client, LLM, 
             "What is the Pass@1 accuracy of Deepseek R1 on the MATH500 benchmark?")
```

### Image Analysis
```python
# Analyze an image
execute_agent(conn, gemini_client, LLM, 
             "Explain the graph in this image:", 
             images=["data/test.png"])
```

## 🏆 Key Technical Innovations

### 1. Snowflake VECTOR Workaround
- **Problem**: Snowflake VECTOR data type limitations with Python parameter binding
- **Solution**: STRING storage + Python-based vector operations
- **Benefits**: Full compatibility with existing Snowflake infrastructure

### 2. Hybrid Vector Search
- **Approach**: Store in Snowflake, compute in Python
- **Benefits**: Best of both worlds - scalable storage + flexible computation

### 3. Scientific Notation Handling
- **Problem**: Embedding values in scientific notation cause parsing errors
- **Solution**: Custom formatting with precision control
- **Benefits**: Reliable data serialization/deserialization

## 📊 Performance Characteristics

- **Embedding Storage**: Efficient STRING-based storage in Snowflake
- **Vector Search**: O(n) complexity with Python optimization
- **Memory Usage**: Optimized with batch processing and cleanup
- **Scalability**: Snowflake's distributed architecture + Python's computational flexibility

## 🧪 Testing

Run the comprehensive test suite:

```bash
# Test Snowflake connection
python test_snowflake_connection.py

# Test the complete solution
python test_working_final_solution.py

# Test specific components
python test_snowflake_only.py
```

## 📚 Documentation

- **[SNOWFLAKE_README.md](SNOWFLAKE_README.md)**: Comprehensive technical guide
- **[QUICK_START.md](QUICK_START.md)**: Quick start instructions
- **[migration_guide.md](migration_guide.md)**: MongoDB to Snowflake migration guide
- **[FINAL_WORKING_SOLUTION.md](FINAL_WORKING_SOLUTION.md)**: Technical implementation details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Original multimodal agents lab by MongoDB
- Google Gemini for AI capabilities
- Snowflake for data platform
- Voyage AI for embedding generation

## 📞 Support

For questions and support:
- Create an issue in this repository
- Check the documentation in the `/docs` folder
- Review the troubleshooting guides

---

**Made with ❤️ by [hjleepapa](https://github.com/hjleepapa)**

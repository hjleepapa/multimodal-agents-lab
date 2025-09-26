# 📁 Data Directory Structure

This directory contains all the data files for the Multimodal Agents Lab project.

## 📂 Directory Structure

```
data/
├── 📄 pdfs/                 # PDF documents to process
├── 🖼️ images/              # Image files (PNG, JPG, etc.)
├── 📝 text/                # Text files (TXT, MD, CSV)
├── 🧠 embeddings.json      # Pre-generated embeddings
├── 🖼️ test.png            # Test image file
└── 📋 README.md           # This file
```

## 🚀 How to Add New Data

### 1. **PDF Files** 📄
- **Location**: `data/pdfs/`
- **Supported formats**: `.pdf`
- **Processing**: Automatically extracts images from each page
- **Output**: Images saved to `data/images/` with naming: `{filename}_page_{number}.png`

**Example**:
```bash
# Add your PDF file
cp your_document.pdf data/pdfs/

# Process the PDF
python process_new_data.py
```

### 2. **Image Files** 🖼️
- **Location**: `data/images/`
- **Supported formats**: `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`
- **Processing**: Extracts metadata (width, height) and prepares for embedding

**Example**:
```bash
# Add your image files
cp your_image.png data/images/
cp your_photo.jpg data/images/

# Process the images
python process_new_data.py
```

### 3. **Text Files** 📝
- **Location**: `data/text/`
- **Supported formats**: `.txt`, `.md`, `.csv`
- **Processing**: Reads content and prepares for text embedding (placeholder implementation)

**Example**:
```bash
# Add your text files
cp your_document.txt data/text/
cp your_notes.md data/text/

# Process the text files
python process_new_data.py
```

## 🔧 Processing New Data

### **Automatic Processing**
```bash
# Process all new files in data directories
python process_new_data.py
```

### **Manual Processing**
```python
from process_new_data import process_pdf_file, process_image_file, process_text_file

# Process a specific PDF
docs = process_pdf_file("data/pdfs/my_document.pdf")

# Process a specific image
docs = process_image_file("data/images/my_image.png")

# Process a specific text file
docs = process_text_file("data/text/my_document.txt")
```

## 📊 Data Flow

```
New Files → process_new_data.py → Snowflake Database → AI Agent
    ↓              ↓                    ↓              ↓
PDF/Images    Extract & Process    Store Embeddings   Query & Analyze
```

## 🎯 Usage Examples

### **Adding a Research Paper**
```bash
# 1. Add PDF to data/pdfs/
cp research_paper.pdf data/pdfs/

# 2. Process the PDF
python process_new_data.py

# 3. Query the agent
python snowflake_solution_working_final.py
# Then ask: "What are the main findings in the research paper?"
```

### **Adding Product Images**
```bash
# 1. Add images to data/images/
cp product1.png data/images/
cp product2.jpg data/images/

# 2. Process the images
python process_new_data.py

# 3. Query the agent
python snowflake_solution_working_final.py
# Then ask: "Compare these products" or "What do you see in these images?"
```

### **Adding Documentation**
```bash
# 1. Add text files to data/text/
cp user_manual.txt data/text/
cp api_docs.md data/text/

# 2. Process the text files
python process_new_data.py

# 3. Query the agent
python snowflake_solution_working_final.py
# Then ask: "How do I use the API?" or "What's in the user manual?"
```

## ⚙️ Configuration

### **Environment Variables**
Make sure your `.env` file contains:
```env
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-username
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=multimodal_agents_db
SNOWFLAKE_SCHEMA=multimodal_schema
GOOGLE_API_KEY=your-google-api-key
```

### **Snowflake Setup**
Ensure your Snowflake database is set up:
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

## 🧪 Testing

### **Test Data Processing**
```bash
# Test with sample data
python process_new_data.py

# Check Snowflake for new data
python test_snowflake_connection.py
```

### **Test AI Agent**
```bash
# Run the complete solution
python snowflake_solution_working_final.py

# Test specific queries
python -c "
from snowflake_solution_working_final import execute_agent, setup_snowflake_connection, setup_gemini
conn = setup_snowflake_connection()
gemini_client, LLM = setup_gemini()
execute_agent(conn, gemini_client, LLM, 'What new data was added?')
conn.close()
"
```

## 📋 Best Practices

1. **File Naming**: Use descriptive names without spaces
2. **File Size**: Keep files under 100MB for optimal processing
3. **Batch Processing**: Add multiple files and process them together
4. **Backup**: Keep original files in a separate location
5. **Testing**: Always test with a small dataset first

## 🚨 Troubleshooting

### **Common Issues**

1. **"Directory not found"**: Ensure the data directories exist
2. **"Snowflake connection failed"**: Check your `.env` file
3. **"No documents found"**: Verify files are in the correct directories
4. **"Processing failed"**: Check file formats and permissions

### **Debug Commands**
```bash
# Check directory structure
ls -la data/

# Check file permissions
ls -la data/pdfs/ data/images/ data/text/

# Test Snowflake connection
python test_snowflake_connection.py

# Check processed data
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

cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM multimodal_documents')
count = cursor.fetchone()[0]
print(f'Total documents in database: {count}')

cursor.execute('SELECT KEY FROM multimodal_documents ORDER BY created_at DESC LIMIT 5')
recent = cursor.fetchall()
print('Recent documents:')
for doc in recent:
    print(f'  - {doc[0]}')

cursor.close()
conn.close()
"
```

## 📚 Related Files

- `process_new_data.py` - Main data processing script
- `snowflake_solution_working_final.py` - AI agent solution
- `snowflake_setup_final_working.sql` - Database schema
- `test_snowflake_connection.py` - Connection testing

---

**Happy data processing! 🎉**

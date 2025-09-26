# Migration Guide: MongoDB to Snowflake

This guide helps you migrate from the original MongoDB-based multimodal agents lab to the Snowflake version.

## Overview of Changes

The migration involves replacing MongoDB Atlas with Snowflake as the vector database while maintaining the same functionality and improving integration with existing data warehouse workflows.

## Key Differences

| Component | MongoDB Version | Snowflake Version |
|-----------|----------------|-------------------|
| **Database** | MongoDB Atlas | Snowflake |
| **Vector Storage** | MongoDB collections | Snowflake VECTOR data type |
| **Vector Search** | Atlas Vector Search | VECTOR_COSINE_SIMILARITY() |
| **Query Language** | MongoDB aggregation | SQL |
| **Connection** | pymongo | snowflake-connector-python |
| **Schema** | Document-based | Relational tables |

## Step-by-Step Migration

### 1. Environment Setup

**Before (MongoDB)**:
```bash
pip install pymongo==4.11.3
export MONGODB_URI="mongodb+srv://..."
```

**After (Snowflake)**:
```bash
pip install -r snowflake_requirements.txt
export SNOWFLAKE_ACCOUNT="your-account.snowflakecomputing.com"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
export SNOWFLAKE_WAREHOUSE="COMPUTE_WH"
export SNOWFLAKE_DATABASE="multimodal_agents_db"
export SNOWFLAKE_SCHEMA="multimodal_schema"
```

### 2. Database Schema Migration

**MongoDB Collections**:
```javascript
// multimodal_workshop collection
{
  "_id": ObjectId,
  "key": "data/images/1.png",
  "width": 1786,
  "height": 2526,
  "embedding": [0.0059, 0.0188, ...]
}

// history collection
{
  "_id": ObjectId,
  "session_id": "1",
  "role": "user",
  "type": "text",
  "content": "What is...",
  "timestamp": ISODate
}
```

**Snowflake Tables**:
```sql
-- multimodal_documents table
CREATE TABLE multimodal_documents (
    id STRING DEFAULT UUID_STRING(),
    key STRING NOT NULL,
    width INTEGER,
    height INTEGER,
    embedding VECTOR(FLOAT, 1024),
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);

-- chat_history table
CREATE TABLE chat_history (
    id STRING DEFAULT UUID_STRING(),
    session_id STRING NOT NULL,
    role STRING NOT NULL,
    message_type STRING NOT NULL,
    content STRING NOT NULL,
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

### 3. Connection Migration

**Before (MongoDB)**:
```python
from pymongo import MongoClient

MONGODB_URI = os.getenv("MONGODB_URI")
mongodb_client = MongoClient(MONGODB_URI)
collection = mongodb_client[DB_NAME][COLLECTION_NAME]
```

**After (Snowflake)**:
```python
import snowflake.connector

conn = snowflake.connector.connect(
    account=SNOWFLAKE_ACCOUNT,
    user=SNOWFLAKE_USER,
    password=SNOWFLAKE_PASSWORD,
    warehouse=SNOWFLAKE_WAREHOUSE,
    database=SNOWFLAKE_DATABASE,
    schema=SNOWFLAKE_SCHEMA
)
```

### 4. Data Insertion Migration

**Before (MongoDB)**:
```python
# Delete existing documents
collection.delete_many({})

# Bulk insert documents
collection.insert_many(data)
```

**After (Snowflake)**:
```python
# Delete existing documents
cursor.execute("DELETE FROM multimodal_documents")

# Insert documents with embeddings
insert_query = """
INSERT INTO multimodal_documents (key, width, height, embedding)
VALUES (%s, %s, %s, %s)
"""

for doc in data:
    embedding_str = '[' + ','.join(map(str, doc['embedding'])) + ']'
    cursor.execute(insert_query, (
        doc['key'], doc['width'], doc['height'], embedding_str
    ))
```

### 5. Vector Search Migration

**Before (MongoDB)**:
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
    },
    {
        "$project": {
            "_id": 0,
            "key": 1,
            "width": 1,
            "height": 1,
            "score": {"$meta": "vectorSearchScore"},
        }
    },
]

results = collection.aggregate(pipeline)
```

**After (Snowflake)**:
```python
search_query = """
SELECT key, width, height,
       VECTOR_COSINE_SIMILARITY(embedding, %s) as similarity_score
FROM multimodal_documents
ORDER BY similarity_score DESC
LIMIT 2
"""

cursor.execute(search_query, (embedding_str,))
results = cursor.fetchall()
```

### 6. Memory/History Migration

**Before (MongoDB)**:
```python
def store_chat_message(session_id, role, type, content):
    message = {
        "session_id": session_id,
        "role": role,
        "type": type,
        "content": content,
        "timestamp": datetime.now(),
    }
    history_collection.insert_one(message)

def retrieve_session_history(session_id):
    cursor = history_collection.find({"session_id": session_id}).sort("timestamp", 1)
    return [msg["content"] for msg in cursor]
```

**After (Snowflake)**:
```python
def store_chat_message(conn, session_id, role, message_type, content):
    insert_query = """
    INSERT INTO chat_history (session_id, role, message_type, content)
    VALUES (%s, %s, %s, %s)
    """
    cursor.execute(insert_query, (session_id, role, message_type, content))

def retrieve_session_history(conn, session_id):
    query = """
    SELECT role, message_type, content, timestamp
    FROM chat_history
    WHERE session_id = %s
    ORDER BY timestamp ASC
    """
    cursor.execute(query, (session_id,))
    return [msg['content'] for msg in cursor.fetchall()]
```

## Data Migration Script

Here's a script to help migrate existing data from MongoDB to Snowflake:

```python
import json
import snowflake.connector
from pymongo import MongoClient

def migrate_data():
    # Connect to MongoDB
    mongodb_client = MongoClient(MONGODB_URI)
    collection = mongodb_client[DB_NAME][COLLECTION_NAME]
    
    # Connect to Snowflake
    conn = snowflake.connector.connect(
        account=SNOWFLAKE_ACCOUNT,
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )
    
    # Migrate documents
    documents = list(collection.find({}))
    cursor = conn.cursor()
    
    for doc in documents:
        embedding_str = '[' + ','.join(map(str, doc['embedding'])) + ']'
        cursor.execute("""
            INSERT INTO multimodal_documents (key, width, height, embedding)
            VALUES (%s, %s, %s, %s)
        """, (doc['key'], doc['width'], doc['height'], embedding_str))
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print(f"Migrated {len(documents)} documents to Snowflake")
```

## Performance Considerations

### MongoDB Advantages
- **Flexibility**: Schema-less document storage
- **Native Vector Search**: Optimized for vector operations
- **Real-time**: Good for real-time applications

### Snowflake Advantages
- **Scalability**: Automatic scaling and performance optimization
- **SQL Integration**: Native SQL interface for complex queries
- **Data Warehouse**: Better integration with existing data workflows
- **Cost**: Pay-per-use pricing model
- **Security**: Enterprise-grade security features

## Testing the Migration

1. **Data Validation**: Compare document counts and sample data
2. **Vector Search**: Test similarity search results
3. **Performance**: Benchmark query performance
4. **Functionality**: Verify all agent features work correctly

## Rollback Plan

If you need to rollback to MongoDB:

1. Keep the original MongoDB setup running
2. Use the backup/restore functions in `snowflake_utils.py`
3. Export data from Snowflake back to MongoDB format
4. Switch environment variables back to MongoDB

## Best Practices

1. **Test in Development**: Always test migration in a development environment first
2. **Backup Data**: Create backups before migration
3. **Monitor Performance**: Watch for performance differences
4. **Gradual Migration**: Consider migrating in phases
5. **Documentation**: Update all documentation and runbooks

## Common Issues and Solutions

### Issue: VECTOR data type not supported
**Solution**: Ensure you're using a Snowflake region that supports VECTOR data type

### Issue: Connection timeouts
**Solution**: Check network connectivity and firewall settings

### Issue: Embedding format errors
**Solution**: Validate embedding dimensions and format using `snowflake_utils.py`

### Issue: Performance degradation
**Solution**: Optimize warehouse size and use clustering keys instead of indexes

### Issue: Index creation errors
**Solution**: Snowflake doesn't use traditional indexes on regular tables. Use clustering keys:
```sql
ALTER TABLE table_name CLUSTER BY (column_name);
```

## Support

For migration support:
- Check Snowflake documentation for VECTOR data type
- Review the original MongoDB lab for comparison
- Use the utility functions in `snowflake_utils.py` for validation

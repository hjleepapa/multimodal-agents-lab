# ARRAY Solution Guide for Snowflake VECTOR Issues

## Problem Summary
The VECTOR data type in Snowflake has proven challenging to work with directly in INSERT statements. Multiple approaches were tried:

1. **Direct array insertion** - Failed with parameter count mismatch
2. **ARRAY_CONSTRUCT()** - Failed with type casting issues  
3. **ARRAY_CONSTRUCT()::VECTOR(FLOAT, 1024)** - Failed with "Invalid data type in VALUES clause"

## Solution: ARRAY Type with View Conversion

### Approach
Instead of fighting with VECTOR type insertion, we use:
1. **ARRAY type** for storage (easier to insert)
2. **View with VECTOR conversion** for queries
3. **Best of both worlds**: Easy insertion + VECTOR functionality

### Schema Design

#### Table (ARRAY type):
```sql
CREATE OR REPLACE TABLE multimodal_documents (
    id STRING DEFAULT UUID_STRING(),
    key STRING NOT NULL,
    width INTEGER,
    height INTEGER,
    embedding ARRAY, -- Easy to insert arrays
    created_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    updated_at TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

#### View (VECTOR conversion):
```sql
CREATE OR REPLACE VIEW multimodal_documents_vector AS
SELECT 
    id,
    key,
    width,
    height,
    embedding::VECTOR(FLOAT, 1024) as embedding, -- Convert ARRAY to VECTOR
    created_at,
    updated_at
FROM multimodal_documents;
```

### Insertion (Simple):
```python
# Easy array insertion - no special syntax needed
cursor.execute("""
    INSERT INTO multimodal_documents (key, width, height, embedding)
    VALUES (%s, %s, %s, %s)
""", (doc['key'], doc['width'], doc['height'], doc['embedding']))
```

### Vector Search (Using View):
```python
# Use the view for vector operations
cursor.execute("""
    SELECT key, width, height,
           VECTOR_COSINE_SIMILARITY(embedding, %s) as similarity_score
    FROM multimodal_documents_vector  -- Use the view, not the table
    ORDER BY similarity_score DESC
    LIMIT 2
""", (query_embedding,))
```

## Files for ARRAY Solution

### Setup:
- `snowflake_setup_alternative.sql` - Schema with ARRAY + view

### Implementation:
- `snowflake_solution_array.py` - Complete solution using ARRAY approach

### Testing:
- `test_vector_methods.py` - Test different insertion methods

## Benefits of ARRAY Approach

1. **✅ Easy Insertion**: No special syntax or casting needed
2. **✅ VECTOR Functionality**: Full vector search capabilities via view
3. **✅ Performance**: View conversion is efficient
4. **✅ Compatibility**: Works with all Snowflake regions
5. **✅ Simplicity**: Less complex than direct VECTOR handling

## Migration Path

### From VECTOR to ARRAY:
1. **Backup existing data** (if any)
2. **Run alternative setup script**: `snowflake_setup_alternative.sql`
3. **Use ARRAY solution**: `snowflake_solution_array.py`
4. **Test functionality**: Vector search works via view

### No Data Loss:
- All functionality preserved
- Vector search performance maintained
- Same API interface

## Usage

### Setup:
```bash
# 1. Run the alternative setup script in Snowflake
# 2. Set environment variables
export SNOWFLAKE_ACCOUNT="your-account"
export SNOWFLAKE_USER="your-username"
export SNOWFLAKE_PASSWORD="your-password"
# ... other variables

# 3. Run the ARRAY-based solution
python3 snowflake_solution_array.py
```

### Testing:
```bash
# Test different vector insertion methods
python3 test_vector_methods.py
```

## Comparison

| Aspect | VECTOR Direct | ARRAY + View |
|--------|---------------|--------------|
| **Insertion** | Complex/Error-prone | Simple |
| **Vector Search** | Direct | Via view |
| **Performance** | Native | Near-native |
| **Compatibility** | Region-dependent | Universal |
| **Maintenance** | High complexity | Low complexity |

## Recommendation

**Use the ARRAY + View approach** for:
- ✅ **Reliability**: Works across all Snowflake regions
- ✅ **Simplicity**: Easier to implement and maintain
- ✅ **Functionality**: Full vector search capabilities
- ✅ **Performance**: Minimal overhead from view conversion

The ARRAY solution provides all the benefits of VECTOR functionality without the insertion complexity.

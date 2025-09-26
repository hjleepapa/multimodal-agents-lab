#!/usr/bin/env python3
"""
Debug script to find and fix scientific notation values
"""

import json

def find_scientific_notation():
    """Find values with scientific notation"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    first_embedding = embeddings_data[0]['embedding']
    
    print("=== FINDING SCIENTIFIC NOTATION VALUES ===")
    
    scientific_values = []
    for i, val in enumerate(first_embedding):
        val_str = str(val)
        if 'e' in val_str.lower():
            scientific_values.append((i, val, val_str))
    
    print(f"Found {len(scientific_values)} scientific notation values:")
    for idx, val, val_str in scientific_values:
        formatted = f"{val:.15f}".rstrip('0').rstrip('.')
        print(f"  Index {idx}: {val} -> '{formatted}'")
    
    return scientific_values

def test_fixed_formatting():
    """Test the fixed formatting approach"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    first_embedding = embeddings_data[0]['embedding']
    
    print("\n=== TESTING FIXED FORMATTING ===")
    
    # Format the embedding properly
    formatted_values = []
    for val in first_embedding:
        # Use a more robust formatting approach
        if abs(val) < 1e-10:
            # For very small numbers, use scientific notation but ensure it's parseable
            formatted_val = f"{val:.15g}"
        else:
            # For normal numbers, use fixed decimal format
            formatted_val = f"{val:.15f}".rstrip('0').rstrip('.')
        formatted_values.append(formatted_val)
    
    embedding_str = ','.join(formatted_values)
    
    print(f"First 100 characters of formatted string:")
    print(f"  {embedding_str[:100]}...")
    
    print(f"Last 100 characters of formatted string:")
    print(f"  ...{embedding_str[-100:]}")
    
    # Test parsing back
    try:
        parsed_values = [float(x) for x in embedding_str.split(',')]
        print(f"\nParsing test: SUCCESS")
        print(f"  Original length: {len(first_embedding)}")
        print(f"  Parsed length: {len(parsed_values)}")
        print(f"  Values match: {first_embedding == parsed_values}")
    except Exception as e:
        print(f"\nParsing test: FAILED - {e}")

if __name__ == "__main__":
    find_scientific_notation()
    test_fixed_formatting()

#!/usr/bin/env python3
"""
Debug script to understand the embedding format issues
"""

import json

def analyze_embedding_format():
    """Analyze the format of embeddings to understand the issue"""
    with open("data/embeddings.json", "r") as data_file:
        embeddings_data = json.load(data_file)
    
    print("=== EMBEDDING ANALYSIS ===")
    print(f"Total documents: {len(embeddings_data)}")
    
    # Analyze first embedding
    first_embedding = embeddings_data[0]['embedding']
    print(f"\nFirst embedding info:")
    print(f"  Type: {type(first_embedding)}")
    print(f"  Length: {len(first_embedding)}")
    print(f"  First 10 values: {first_embedding[:10]}")
    print(f"  Last 10 values: {first_embedding[-10:]}")
    
    # Check for problematic values
    print(f"\nValue analysis:")
    print(f"  Min value: {min(first_embedding)}")
    print(f"  Max value: {max(first_embedding)}")
    
    # Check for scientific notation
    scientific_count = 0
    for val in first_embedding:
        if 'e' in str(val).lower() or 'E' in str(val):
            scientific_count += 1
    
    print(f"  Values with scientific notation: {scientific_count}")
    
    # Check for very small numbers
    very_small = [v for v in first_embedding if abs(v) < 1e-10]
    print(f"  Very small values (< 1e-10): {len(very_small)}")
    if very_small:
        print(f"    Examples: {very_small[:5]}")
    
    # Test formatting
    print(f"\n=== FORMATTING TEST ===")
    test_values = [1.23e-5, -2.45e-10, 0.000001, -0.0000001, 1.0, -1.0]
    
    for val in test_values:
        formatted = f"{val:.15f}".rstrip('0').rstrip('.')
        print(f"  {val} -> '{formatted}'")
    
    # Test with actual embedding values
    print(f"\n=== ACTUAL EMBEDDING FORMATTING TEST ===")
    sample_values = first_embedding[:5]
    for val in sample_values:
        formatted = f"{val:.15f}".rstrip('0').rstrip('.')
        print(f"  {val} -> '{formatted}'")

if __name__ == "__main__":
    analyze_embedding_format()

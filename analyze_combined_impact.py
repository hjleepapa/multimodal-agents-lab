#!/usr/bin/env python3
"""
Analyze the Combined Impact of DOCX and JSON Metadata Files

This script analyzes both the DOCX medical content and JSON metadata files
to show their combined impact on the multimodal agents lab.
"""

import os
import json
from process_new_data import process_text_file
from collections import Counter
import re

def analyze_json_metadata():
    """Analyze the JSON metadata files"""
    print("🔍 Analyzing JSON Metadata Files")
    print("=" * 50)
    
    json_files = []
    for filename in os.listdir('data/images/'):
        if filename.lower().endswith('.json'):
            json_files.append(filename)
    
    print(f"📄 Found {len(json_files)} JSON metadata files:")
    for i, filename in enumerate(json_files, 1):
        print(f"  {i:2d}. {filename}")
    
    # Analyze each JSON file
    all_metadata = {}
    total_size = 0
    
    print(f"\n📊 Processing JSON metadata files...")
    print("=" * 50)
    
    for filename in json_files:
        filepath = f'data/images/{filename}'
        print(f"\n🔍 Analyzing: {filename}")
        
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            file_size = os.path.getsize(filepath)
            total_size += file_size
            
            all_metadata[filename] = {
                'size': file_size,
                'data': data
            }
            
            # Extract key information
            modality = data.get('Modality', 'Unknown')
            manufacturer = data.get('Manufacturer', 'Unknown')
            body_part = data.get('BodyPartExamined', 'Unknown')
            sequence = data.get('SequenceName', 'Unknown')
            echo_time = data.get('EchoTime', 'Unknown')
            repetition_time = data.get('RepetitionTime', 'Unknown')
            
            print(f"  📊 Size: {file_size:,} bytes")
            print(f"  🏥 Modality: {modality}")
            print(f"  🏭 Manufacturer: {manufacturer}")
            print(f"  🎯 Body Part: {body_part}")
            print(f"  🔬 Sequence: {sequence}")
            print(f"  ⏱️ Echo Time: {echo_time}")
            print(f"  🔄 Repetition Time: {repetition_time}")
            
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    return all_metadata, total_size

def analyze_docx_content():
    """Analyze the DOCX content (reuse from previous analysis)"""
    print(f"\n📄 Analyzing DOCX Medical Content")
    print("=" * 50)
    
    docx_files = []
    for filename in os.listdir('data/text/'):
        if filename.lower().endswith('.docx'):
            docx_files.append(filename)
    
    print(f"📄 Found {len(docx_files)} DOCX files:")
    for i, filename in enumerate(docx_files, 1):
        print(f"  {i:2d}. {filename}")
    
    # Analyze each file
    all_content = ""
    file_analysis = {}
    
    print(f"\n📊 Processing DOCX files...")
    print("=" * 50)
    
    for filename in docx_files:
        filepath = f'data/text/{filename}'
        print(f"\n🔍 Analyzing: {filename}")
        
        try:
            docs = process_text_file(filepath)
            if docs:
                doc = docs[0]
                content = doc['full_content']
                all_content += content + " "
                
                # Basic analysis
                char_count = len(content)
                word_count = len(content.split())
                line_count = len(content.split('\n'))
                
                file_analysis[filename] = {
                    'characters': char_count,
                    'words': word_count,
                    'lines': line_count,
                    'content': content
                }
                
                print(f"  📊 Characters: {char_count:,}")
                print(f"  📝 Words: {word_count:,}")
                print(f"  📋 Lines: {line_count:,}")
                
            else:
                print(f"  ❌ Failed to process {filename}")
                
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    return file_analysis, all_content

def analyze_combined_impact():
    """Analyze the combined impact of both data types"""
    print(f"\n🚀 Combined Impact Analysis")
    print("=" * 60)
    
    # Analyze JSON metadata
    json_metadata, json_total_size = analyze_json_metadata()
    
    # Analyze DOCX content
    docx_analysis, docx_content = analyze_docx_content()
    
    # Combined statistics
    print(f"\n📈 Combined Statistics")
    print("=" * 60)
    
    # JSON statistics
    json_count = len(json_metadata)
    json_size_mb = json_total_size / (1024 * 1024)
    
    # DOCX statistics
    docx_count = len(docx_analysis)
    docx_chars = sum(analysis['characters'] for analysis in docx_analysis.values())
    docx_words = sum(analysis['words'] for analysis in docx_analysis.values())
    docx_lines = sum(analysis['lines'] for analysis in docx_analysis.values())
    
    print(f"📊 JSON Metadata Files:")
    print(f"  Count: {json_count}")
    print(f"  Total Size: {json_total_size:,} bytes ({json_size_mb:.2f} MB)")
    print(f"  Average Size: {json_total_size // json_count if json_count > 0 else 0:,} bytes")
    
    print(f"\n📊 DOCX Medical Content:")
    print(f"  Count: {docx_count}")
    print(f"  Total Characters: {docx_chars:,}")
    print(f"  Total Words: {docx_words:,}")
    print(f"  Total Lines: {docx_lines:,}")
    
    print(f"\n📊 Combined Total:")
    print(f"  Total Files: {json_count + docx_count}")
    print(f"  Total Data: {json_total_size + docx_chars:,} bytes")
    print(f"  Data Types: Medical text + Imaging metadata")
    
    # Content analysis
    print(f"\n🏥 Medical Content Analysis")
    print("=" * 60)
    
    # Extract medical terms from DOCX
    medical_patterns = [
        r'\b(?:pain|symptoms|diagnosis|treatment|patient|medical|clinical|imaging|MRI|CT|X-ray|ultrasound)\b',
        r'\b(?:osteoarthritis|radiculopathy|carotid|stenosis|hypertension|diabetes)\b',
        r'\b(?:knee|hip|lumbar|cervical|spine|joint|muscle|nerve)\b'
    ]
    
    medical_terms = []
    for pattern in medical_patterns:
        matches = re.findall(pattern, docx_content, re.IGNORECASE)
        medical_terms.extend(matches)
    
    medical_counter = Counter(medical_terms)
    top_medical_terms = medical_counter.most_common(15)
    
    print(f"  Most common medical terms:")
    for term, count in top_medical_terms:
        print(f"    {term}: {count}")
    
    # Imaging metadata analysis
    print(f"\n🔬 Imaging Metadata Analysis")
    print("=" * 60)
    
    modalities = []
    manufacturers = []
    body_parts = []
    sequences = []
    
    for filename, metadata in json_metadata.items():
        data = metadata['data']
        modalities.append(data.get('Modality', 'Unknown'))
        manufacturers.append(data.get('Manufacturer', 'Unknown'))
        body_parts.append(data.get('BodyPartExamined', 'Unknown'))
        sequences.append(data.get('SequenceName', 'Unknown'))
    
    print(f"  Modalities: {Counter(modalities)}")
    print(f"  Manufacturers: {Counter(manufacturers)}")
    print(f"  Body Parts: {Counter(body_parts)}")
    print(f"  Sequences: {Counter(sequences)}")
    
    return json_metadata, docx_analysis

def show_ai_agent_impact():
    """Show how the combined data affects the AI agent"""
    print(f"\n🤖 AI Agent Impact Analysis")
    print("=" * 60)
    
    print("✅ Enhanced Knowledge Base:")
    print("  📄 Medical Documentation (DOCX)")
    print("    - Patient case studies and charts")
    print("    - Clinical decision-making scenarios")
    print("    - Diagnostic and treatment information")
    print("    - Medical terminology and concepts")
    
    print("  🔬 Imaging Metadata (JSON)")
    print("    - MRI scan parameters and settings")
    print("    - Imaging protocol information")
    print("    - Technical specifications")
    print("    - Equipment and manufacturer data")
    
    print(f"\n🔍 New Query Capabilities:")
    print("  Medical Content Queries:")
    print("    - 'What are the symptoms of knee osteoarthritis?'")
    print("    - 'Compare treatment approaches for different patients'")
    print("    - 'What imaging studies are mentioned in the charts?'")
    print("    - 'Analyze patient demographics and conditions'")
    
    print("  Imaging Metadata Queries:")
    print("    - 'What MRI sequences are used in the studies?'")
    print("    - 'What are the technical parameters of the scans?'")
    print("    - 'Which manufacturers and equipment are used?'")
    print("    - 'What body parts are being examined?'")
    
    print(f"\n📊 Data Volume Impact:")
    print("  - Significantly expanded multimodal corpus")
    print("  - Rich medical domain knowledge")
    print("  - Technical imaging metadata")
    print("  - Diverse patient case examples")
    print("  - Clinical decision support data")
    
    print(f"\n🎯 Use Cases Enabled:")
    print("  - Medical education and training")
    print("  - Clinical decision support")
    print("  - Patient case analysis")
    print("  - Medical knowledge extraction")
    print("  - Diagnostic pattern recognition")
    print("  - Imaging protocol analysis")
    print("  - Equipment specification queries")

def show_processing_status():
    """Show the current processing status"""
    print(f"\n⚙️ Processing Status")
    print("=" * 60)
    
    print("📁 Files Ready for Processing:")
    
    # Check JSON files
    json_files = [f for f in os.listdir('data/images/') if f.lower().endswith('.json')]
    print(f"  JSON Metadata Files: {len(json_files)}")
    for filename in json_files[:5]:  # Show first 5
        filepath = f'data/images/{filename}'
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"    ✅ {filename} ({size:,} bytes)")
    if len(json_files) > 5:
        print(f"    ... and {len(json_files) - 5} more")
    
    # Check DOCX files
    docx_files = [f for f in os.listdir('data/text/') if f.lower().endswith('.docx')]
    print(f"  DOCX Medical Files: {len(docx_files)}")
    for filename in docx_files[:5]:  # Show first 5
        filepath = f'data/text/{filename}'
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"    ✅ {filename} ({size:,} bytes)")
    if len(docx_files) > 5:
        print(f"    ... and {len(docx_files) - 5} more")
    
    print(f"\n🔄 Next Steps:")
    print("  1. Run: python process_new_data.py")
    print("  2. This will process both JSON and DOCX files")
    print("  3. Store the content in Snowflake database")
    print("  4. Generate embeddings for AI querying")
    print("  5. Enable multimodal knowledge queries")
    
    print(f"\n🧪 Test the Impact:")
    print("  python snowflake_solution_working_final.py")
    print("  Then ask:")
    print("    - 'What medical conditions are covered?'")
    print("    - 'What MRI sequences are used?'")
    print("    - 'What are the imaging parameters?'")

def main():
    """Main analysis function"""
    print("🚀 Combined DOCX + JSON Impact Analysis")
    print("=" * 60)
    
    # Analyze combined impact
    json_metadata, docx_analysis = analyze_combined_impact()
    
    # Show AI agent impact
    show_ai_agent_impact()
    
    # Show processing status
    show_processing_status()
    
    print(f"\n🎉 Analysis Complete!")
    print("=" * 60)
    print("The combination of DOCX medical content and JSON imaging metadata")
    print("creates a comprehensive multimodal medical knowledge system.")
    print("The AI agent can now answer both clinical and technical questions!")

if __name__ == "__main__":
    main()

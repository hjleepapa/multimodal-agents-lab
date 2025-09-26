#!/usr/bin/env python3
"""
Analyze the Impact of DOCX Files on Multimodal Agents Lab

This script analyzes the DOCX files added to data/text/ and shows how they affect the system.
"""

import os
from process_new_data import process_text_file
from collections import Counter
import re

def analyze_docx_content():
    """Analyze the content of DOCX files"""
    print("🔍 Analyzing DOCX Files Impact on Multimodal Agents Lab")
    print("=" * 60)
    
    # Get all DOCX files
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
    medical_terms = []
    
    print(f"\n📊 Processing and analyzing each file...")
    print("=" * 60)
    
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
                
                # Extract medical terms (basic pattern matching)
                medical_patterns = [
                    r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Proper nouns (likely names)
                    r'\b\d+[-/]\d+[-/]\d+\b',        # Dates
                    r'\b\d+[ym]o\b',                 # Age patterns
                    r'\b[A-Z]{2,}\b',                # Acronyms
                    r'\b(?:pain|symptoms|diagnosis|treatment|patient|medical|clinical)\b',  # Medical terms
                ]
                
                for pattern in medical_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    medical_terms.extend(matches)
                
                # Show preview
                preview = content[:200] + "..." if len(content) > 200 else content
                print(f"  📖 Preview: {preview}")
                
            else:
                print(f"  ❌ Failed to process {filename}")
                
        except Exception as e:
            print(f"  ❌ Error processing {filename}: {e}")
    
    # Overall analysis
    print(f"\n📈 Overall Impact Analysis")
    print("=" * 60)
    
    total_chars = sum(analysis['characters'] for analysis in file_analysis.values())
    total_words = sum(analysis['words'] for analysis in file_analysis.values())
    total_lines = sum(analysis['lines'] for analysis in file_analysis.values())
    
    print(f"📊 Total Content Added:")
    print(f"  Characters: {total_chars:,}")
    print(f"  Words: {total_words:,}")
    print(f"  Lines: {total_lines:,}")
    print(f"  Files: {len(docx_files)}")
    
    # Medical content analysis
    print(f"\n🏥 Medical Content Analysis:")
    medical_counter = Counter(medical_terms)
    top_medical_terms = medical_counter.most_common(20)
    
    print(f"  Most common medical terms:")
    for term, count in top_medical_terms:
        print(f"    {term}: {count}")
    
    # File size distribution
    print(f"\n📁 File Size Distribution:")
    sorted_files = sorted(file_analysis.items(), key=lambda x: x[1]['characters'], reverse=True)
    for filename, analysis in sorted_files:
        size_kb = analysis['characters'] / 1024
        print(f"  {filename}: {analysis['characters']:,} chars ({size_kb:.1f} KB)")
    
    # Content categories
    print(f"\n🏷️ Content Categories Identified:")
    categories = {
        'Patient Charts': [f for f in docx_files if 'Chart' in f or any(term in f for term in ['OA', 'Radiculopathy', 'Carotid', 'TTE', 'MRI', 'CT'])],
        'Medical Reports': [f for f in docx_files if any(term in f for term in ['History', 'Diagnosis', 'Treatment'])],
        'Test Documents': [f for f in docx_files if 'sample' in f.lower() or 'test' in f.lower()]
    }
    
    for category, files in categories.items():
        if files:
            print(f"  {category}: {len(files)} files")
            for file in files:
                print(f"    - {file}")
    
    return file_analysis, all_content

def show_impact_on_ai_agent():
    """Show how the DOCX files impact the AI agent"""
    print(f"\n🤖 Impact on AI Agent Capabilities")
    print("=" * 60)
    
    print("✅ Enhanced Knowledge Base:")
    print("  - Medical terminology and concepts")
    print("  - Patient case studies and charts")
    print("  - Clinical decision-making scenarios")
    print("  - Diagnostic and treatment information")
    
    print(f"\n🔍 New Query Capabilities:")
    print("  - 'What are the symptoms of knee osteoarthritis?'")
    print("  - 'Compare the treatment approaches for different patients'")
    print("  - 'What imaging studies are mentioned in the charts?'")
    print("  - 'Analyze the patient demographics in the data'")
    print("  - 'What are the common diagnostic patterns?'")
    
    print(f"\n📊 Data Volume Impact:")
    print("  - Significantly expanded text corpus")
    print("  - Rich medical domain knowledge")
    print("  - Diverse patient case examples")
    print("  - Clinical decision support data")
    
    print(f"\n🎯 Use Cases Enabled:")
    print("  - Medical education and training")
    print("  - Clinical decision support")
    print("  - Patient case analysis")
    print("  - Medical knowledge extraction")
    print("  - Diagnostic pattern recognition")

def show_processing_status():
    """Show the current processing status"""
    print(f"\n⚙️ Processing Status")
    print("=" * 60)
    
    print("📁 Files Ready for Processing:")
    docx_files = [f for f in os.listdir('data/text/') if f.lower().endswith('.docx')]
    for filename in docx_files:
        filepath = f'data/text/{filename}'
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"  ✅ {filename} ({size:,} bytes)")
        else:
            print(f"  ❌ {filename} (not found)")
    
    print(f"\n🔄 Next Steps:")
    print("  1. Run: python process_new_data.py")
    print("  2. This will extract text from all DOCX files")
    print("  3. Store the content in Snowflake database")
    print("  4. Generate embeddings for AI querying")
    print("  5. Enable medical knowledge queries")
    
    print(f"\n🧪 Test the Impact:")
    print("  python snowflake_solution_working_final.py")
    print("  Then ask: 'What medical conditions are covered in the documents?'")

def main():
    """Main analysis function"""
    print("🚀 DOCX Files Impact Analysis")
    print("=" * 60)
    
    # Analyze content
    file_analysis, all_content = analyze_docx_content()
    
    # Show AI agent impact
    show_impact_on_ai_agent()
    
    # Show processing status
    show_processing_status()
    
    print(f"\n🎉 Analysis Complete!")
    print("=" * 60)
    print("The DOCX files contain rich medical content that will significantly")
    print("enhance the AI agent's knowledge base and querying capabilities.")

if __name__ == "__main__":
    main()

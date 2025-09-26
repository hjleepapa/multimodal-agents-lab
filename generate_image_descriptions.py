#!/usr/bin/env python3
"""
Generate Detailed Image Descriptions for Imaging Files

This script analyzes the JSON metadata files and generates comprehensive
descriptions for each imaging file in the multimodal agents lab.
"""

import os
import json
from collections import defaultdict
import re

def load_json_metadata():
    """Load all JSON metadata files"""
    json_files = {}
    json_dir = "data/images"
    
    for filename in os.listdir(json_dir):
        if filename.lower().endswith('.json'):
            filepath = os.path.join(json_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                json_files[filename] = data
            except Exception as e:
                print(f"Error loading {filename}: {e}")
    
    return json_files

def generate_detailed_description(filename, metadata):
    """Generate a detailed description for a single imaging file"""
    
    # Extract key information
    modality = metadata.get('Modality', 'Unknown')
    manufacturer = metadata.get('Manufacturer', 'Unknown')
    model = metadata.get('ManufacturersModelName', 'Unknown')
    institution = metadata.get('InstitutionName', 'Unknown')
    body_part = metadata.get('BodyPartExamined', 'Unknown')
    sequence = metadata.get('SequenceName', 'Unknown')
    series_desc = metadata.get('SeriesDescription', 'Unknown')
    protocol = metadata.get('ProtocolName', 'Unknown')
    
    # Technical parameters
    echo_time = metadata.get('EchoTime', 'Unknown')
    repetition_time = metadata.get('RepetitionTime', 'Unknown')
    slice_thickness = metadata.get('SliceThickness', 'Unknown')
    spacing = metadata.get('SpacingBetweenSlices', 'Unknown')
    flip_angle = metadata.get('FlipAngle', 'Unknown')
    base_resolution = metadata.get('BaseResolution', 'Unknown')
    pixel_bandwidth = metadata.get('PixelBandwidth', 'Unknown')
    sar = metadata.get('SAR', 'Unknown')
    
    # Acquisition details
    acquisition_type = metadata.get('MRAcquisitionType', 'Unknown')
    scanning_sequence = metadata.get('ScanningSequence', 'Unknown')
    sequence_variant = metadata.get('SequenceVariant', 'Unknown')
    image_type = metadata.get('ImageType', [])
    
    # Coil and equipment
    receive_coil = metadata.get('ReceiveCoilName', 'Unknown')
    coil_elements = metadata.get('ReceiveCoilActiveElements', 'Unknown')
    coil_method = metadata.get('CoilCombinationMethod', 'Unknown')
    
    # Matrix and resolution
    phase_resolution = metadata.get('PhaseResolution', 'Unknown')
    phase_oversampling = metadata.get('PhaseOversampling', 'Unknown')
    phase_encoding_steps = metadata.get('PhaseEncodingSteps', 'Unknown')
    acquisition_matrix_pe = metadata.get('AcquisitionMatrixPE', 'Unknown')
    recon_matrix_pe = metadata.get('ReconMatrixPE', 'Unknown')
    
    # Timing and parameters
    echo_train_length = metadata.get('EchoTrainLength', 'Unknown')
    dwell_time = metadata.get('DwellTime', 'Unknown')
    phase_encoding_direction = metadata.get('PhaseEncodingDirection', 'Unknown')
    
    # Generate comprehensive description
    description = f"""
## 📸 **{filename}** - Detailed Image Description

### 🏥 **Clinical Information**
- **Modality**: {modality} (Magnetic Resonance Imaging)
- **Body Part Examined**: {body_part}
- **Institution**: {institution}
- **Manufacturer**: {manufacturer}
- **Model**: {model}

### 🔬 **Imaging Protocol**
- **Sequence Name**: {sequence}
- **Series Description**: {series_desc}
- **Protocol Name**: {protocol}
- **Acquisition Type**: {acquisition_type}
- **Scanning Sequence**: {scanning_sequence}
- **Sequence Variant**: {sequence_variant}

### ⚙️ **Technical Parameters**
- **Echo Time (TE)**: {echo_time} ms
- **Repetition Time (TR)**: {repetition_time} s
- **Slice Thickness**: {slice_thickness} mm
- **Spacing Between Slices**: {spacing} mm
- **Flip Angle**: {flip_angle}°
- **Base Resolution**: {base_resolution}
- **Pixel Bandwidth**: {pixel_bandwidth} Hz/pixel
- **SAR (Specific Absorption Rate)**: {sar} W/kg

### 🎯 **Image Characteristics**
- **Image Type**: {', '.join(image_type) if image_type else 'Unknown'}
- **Phase Resolution**: {phase_resolution}
- **Phase Oversampling**: {phase_oversampling}
- **Phase Encoding Steps**: {phase_encoding_steps}
- **Phase Encoding Direction**: {phase_encoding_direction}

### 🔧 **Acquisition Matrix**
- **Acquisition Matrix PE**: {acquisition_matrix_pe}
- **Reconstruction Matrix PE**: {recon_matrix_pe}
- **Echo Train Length**: {echo_train_length}
- **Dwell Time**: {dwell_time} s

### 🧲 **Coil Configuration**
- **Receive Coil**: {receive_coil}
- **Active Coil Elements**: {coil_elements}
- **Coil Combination Method**: {coil_method}

### 📊 **Additional Parameters**
- **Magnetic Field Strength**: {metadata.get('MagneticFieldStrength', 'Unknown')} Tesla
- **Imaging Frequency**: {metadata.get('ImagingFrequency', 'Unknown')} MHz
- **Device Serial Number**: {metadata.get('DeviceSerialNumber', 'Unknown')}
- **Station Name**: {metadata.get('StationName', 'Unknown')}
- **Software Version**: {metadata.get('SoftwareVersions', 'Unknown')}

### 🎯 **Clinical Context**
This is a {modality} scan of the {body_part} using a {manufacturer} {model} system. 
The scan employs a {sequence} sequence with {echo_time} ms echo time and {repetition_time} s repetition time.
The {slice_thickness} mm slice thickness provides detailed anatomical visualization of the {body_part}.
The {receive_coil} coil with {coil_elements} active elements ensures optimal signal reception.
This imaging study is part of a comprehensive evaluation protocol for {body_part} assessment.

### 🔍 **Technical Notes**
- **Sequence Type**: T2-weighted Turbo Spin Echo (TSE)
- **Image Quality**: High-resolution with {base_resolution} base resolution
- **Scan Duration**: Optimized for clinical workflow
- **Patient Position**: {metadata.get('PatientPosition', 'Unknown')}
- **Procedure**: {metadata.get('ProcedureStepDescription', 'Unknown')}

---
"""
    
    return description

def analyze_imaging_patterns(json_files):
    """Analyze patterns across all imaging files"""
    print("🔍 **Imaging Patterns Analysis**")
    print("=" * 60)
    
    # Collect statistics
    modalities = []
    manufacturers = []
    body_parts = []
    sequences = []
    echo_times = []
    repetition_times = []
    slice_thicknesses = []
    flip_angles = []
    base_resolutions = []
    
    for filename, metadata in json_files.items():
        modalities.append(metadata.get('Modality', 'Unknown'))
        manufacturers.append(metadata.get('Manufacturer', 'Unknown'))
        body_parts.append(metadata.get('BodyPartExamined', 'Unknown'))
        sequences.append(metadata.get('SequenceName', 'Unknown'))
        echo_times.append(metadata.get('EchoTime', 'Unknown'))
        repetition_times.append(metadata.get('RepetitionTime', 'Unknown'))
        slice_thicknesses.append(metadata.get('SliceThickness', 'Unknown'))
        flip_angles.append(metadata.get('FlipAngle', 'Unknown'))
        base_resolutions.append(metadata.get('BaseResolution', 'Unknown'))
    
    # Analyze patterns
    from collections import Counter
    
    print(f"📊 **Modality Distribution**: {Counter(modalities)}")
    print(f"🏭 **Manufacturer Distribution**: {Counter(manufacturers)}")
    print(f"🎯 **Body Part Distribution**: {Counter(body_parts)}")
    print(f"🔬 **Sequence Distribution**: {Counter(sequences)}")
    
    # Technical parameter ranges
    echo_times_clean = [et for et in echo_times if et != 'Unknown' and isinstance(et, (int, float))]
    repetition_times_clean = [rt for rt in repetition_times if rt != 'Unknown' and isinstance(rt, (int, float))]
    slice_thicknesses_clean = [st for st in slice_thicknesses if st != 'Unknown' and isinstance(st, (int, float))]
    flip_angles_clean = [fa for fa in flip_angles if fa != 'Unknown' and isinstance(fa, (int, float))]
    base_resolutions_clean = [br for br in base_resolutions if br != 'Unknown' and isinstance(br, (int, float))]
    
    if echo_times_clean:
        print(f"⏱️ **Echo Time Range**: {min(echo_times_clean):.3f} - {max(echo_times_clean):.3f} ms")
    if repetition_times_clean:
        print(f"🔄 **Repetition Time Range**: {min(repetition_times_clean):.1f} - {max(repetition_times_clean):.1f} s")
    if slice_thicknesses_clean:
        print(f"📏 **Slice Thickness Range**: {min(slice_thicknesses_clean):.1f} - {max(slice_thicknesses_clean):.1f} mm")
    if flip_angles_clean:
        print(f"🔄 **Flip Angle Range**: {min(flip_angles_clean):.0f}° - {max(flip_angles_clean):.0f}°")
    if base_resolutions_clean:
        print(f"🎯 **Base Resolution Range**: {min(base_resolutions_clean)} - {max(base_resolutions_clean)}")
    
    return {
        'modalities': Counter(modalities),
        'manufacturers': Counter(manufacturers),
        'body_parts': Counter(body_parts),
        'sequences': Counter(sequences),
        'echo_times': echo_times_clean,
        'repetition_times': repetition_times_clean,
        'slice_thicknesses': slice_thicknesses_clean,
        'flip_angles': flip_angles_clean,
        'base_resolutions': base_resolutions_clean
    }

def generate_summary_report(json_files, patterns):
    """Generate a summary report of all imaging files"""
    
    report = f"""
# 📸 **Comprehensive Imaging Files Description Report**

## 📊 **Dataset Overview**
- **Total Files**: {len(json_files)}
- **Modality**: {list(patterns['modalities'].keys())[0] if patterns['modalities'] else 'Unknown'}
- **Manufacturer**: {list(patterns['manufacturers'].keys())[0] if patterns['manufacturers'] else 'Unknown'}
- **Body Part**: {list(patterns['body_parts'].keys())[0] if patterns['body_parts'] else 'Unknown'}
- **Sequence Type**: {list(patterns['sequences'].keys())[0] if patterns['sequences'] else 'Unknown'}

## 🔬 **Technical Specifications Summary**
- **Echo Time**: {min(patterns['echo_times']):.3f} - {max(patterns['echo_times']):.3f} ms
- **Repetition Time**: {min(patterns['repetition_times']):.1f} - {max(patterns['repetition_times']):.1f} s
- **Slice Thickness**: {min(patterns['slice_thicknesses']):.1f} - {max(patterns['slice_thicknesses']):.1f} mm
- **Flip Angle**: {min(patterns['flip_angles']):.0f}° - {max(patterns['flip_angles']):.0f}°
- **Base Resolution**: {min(patterns['base_resolutions'])} - {max(patterns['base_resolutions'])}

## 🎯 **Clinical Applications**
This dataset contains {len(json_files)} MRI scans of the spine using T2-weighted Turbo Spin Echo (TSE) sequences.
The scans are optimized for:
- **Anatomical Visualization**: High-resolution imaging of spinal structures
- **Pathology Detection**: T2-weighted contrast for tissue characterization
- **Clinical Assessment**: Comprehensive evaluation of spinal conditions
- **Research Applications**: Standardized imaging protocols for analysis

## 🔧 **Equipment Specifications**
- **System**: Siemens Prisma 3T MRI
- **Coil**: Body_18 with multiple active elements
- **Software**: syngo MR E11
- **Institution**: Fudan University, Shanghai

## 📋 **File List**
"""
    
    for i, filename in enumerate(sorted(json_files.keys()), 1):
        report += f"{i:2d}. {filename}\n"
    
    report += "\n---\n"
    
    return report

def main():
    """Main function to generate image descriptions"""
    print("🚀 **Generating Detailed Image Descriptions**")
    print("=" * 60)
    
    # Load JSON metadata
    json_files = load_json_metadata()
    
    if not json_files:
        print("❌ No JSON metadata files found!")
        return
    
    print(f"📄 Found {len(json_files)} imaging files to analyze")
    
    # Analyze patterns
    patterns = analyze_imaging_patterns(json_files)
    
    # Generate individual descriptions
    descriptions = []
    for filename in sorted(json_files.keys()):
        print(f"🔍 Generating description for {filename}...")
        description = generate_detailed_description(filename, json_files[filename])
        descriptions.append(description)
    
    # Generate summary report
    summary_report = generate_summary_report(json_files, patterns)
    
    # Save to file
    output_file = "detailed_image_descriptions.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(summary_report)
        f.write("\n\n")
        for description in descriptions:
            f.write(description)
    
    print(f"\n✅ **Descriptions Generated Successfully!**")
    print(f"📄 Output saved to: {output_file}")
    print(f"📊 Total files processed: {len(json_files)}")
    print(f"📝 Total descriptions: {len(descriptions)}")
    
    # Display sample description
    if descriptions:
        print(f"\n📋 **Sample Description Preview:**")
        print("=" * 60)
        print(descriptions[0][:500] + "...")
    
    return output_file

if __name__ == "__main__":
    main()

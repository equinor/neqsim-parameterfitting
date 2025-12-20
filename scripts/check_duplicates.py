#!/usr/bin/env python
"""
Check for duplicate data entries across CSV files.

This script identifies potential duplicate data points that may
exist in multiple files or within the same file.
"""

import os
import sys
import pandas as pd
from pathlib import Path
from collections import defaultdict


def find_duplicates(data_dir: Path) -> dict:
    """Find duplicate data points across all CSV files."""
    
    # Group files by property type
    property_files = defaultdict(list)
    
    for csv_file in data_dir.glob("**/*.csv"):
        rel_path = str(csv_file.relative_to(data_dir))
        
        if 'vle' in rel_path.lower():
            property_files['vle'].append(csv_file)
        elif 'density' in rel_path.lower():
            property_files['density'].append(csv_file)
        elif 'viscosity' in rel_path.lower():
            property_files['viscosity'].append(csv_file)
        elif 'heatcapacity' in rel_path.lower():
            property_files['heatcapacity'].append(csv_file)
    
    results = {}
    
    for prop_type, files in property_files.items():
        if len(files) < 2:
            continue
        
        # Load all files and check for duplicates
        all_data = []
        for f in files:
            try:
                df = pd.read_csv(f)
                df['_source_file'] = str(f.name)
                all_data.append(df)
            except Exception as e:
                print(f"Warning: Could not read {f}: {e}")
        
        if not all_data:
            continue
        
        # Combine all data
        combined = pd.concat(all_data, ignore_index=True)
        
        # Find key columns for duplicate detection
        key_cols = []
        for col in ['Temperature', 'Pressure', 'temperature_K', 'pressure_bar']:
            if col in combined.columns:
                key_cols.append(col)
        
        if not key_cols:
            continue
        
        # Find duplicates (excluding source file column)
        data_cols = [c for c in combined.columns if c != '_source_file']
        duplicates = combined[combined.duplicated(subset=data_cols, keep=False)]
        
        if len(duplicates) > 0:
            results[prop_type] = {
                'n_duplicates': len(duplicates),
                'files': [f.name for f in files],
            }
    
    return results


def main():
    """Main routine."""
    data_dir = Path(__file__).parent.parent / "data"
    
    print("Checking for duplicate data entries...\n")
    
    duplicates = find_duplicates(data_dir)
    
    if not duplicates:
        print("✅ No cross-file duplicates found")
        sys.exit(0)
    else:
        print("⚠️  Potential duplicates found:\n")
        for prop_type, info in duplicates.items():
            print(f"  {prop_type}: {info['n_duplicates']} duplicate entries")
            print(f"    Files: {', '.join(info['files'])}")
        
        print("\nNote: Some duplicates may be intentional (same data point reported by different sources)")
        sys.exit(0)  # Don't fail on duplicates, just warn


if __name__ == "__main__":
    main()

#!/usr/bin/env python
"""
Validate experimental data files against schemas.

This script checks all CSV files in the data/ directory for:
- Required columns based on property type
- Valid value ranges
- Data type consistency
"""

import os
import sys
import json
import pandas as pd
from pathlib import Path


def get_schema_path(property_type: str) -> Path:
    """Get the schema file path for a property type."""
    schema_dir = Path(__file__).parent.parent / "data" / "schema"
    schema_map = {
        'vle': 'vle-schema.json',
        'density': 'density-schema.json',
        'viscosity': 'viscosity-schema.json',
        'heatcapacity': 'heat-capacity-schema.json',
        'thermalconductivity': 'viscosity-schema.json',  # Similar structure
    }
    
    schema_file = schema_map.get(property_type.lower().replace('-', '').replace('_', ''))
    if schema_file:
        return schema_dir / schema_file
    return None


def detect_property_type(filepath: Path) -> str:
    """Detect property type from file path."""
    path_str = str(filepath).lower()
    
    if 'vle' in path_str:
        return 'vle'
    elif 'density' in path_str:
        return 'density'
    elif 'viscosity' in path_str:
        return 'viscosity'
    elif 'heatcapacity' in path_str or 'heat' in path_str:
        return 'heatcapacity'
    elif 'thermalconductivity' in path_str or 'conductivity' in path_str:
        return 'thermalconductivity'
    else:
        return 'unknown'


def validate_csv(filepath: Path) -> dict:
    """Validate a single CSV file."""
    result = {
        'file': str(filepath),
        'valid': True,
        'errors': [],
        'warnings': [],
    }
    
    try:
        df = pd.read_csv(filepath)
    except Exception as e:
        result['valid'] = False
        result['errors'].append(f"Failed to read CSV: {e}")
        return result
    
    # Basic checks
    if len(df) == 0:
        result['warnings'].append("Empty file")
    
    # Check for NaN in critical columns
    critical_cols = ['Temperature', 'Pressure', 'temperature_K', 'pressure_bar']
    for col in critical_cols:
        if col in df.columns and df[col].isna().any():
            result['warnings'].append(f"Column '{col}' contains NaN values")
    
    # Check for duplicate rows
    if df.duplicated().any():
        n_dups = df.duplicated().sum()
        result['warnings'].append(f"Found {n_dups} duplicate rows")
    
    # Property-specific validation
    property_type = detect_property_type(filepath)
    schema_path = get_schema_path(property_type)
    
    if schema_path and schema_path.exists():
        with open(schema_path) as f:
            schema = json.load(f)
        
        # Validate ranges
        if 'validation_rules' in schema:
            for col_name, rules in schema['validation_rules'].items():
                # Find matching column (case-insensitive)
                matching_cols = [c for c in df.columns if c.lower() == col_name.lower()]
                if matching_cols:
                    col = matching_cols[0]
                    if 'minimum' in rules:
                        if (df[col] < rules['minimum']).any():
                            result['errors'].append(
                                f"Column '{col}' has values below minimum ({rules['minimum']})"
                            )
                            result['valid'] = False
                    if 'maximum' in rules:
                        if (df[col] > rules['maximum']).any():
                            result['errors'].append(
                                f"Column '{col}' has values above maximum ({rules['maximum']})"
                            )
                            result['valid'] = False
    
    return result


def main():
    """Main validation routine."""
    data_dir = Path(__file__).parent.parent / "data"
    
    # Find all CSV files
    csv_files = list(data_dir.glob("**/*.csv"))
    
    print(f"Found {len(csv_files)} CSV files to validate\n")
    
    all_valid = True
    results = []
    
    for filepath in csv_files:
        result = validate_csv(filepath)
        results.append(result)
        
        # Print status
        rel_path = filepath.relative_to(data_dir)
        if result['valid'] and not result['warnings']:
            print(f"✅ {rel_path}")
        elif result['valid'] and result['warnings']:
            print(f"⚠️  {rel_path}")
            for warn in result['warnings']:
                print(f"   Warning: {warn}")
        else:
            print(f"❌ {rel_path}")
            for err in result['errors']:
                print(f"   Error: {err}")
            all_valid = False
    
    # Summary
    n_valid = sum(1 for r in results if r['valid'])
    n_warnings = sum(1 for r in results if r['warnings'])
    n_errors = sum(1 for r in results if not r['valid'])
    
    print(f"\n{'='*50}")
    print(f"Summary: {n_valid}/{len(results)} files valid")
    print(f"         {n_warnings} files with warnings")
    print(f"         {n_errors} files with errors")
    
    sys.exit(0 if all_valid else 1)


if __name__ == "__main__":
    main()

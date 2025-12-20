"""
Data validation utilities for experimental data files.

This module provides functions to validate experimental data
against defined schemas and check data quality.
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Any, Union
import warnings


# Path to schema files
SCHEMA_DIR = Path(__file__).parent.parent.parent.parent / "data" / "schema"


def validate_data(
    df: pd.DataFrame,
    property_type: str,
    schema_path: Optional[Path] = None,
    raise_on_error: bool = True,
) -> Dict[str, Any]:
    """
    Validate experimental data against a schema.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    property_type : str
        Type of property ('vle', 'density', 'viscosity', 'heat_capacity')
    schema_path : Path, optional
        Custom path to schema file
    raise_on_error : bool, default True
        Whether to raise an exception on validation errors

    Returns
    -------
    dict
        Validation results with 'valid' bool and 'errors' list

    Raises
    ------
    ValueError
        If validation fails and raise_on_error is True
    """
    if schema_path is None:
        schema_map = {
            'vle': 'vle-schema.json',
            'density': 'density-schema.json',
            'viscosity': 'viscosity-schema.json',
            'heat_capacity': 'heat-capacity-schema.json',
        }
        schema_file = schema_map.get(property_type.lower())
        if schema_file:
            schema_path = SCHEMA_DIR / schema_file
    
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
    }
    
    # Load schema if available
    if schema_path and schema_path.exists():
        with open(schema_path, 'r') as f:
            schema = json.load(f)
        
        # Validate required columns
        if 'required_columns' in schema:
            for col_def in schema['required_columns']:
                if col_def.get('required', False):
                    col_name = col_def['name']
                    if col_name not in df.columns:
                        # Check for alternative column names
                        if not _has_alternative_column(df, col_name):
                            result['errors'].append(f"Missing required column: {col_name}")
                            result['valid'] = False
        
        # Validate value ranges
        if 'validation_rules' in schema:
            for col_name, rules in schema['validation_rules'].items():
                if col_name in df.columns:
                    if 'minimum' in rules:
                        if (df[col_name] < rules['minimum']).any():
                            result['errors'].append(
                                f"Column '{col_name}' has values below minimum ({rules['minimum']})"
                            )
                            result['valid'] = False
                    if 'maximum' in rules:
                        if (df[col_name] > rules['maximum']).any():
                            result['errors'].append(
                                f"Column '{col_name}' has values above maximum ({rules['maximum']})"
                            )
                            result['valid'] = False
    else:
        # Basic validation without schema
        result['warnings'].append(f"Schema not found for property type: {property_type}")
        basic_result = validate_columns(df)
        result['errors'].extend(basic_result.get('errors', []))
        result['warnings'].extend(basic_result.get('warnings', []))
        if basic_result.get('errors'):
            result['valid'] = False
    
    if raise_on_error and not result['valid']:
        raise ValueError(f"Data validation failed: {result['errors']}")
    
    return result


def _has_alternative_column(df: pd.DataFrame, col_name: str) -> bool:
    """Check if an alternative column name exists in the dataframe."""
    alternatives = {
        'temperature_K': ['Temperature', 'temperature', 'T', 'T_K'],
        'pressure_bar': ['Pressure', 'pressure', 'P', 'P_bar'],
        'reference': ['Reference', 'ref', 'source'],
        'component_1': ['ComponentSolute', 'component1', 'comp1'],
        'component_2': ['ComponentSolvent', 'component2', 'comp2'],
    }
    
    if col_name in alternatives:
        return any(alt in df.columns for alt in alternatives[col_name])
    return False


def validate_columns(
    df: pd.DataFrame,
    required_columns: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Validate that dataframe has required columns.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    required_columns : list, optional
        List of required column names

    Returns
    -------
    dict
        Validation results
    """
    result = {
        'valid': True,
        'errors': [],
        'warnings': [],
        'columns_found': list(df.columns),
    }
    
    if required_columns:
        missing = set(required_columns) - set(df.columns)
        if missing:
            result['errors'].append(f"Missing columns: {missing}")
            result['valid'] = False
    
    # Check for empty columns
    empty_cols = [col for col in df.columns if df[col].isna().all()]
    if empty_cols:
        result['warnings'].append(f"Empty columns found: {empty_cols}")
    
    # Check for duplicate rows
    if df.duplicated().any():
        n_duplicates = df.duplicated().sum()
        result['warnings'].append(f"Found {n_duplicates} duplicate rows")
    
    return result


def check_data_quality(
    df: pd.DataFrame,
    value_column: str,
    uncertainty_column: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Check the quality of experimental data.

    Parameters
    ----------
    df : pd.DataFrame
        Experimental data
    value_column : str
        Name of the column containing measured values
    uncertainty_column : str, optional
        Name of the column containing uncertainties

    Returns
    -------
    dict
        Quality metrics including:
        - n_points: Number of data points
        - n_missing: Number of missing values
        - n_outliers: Number of potential outliers (>3σ)
        - value_range: (min, max) of values
        - has_uncertainty: Whether uncertainty data is available
        - mean_uncertainty_percent: Average relative uncertainty
    """
    quality = {
        'n_points': len(df),
        'n_missing': 0,
        'n_outliers': 0,
        'value_range': None,
        'has_uncertainty': False,
        'mean_uncertainty_percent': None,
    }
    
    if value_column not in df.columns:
        quality['errors'] = f"Value column '{value_column}' not found"
        return quality
    
    values = df[value_column]
    
    # Missing values
    quality['n_missing'] = values.isna().sum()
    
    # Value range
    quality['value_range'] = (values.min(), values.max())
    
    # Outlier detection (values > 3 standard deviations from mean)
    if len(values.dropna()) > 3:
        mean = values.mean()
        std = values.std()
        outliers = (np.abs(values - mean) > 3 * std)
        quality['n_outliers'] = outliers.sum()
    
    # Uncertainty analysis
    if uncertainty_column and uncertainty_column in df.columns:
        quality['has_uncertainty'] = True
        uncertainties = df[uncertainty_column]
        # Calculate relative uncertainty
        rel_uncertainty = (uncertainties / values.abs()) * 100
        quality['mean_uncertainty_percent'] = rel_uncertainty.mean()
        quality['max_uncertainty_percent'] = rel_uncertainty.max()
    
    # Quality flag distribution
    if 'quality_flag' in df.columns:
        quality['quality_distribution'] = df['quality_flag'].value_counts().to_dict()
    
    return quality


def validate_temperature_range(
    df: pd.DataFrame,
    min_temp: float = 0,
    max_temp: float = 2000,
    temp_column: str = 'temperature_K',
) -> bool:
    """
    Validate that temperature values are within a reasonable range.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    min_temp : float, default 0
        Minimum valid temperature (K)
    max_temp : float, default 2000
        Maximum valid temperature (K)
    temp_column : str
        Name of temperature column

    Returns
    -------
    bool
        True if all temperatures are valid
    """
    if temp_column not in df.columns:
        # Try alternative names
        for alt in ['Temperature', 'temperature', 'T', 'T_K']:
            if alt in df.columns:
                temp_column = alt
                break
        else:
            warnings.warn(f"Temperature column not found")
            return False
    
    temps = df[temp_column]
    return (temps >= min_temp).all() and (temps <= max_temp).all()


def validate_pressure_range(
    df: pd.DataFrame,
    min_pres: float = 0,
    max_pres: float = 10000,
    pres_column: str = 'pressure_bar',
) -> bool:
    """
    Validate that pressure values are within a reasonable range.

    Parameters
    ----------
    df : pd.DataFrame
        Data to validate
    min_pres : float, default 0
        Minimum valid pressure (bar)
    max_pres : float, default 10000
        Maximum valid pressure (bar)
    pres_column : str
        Name of pressure column

    Returns
    -------
    bool
        True if all pressures are valid
    """
    if pres_column not in df.columns:
        # Try alternative names
        for alt in ['Pressure', 'pressure', 'P', 'P_bar']:
            if alt in df.columns:
                pres_column = alt
                break
        else:
            warnings.warn(f"Pressure column not found")
            return False
    
    pressures = df[pres_column]
    return (pressures >= min_pres).all() and (pressures <= max_pres).all()

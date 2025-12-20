"""
Data loading utilities for experimental data files.

This module provides functions to load and preprocess experimental data
from CSV files for use in parameter fitting and model evaluation.
"""

import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, List, Dict, Union, Any


def load_experimental_data(
    filepath: Union[str, Path],
    property_type: Optional[str] = None,
    validate: bool = True,
) -> pd.DataFrame:
    """
    Load experimental data from a CSV file.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    property_type : str, optional
        Type of property data ('vle', 'density', 'viscosity', 'heat_capacity', etc.)
        Used for validation if validate=True
    validate : bool, default True
        Whether to validate the data against the schema

    Returns
    -------
    pd.DataFrame
        Loaded experimental data

    Examples
    --------
    >>> df = load_experimental_data('data/thermodynamics/VLE/water-CO2.csv', property_type='vle')
    >>> print(df.head())
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Data file not found: {filepath}")
    
    # Load CSV with standard settings
    df = pd.read_csv(filepath)
    
    # Standardize column names (lowercase, replace spaces with underscores)
    df.columns = [_standardize_column_name(col) for col in df.columns]
    
    if validate and property_type:
        from neqsim_fitting.data.validator import validate_data
        validate_data(df, property_type)
    
    return df


def _standardize_column_name(name: str) -> str:
    """Standardize column name to lowercase with underscores."""
    # Handle common variations
    name = str(name).strip()
    
    # Common replacements
    replacements = {
        'Temperature (K)': 'temperature_K',
        'Temperature': 'temperature_K',
        'Pressure (bar)': 'pressure_bar',
        'Pressure': 'pressure_bar',
        'Density (kg/m3)': 'density_kg_m3',
        'Reference': 'reference',
        'ID': 'id',
        'ComponentSolute': 'component_1',
        'ComponentSolvent': 'component_2',
        'StandardDeviation': 'uncertainty',
        'Cp': 'cp_J_molK',
    }
    
    if name in replacements:
        return replacements[name]
    
    return name


def load_vle_data(
    filepath: Union[str, Path],
    temperature_range: Optional[tuple] = None,
    pressure_range: Optional[tuple] = None,
    exclude_references: Optional[List[str]] = None,
) -> pd.DataFrame:
    """
    Load VLE (Vapor-Liquid Equilibrium) experimental data.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    temperature_range : tuple, optional
        (min, max) temperature range to filter (in Kelvin)
    pressure_range : tuple, optional
        (min, max) pressure range to filter (in bar)
    exclude_references : list, optional
        List of reference names to exclude from the data

    Returns
    -------
    pd.DataFrame
        Filtered VLE data
    """
    df = load_experimental_data(filepath, property_type='vle')
    
    # Apply filters
    if temperature_range:
        temp_col = _find_temperature_column(df)
        df = df[(df[temp_col] >= temperature_range[0]) & 
                (df[temp_col] <= temperature_range[1])]
    
    if pressure_range:
        pres_col = _find_pressure_column(df)
        df = df[(df[pres_col] >= pressure_range[0]) & 
                (df[pres_col] <= pressure_range[1])]
    
    if exclude_references:
        ref_col = _find_reference_column(df)
        df = df[~df[ref_col].isin(exclude_references)]
    
    return df


def load_density_data(
    filepath: Union[str, Path],
    temperature_range: Optional[tuple] = None,
    pressure_range: Optional[tuple] = None,
    phase: Optional[str] = None,
) -> pd.DataFrame:
    """
    Load density experimental data.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    temperature_range : tuple, optional
        (min, max) temperature range to filter (in Kelvin)
    pressure_range : tuple, optional
        (min, max) pressure range to filter (in bar)
    phase : str, optional
        Phase to filter ('liquid', 'vapor', 'gas', 'supercritical')

    Returns
    -------
    pd.DataFrame
        Filtered density data
    """
    df = load_experimental_data(filepath, property_type='density')
    
    if temperature_range:
        temp_col = _find_temperature_column(df)
        df = df[(df[temp_col] >= temperature_range[0]) & 
                (df[temp_col] <= temperature_range[1])]
    
    if pressure_range:
        pres_col = _find_pressure_column(df)
        df = df[(df[pres_col] >= pressure_range[0]) & 
                (df[pres_col] <= pressure_range[1])]
    
    if phase and 'phase' in df.columns:
        df = df[df['phase'] == phase]
    
    return df


def load_viscosity_data(
    filepath: Union[str, Path],
    temperature_range: Optional[tuple] = None,
    pressure_range: Optional[tuple] = None,
) -> pd.DataFrame:
    """
    Load viscosity experimental data.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    temperature_range : tuple, optional
        (min, max) temperature range to filter (in Kelvin)
    pressure_range : tuple, optional
        (min, max) pressure range to filter (in bar)

    Returns
    -------
    pd.DataFrame
        Filtered viscosity data
    """
    df = load_experimental_data(filepath, property_type='viscosity')
    
    if temperature_range:
        temp_col = _find_temperature_column(df)
        df = df[(df[temp_col] >= temperature_range[0]) & 
                (df[temp_col] <= temperature_range[1])]
    
    if pressure_range:
        pres_col = _find_pressure_column(df)
        df = df[(df[pres_col] >= pressure_range[0]) & 
                (df[pres_col] <= pressure_range[1])]
    
    return df


def load_heat_capacity_data(
    filepath: Union[str, Path],
    temperature_range: Optional[tuple] = None,
    pressure_range: Optional[tuple] = None,
) -> pd.DataFrame:
    """
    Load heat capacity (Cp/Cv) experimental data.

    Parameters
    ----------
    filepath : str or Path
        Path to the CSV file
    temperature_range : tuple, optional
        (min, max) temperature range to filter (in Kelvin)
    pressure_range : tuple, optional
        (min, max) pressure range to filter (in bar)

    Returns
    -------
    pd.DataFrame
        Filtered heat capacity data
    """
    df = load_experimental_data(filepath, property_type='heat_capacity')
    
    if temperature_range:
        temp_col = _find_temperature_column(df)
        df = df[(df[temp_col] >= temperature_range[0]) & 
                (df[temp_col] <= temperature_range[1])]
    
    if pressure_range:
        pres_col = _find_pressure_column(df)
        df = df[(df[pres_col] >= pressure_range[0]) & 
                (df[pres_col] <= pressure_range[1])]
    
    return df


def get_data_summary(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Get a summary of the experimental dataset.

    Parameters
    ----------
    df : pd.DataFrame
        Experimental data

    Returns
    -------
    dict
        Summary statistics including:
        - n_points: Number of data points
        - temperature_range: (min, max) temperature
        - pressure_range: (min, max) pressure
        - references: List of unique references
        - components: List of components
    """
    summary = {
        'n_points': len(df),
    }
    
    # Temperature range
    temp_col = _find_temperature_column(df)
    if temp_col:
        summary['temperature_range'] = (df[temp_col].min(), df[temp_col].max())
        summary['temperature_column'] = temp_col
    
    # Pressure range
    pres_col = _find_pressure_column(df)
    if pres_col:
        summary['pressure_range'] = (df[pres_col].min(), df[pres_col].max())
        summary['pressure_column'] = pres_col
    
    # References
    ref_col = _find_reference_column(df)
    if ref_col:
        summary['references'] = df[ref_col].unique().tolist()
        summary['n_references'] = len(summary['references'])
    
    # Components
    components = []
    for col in ['component_1', 'component_2', 'component_3']:
        if col in df.columns:
            components.extend(df[col].unique().tolist())
    summary['components'] = list(set(components))
    
    # Data points per temperature
    if temp_col:
        summary['points_per_temperature'] = df.groupby(temp_col).size().to_dict()
    
    return summary


def _find_temperature_column(df: pd.DataFrame) -> Optional[str]:
    """Find the temperature column in the dataframe."""
    candidates = ['temperature_K', 'Temperature', 'temperature', 'T', 'T_K', 'temp']
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _find_pressure_column(df: pd.DataFrame) -> Optional[str]:
    """Find the pressure column in the dataframe."""
    candidates = ['pressure_bar', 'Pressure', 'pressure', 'P', 'P_bar', 'pres']
    for col in candidates:
        if col in df.columns:
            return col
    return None


def _find_reference_column(df: pd.DataFrame) -> Optional[str]:
    """Find the reference column in the dataframe."""
    candidates = ['reference', 'Reference', 'ref', 'source', 'Source']
    for col in candidates:
        if col in df.columns:
            return col
    return None

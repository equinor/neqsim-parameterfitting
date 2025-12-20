"""
Statistical metrics for model evaluation.

This module provides standard metrics for comparing model predictions
against experimental data in thermodynamic property fitting.
"""

import numpy as np
import pandas as pd
from typing import Union, Dict, List, Optional, Any


def calculate_aad(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate Average Absolute Deviation (AAD).

    AAD = (1/n) * Σ|experimental - calculated|

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Average absolute deviation
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.mean(np.abs(exp - calc))


def calculate_aad_percent(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate Average Absolute Deviation as percentage (AAD%).

    AAD% = (1/n) * Σ|((experimental - calculated) / experimental)| * 100

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Average absolute percentage deviation
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values and zeros in experimental
    mask = ~(np.isnan(exp) | np.isnan(calc) | (exp == 0))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.mean(np.abs((exp - calc) / exp)) * 100


def calculate_rmse(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate Root Mean Square Error (RMSE).

    RMSE = sqrt((1/n) * Σ(experimental - calculated)²)

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Root mean square error
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.sqrt(np.mean((exp - calc) ** 2))


def calculate_bias(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate systematic bias (mean deviation).

    Bias = (1/n) * Σ(calculated - experimental)

    A positive bias indicates the model over-predicts on average.
    A negative bias indicates the model under-predicts on average.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Mean bias
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.mean(calc - exp)


def calculate_bias_percent(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate systematic bias as percentage.

    Bias% = (1/n) * Σ((calculated - experimental) / experimental) * 100

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Mean percentage bias
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values and zeros
    mask = ~(np.isnan(exp) | np.isnan(calc) | (exp == 0))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.mean((calc - exp) / exp) * 100


def calculate_max_error(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate maximum absolute error.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Maximum absolute error
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.max(np.abs(exp - calc))


def calculate_max_error_percent(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate maximum absolute percentage error.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Maximum absolute percentage error
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values and zeros
    mask = ~(np.isnan(exp) | np.isnan(calc) | (exp == 0))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    return np.max(np.abs((exp - calc) / exp)) * 100


def calculate_r_squared(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
) -> float:
    """
    Calculate coefficient of determination (R²).

    R² = 1 - (SS_res / SS_tot)

    where SS_res = Σ(experimental - calculated)²
    and SS_tot = Σ(experimental - mean(experimental))²

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values

    Returns
    -------
    float
        Coefficient of determination (0 to 1, 1 being perfect)
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    if len(exp) == 0:
        return np.nan
    
    ss_res = np.sum((exp - calc) ** 2)
    ss_tot = np.sum((exp - np.mean(exp)) ** 2)
    
    if ss_tot == 0:
        return np.nan
    
    return 1 - (ss_res / ss_tot)


def calculate_all_metrics(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    name: str = "Model",
) -> Dict[str, Any]:
    """
    Calculate all standard metrics for model evaluation.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    name : str, optional
        Name of the model for labeling

    Returns
    -------
    dict
        Dictionary containing all metrics:
        - n_points: Number of data points
        - aad: Average absolute deviation
        - aad_percent: Average absolute deviation (%)
        - rmse: Root mean square error
        - bias: Mean bias
        - bias_percent: Mean bias (%)
        - max_error: Maximum absolute error
        - max_error_percent: Maximum absolute error (%)
        - r_squared: Coefficient of determination
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Count valid points
    mask = ~(np.isnan(exp) | np.isnan(calc))
    n_points = mask.sum()
    
    return {
        'model_name': name,
        'n_points': n_points,
        'aad': calculate_aad(exp, calc),
        'aad_percent': calculate_aad_percent(exp, calc),
        'rmse': calculate_rmse(exp, calc),
        'bias': calculate_bias(exp, calc),
        'bias_percent': calculate_bias_percent(exp, calc),
        'max_error': calculate_max_error(exp, calc),
        'max_error_percent': calculate_max_error_percent(exp, calc),
        'r_squared': calculate_r_squared(exp, calc),
    }


def compare_models(
    experimental: Union[np.ndarray, pd.Series, List],
    model_results: Dict[str, Union[np.ndarray, pd.Series, List]],
) -> pd.DataFrame:
    """
    Compare multiple models against experimental data.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    model_results : dict
        Dictionary mapping model names to their calculated values

    Returns
    -------
    pd.DataFrame
        Comparison table with metrics for each model

    Examples
    --------
    >>> exp = [1.0, 2.0, 3.0]
    >>> models = {
    ...     'SRK': [1.1, 2.1, 3.0],
    ...     'PR': [0.9, 1.9, 3.1],
    ...     'CPA': [1.0, 2.0, 3.0],
    ... }
    >>> compare_models(exp, models)
    """
    results = []
    for name, calculated in model_results.items():
        metrics = calculate_all_metrics(experimental, calculated, name=name)
        results.append(metrics)
    
    df = pd.DataFrame(results)
    df = df.set_index('model_name')
    
    # Sort by AAD%
    df = df.sort_values('aad_percent')
    
    return df


def format_metrics_table(
    metrics: Dict[str, Any],
    precision: int = 4,
) -> str:
    """
    Format metrics dictionary as a readable table string.

    Parameters
    ----------
    metrics : dict
        Metrics dictionary from calculate_all_metrics
    precision : int, default 4
        Number of decimal places

    Returns
    -------
    str
        Formatted table string
    """
    lines = [
        f"Model: {metrics.get('model_name', 'Unknown')}",
        f"{'='*40}",
        f"Data points:      {metrics['n_points']}",
        f"AAD:              {metrics['aad']:.{precision}f}",
        f"AAD%:             {metrics['aad_percent']:.{precision}f}%",
        f"RMSE:             {metrics['rmse']:.{precision}f}",
        f"Bias:             {metrics['bias']:.{precision}f}",
        f"Bias%:            {metrics['bias_percent']:.{precision}f}%",
        f"Max Error:        {metrics['max_error']:.{precision}f}",
        f"Max Error%:       {metrics['max_error_percent']:.{precision}f}%",
        f"R²:               {metrics['r_squared']:.{precision}f}",
    ]
    return '\n'.join(lines)

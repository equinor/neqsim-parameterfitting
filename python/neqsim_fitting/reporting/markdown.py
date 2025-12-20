"""
Markdown report generation utilities.

This module provides functions for generating standardized
fitting reports in Markdown format.
"""

from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any, Union
import pandas as pd


def generate_fitting_report(
    fitting_result: Any,
    property_type: str,
    components: List[str],
    equation_of_state: str,
    data_references: Optional[List[str]] = None,
    additional_notes: Optional[str] = None,
    author: Optional[str] = None,
) -> str:
    """
    Generate a complete fitting report in Markdown format.

    Parameters
    ----------
    fitting_result : FittingResult
        Results from a fitting operation
    property_type : str
        Type of property fitted ('VLE', 'density', 'viscosity', etc.)
    components : list
        List of component names
    equation_of_state : str
        Equation of state used
    data_references : list, optional
        List of literature references for the data
    additional_notes : str, optional
        Additional notes to include
    author : str, optional
        Author of the fitting

    Returns
    -------
    str
        Markdown formatted report
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    sections = []
    
    # Header
    title = f"{property_type} Parameter Fitting: {'-'.join(components)}"
    sections.append(f"# {title}\n")
    sections.append(f"**Generated:** {timestamp}")
    if author:
        sections.append(f"**Author:** {author}")
    sections.append("")
    
    # Overview
    sections.append("## Overview\n")
    sections.append(f"- **Property Type:** {property_type}")
    sections.append(f"- **Components:** {', '.join(components)}")
    sections.append(f"- **Equation of State:** {equation_of_state}")
    sections.append(f"- **Fitting Status:** {'✅ Success' if fitting_result.success else '❌ Failed'}")
    sections.append("")
    
    # Fitted Parameters
    sections.append("## Fitted Parameters\n")
    sections.append("| Parameter | Value | Initial Value |")
    sections.append("|-----------|-------|---------------|")
    for name, value in fitting_result.parameters.items():
        initial = fitting_result.initial_parameters.get(name, '-')
        sections.append(f"| {name} | {value:.6g} | {initial} |")
    sections.append("")
    
    # Metrics
    sections.append("## Fitting Metrics\n")
    sections.append("| Metric | Value |")
    sections.append("|--------|-------|")
    metric_labels = {
        'n_points': 'Data Points',
        'aad': 'AAD',
        'aad_percent': 'AAD (%)',
        'rmse': 'RMSE',
        'bias': 'Bias',
        'bias_percent': 'Bias (%)',
        'max_error': 'Max Error',
        'max_error_percent': 'Max Error (%)',
        'r_squared': 'R²',
    }
    for key, value in fitting_result.metrics.items():
        if key == 'model_name':
            continue
        label = metric_labels.get(key, key)
        if isinstance(value, float):
            sections.append(f"| {label} | {value:.4g} |")
        else:
            sections.append(f"| {label} | {value} |")
    sections.append("")
    
    # Data Sources
    if data_references:
        sections.append("## Data Sources\n")
        for ref in data_references:
            sections.append(f"- {ref}")
        sections.append("")
    
    # Valid Range
    sections.append("## Valid Range\n")
    if hasattr(fitting_result, 'experimental_data') and fitting_result.experimental_data is not None:
        df = fitting_result.experimental_data
        temp_cols = [c for c in df.columns if 'temp' in c.lower() or c == 'T']
        pres_cols = [c for c in df.columns if 'pres' in c.lower() or c == 'P']
        
        if temp_cols:
            t_min, t_max = df[temp_cols[0]].min(), df[temp_cols[0]].max()
            sections.append(f"- **Temperature:** {t_min:.2f} - {t_max:.2f} K")
        if pres_cols:
            p_min, p_max = df[pres_cols[0]].min(), df[pres_cols[0]].max()
            sections.append(f"- **Pressure:** {p_min:.2f} - {p_max:.2f} bar")
    sections.append("")
    
    # Fitting Details
    sections.append("## Fitting Details\n")
    sections.append(f"- **Iterations:** {fitting_result.n_iterations}")
    sections.append(f"- **Function Evaluations:** {fitting_result.n_function_calls}")
    sections.append(f"- **Fitting Time:** {fitting_result.fitting_time:.2f} seconds")
    sections.append(f"- **Optimizer Message:** {fitting_result.message}")
    sections.append("")
    
    # Additional Notes
    if additional_notes:
        sections.append("## Notes\n")
        sections.append(additional_notes)
        sections.append("")
    
    # Usage Example
    sections.append("## Usage in NeqSim\n")
    sections.append("```python")
    sections.append("from neqsim.thermo.thermoTools import fluid")
    sections.append("")
    sections.append(f"fluid1 = fluid('{equation_of_state}')")
    for comp in components:
        sections.append(f"fluid1.addComponent('{comp}', 1.0)")
    sections.append("fluid1.autoSelectMixingRule()")
    sections.append("")
    sections.append("# Set fitted parameters")
    for name, value in fitting_result.parameters.items():
        sections.append(f"# {name} = {value:.6g}")
    sections.append("```")
    sections.append("")
    
    return '\n'.join(sections)


def generate_parameter_card(
    component_1: str,
    component_2: Optional[str],
    parameters: Dict[str, float],
    equation_of_state: str,
    valid_range: Optional[Dict[str, Any]] = None,
    metrics: Optional[Dict[str, float]] = None,
) -> str:
    """
    Generate a compact parameter card in Markdown.

    Parameters
    ----------
    component_1 : str
        First component
    component_2 : str, optional
        Second component (for binary parameters)
    parameters : dict
        Parameter values
    equation_of_state : str
        Equation of state
    valid_range : dict, optional
        Valid temperature/pressure range
    metrics : dict, optional
        Fitting metrics

    Returns
    -------
    str
        Markdown formatted parameter card
    """
    sections = []
    
    if component_2:
        title = f"### {component_1} - {component_2}"
    else:
        title = f"### {component_1}"
    
    sections.append(title)
    sections.append(f"**EoS:** {equation_of_state}\n")
    
    sections.append("**Parameters:**")
    for name, value in parameters.items():
        sections.append(f"- `{name}`: {value:.6g}")
    
    if valid_range:
        sections.append("\n**Valid Range:**")
        if 'temperature_min_K' in valid_range:
            sections.append(f"- T: {valid_range['temperature_min_K']:.1f} - {valid_range['temperature_max_K']:.1f} K")
        if 'pressure_max_bar' in valid_range:
            sections.append(f"- P: 0 - {valid_range['pressure_max_bar']:.1f} bar")
    
    if metrics:
        sections.append(f"\n**AAD:** {metrics.get('aad_percent', 'N/A'):.2f}%")
    
    sections.append("")
    
    return '\n'.join(sections)


def generate_comparison_table(
    comparison_df: pd.DataFrame,
    title: str = "Model Comparison",
) -> str:
    """
    Generate a Markdown table from model comparison results.

    Parameters
    ----------
    comparison_df : pd.DataFrame
        Comparison dataframe from compare_models()
    title : str
        Table title

    Returns
    -------
    str
        Markdown formatted table
    """
    sections = [f"## {title}\n"]
    
    # Format numbers
    formatted_df = comparison_df.copy()
    for col in formatted_df.columns:
        if formatted_df[col].dtype == float:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:.4g}")
    
    # Create markdown table
    header = "| Model | " + " | ".join(formatted_df.columns) + " |"
    separator = "|-------|" + "|".join(["-------" for _ in formatted_df.columns]) + "|"
    
    sections.append(header)
    sections.append(separator)
    
    for model_name, row in formatted_df.iterrows():
        row_str = f"| {model_name} | " + " | ".join(str(v) for v in row.values) + " |"
        sections.append(row_str)
    
    sections.append("")
    
    return '\n'.join(sections)


def save_report(
    content: str,
    filepath: Union[str, Path],
    create_dirs: bool = True,
) -> Path:
    """
    Save a report to a file.

    Parameters
    ----------
    content : str
        Report content
    filepath : str or Path
        Output file path
    create_dirs : bool
        Whether to create parent directories

    Returns
    -------
    Path
        Path to saved file
    """
    filepath = Path(filepath)
    
    if create_dirs:
        filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filepath

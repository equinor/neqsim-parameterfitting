"""
Plotting utilities for model evaluation and comparison.

This module provides standard plots for visualizing model performance
against experimental data.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from typing import Optional, List, Dict, Union, Tuple, Any


def parity_plot(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    title: str = "Parity Plot",
    xlabel: str = "Experimental",
    ylabel: str = "Calculated",
    deviation_lines: List[float] = [5, 10],
    figsize: Tuple[int, int] = (8, 8),
    save_path: Optional[str] = None,
    show: bool = True,
    **kwargs,
) -> Figure:
    """
    Create a parity plot comparing calculated vs experimental values.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    deviation_lines : list
        Percentage deviation lines to show (e.g., [5, 10] for ±5% and ±10%)
    figsize : tuple
        Figure size (width, height)
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot
    **kwargs
        Additional arguments passed to scatter

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(exp) | np.isnan(calc))
    exp, calc = exp[mask], calc[mask]
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Plot data points
    scatter_kwargs = {'alpha': 0.6, 's': 50, 'edgecolors': 'black', 'linewidths': 0.5}
    scatter_kwargs.update(kwargs)
    ax.scatter(exp, calc, **scatter_kwargs)
    
    # Diagonal line (perfect agreement)
    min_val = min(exp.min(), calc.min())
    max_val = max(exp.max(), calc.max())
    margin = (max_val - min_val) * 0.05
    plot_range = [min_val - margin, max_val + margin]
    
    ax.plot(plot_range, plot_range, 'k-', linewidth=1.5, label='Perfect agreement')
    
    # Deviation lines
    colors = ['green', 'orange', 'red']
    for i, dev in enumerate(deviation_lines):
        color = colors[i] if i < len(colors) else 'gray'
        factor = dev / 100
        ax.plot(plot_range, [x * (1 + factor) for x in plot_range], 
                f'--', color=color, linewidth=1, alpha=0.7, label=f'+{dev}%')
        ax.plot(plot_range, [x * (1 - factor) for x in plot_range], 
                f'--', color=color, linewidth=1, alpha=0.7, label=f'-{dev}%')
    
    ax.set_xlim(plot_range)
    ax.set_ylim(plot_range)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def deviation_plot(
    x_values: Union[np.ndarray, pd.Series, List],
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    xlabel: str = "X",
    ylabel: str = "Deviation (%)",
    title: str = "Deviation Plot",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    show: bool = True,
    **kwargs,
) -> Figure:
    """
    Create a deviation plot showing percentage error vs independent variable.

    Parameters
    ----------
    x_values : array-like
        Independent variable values (e.g., temperature, pressure)
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot
    **kwargs
        Additional arguments passed to scatter

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    x = np.asarray(x_values)
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN values
    mask = ~(np.isnan(x) | np.isnan(exp) | np.isnan(calc) | (exp == 0))
    x, exp, calc = x[mask], exp[mask], calc[mask]
    
    # Calculate percentage deviation
    deviation = ((calc - exp) / exp) * 100
    
    fig, ax = plt.subplots(figsize=figsize)
    
    scatter_kwargs = {'alpha': 0.6, 's': 50, 'edgecolors': 'black', 'linewidths': 0.5}
    scatter_kwargs.update(kwargs)
    ax.scatter(x, deviation, **scatter_kwargs)
    
    # Zero line
    ax.axhline(y=0, color='black', linewidth=1.5)
    
    # Reference lines
    for dev in [5, 10]:
        ax.axhline(y=dev, color='orange', linestyle='--', alpha=0.7)
        ax.axhline(y=-dev, color='orange', linestyle='--', alpha=0.7)
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def deviation_histogram(
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    bins: int = 30,
    title: str = "Deviation Distribution",
    xlabel: str = "Deviation (%)",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    show: bool = True,
) -> Figure:
    """
    Create a histogram of percentage deviations.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    bins : int
        Number of histogram bins
    title : str
        Plot title
    xlabel : str
        X-axis label
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    exp = np.asarray(experimental)
    calc = np.asarray(calculated)
    
    # Remove NaN and zero values
    mask = ~(np.isnan(exp) | np.isnan(calc) | (exp == 0))
    exp, calc = exp[mask], calc[mask]
    
    deviation = ((calc - exp) / exp) * 100
    
    fig, ax = plt.subplots(figsize=figsize)
    
    ax.hist(deviation, bins=bins, edgecolor='black', alpha=0.7)
    ax.axvline(x=0, color='red', linestyle='--', linewidth=2, label='Zero deviation')
    ax.axvline(x=deviation.mean(), color='green', linestyle='-', linewidth=2, 
               label=f'Mean: {deviation.mean():.2f}%')
    
    ax.set_xlabel(xlabel)
    ax.set_ylabel('Frequency')
    ax.set_title(title)
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig


def temperature_deviation_plot(
    temperature: Union[np.ndarray, pd.Series, List],
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    title: str = "Deviation vs Temperature",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    show: bool = True,
) -> Figure:
    """
    Create a deviation plot vs temperature.

    Parameters
    ----------
    temperature : array-like
        Temperature values (K)
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    return deviation_plot(
        temperature, experimental, calculated,
        xlabel="Temperature (K)",
        title=title,
        figsize=figsize,
        save_path=save_path,
        show=show,
    )


def pressure_deviation_plot(
    pressure: Union[np.ndarray, pd.Series, List],
    experimental: Union[np.ndarray, pd.Series, List],
    calculated: Union[np.ndarray, pd.Series, List],
    title: str = "Deviation vs Pressure",
    figsize: Tuple[int, int] = (10, 6),
    save_path: Optional[str] = None,
    show: bool = True,
) -> Figure:
    """
    Create a deviation plot vs pressure.

    Parameters
    ----------
    pressure : array-like
        Pressure values (bar)
    experimental : array-like
        Experimental values
    calculated : array-like
        Model calculated values
    title : str
        Plot title
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    return deviation_plot(
        pressure, experimental, calculated,
        xlabel="Pressure (bar)",
        title=title,
        figsize=figsize,
        save_path=save_path,
        show=show,
    )


def multi_model_comparison_plot(
    experimental: Union[np.ndarray, pd.Series, List],
    model_results: Dict[str, Union[np.ndarray, pd.Series, List]],
    title: str = "Model Comparison",
    xlabel: str = "Experimental",
    ylabel: str = "Calculated",
    figsize: Tuple[int, int] = (10, 8),
    save_path: Optional[str] = None,
    show: bool = True,
) -> Figure:
    """
    Create a parity plot comparing multiple models.

    Parameters
    ----------
    experimental : array-like
        Experimental values
    model_results : dict
        Dictionary mapping model names to calculated values
    title : str
        Plot title
    xlabel : str
        X-axis label
    ylabel : str
        Y-axis label
    figsize : tuple
        Figure size
    save_path : str, optional
        Path to save the figure
    show : bool
        Whether to display the plot

    Returns
    -------
    matplotlib.figure.Figure
        The generated figure
    """
    exp = np.asarray(experimental)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    colors = plt.cm.tab10.colors
    markers = ['o', 's', '^', 'D', 'v', '<', '>', 'p', 'h', '*']
    
    for i, (name, calc) in enumerate(model_results.items()):
        calc = np.asarray(calc)
        mask = ~(np.isnan(exp) | np.isnan(calc))
        
        ax.scatter(
            exp[mask], calc[mask],
            label=name,
            color=colors[i % len(colors)],
            marker=markers[i % len(markers)],
            alpha=0.6,
            s=50,
            edgecolors='black',
            linewidths=0.5,
        )
    
    # Diagonal and deviation lines
    min_val = exp[~np.isnan(exp)].min()
    max_val = exp[~np.isnan(exp)].max()
    margin = (max_val - min_val) * 0.05
    plot_range = [min_val - margin, max_val + margin]
    
    ax.plot(plot_range, plot_range, 'k-', linewidth=1.5, label='Perfect')
    ax.plot(plot_range, [x * 1.1 for x in plot_range], 'g--', alpha=0.5)
    ax.plot(plot_range, [x * 0.9 for x in plot_range], 'g--', alpha=0.5)
    
    ax.set_xlim(plot_range)
    ax.set_ylim(plot_range)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.legend(loc='upper left')
    ax.set_aspect('equal')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches='tight')
    
    if show:
        plt.show()
    
    return fig

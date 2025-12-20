"""
NeqSim Fitting - Parameter fitting and evaluation utilities for NeqSim

This package provides tools for:
- Loading and validating experimental data
- Fitting thermodynamic and physical property parameters
- Evaluating model performance with standard metrics
- Generating fitting reports
"""

__version__ = "0.1.0"
__author__ = "Equinor"

from neqsim_fitting.data import loader, validator
from neqsim_fitting.evaluation import metrics, plots
from neqsim_fitting.fitting import base
from neqsim_fitting.reporting import markdown

__all__ = [
    "loader",
    "validator", 
    "metrics",
    "plots",
    "base",
    "markdown",
]

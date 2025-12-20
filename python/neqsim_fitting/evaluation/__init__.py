"""Evaluation utilities for model comparison and error metrics."""

from neqsim_fitting.evaluation.metrics import (
    calculate_aad,
    calculate_aad_percent,
    calculate_rmse,
    calculate_bias,
    calculate_max_error,
    calculate_r_squared,
    calculate_all_metrics,
    compare_models,
)
from neqsim_fitting.evaluation.plots import (
    parity_plot,
    deviation_plot,
    deviation_histogram,
    temperature_deviation_plot,
    pressure_deviation_plot,
    multi_model_comparison_plot,
)

__all__ = [
    "calculate_aad",
    "calculate_aad_percent",
    "calculate_rmse",
    "calculate_bias",
    "calculate_max_error",
    "calculate_r_squared",
    "calculate_all_metrics",
    "compare_models",
    "parity_plot",
    "deviation_plot",
    "deviation_histogram",
    "temperature_deviation_plot",
    "pressure_deviation_plot",
    "multi_model_comparison_plot",
]

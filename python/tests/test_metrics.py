"""Tests for evaluation metrics."""

import pytest
import numpy as np
from neqsim_fitting.evaluation.metrics import (
    calculate_aad,
    calculate_aad_percent,
    calculate_rmse,
    calculate_bias,
    calculate_r_squared,
    calculate_all_metrics,
    compare_models,
)


class TestMetrics:
    """Test metric calculations."""

    def test_calculate_aad(self):
        """Test AAD calculation."""
        exp = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        calc = np.array([1.1, 1.9, 3.2, 3.8, 5.1])
        
        aad = calculate_aad(exp, calc)
        
        # Manual calculation
        expected = np.mean(np.abs(exp - calc))
        assert abs(aad - expected) < 1e-10

    def test_calculate_aad_percent(self):
        """Test AAD% calculation."""
        exp = np.array([100.0, 200.0, 300.0])
        calc = np.array([105.0, 190.0, 315.0])
        
        aad_pct = calculate_aad_percent(exp, calc)
        
        # Should be around 5%
        assert 4.0 < aad_pct < 6.0

    def test_calculate_rmse(self):
        """Test RMSE calculation."""
        exp = np.array([1.0, 2.0, 3.0])
        calc = np.array([1.0, 2.0, 3.0])  # Perfect match
        
        rmse = calculate_rmse(exp, calc)
        
        assert rmse == 0.0

    def test_calculate_bias(self):
        """Test bias calculation."""
        exp = np.array([1.0, 2.0, 3.0])
        calc = np.array([1.1, 2.1, 3.1])  # Systematic over-prediction
        
        bias = calculate_bias(exp, calc)
        
        assert abs(bias - 0.1) < 1e-10

    def test_calculate_r_squared(self):
        """Test R² calculation."""
        exp = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        calc = exp.copy()  # Perfect match
        
        r2 = calculate_r_squared(exp, calc)
        
        assert abs(r2 - 1.0) < 1e-10

    def test_calculate_all_metrics(self):
        """Test that all metrics are calculated."""
        exp = np.array([1.0, 2.0, 3.0, 4.0, 5.0])
        calc = np.array([1.1, 1.9, 3.1, 3.9, 5.1])
        
        metrics = calculate_all_metrics(exp, calc, name="Test")
        
        assert 'aad' in metrics
        assert 'aad_percent' in metrics
        assert 'rmse' in metrics
        assert 'bias' in metrics
        assert 'r_squared' in metrics
        assert metrics['model_name'] == "Test"

    def test_handles_nan_values(self):
        """Test that NaN values are handled correctly."""
        exp = np.array([1.0, np.nan, 3.0])
        calc = np.array([1.0, 2.0, np.nan])
        
        aad = calculate_aad(exp, calc)
        
        # Should only use the one valid pair
        assert abs(aad) < 1e-10

    def test_compare_models(self):
        """Test model comparison."""
        exp = np.array([1.0, 2.0, 3.0])
        models = {
            'Model A': np.array([1.1, 2.1, 3.1]),
            'Model B': np.array([1.0, 2.0, 3.0]),  # Perfect
        }
        
        comparison = compare_models(exp, models)
        
        # Model B should have lower AAD%
        assert comparison.loc['Model B', 'aad_percent'] < comparison.loc['Model A', 'aad_percent']

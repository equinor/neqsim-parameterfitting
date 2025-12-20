"""Tests for data loading utilities."""

import pytest
import pandas as pd
import numpy as np
from pathlib import Path
import tempfile
import os


class TestDataLoader:
    """Test data loading functions."""

    def test_load_experimental_data_basic(self):
        """Test basic CSV loading."""
        from neqsim_fitting.data.loader import load_experimental_data
        
        # Create temporary CSV
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            f.write("Temperature,Pressure,Value\n")
            f.write("298.15,1.0,0.5\n")
            f.write("323.15,2.0,0.6\n")
            temp_path = f.name
        
        try:
            df = load_experimental_data(temp_path, validate=False)
            assert len(df) == 2
            assert 'temperature_K' in df.columns or 'Temperature' in df.columns
        finally:
            os.unlink(temp_path)

    def test_get_data_summary(self):
        """Test data summary generation."""
        from neqsim_fitting.data.loader import get_data_summary
        
        df = pd.DataFrame({
            'temperature_K': [298.15, 323.15, 373.15],
            'pressure_bar': [1.0, 10.0, 50.0],
            'reference': ['Ref1', 'Ref1', 'Ref2'],
            'component_1': ['CO2', 'CO2', 'CO2'],
        })
        
        summary = get_data_summary(df)
        
        assert summary['n_points'] == 3
        assert summary['temperature_range'] == (298.15, 373.15)
        assert summary['pressure_range'] == (1.0, 50.0)
        assert 'Ref1' in summary['references']
        assert 'Ref2' in summary['references']


class TestDataValidator:
    """Test data validation functions."""

    def test_validate_columns_basic(self):
        """Test column validation."""
        from neqsim_fitting.data.validator import validate_columns
        
        df = pd.DataFrame({
            'col1': [1, 2, 3],
            'col2': [4, 5, 6],
        })
        
        result = validate_columns(df, required_columns=['col1', 'col2'])
        assert result['valid'] is True

    def test_validate_columns_missing(self):
        """Test missing column detection."""
        from neqsim_fitting.data.validator import validate_columns
        
        df = pd.DataFrame({
            'col1': [1, 2, 3],
        })
        
        result = validate_columns(df, required_columns=['col1', 'col2'])
        assert result['valid'] is False
        assert len(result['errors']) > 0

    def test_check_data_quality(self):
        """Test data quality check."""
        from neqsim_fitting.data.validator import check_data_quality
        
        df = pd.DataFrame({
            'value': [1.0, 2.0, 3.0, 100.0],  # 100.0 is an outlier
            'uncertainty': [0.1, 0.1, 0.1, 0.1],
        })
        
        quality = check_data_quality(df, 'value', 'uncertainty')
        
        assert quality['n_points'] == 4
        assert quality['has_uncertainty'] is True
        assert quality['n_outliers'] >= 1  # Should detect 100.0 as outlier

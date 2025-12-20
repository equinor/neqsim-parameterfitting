"""
Density parameter fitting.

This module provides utilities for fitting pure component parameters
to experimental density data.
"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, List, Any, Tuple

from neqsim_fitting.fitting.base import BaseFitter, FittingResult


class DensityFitter(BaseFitter):
    """
    Fitter for density-related parameters.
    
    This class fits volume translation and other density-related
    parameters to experimental density data.
    """
    
    def __init__(
        self,
        component: str,
        equation_of_state: str = 'srk',
    ):
        """
        Initialize the density fitter.

        Parameters
        ----------
        component : str
            Component name
        equation_of_state : str
            Equation of state ('srk', 'pr', 'cpa', etc.)
        """
        super().__init__(equation_of_state)
        self.component = component
        
        if self._neqsim_available:
            self._create_fluid([component])
    
    def objective_function(
        self,
        parameters: np.ndarray,
        experimental_data: pd.DataFrame,
    ) -> float:
        """
        Calculate sum of squared relative errors for density.

        Parameters
        ----------
        parameters : np.ndarray
            Model parameters
        experimental_data : pd.DataFrame
            Experimental density data

        Returns
        -------
        float
            Sum of squared relative errors
        """
        calculated = self._calculate_all(experimental_data)
        experimental = self._get_experimental_values(experimental_data)
        
        # Remove invalid values
        mask = ~(np.isnan(calculated) | np.isnan(experimental) | (experimental == 0))
        calc, exp = calculated[mask], experimental[mask]
        
        if len(calc) == 0:
            return 1e10
        
        return np.sum(((calc - exp) / exp) ** 2)
    
    def calculate_property(
        self,
        conditions: Dict[str, float],
    ) -> float:
        """
        Calculate density at given conditions.

        Parameters
        ----------
        conditions : dict
            Must contain 'temperature' (K) and 'pressure' (bar)

        Returns
        -------
        float
            Density in kg/m³
        """
        if not self._neqsim_available:
            raise ImportError("neqsim required")
        
        from neqsim.thermo.thermoTools import TPflash
        
        try:
            self.fluid.setTemperature(conditions['temperature'], 'K')
            self.fluid.setPressure(conditions['pressure'], 'bara')
            TPflash(self.fluid)
            self.fluid.initPhysicalProperties()
            
            return self.fluid.getPhase(0).getPhysicalProperties().getDensity()
        except Exception:
            return float('nan')
    
    def _set_parameters(self, parameters: Dict[str, float]):
        """Set volume translation or other parameters."""
        if not self._neqsim_available or self.fluid is None:
            return
        
        # Volume translation parameter
        if 'volume_translation' in parameters:
            # Set volume translation on component
            comp = self.fluid.getPhase(0).getComponent(self.component)
            comp.setVolumeCorrectionT(parameters['volume_translation'])
    
    def _calculate_all(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Calculate density for all experimental conditions."""
        results = []
        
        temp_col = self._find_column(experimental_data,
                                      ['temperature_K', 'Temperature (K)', 'Temperature', 'T'])
        pres_col = self._find_column(experimental_data,
                                      ['pressure_bar', 'Pressure (bar)', 'Pressure', 'P'])
        
        for _, row in experimental_data.iterrows():
            conditions = {
                'temperature': row[temp_col],
                'pressure': row[pres_col],
            }
            results.append(self.calculate_property(conditions))
        
        return np.array(results)
    
    def _get_experimental_values(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Extract experimental density values."""
        density_col = self._find_column(experimental_data,
                                         ['density_kg_m3', 'Density (kg/m3)', 'Density', 'rho'])
        return experimental_data[density_col].values
    
    def _find_column(self, df: pd.DataFrame, candidates: List[str]) -> str:
        """Find column name from candidates."""
        for col in candidates:
            if col in df.columns:
                return col
        raise ValueError(f"Could not find column. Tried: {candidates}")
    
    def calculate_deviation(
        self,
        experimental_data: pd.DataFrame,
    ) -> pd.DataFrame:
        """
        Calculate deviations between model and experimental data.

        Parameters
        ----------
        experimental_data : pd.DataFrame
            Experimental density data

        Returns
        -------
        pd.DataFrame
            Original data with calculated values and deviations
        """
        calculated = self._calculate_all(experimental_data)
        experimental = self._get_experimental_values(experimental_data)
        
        result = experimental_data.copy()
        result['calculated_density'] = calculated
        result['deviation'] = calculated - experimental
        result['deviation_percent'] = ((calculated - experimental) / experimental) * 100
        
        return result

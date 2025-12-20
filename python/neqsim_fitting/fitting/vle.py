"""
VLE (Vapor-Liquid Equilibrium) parameter fitting.

This module provides utilities for fitting binary interaction parameters
and other VLE-related parameters to experimental solubility data.
"""

import numpy as np
import pandas as pd
from typing import Optional, Dict, List, Any, Tuple

from neqsim_fitting.fitting.base import BaseFitter, FittingResult


class VLEFitter(BaseFitter):
    """
    Fitter for VLE binary interaction parameters.
    
    This class fits kij and kij_T parameters for binary mixtures
    to experimental solubility data.
    """
    
    def __init__(
        self,
        component_1: str,
        component_2: str,
        equation_of_state: str = 'cpa',
        mixing_rule: str = 'classic',
    ):
        """
        Initialize the VLE fitter.

        Parameters
        ----------
        component_1 : str
            First component (typically the solute)
        component_2 : str
            Second component (typically the solvent)
        equation_of_state : str
            Equation of state ('srk', 'pr', 'cpa', etc.)
        mixing_rule : str
            Mixing rule
        """
        super().__init__(equation_of_state, mixing_rule)
        self.component_1 = component_1
        self.component_2 = component_2
        
        if self._neqsim_available:
            self._create_fluid([component_1, component_2])
    
    def objective_function(
        self,
        parameters: np.ndarray,
        experimental_data: pd.DataFrame,
    ) -> float:
        """
        Calculate sum of squared relative errors.

        Parameters
        ----------
        parameters : np.ndarray
            [kij, kij_T] parameters
        experimental_data : pd.DataFrame
            Experimental VLE data

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
        
        # Sum of squared relative errors
        return np.sum(((calc - exp) / exp) ** 2)
    
    def calculate_property(
        self,
        conditions: Dict[str, float],
    ) -> float:
        """
        Calculate solubility at given conditions.

        Parameters
        ----------
        conditions : dict
            Must contain 'temperature' (K) and 'pressure' (bar)

        Returns
        -------
        float
            Mole fraction of component 1 in liquid phase
        """
        if not self._neqsim_available:
            raise ImportError("neqsim required")
        
        from neqsim.thermo.thermoTools import TPflash
        
        try:
            self.fluid.setTemperature(conditions['temperature'], 'K')
            self.fluid.setPressure(conditions['pressure'], 'bara')
            TPflash(self.fluid)
            
            # Get liquid phase composition
            if self.fluid.hasPhaseType('aqueous'):
                return self.fluid.getPhase('aqueous').getComponent(self.component_1).getx()
            elif self.fluid.hasPhaseType('oil'):
                return self.fluid.getPhase('oil').getComponent(self.component_1).getx()
            else:
                return float('nan')
        except Exception:
            return float('nan')
    
    def _set_parameters(self, parameters: Dict[str, float]):
        """Set kij parameters on the fluid."""
        if not self._neqsim_available or self.fluid is None:
            return
        
        kij = parameters.get('kij', 0.0)
        kij_T = parameters.get('kij_T', 0.0)
        
        # Set binary interaction parameters
        phase = self.fluid.getPhase(0)
        mixing_rule = phase.getMixingRule()
        
        # Get component indices
        idx1 = phase.getComponent(self.component_1).getComponentNumber()
        idx2 = phase.getComponent(self.component_2).getComponentNumber()
        
        mixing_rule.setBinaryInteractionParameter(idx1, idx2, kij)
        mixing_rule.setBinaryInteractionParameterT1(idx1, idx2, kij_T)
    
    def _calculate_all(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Calculate solubility for all experimental conditions."""
        results = []
        
        # Find column names
        temp_col = self._find_column(experimental_data, 
                                      ['temperature_K', 'Temperature', 'temperature', 'T'])
        pres_col = self._find_column(experimental_data,
                                      ['pressure_bar', 'Pressure', 'pressure', 'P'])
        
        for _, row in experimental_data.iterrows():
            conditions = {
                'temperature': row[temp_col],
                'pressure': row[pres_col],
            }
            results.append(self.calculate_property(conditions))
        
        return np.array(results)
    
    def _get_experimental_values(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Extract experimental mole fractions."""
        x_col = self._find_column(experimental_data, ['x1', 'x_1', 'mole_fraction'])
        return experimental_data[x_col].values
    
    def _find_column(self, df: pd.DataFrame, candidates: List[str]) -> str:
        """Find column name from candidates."""
        for col in candidates:
            if col in df.columns:
                return col
        raise ValueError(f"Could not find column. Tried: {candidates}")
    
    def get_current_parameters(self) -> Dict[str, float]:
        """Get current kij parameters from the fluid."""
        if not self._neqsim_available or self.fluid is None:
            return {}
        
        phase = self.fluid.getPhase(0)
        mixing_rule = phase.getMixingRule()
        
        idx1 = phase.getComponent(self.component_1).getComponentNumber()
        idx2 = phase.getComponent(self.component_2).getComponentNumber()
        
        return {
            'kij': mixing_rule.getBinaryInteractionParameter(idx1, idx2),
            'kij_T': mixing_rule.getBinaryInteractionParameterT1(idx1, idx2),
        }
    
    def fit_kij(
        self,
        experimental_data: pd.DataFrame,
        fit_kij_T: bool = False,
        initial_kij: float = 0.0,
        initial_kij_T: float = 0.0,
        kij_bounds: Tuple[float, float] = (-1.0, 1.0),
        kij_T_bounds: Tuple[float, float] = (-0.01, 0.01),
    ) -> FittingResult:
        """
        Fit binary interaction parameters.

        Parameters
        ----------
        experimental_data : pd.DataFrame
            Experimental VLE data
        fit_kij_T : bool
            Whether to also fit temperature-dependent kij_T
        initial_kij : float
            Initial value for kij
        initial_kij_T : float
            Initial value for kij_T
        kij_bounds : tuple
            Bounds for kij
        kij_T_bounds : tuple
            Bounds for kij_T

        Returns
        -------
        FittingResult
            Fitting results
        """
        initial_params = {'kij': initial_kij}
        bounds = {'kij': kij_bounds}
        
        if fit_kij_T:
            initial_params['kij_T'] = initial_kij_T
            bounds['kij_T'] = kij_T_bounds
        
        return self.fit(
            experimental_data,
            initial_params,
            bounds=bounds,
            method='L-BFGS-B',
        )

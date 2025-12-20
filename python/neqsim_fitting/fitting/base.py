"""
Base fitting utilities for NeqSim parameter optimization.

This module provides base classes and utilities for fitting
thermodynamic parameters to experimental data.
"""

import numpy as np
import pandas as pd
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any, Callable, Union, Tuple
from abc import ABC, abstractmethod
from datetime import datetime


@dataclass
class FittingResult:
    """
    Container for fitting results.

    Attributes
    ----------
    success : bool
        Whether the fitting converged successfully
    parameters : dict
        Dictionary of fitted parameter names and values
    initial_parameters : dict
        Initial parameter values before fitting
    metrics : dict
        Evaluation metrics (AAD, RMSE, etc.)
    n_iterations : int
        Number of optimization iterations
    n_function_calls : int
        Number of function evaluations
    fitting_time : float
        Time taken for fitting (seconds)
    experimental_data : pd.DataFrame
        The experimental data used for fitting
    calculated_values : np.ndarray
        Model values calculated with fitted parameters
    residuals : np.ndarray
        Residuals (experimental - calculated)
    message : str
        Status message from the optimizer
    """
    success: bool
    parameters: Dict[str, float]
    initial_parameters: Dict[str, float]
    metrics: Dict[str, float]
    n_iterations: int = 0
    n_function_calls: int = 0
    fitting_time: float = 0.0
    experimental_data: Optional[pd.DataFrame] = None
    calculated_values: Optional[np.ndarray] = None
    residuals: Optional[np.ndarray] = None
    message: str = ""
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            'success': self.success,
            'parameters': self.parameters,
            'initial_parameters': self.initial_parameters,
            'metrics': self.metrics,
            'n_iterations': self.n_iterations,
            'n_function_calls': self.n_function_calls,
            'fitting_time': self.fitting_time,
            'message': self.message,
            'timestamp': self.timestamp,
        }
    
    def summary(self) -> str:
        """Generate a text summary of the fitting results."""
        lines = [
            "=" * 50,
            "FITTING RESULTS",
            "=" * 50,
            f"Success: {self.success}",
            f"Message: {self.message}",
            "",
            "Fitted Parameters:",
        ]
        for name, value in self.parameters.items():
            initial = self.initial_parameters.get(name, 'N/A')
            lines.append(f"  {name}: {value:.6g} (initial: {initial})")
        
        lines.extend([
            "",
            "Metrics:",
        ])
        for name, value in self.metrics.items():
            lines.append(f"  {name}: {value:.4g}")
        
        lines.extend([
            "",
            f"Iterations: {self.n_iterations}",
            f"Function calls: {self.n_function_calls}",
            f"Fitting time: {self.fitting_time:.2f} s",
            "=" * 50,
        ])
        
        return '\n'.join(lines)


class BaseFitter(ABC):
    """
    Abstract base class for parameter fitting.

    This class provides the common interface and utilities for fitting
    thermodynamic parameters to experimental data.
    """
    
    def __init__(
        self,
        equation_of_state: str = 'srk',
        mixing_rule: str = 'classic',
    ):
        """
        Initialize the fitter.

        Parameters
        ----------
        equation_of_state : str
            Equation of state to use ('srk', 'pr', 'cpa', etc.)
        mixing_rule : str
            Mixing rule to use ('classic', 'HV', 'WS', etc.)
        """
        self.equation_of_state = equation_of_state
        self.mixing_rule = mixing_rule
        self.fluid = None
        self._neqsim_available = self._check_neqsim()
    
    def _check_neqsim(self) -> bool:
        """Check if neqsim is available."""
        try:
            import neqsim
            return True
        except ImportError:
            return False
    
    def _create_fluid(self, components: List[str]):
        """Create a NeqSim fluid with the specified components."""
        if not self._neqsim_available:
            raise ImportError("neqsim is required for fitting. Install with: pip install neqsim")
        
        from neqsim.thermo.thermoTools import fluid
        
        self.fluid = fluid(self.equation_of_state)
        for comp in components:
            self.fluid.addComponent(comp, 1.0)
        self.fluid.autoSelectMixingRule()
        
        return self.fluid
    
    @abstractmethod
    def objective_function(
        self,
        parameters: np.ndarray,
        experimental_data: pd.DataFrame,
    ) -> float:
        """
        Calculate the objective function value.

        Parameters
        ----------
        parameters : np.ndarray
            Current parameter values
        experimental_data : pd.DataFrame
            Experimental data

        Returns
        -------
        float
            Objective function value (to be minimized)
        """
        pass
    
    @abstractmethod
    def calculate_property(
        self,
        conditions: Dict[str, float],
    ) -> float:
        """
        Calculate the property value at given conditions.

        Parameters
        ----------
        conditions : dict
            Dictionary of conditions (temperature, pressure, composition, etc.)

        Returns
        -------
        float
            Calculated property value
        """
        pass
    
    def fit(
        self,
        experimental_data: pd.DataFrame,
        initial_parameters: Dict[str, float],
        bounds: Optional[Dict[str, Tuple[float, float]]] = None,
        method: str = 'L-BFGS-B',
        options: Optional[Dict[str, Any]] = None,
    ) -> FittingResult:
        """
        Fit parameters to experimental data.

        Parameters
        ----------
        experimental_data : pd.DataFrame
            Experimental data
        initial_parameters : dict
            Initial parameter values
        bounds : dict, optional
            Parameter bounds as {name: (min, max)}
        method : str
            Optimization method ('L-BFGS-B', 'Nelder-Mead', 'Powell', etc.)
        options : dict, optional
            Additional options for the optimizer

        Returns
        -------
        FittingResult
            Fitting results
        """
        from scipy.optimize import minimize
        import time
        
        param_names = list(initial_parameters.keys())
        x0 = np.array([initial_parameters[name] for name in param_names])
        
        # Setup bounds
        if bounds:
            scipy_bounds = [bounds.get(name, (None, None)) for name in param_names]
        else:
            scipy_bounds = None
        
        # Count function calls
        n_calls = [0]
        
        def wrapped_objective(x):
            n_calls[0] += 1
            params = {name: val for name, val in zip(param_names, x)}
            self._set_parameters(params)
            return self.objective_function(x, experimental_data)
        
        # Run optimization
        start_time = time.time()
        
        result = minimize(
            wrapped_objective,
            x0,
            method=method,
            bounds=scipy_bounds,
            options=options or {'maxiter': 1000},
        )
        
        fitting_time = time.time() - start_time
        
        # Get final parameters
        fitted_params = {name: val for name, val in zip(param_names, result.x)}
        
        # Calculate final values and metrics
        self._set_parameters(fitted_params)
        calculated = self._calculate_all(experimental_data)
        experimental = self._get_experimental_values(experimental_data)
        
        from neqsim_fitting.evaluation.metrics import calculate_all_metrics
        metrics = calculate_all_metrics(experimental, calculated)
        
        return FittingResult(
            success=result.success,
            parameters=fitted_params,
            initial_parameters=initial_parameters,
            metrics=metrics,
            n_iterations=result.nit if hasattr(result, 'nit') else 0,
            n_function_calls=n_calls[0],
            fitting_time=fitting_time,
            experimental_data=experimental_data,
            calculated_values=calculated,
            residuals=experimental - calculated,
            message=result.message if hasattr(result, 'message') else str(result),
        )
    
    @abstractmethod
    def _set_parameters(self, parameters: Dict[str, float]):
        """Set the parameters on the fluid/model."""
        pass
    
    @abstractmethod
    def _calculate_all(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Calculate property values for all experimental conditions."""
        pass
    
    @abstractmethod
    def _get_experimental_values(self, experimental_data: pd.DataFrame) -> np.ndarray:
        """Extract experimental values from the dataframe."""
        pass


class SimplePolynomialFitter:
    """
    Simple polynomial fitting for temperature-dependent properties.
    
    Fits a polynomial of the form:
    y = a0 + a1*T + a2*T^2 + ... + an*T^n
    """
    
    def __init__(self, degree: int = 2):
        """
        Initialize the polynomial fitter.

        Parameters
        ----------
        degree : int
            Degree of the polynomial
        """
        self.degree = degree
        self.coefficients = None
    
    def fit(
        self,
        temperature: Union[np.ndarray, pd.Series],
        values: Union[np.ndarray, pd.Series],
    ) -> FittingResult:
        """
        Fit polynomial to data.

        Parameters
        ----------
        temperature : array-like
            Temperature values
        values : array-like
            Property values

        Returns
        -------
        FittingResult
            Fitting results
        """
        import time
        
        temp = np.asarray(temperature)
        val = np.asarray(values)
        
        # Remove NaN
        mask = ~(np.isnan(temp) | np.isnan(val))
        temp, val = temp[mask], val[mask]
        
        start_time = time.time()
        
        # Fit polynomial
        self.coefficients = np.polyfit(temp, val, self.degree)
        
        fitting_time = time.time() - start_time
        
        # Calculate fitted values
        calculated = np.polyval(self.coefficients, temp)
        
        # Create parameter dictionary
        params = {f'a{i}': coef for i, coef in enumerate(reversed(self.coefficients))}
        
        from neqsim_fitting.evaluation.metrics import calculate_all_metrics
        metrics = calculate_all_metrics(val, calculated)
        
        return FittingResult(
            success=True,
            parameters=params,
            initial_parameters={},
            metrics=metrics,
            fitting_time=fitting_time,
            calculated_values=calculated,
            residuals=val - calculated,
            message=f"Polynomial degree {self.degree} fitted successfully",
        )
    
    def predict(self, temperature: Union[float, np.ndarray]) -> Union[float, np.ndarray]:
        """
        Predict values at given temperatures.

        Parameters
        ----------
        temperature : float or array-like
            Temperature(s) to predict

        Returns
        -------
        float or np.ndarray
            Predicted value(s)
        """
        if self.coefficients is None:
            raise ValueError("Model not fitted. Call fit() first.")
        
        return np.polyval(self.coefficients, temperature)

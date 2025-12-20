"""
NeqSim helper utilities.

This module provides utility functions for working with NeqSim
in the context of parameter fitting.
"""

from typing import Optional, List, Dict, Any, Union
import numpy as np


def create_fluid(
    equation_of_state: str,
    components: List[str],
    compositions: Optional[List[float]] = None,
    mixing_rule: str = 'classic',
):
    """
    Create a NeqSim fluid with specified components.

    Parameters
    ----------
    equation_of_state : str
        Equation of state ('srk', 'pr', 'cpa', etc.)
    components : list
        List of component names
    compositions : list, optional
        Mole fractions (default: equal moles)
    mixing_rule : str
        Mixing rule to use

    Returns
    -------
    SystemInterface
        NeqSim fluid object
    """
    try:
        from neqsim.thermo.thermoTools import fluid
    except ImportError:
        raise ImportError("neqsim is required. Install with: pip install neqsim")
    
    if compositions is None:
        compositions = [1.0] * len(components)
    
    fluid1 = fluid(equation_of_state)
    
    for comp, mol in zip(components, compositions):
        fluid1.addComponent(comp, mol)
    
    fluid1.autoSelectMixingRule()
    
    return fluid1


def flash_pt(
    fluid,
    pressure: float,
    temperature: float,
    pressure_unit: str = 'bara',
    temperature_unit: str = 'K',
):
    """
    Perform a PT flash calculation.

    Parameters
    ----------
    fluid : SystemInterface
        NeqSim fluid object
    pressure : float
        Pressure
    temperature : float
        Temperature
    pressure_unit : str
        Pressure unit ('bara', 'Pa', 'psi', etc.)
    temperature_unit : str
        Temperature unit ('K', 'C', etc.)

    Returns
    -------
    SystemInterface
        Flashed fluid
    """
    from neqsim.thermo.thermoTools import TPflash
    
    fluid.setPressure(pressure, pressure_unit)
    fluid.setTemperature(temperature, temperature_unit)
    TPflash(fluid)
    
    return fluid


def get_property(
    fluid,
    property_name: str,
    phase: str = 'overall',
    unit: Optional[str] = None,
) -> float:
    """
    Get a property value from a NeqSim fluid.

    Parameters
    ----------
    fluid : SystemInterface
        NeqSim fluid object (should be flashed first)
    property_name : str
        Property name ('density', 'viscosity', 'Cp', etc.)
    phase : str
        Phase ('overall', 'gas', 'oil', 'aqueous')
    unit : str, optional
        Unit for the property

    Returns
    -------
    float
        Property value
    """
    fluid.initPhysicalProperties()
    
    if phase == 'overall':
        phase_obj = fluid
    else:
        phase_obj = fluid.getPhase(phase)
    
    property_map = {
        'density': lambda p: p.getPhysicalProperties().getDensity(),
        'viscosity': lambda p: p.getPhysicalProperties().getViscosity(),
        'thermal_conductivity': lambda p: p.getPhysicalProperties().getConductivity(),
        'Cp': lambda p: p.getCp(),
        'Cv': lambda p: p.getCv(),
        'enthalpy': lambda p: p.getEnthalpy(),
        'entropy': lambda p: p.getEntropy(),
        'molar_mass': lambda p: p.getMolarMass(),
        'compressibility': lambda p: p.getZ(),
    }
    
    if property_name.lower() in property_map:
        return property_map[property_name.lower()](phase_obj)
    else:
        raise ValueError(f"Unknown property: {property_name}")


def get_component_list() -> List[str]:
    """
    Get list of available components in NeqSim database.

    Returns
    -------
    list
        List of component names
    """
    # Common components available in NeqSim
    return [
        'methane', 'ethane', 'propane', 'n-butane', 'i-butane',
        'n-pentane', 'i-pentane', 'n-hexane', 'n-heptane', 'n-octane',
        'nitrogen', 'oxygen', 'CO2', 'H2S', 'water', 'hydrogen',
        'helium', 'argon', 'benzene', 'toluene',
        'MEG', 'TEG', 'methanol', 'ethanol',
    ]


def get_available_equations_of_state() -> List[str]:
    """
    Get list of available equations of state in NeqSim.

    Returns
    -------
    list
        List of EoS names
    """
    return [
        'srk',      # Soave-Redlich-Kwong
        'pr',       # Peng-Robinson
        'cpa',      # Cubic Plus Association
        'srk-mc',   # SRK with Mathias-Copeman alpha
        'pr-mc',    # PR with Mathias-Copeman alpha
        'gerg2008', # GERG-2008 multiparameter
        'umb-euv',  # UMR-PRU
    ]


def calculate_kij_temperature_dependent(
    kij: float,
    kij_T: float,
    temperature: float,
) -> float:
    """
    Calculate temperature-dependent kij.

    kij(T) = kij + kij_T * T

    Parameters
    ----------
    kij : float
        Base kij value
    kij_T : float
        Temperature coefficient
    temperature : float
        Temperature in Kelvin

    Returns
    -------
    float
        Temperature-dependent kij value
    """
    return kij + kij_T * temperature

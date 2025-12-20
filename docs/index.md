# NeqSim Parameter Fitting

Welcome to the NeqSim Parameter Fitting documentation!

This repository provides tools for fitting and validating thermodynamic parameters used in [NeqSim](https://github.com/equinor/neqsim).

## Features

- **Experimental Data**: Curated datasets for thermodynamic properties
- **Fitting Utilities**: Python package for parameter optimization  
- **Evaluation Tools**: Standard metrics and visualization
- **Parameter Registry**: Version-controlled fitted parameters
- **Report Generation**: Automated documentation

## Quick Start

```python
from neqsim_fitting.data import load_vle_data
from neqsim_fitting.fitting import VLEFitter

# Load data
df = load_vle_data('data/thermodynamics/VLE/water-CO2.csv')

# Fit parameters
fitter = VLEFitter('CO2', 'water', equation_of_state='cpa')
result = fitter.fit_kij(df)

print(result.summary())
```

## Navigation

- [Getting Started](getting-started/installation.md) - Installation and setup
- [Data](data/overview.md) - Available experimental data
- [Fitting](fitting/workflow.md) - Parameter fitting guides
- [API Reference](api/data.md) - Python API documentation
- [Parameters](parameters/registry.md) - Fitted parameter registry

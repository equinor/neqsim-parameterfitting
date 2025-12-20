# NeqSim Parameter Fitting

[![Run Tests](https://github.com/equinor/neqsim-parameterfitting/actions/workflows/run-tests.yml/badge.svg)](https://github.com/equinor/neqsim-parameterfitting/actions/workflows/run-tests.yml)
[![Validate Data](https://github.com/equinor/neqsim-parameterfitting/actions/workflows/validate-data.yml/badge.svg)](https://github.com/equinor/neqsim-parameterfitting/actions/workflows/validate-data.yml)
[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)

Central repository for experimental data, parameter fitting, and model validation for [NeqSim](https://github.com/equinor/neqsim) - the thermodynamic and fluid behavior simulation library.

## 📋 Overview

This repository provides:

- **Experimental Data**: Curated datasets for thermodynamic properties (VLE, density, viscosity, etc.)
- **Fitting Utilities**: Python package for parameter optimization
- **Evaluation Tools**: Standard metrics and visualization for model comparison
- **Parameter Registry**: Version-controlled fitted parameters
- **Report Generation**: Automated documentation of fitting results

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/equinor/neqsim-parameterfitting.git
cd neqsim-parameterfitting

# Install Python package
pip install -e ./python

# Or with all optional dependencies
pip install -e "./python[all]"
```

### Basic Usage

```python
from neqsim_fitting.data import load_vle_data, get_data_summary
from neqsim_fitting.evaluation import calculate_all_metrics, parity_plot
from neqsim_fitting.fitting import VLEFitter

# Load experimental data
df = load_vle_data('data/thermodynamics/VLE/water-CO2.csv')
print(get_data_summary(df))

# Fit parameters
fitter = VLEFitter('CO2', 'water', equation_of_state='cpa')
result = fitter.fit_kij(df, fit_kij_T=True)

# Evaluate results
print(result.summary())
parity_plot(df['x1'], result.calculated_values)
```

## 📁 Repository Structure

```
neqsim-parameterfitting/
├── data/                       # Experimental datasets
│   ├── schema/                 # JSON schemas for validation
│   ├── physicalproperties/     # Viscosity, conductivity, etc.
│   └── thermodynamics/         # VLE, density, Cp, etc.
├── example/                    # Jupyter notebooks
│   ├── thermodynamics/
│   └── physicalproperties/
├── parameters/                 # Fitted parameter registry
│   ├── registry.yaml           # Index of all parameters
│   └── fitted/                 # Individual parameter files
├── python/                     # Python utilities package
│   └── neqsim_fitting/
├── reports/                    # Generated reports
│   ├── templates/              # Jinja2 templates
│   └── generated/              # Output reports
├── scripts/                    # Utility scripts
├── src/                        # Java fitting code
├── templates/                  # Notebook templates
└── pyproject.toml              # Python project config
```

## 📊 Available Data

| Property | Pure Components | Binary Mixtures |
|----------|-----------------|-----------------|
| VLE | - | CO2-water, methane-water, nitrogen-water, oxygen-water |
| Density | hydrogen, water, MEG, TEG | hydrogen-methane |
| Viscosity | hydrogen, water | hydrogen-methane |
| Heat Capacity | CO2, hydrogen, methane, nitrogen, oxygen, TEG, water | - |
| Thermal Conductivity | hydrogen, TEG | hydrogen-methane |
| Speed of Sound | - | hydrogen-methane |

## 🔧 Parameter Fitting Workflow

1. **Load Data** using standardized loaders
2. **Validate** against schemas
3. **Evaluate Baseline** model performance
4. **Fit Parameters** using optimization
5. **Validate Results** with metrics and plots
6. **Export** fitted parameters and reports

See the [template notebooks](templates/notebooks/) for complete examples.

## 📈 Fitted Parameters

All fitted parameters are stored in the [parameters/](parameters/) directory with:
- YAML format for easy reading and version control
- Complete metadata (valid range, data sources, metrics)
- Usage examples for NeqSim

Browse the [parameter registry](parameters/registry.yaml) for available parameters.

## 📖 Documentation

- [Data Format Standards](data/schema/common-columns.md)
- [Python API Documentation](docs/)
- [Notebook Templates](templates/notebooks/README.md)
- [Contributing Guide](CONTRIBUTING.md)

## 🔬 Using with NeqSim

```python
from neqsim.thermo.thermoTools import fluid, TPflash

# Create fluid with fitted parameters
fluid1 = fluid('cpa')
fluid1.addComponent('CO2', 1.0)
fluid1.addComponent('water', 100.0)
fluid1.autoSelectMixingRule()

# Perform flash calculation
fluid1.setTemperature(25, 'C')
fluid1.setPressure(50, 'bara')
TPflash(fluid1)

# Get results
x_CO2 = fluid1.getPhase('aqueous').getComponent('CO2').getx()
print(f"CO2 solubility: {x_CO2:.6f} mol/mol")
```

See the [NeqSim Wiki](https://github.com/equinor/neqsim/wiki) for more information.

## 🛠️ Setting up Maven Project (Java)

Call `mvn validate` to install the NeqSim core jar file located in resources folder to a local maven repository. Then the neqsim package shall be available for the java code. Try it out by calling `mvn test`.

See notebook on [how to work with the NeqSim parameter database](https://colab.research.google.com/github/EvenSol/NeqSim-Colab/blob/master/notebooks/PVT/parameter_database.ipynb), and the description in the [neqsim wiki](https://github.com/equinor/neqsim/wiki/The-NeqSim-parameter-database).

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Quick contribution guide:

1. **Add experimental data**: Follow the [data format standards](data/schema/common-columns.md)
2. **Fit new parameters**: Use the [template notebooks](templates/notebooks/)
3. **Report issues**: Use the issue templates

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [NeqSim](https://github.com/equinor/neqsim) - Main thermodynamic library
- [neqsim-python](https://pypi.org/project/neqsim/) - Python wrapper
- [NeqSim-Colab](https://github.com/EvenSol/NeqSim-Colab) - Jupyter notebooks

## 📧 Contact

- GitHub Issues: [Create an issue](https://github.com/equinor/neqsim-parameterfitting/issues)
- NeqSim Wiki: [Parameter Database](https://github.com/equinor/neqsim/wiki/The-NeqSim-parameter-database)

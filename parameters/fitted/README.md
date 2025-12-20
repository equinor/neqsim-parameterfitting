# Fitted Parameters

This directory contains YAML files with fitted thermodynamic parameters for NeqSim.

## Directory Structure

```
fitted/
├── binary-interaction/    # Binary interaction parameters (kij)
│   ├── CO2-water.yaml
│   ├── methane-water.yaml
│   └── ...
├── pure-component/        # Pure component parameters
│   ├── hydrogen-cp.yaml
│   └── ...
└── README.md
```

## File Format

Each YAML file contains:

1. **Metadata**: ID, creation date, author, status
2. **Components**: Component names as used in NeqSim
3. **Equation of State**: The EoS the parameters are valid for
4. **Parameters**: The fitted parameter values
5. **Valid Range**: Temperature and pressure range
6. **Fitting Information**: Metrics, optimizer details
7. **Data Sources**: References to experimental data
8. **Usage Example**: Python code snippet

## Status Definitions

| Status | Description |
|--------|-------------|
| `draft` | Initial fitting, needs peer review |
| `validated` | Reviewed and tested against additional data |
| `production` | Approved for inclusion in NeqSim database |
| `deprecated` | Superseded by newer fitting |

## Contributing New Parameters

1. Create a fitting notebook in `example/` folder
2. Run the fitting and validate results
3. Create a YAML file following the template structure
4. Add an entry to `../registry.yaml`
5. Submit a pull request

## Template

See [CO2-water.yaml](binary-interaction/CO2-water.yaml) for a complete example.

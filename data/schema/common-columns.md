# Standard Column Definitions for NeqSim Parameter Fitting Data

This document defines the standard column names and formats for all experimental data files in this repository.

## Mandatory Columns

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `id` | integer | Unique row identifier within the file | `1` |
| `temperature_K` | float | Temperature in Kelvin | `298.15` |
| `pressure_bar` | float | Pressure in bar | `10.0` |
| `reference` | string | Literature reference (Author+Year format) | `Houghton1957` |

## Component Columns

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `component_1` | string | Primary component name (NeqSim compatible) | `CO2` |
| `component_2` | string | Secondary component (for mixtures) | `water` |
| `component_3` | string | Tertiary component (for ternary systems) | `methane` |

## Property-Specific Columns

### VLE Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `x1` | float | Liquid mole fraction of component 1 | mol/mol |
| `y1` | float | Vapor mole fraction of component 1 | mol/mol |
| `x2` | float | Liquid mole fraction of component 2 | mol/mol |
| `y2` | float | Vapor mole fraction of component 2 | mol/mol |

### Density Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `density_kg_m3` | float | Mass density | kg/m³ |
| `molar_density_mol_m3` | float | Molar density | mol/m³ |

### Viscosity Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `viscosity_Pa_s` | float | Dynamic viscosity | Pa·s |
| `viscosity_cP` | float | Dynamic viscosity | cP (mPa·s) |

### Thermal Conductivity Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `thermal_conductivity_W_mK` | float | Thermal conductivity | W/(m·K) |

### Heat Capacity Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `cp_J_molK` | float | Isobaric heat capacity | J/(mol·K) |
| `cv_J_molK` | float | Isochoric heat capacity | J/(mol·K) |
| `cp_J_kgK` | float | Specific isobaric heat capacity | J/(kg·K) |

### Speed of Sound Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `speed_of_sound_m_s` | float | Speed of sound | m/s |

### Joule-Thomson Coefficient Data
| Column Name | Type | Description | Unit |
|-------------|------|-------------|------|
| `joule_thomson_K_bar` | float | Joule-Thomson coefficient | K/bar |

## Quality & Uncertainty Columns

| Column Name | Type | Description | Example |
|-------------|------|-------------|---------|
| `uncertainty` | float | Measurement uncertainty (same unit as value) | `0.00002` |
| `uncertainty_percent` | float | Relative uncertainty | `2.0` |
| `quality_flag` | string | Data quality rating (A=excellent, B=good, C=fair) | `A` |
| `doi` | string | DOI of source publication | `10.1021/je00001a001` |
| `notes` | string | Additional notes or comments | `Extrapolated value` |

## File Naming Convention

Files should be named following this pattern:
- Pure components: `{component}.csv` (e.g., `hydrogen.csv`)
- Binary mixtures: `{component1}-{component2}.csv` (e.g., `CO2-water.csv`)
- With electrolytes: `{component1}-{component2}-{salt}.csv` (e.g., `water-CO2-NaCl.csv`)

## Example CSV Header

```csv
id,component_1,component_2,temperature_K,pressure_bar,x1,uncertainty,reference,doi,quality_flag
1,CO2,water,283.15,1.01325,0.000985,0.0000197,Houghton1957,10.1021/je60004a001,A
```

## Data Quality Guidelines

### Quality Flag Criteria
- **A (Excellent)**: Primary literature source, reported uncertainty < 1%, multiple independent measurements
- **B (Good)**: Primary literature source, reported uncertainty 1-5%, single measurement series
- **C (Fair)**: Secondary source, estimated uncertainty, or older publications with limited methodology details

### Recommended Practices
1. Always include the original literature reference
2. Include DOI when available
3. Report uncertainty if provided in the source
4. Use consistent temperature scale (Kelvin)
5. Use consistent pressure unit (bar)
6. Document any data transformations or unit conversions in notes

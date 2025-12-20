# Notebook Templates

This folder contains standardized Jupyter notebook templates for parameter fitting and model evaluation.

## Available Templates

| Template | Purpose | Use Case |
|----------|---------|----------|
| [vle-fitting-template.ipynb](vle-fitting-template.ipynb) | VLE parameter fitting | Fitting binary interaction parameters (kij) |
| [density-fitting-template.ipynb](density-fitting-template.ipynb) | Density evaluation | Comparing EoS density predictions |
| [heat-capacity-template.ipynb](heat-capacity-template.ipynb) | Heat capacity fitting | Fitting Cp polynomial parameters |
| [viscosity-template.ipynb](viscosity-template.ipynb) | Viscosity evaluation | Comparing viscosity models |

## How to Use Templates

1. **Copy the template** to the appropriate folder in `example/`:
   ```bash
   cp templates/notebooks/vle-fitting-template.ipynb example/thermodynamics/VLE/my-system.ipynb
   ```

2. **Edit the configuration section** at the top of the notebook:
   - Set component names
   - Set data file path
   - Choose equation of state

3. **Run through the notebook** step by step:
   - Load and visualize data
   - Evaluate baseline model
   - Perform fitting (if applicable)
   - Validate results
   - Export fitted parameters and report

## Template Structure

All templates follow this standard structure:

1. **Setup & Imports** - Package installation and configuration
2. **Load Experimental Data** - Read and summarize data
3. **Data Visualization** - Exploratory plots
4. **Data Quality Evaluation** - Filtering and cleaning
5. **Baseline Model Comparison** - Default model performance
6. **Parameter Fitting** - Optimization (if applicable)
7. **Validation & Error Analysis** - Parity plots, deviation analysis
8. **Export Results** - Save fitted parameters and reports
9. **Summary & Recommendations** - Conclusions

## Creating New Templates

When creating a new template:

1. Follow the standard section structure above
2. Include clear documentation in markdown cells
3. Use the `neqsim_fitting` package utilities
4. Make the template self-contained (all imports at top)
5. Include configuration section for easy customization
6. Add example output cells where helpful

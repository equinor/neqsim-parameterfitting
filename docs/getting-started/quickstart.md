# Quick Start

This guide shows how to load data, evaluate models, and fit parameters.

## 1. Loading Data

```python
from neqsim_fitting.data import load_vle_data, get_data_summary

# Load VLE data
df = load_vle_data('data/thermodynamics/VLE/water-CO2.csv')

# View summary
summary = get_data_summary(df)
print(f"Points: {summary['n_points']}")
print(f"T range: {summary['temperature_range']}")
print(f"P range: {summary['pressure_range']}")
```

## 2. Evaluating Models

```python
from neqsim_fitting.evaluation import calculate_all_metrics, parity_plot
import numpy as np

# Example: compare experimental vs calculated values
exp_values = df['x1'].values
calc_values = model_results  # Your calculated values

# Calculate metrics
metrics = calculate_all_metrics(exp_values, calc_values, name="SRK")
print(f"AAD%: {metrics['aad_percent']:.2f}%")
print(f"RMSE: {metrics['rmse']:.4e}")

# Create parity plot
parity_plot(exp_values, calc_values, title="Model Evaluation")
```

## 3. Fitting Parameters

```python
from neqsim_fitting.fitting import VLEFitter

# Create fitter
fitter = VLEFitter('CO2', 'water', equation_of_state='cpa')

# Fit binary interaction parameter
result = fitter.fit_kij(df, fit_kij_T=True)

# View results
print(result.summary())
print(f"Optimized kij: {result.parameters['kij']}")
print(f"Final AAD%: {result.metrics['aad_percent']:.2f}%")
```

## 4. Generating Reports

```python
from neqsim_fitting.reporting import generate_fitting_report, save_report

# Generate report
report = generate_fitting_report(
    result=result,
    experimental_data=df,
    title="CO2-Water kij Fitting"
)

# Save report
save_report(report, 'reports/generated/CO2-water-fitting.md')
```

## Next Steps

- Explore the [template notebooks](templates/notebooks/)
- Read about [data format standards](data/format.md)
- Check the [parameter registry](parameters/registry.md)

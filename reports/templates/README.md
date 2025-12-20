# Report Templates

This folder contains Jinja2 templates for generating standardized fitting reports.

## Available Templates

| Template | Purpose |
|----------|---------|
| `fitting-report.md.jinja2` | Full fitting report with all details |
| `parameter-card.md.jinja2` | Compact parameter summary card |

## Usage

```python
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Load templates
env = Environment(loader=FileSystemLoader('reports/templates'))
template = env.get_template('fitting-report.md.jinja2')

# Render with data
report = template.render(
    title="CO2-water VLE Fitting",
    timestamp=datetime.now().isoformat(),
    author="Your Name",
    property_type="VLE Solubility",
    components=["CO2", "water"],
    equation_of_state="cpa",
    success=True,
    parameters={'kij': -0.1534, 'kij_T': 0.00023},
    initial_parameters={'kij': -0.15, 'kij_T': 0.0002},
    metrics={
        'n_points': 134,
        'aad': 0.000156,
        'aad_percent': 2.34,
        'rmse': 0.000156,
        'bias': -0.000002,
        'bias_percent': -0.12,
        'max_error': 0.00089,
        'max_error_percent': 8.45,
        'r_squared': 0.9987,
    },
    valid_range={
        'temperature_min_K': 273.15,
        'temperature_max_K': 473.15,
        'pressure_min_bar': 1.0,
        'pressure_max_bar': 200.0,
    },
    data_references=['Houghton1957', 'Addicks2001'],
    n_iterations=25,
    n_function_calls=89,
    fitting_time=1.23,
    message='Optimization converged successfully',
    notes='Temperature-dependent kij provides better accuracy.',
)

# Save report
with open('reports/generated/my-report.md', 'w') as f:
    f.write(report)
```

## Template Variables

### fitting-report.md.jinja2

| Variable | Type | Description |
|----------|------|-------------|
| `title` | str | Report title |
| `timestamp` | str | Generation timestamp |
| `author` | str | Author name |
| `property_type` | str | Property being fitted |
| `components` | list | List of component names |
| `equation_of_state` | str | EoS used |
| `success` | bool | Whether fitting succeeded |
| `parameters` | dict | Fitted parameter values |
| `initial_parameters` | dict | Initial parameter values |
| `metrics` | dict | Fitting metrics |
| `valid_range` | dict | Valid T/P range |
| `data_references` | list | Literature references |
| `n_iterations` | int | Optimizer iterations |
| `n_function_calls` | int | Function evaluations |
| `fitting_time` | float | Time in seconds |
| `message` | str | Optimizer message |
| `notes` | str | Additional notes |

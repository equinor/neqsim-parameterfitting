# Generated Reports

This folder contains auto-generated fitting reports.

## Naming Convention

Reports are named using the pattern:
```
YYYY-MM-DD-component1-component2-property.md
```

Examples:
- `2024-01-15-CO2-water-kij.md`
- `2024-02-01-hydrogen-Cp.md`
- `2024-03-10-methane-water-vle.md`

## How to Generate Reports

Reports are generated using the `neqsim_fitting.reporting` module:

```python
from neqsim_fitting.reporting import generate_fitting_report, save_report
from datetime import datetime

# After fitting...
report = generate_fitting_report(
    fitting_result,
    property_type='VLE',
    components=['CO2', 'water'],
    equation_of_state='cpa',
    data_references=['Houghton1957'],
    author='Your Name',
)

# Save with date prefix
date_str = datetime.now().strftime('%Y-%m-%d')
save_report(report, f'reports/generated/{date_str}-CO2-water-kij.md')
```

## Report Archive

| Date | System | Property | AAD% | Status |
|------|--------|----------|------|--------|
| 2024-01-15 | CO2-water | kij | 2.34% | ✅ Validated |
| 2024-01-20 | methane-water | kij | 3.12% | 📝 Draft |

*Reports in this folder are auto-generated. Do not edit manually.*

# Contributing to NeqSim Parameter Fitting

Thank you for your interest in contributing! This document provides guidelines for contributing to this repository.

## Ways to Contribute

### 1. Adding Experimental Data

To add new experimental data:

1. **Format your data** according to the [standard column definitions](data/schema/common-columns.md)
2. **Create a CSV file** with the appropriate name:
   - Pure components: `{component}.csv`
   - Binary mixtures: `{component1}-{component2}.csv`
3. **Place the file** in the correct directory under `data/`
4. **Submit a PR** with:
   - The data file
   - Reference information (DOI if available)
   - Description of data source and quality

### 2. Fitting New Parameters

To contribute fitted parameters:

1. **Create a fitting notebook** using the templates in `templates/notebooks/`
2. **Run the fitting** and document the results
3. **Create a parameter YAML file** in `parameters/fitted/`
4. **Update the registry** in `parameters/registry.yaml`
5. **Generate a report** using the reporting utilities
6. **Submit a PR** with all files

### 3. Improving the Python Package

For code contributions:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes**
4. **Run tests**: `pytest python/tests/`
5. **Format code**: `black python/ && ruff check python/`
6. **Submit a PR**

## Code Style

- Python: Follow PEP 8, use Black for formatting
- Maximum line length: 100 characters
- Use type hints where possible
- Document all public functions with docstrings

## Data Quality Guidelines

When contributing data:

- **Include references**: Always cite the source
- **Report uncertainty**: Include when available
- **Quality flags**: Use A/B/C ratings
- **Avoid duplicates**: Check existing data first
- **Use SI units**: Temperature in K, pressure in bar

## Pull Request Process

1. Ensure all tests pass
2. Update documentation if needed
3. Add entry to CHANGELOG if applicable
4. Request review from maintainers
5. Address review feedback

## Questions?

- Open a [GitHub Issue](https://github.com/equinor/neqsim-parameterfitting/issues)
- Check existing issues and discussions

Thank you for contributing!

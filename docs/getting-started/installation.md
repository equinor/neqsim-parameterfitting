# Installation

## Requirements

- Python 3.9 or higher
- Java 11 or higher (for Java components)
- Maven 3.6+ (for Java components)

## Python Package Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/equinor/neqsim-parameterfitting.git
cd neqsim-parameterfitting

# Install in development mode
pip install -e ./python

# Or with all optional dependencies
pip install -e "./python[all]"
```

### Optional Dependencies

The package has several optional dependency groups:

- `dev`: Development tools (pytest, black, ruff)
- `notebooks`: Jupyter notebook support
- `ml`: Machine learning tools (torch, scikit-learn)
- `docs`: Documentation tools (mkdocs)

Install specific groups:

```bash
pip install -e "./python[dev,notebooks]"
```

## Java Setup

For Java components:

```bash
# Install NeqSim to local Maven repository
mvn validate

# Run tests
mvn test
```

## Verification

Verify the installation:

```python
from neqsim_fitting.data import load_experimental_data
from neqsim_fitting.evaluation import calculate_all_metrics

print("Installation successful!")
```

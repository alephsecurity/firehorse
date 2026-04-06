# Deployment Guide for Firehorse

## Building the Package

The package has been successfully built and is ready for deployment to PyPI.

### Built Artifacts
- **Wheel**: `dist/firehorse-1.0.0-py3-none-any.whl` (38KB)
- **Source**: `dist/firehorse-1.0.0.tar.gz` (18.9MB)

## Testing the Package

### Local Installation Test
```bash
# Install the built wheel
pip install dist/firehorse-1.0.0-py3-none-any.whl

# Test the command
firehorse --help
```

### Development Installation
```bash
# Install in development mode
pip install -e .

# Test the module
python -m firehorse --help
```

## Publishing to PyPI

### Prerequisites
1. Install twine (if not already installed):
```bash
pip install twine
```

2. Create PyPI account at https://pypi.org/account/register/

### Upload to Test PyPI (Recommended First)
```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ firehorse
```

### Upload to Production PyPI
```bash
# Upload to PyPI
twine upload dist/*

# Users can then install with:
pip install firehorse
```

## Version Management

The package uses `setuptools-scm` for version management. To update the version:

1. Create a git tag:
```bash
git tag v1.0.1
git push origin v1.0.1
```

2. Rebuild the package:
```bash
python -m build
```

3. Upload the new version:
```bash
twine upload dist/*
```

## Package Structure

The package has been structured as follows:
```
firehorse/
├── firehorse/           # Main package
│   ├── __init__.py      # Package initialization
│   ├── _version.py      # Version information
│   ├── firehorse.py     # Main entry point
│   ├── *.py           # Core modules
│   └── target/        # Target device configurations
├── device/            # Device payload sources
├── setup.py           # Package setup
├── pyproject.toml      # Modern Python packaging
├── MANIFEST.in        # File inclusion rules
├── requirements.txt    # Runtime dependencies
└── README.md          # Documentation
```

## Dependencies

### Runtime Dependencies
- pyserial>=3.5
- pyusb>=1.0.0
- cryptography>=3.0

### Development Dependencies
- pytest>=6.0
- black>=21.0
- flake8>=3.8
- twine>=3.0
- wheel>=0.36
- build>=0.3
- setuptools-scm>=6.0

## Notes

1. The package includes all necessary XML configuration files and target device definitions
2. Device payload sources are included in the source distribution
3. The package is compatible with Python 3.6+
4. Cross-platform support (Windows and Linux)
5. Console script `firehorse` is automatically installed and available in PATH

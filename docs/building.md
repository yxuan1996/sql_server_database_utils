# Building & Deployment

## Building the Package

The module is packaged using `setuptools`. To build a wheel distribution:

### Prerequisites

Ensure you have the build tools installed:

```bash
pip install build wheel setuptools
```

### Build Commands

Clean previous builds:

```bash
python setup.py clean --all
```

Build the wheel:

```bash
python setup.py bdist_wheel
```

The built wheel will be located in the `dist/` folder.

### Output

```
dist/
├── sql_database_utils-0.2.0-py3-none-any.whl
└── sql_database_utils-0.2.0.tar.gz
```

## Installation from Built Wheel

Once the wheel is built, you can install it locally:

```bash
pip install dist/sql_database_utils-0.2.0-py3-none-any.whl
```

## Distribution

### Uploading to PyPI

To upload the package to PyPI:

1. Install twine:
```bash
pip install twine
```

2. Upload to PyPI:
```bash
twine upload dist/*
```

3. Or upload to TestPyPI first:
```bash
twine upload --repository testpypi dist/*
```

### GitHub Releases

Attach the wheel and source distributions to GitHub releases for distribution:

```bash
# The wheel and tarball in dist/ can be attached to releases
```

## Project Structure

```
sql_server_database_utils/
├── mkdocs.yml                 # MkDocs configuration
├── setup.py                   # Package configuration
├── requirements.txt           # Project dependencies
├── README.md                  # Project README
├── LICENSE                    # MIT License
├── sql_database_utils.py      # Main module
├── docs/                      # Documentation
│   ├── index.md              # Home page
│   ├── installation.md        # Installation guide
│   ├── usage.md              # Usage guide
│   ├── building.md           # This file
│   └── api/
│       └── functions.md      # API reference
└── build/                     # Build output (generated)
    └── lib/
```

## Development Setup

### Install in Development Mode

```bash
# Clone the repository
git clone https://github.com/yxuan1996/sql_server_database_utils.git
cd sql_server_database_utils

# Install dependencies
pip install -r requirements.txt

# Install module in editable mode
pip install -e .
```

### Install Documentation Tools

To build and serve documentation locally:

```bash
pip install mkdocs mkdocs-material pymdown-extensions
```

### Build Documentation

```bash
# Build static site
mkdocs build

# Serve locally for development
mkdocs serve
```

The documentation will be available at `http://localhost:8000`

## Version Management

The current version is **0.2.0** as defined in `setup.py`. To update the version:

1. Update `version` in `setup.py`
2. Update version references in documentation if needed
3. Create a new git tag

```bash
git tag -a v0.2.0 -m "Release version 0.2.0"
git push origin v0.2.0
```

## Dependencies

### Runtime Dependencies

- **pyodbc** - Python ODBC interface
- **pandas** - Data manipulation library

### Development Dependencies

- **mkdocs** - Documentation generator
- **mkdocs-material** - Material design theme
- **pymdown-extensions** - Markdown extensions
- **setuptools** - Package building
- **wheel** - Wheel package format
- **twine** - PyPI upload utility

See `requirements.txt` for the complete list.

## Continuous Integration

For setting up CI/CD pipelines, consider:

- **GitHub Actions** - Automated testing and releases
- **PyPI Workflows** - Automated package distribution
- **ReadTheDocs** - Automatic documentation hosting

## Troubleshooting Build Issues

### Issue: `ModuleNotFoundError: No module named 'setuptools'`

Solution:
```bash
pip install setuptools wheel
```

### Issue: `python setup.py bdist_wheel` command not found

Solution:
```bash
python -m build
```

### Issue: Wheel builds but fails to install

Ensure all dependencies are properly listed in `requirements.txt` and specified in `setup.py`.


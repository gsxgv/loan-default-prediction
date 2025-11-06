# Virtual Environment Setup Guide

This guide explains how to set up and manage the virtual environment for the Loan Default Prediction project.

## Prerequisites

- Python 3.11 installed on your system
- pip (Python package installer)

## Initial Setup

### 1. Create Virtual Environment

```bash
# Navigate to project directory
cd /path/to/loan-default-prediction

# Create virtual environment with Python 3.11
python3.11 -m venv venv
```

### 2. Activate Virtual Environment

```bash
# On macOS/Linux
source venv/bin/activate

# On Windows
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
# Check Python version
python --version

# Check installed packages
pip list
```

## Updating the Virtual Environment

### Scenario 1: Adding New Dependencies

1. **Activate the environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install new packages:**
   ```bash
   pip install package_name
   ```

3. **Update requirements.txt:**
   ```bash
   pip freeze > requirements.txt
   ```

### Scenario 2: Updating Existing Dependencies

1. **Activate the environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Update specific packages:**
   ```bash
   pip install --upgrade package_name
   ```

3. **Update all packages:**
   ```bash
   pip install --upgrade -r requirements.txt
   ```

4. **Update requirements.txt:**
   ```bash
   pip freeze > requirements.txt
   ```

### Scenario 3: Changing Python Version

If you need to change the Python version (e.g., from 3.13 to 3.11):

1. **Deactivate current environment:**
   ```bash
   deactivate
   ```

2. **Remove old virtual environment:**
   ```bash
   rm -rf venv
   ```

3. **Create new environment with desired Python version:**
   ```bash
   python3.11 -m venv venv
   ```

4. **Activate new environment:**
   ```bash
   source venv/bin/activate
   ```

5. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Common Commands

### Environment Management

```bash
# Activate environment
source venv/bin/activate

# Deactivate environment
deactivate

# Check if environment is active (should show venv path)
which python

# Check Python version
python --version
```

### Package Management

```bash
# Install package
pip install package_name

# Install specific version
pip install package_name==1.2.3

# Install from requirements
pip install -r requirements.txt

# Uninstall package
pip uninstall package_name

# List installed packages
pip list

# Show package info
pip show package_name

# Generate requirements file
pip freeze > requirements.txt
```

### Troubleshooting

```bash
# Upgrade pip
pip install --upgrade pip

# Clear pip cache
pip cache purge

# Check for outdated packages
pip list --outdated

# Install with no cache
pip install --no-cache-dir package_name
```

## Project Structure

```
loan-default-prediction/
├── venv/                    # Virtual environment directory
├── requirements.txt         # Python dependencies
├── VENV_SETUP.md          # This guide
├── src/                    # Source code
├── data/                   # Data files
├── notebooks/              # Jupyter notebooks
└── ...
```

## Best Practices

1. **Always activate the virtual environment** before working on the project
2. **Keep requirements.txt updated** when adding new dependencies
3. **Use specific version numbers** in requirements.txt for reproducibility
4. **Don't commit the venv directory** to version control (add to .gitignore)
5. **Document any environment-specific setup** in this file

## Environment Variables

If your project uses environment variables, create a `.env` file in the project root:

```bash
# Example .env file
FLASK_ENV=development
MLFLOW_TRACKING_URI=http://localhost:5000
```

## Integration with IDEs

### VS Code
1. Open the project folder in VS Code
2. Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
3. Type "Python: Select Interpreter"
4. Choose the Python interpreter from your venv: `./venv/bin/python`

### PyCharm
1. Go to File → Settings → Project → Python Interpreter
2. Click the gear icon → Add
3. Choose "Existing Environment"
4. Select the Python executable from your venv: `./venv/bin/python`

## Notes

- The virtual environment isolates project dependencies from your system Python
- Always activate the environment before running scripts or notebooks
- If you encounter permission errors, ensure you have the correct permissions for the project directory
- For production deployments, consider using Docker or similar containerization tools

---

**Last Updated:** January 2025  
**Python Version:** 3.11.5  
**Project:** Loan Default Prediction

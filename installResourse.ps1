<#
    installResources.ps1
    PowerShell script to install all Python dependencies for the project
#>

# Core packages for conversion functionality
pip install pyinstaller==5.13.0       # For EXE building
pip install PyYAML==6.0               # YAML support
pip install xmltodict==0.13.0         # XML parsing
pip install pytest==7.4.0             # For testing (optional)

# GUI dependencies (only needed for Task8)
pip install PyQt5==5.15.9             # Main GUI library
pip install PyQt5-sip==12.13.0        # Required for PyQt5

# Development tools (optional)
pip install black==23.9.1             # Code formatter
pip install flake8==6.1.0             # Linter

# Verify installations
python -c "import yaml, xmltodict, PyQt5; print('All core packages installed successfully')"
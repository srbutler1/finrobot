import sys
import os

# Print Python version and environment information
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Try to import key packages
packages_to_test = [
    "autogen", 
    "pandas", 
    "numpy", 
    "matplotlib", 
    "finnhub",
    "yfinance",
    "mplfinance",
    "backtrader",
    "sec_api"
]

print("\nTesting package imports:")
for package in packages_to_test:
    try:
        __import__(package)
        print(f"✅ {package} imported successfully")
    except ImportError as e:
        print(f"❌ {package} import failed: {e}")

# Print environment variables
print("\nEnvironment variables:")
print(f"PYTHONPATH: {os.environ.get('PYTHONPATH', 'Not set')}")
print(f"CONDA_PREFIX: {os.environ.get('CONDA_PREFIX', 'Not set')}")

# Test imports
import sys
import os
import importlib.util

def check_package(package_name):
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is None:
            print(f"Package {package_name} is NOT installed")
            return False
        else:
            module = importlib.import_module(package_name)
            version = getattr(module, "__version__", "unknown")
            print(f"Package {package_name} is installed (version: {version})")
            return True
    except Exception as e:
        print(f"Error checking {package_name}: {e}")
        return False

# Check Python version
print(f"Python version: {sys.version}")

# Check key packages
packages_to_check = [
    "openai",
    "autogen",
    "numpy",
    "pandas",
    "matplotlib",
    "requests",
    "aiohttp",
    "tiktoken"
]

for package in packages_to_check:
    check_package(package)

# Check if FinRobot package is installed
try:
    spec = importlib.util.find_spec("finrobot")
    if spec is None:
        print("FinRobot package is NOT installed")
        
        # Check if the package is in the current directory
        finrobot_path = os.path.join(os.getcwd(), "FinRobot", "finrobot")
        if os.path.exists(finrobot_path):
            print(f"FinRobot package found at: {finrobot_path}")
            print("You may need to install it with: pip install -e ./FinRobot")
    else:
        print("FinRobot package is installed")
        
        # Try to import a specific module
        try:
            from finrobot.agents.workflow import SingleAssistant
            print("Successfully imported SingleAssistant from finrobot.agents.workflow")
        except Exception as e:
            print(f"Error importing from finrobot: {e}")
except Exception as e:
    print(f"Error checking finrobot package: {e}")

# Test API key configuration
try:
    from finrobot.utils import register_keys_from_json
    print("Testing API key registration...")
    register_keys_from_json('/Users/appleowner/Downloads/FDA II/FinRobot/FinRobot/config_api_keys')
    print("API keys registered successfully")
except Exception as e:
    print(f"Failed to register API keys: {e}")

print("\nPython path:")
for path in sys.path:
    print(path)

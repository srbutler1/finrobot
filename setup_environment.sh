#!/bin/bash

# FinRobot Environment Setup Script

echo "===== FinRobot Environment Setup ====="
echo "This script will help you set up the FinRobot environment."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3 and try again."
    exit 1
fi

# Check if pip is installed
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip and try again."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "finrobot_venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv finrobot_venv
    if [ $? -ne 0 ]; then
        echo "Error: Failed to create virtual environment."
        exit 1
    fi
fi

# Activate virtual environment
echo "Activating virtual environment..."
source finrobot_venv/bin/activate
if [ $? -ne 0 ]; then
    echo "Error: Failed to activate virtual environment."
    exit 1
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r scripts/requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install dependencies."
    exit 1
fi

# Install this package
echo "Installing this package..."
pip install -e .
if [ $? -ne 0 ]; then
    echo "Warning: Failed to install this package. Some functionality may not work."
fi

# Check if original FinRobot repository exists
if [ ! -d "../FinRobot" ]; then
    echo "\nThe original FinRobot repository is not found in the parent directory."
    read -p "Would you like to clone it now? (y/n): " clone_choice
    if [ "$clone_choice" = "y" ] || [ "$clone_choice" = "Y" ]; then
        echo "Cloning original FinRobot repository..."
        cd ..
        git clone https://github.com/AI4Finance-Foundation/FinRobot.git
        if [ $? -ne 0 ]; then
            echo "Error: Failed to clone the repository."
            exit 1
        fi
        cd FinRobot
        echo "Installing original FinRobot package..."
        pip install -e .
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install the original FinRobot package."
            exit 1
        fi
        cd ../finrobot
    else
        echo "\nWarning: The scripts in this repository depend on the original FinRobot package."
        echo "Without it, the scripts will not work properly."
        echo "You can clone it later with: git clone https://github.com/AI4Finance-Foundation/FinRobot.git"
    fi
else
    echo "\nOriginal FinRobot repository found in parent directory."
    if [ ! -f "../FinRobot/setup.py" ]; then
        echo "Warning: The FinRobot directory doesn't seem to contain the expected files."
        echo "It may not be the correct repository."
    else
        echo "Installing original FinRobot package..."
        cd ../FinRobot
        pip install -e .
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install the original FinRobot package."
            exit 1
        fi
        cd ../finrobot
    fi
fi

# Set up API keys
echo "\nWould you like to set up your API keys now?"
read -p "This is required for the scripts to work properly. (y/n): " setup_keys_choice
if [ "$setup_keys_choice" = "y" ] || [ "$setup_keys_choice" = "Y" ]; then
    python scripts/setup_config.py
    if [ $? -ne 0 ]; then
        echo "Error: Failed to set up API keys."
        exit 1
    fi
else
    echo "\nYou can set up your API keys later by running: python scripts/setup_config.py"
fi

echo "\n===== Environment Setup Complete ====="
echo "You can now run the scripts using ./run.sh"
echo "Make sure to activate the virtual environment before running scripts:"
echo "source finrobot_venv/bin/activate"

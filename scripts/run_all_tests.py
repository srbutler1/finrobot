#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Master test script for FinRobot.
This script runs all the test scripts to comprehensively test the FinRobot functionality.
"""

import os
import sys
import logging
import subprocess
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"finrobot_test_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def run_test_script(script_name):
    """Run a test script and return the result."""
    logger.info(f"Running test script: {script_name}")
    
    try:
        result = subprocess.run(
            [sys.executable, script_name],
            capture_output=True,
            text=True,
            check=False
        )
        
        # Log the output
        logger.info(f"Output from {script_name}:")
        for line in result.stdout.splitlines():
            logger.info(f"  {line}")
        
        if result.stderr:
            logger.warning(f"Errors from {script_name}:")
            for line in result.stderr.splitlines():
                logger.warning(f"  {line}")
        
        return result.returncode == 0
    except Exception as e:
        logger.error(f"Error running {script_name}: {e}")
        return False

def main():
    """Main function to run all test scripts."""
    logger.info("Starting FinRobot comprehensive tests...")
    
    # List of test scripts to run
    test_scripts = [
        "test_imports.py",
        "test_basic_agents.py",
        "test_data_sources.py",
        "test_functional.py",
        "test_advanced_agents.py"
    ]
    
    # Run each test script
    results = []
    for script in test_scripts:
        script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), script)
        if os.path.exists(script_path):
            result = run_test_script(script_path)
            results.append((script, result))
        else:
            logger.warning(f"Test script not found: {script_path}")
            results.append((script, False))
    
    # Print summary
    logger.info("\nTest Summary:")
    for script, result in results:
        logger.info(f"{script}: {'PASSED' if result else 'FAILED'}")
    
    # Check if all tests passed
    if all(result for _, result in results):
        logger.info("All tests passed!")
        return 0
    else:
        logger.error("Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

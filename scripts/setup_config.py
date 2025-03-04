#!/usr/bin/env python
# setup_config.py

import os
import json
import sys

# Add parent directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

def setup_api_keys():
    """
    Set up API keys for FinRobot.
    """
    print("===== FinRobot API Key Setup =====\n")
    
    # Set up config_api_keys
    config_api_keys_path = os.path.join(parent_dir, "FinRobot", "config_api_keys")
    
    # Check if config_api_keys already exists
    if os.path.exists(config_api_keys_path):
        overwrite = input("config_api_keys already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Skipping config_api_keys setup.")
            return
    
    # Get API keys from user
    print("\nPlease enter your API keys (leave blank if not available):")
    sec_api_key = input("SEC API Key: ")
    finnhub_api_key = input("Finnhub API Key: ")
    alpha_vantage_api_key = input("Alpha Vantage API Key: ")
    openai_api_key = input("OpenAI API Key: ")
    
    # Create config_api_keys
    config_api_keys = {}
    if sec_api_key:
        config_api_keys["SEC_API_KEY"] = sec_api_key
    if finnhub_api_key:
        config_api_keys["FINNHUB_API_KEY"] = finnhub_api_key
    if alpha_vantage_api_key:
        config_api_keys["ALPHA_VANTAGE_API_KEY"] = alpha_vantage_api_key
    
    # Write config_api_keys to file
    os.makedirs(os.path.dirname(config_api_keys_path), exist_ok=True)
    with open(config_api_keys_path, "w") as f:
        json.dump(config_api_keys, f, indent=4)
    
    print(f"\nconfig_api_keys saved to {config_api_keys_path}")
    
    # Set up OAI_CONFIG_LIST
    oai_config_list_path = os.path.join(parent_dir, "FinRobot", "OAI_CONFIG_LIST")
    
    # Check if OAI_CONFIG_LIST already exists
    if os.path.exists(oai_config_list_path):
        overwrite = input("\nOAI_CONFIG_LIST already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Skipping OAI_CONFIG_LIST setup.")
            return
    
    # Create OAI_CONFIG_LIST if we have an OpenAI API key
    if openai_api_key:
        oai_config_list = [
            {
                "model": "gpt-4o",
                "api_key": openai_api_key
            },
            {
                "model": "gpt-3.5-turbo",
                "api_key": openai_api_key
            }
        ]
        
        # Write OAI_CONFIG_LIST to file
        os.makedirs(os.path.dirname(oai_config_list_path), exist_ok=True)
        with open(oai_config_list_path, "w") as f:
            json.dump(oai_config_list, f, indent=4)
        
        print(f"OAI_CONFIG_LIST saved to {oai_config_list_path}")
    else:
        print("\nOpenAI API Key not provided. Skipping OAI_CONFIG_LIST setup.")
    
    print("\n===== API Key Setup Complete =====\n")
    print("SECURITY NOTE: These files contain sensitive API keys and are included in .gitignore")
    print("to prevent accidental commits. Never commit these files to your repository.")

if __name__ == "__main__":
    setup_api_keys()

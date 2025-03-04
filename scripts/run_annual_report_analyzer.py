#!/usr/bin/env python
# run_annual_report_analyzer.py

import sys
import os
from datetime import datetime, timedelta
import autogen

# Add parent directory to path to import finrobot modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from FinRobot.finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
from FinRobot.finrobot.utils import register_keys_from_json

# Set the paths
config_api_keys_path = os.path.join(parent_dir, "FinRobot", "config_api_keys")
oai_config_list_path = os.path.join(parent_dir, "FinRobot", "OAI_CONFIG_LIST")

# Register API keys
try:
    register_keys_from_json(config_api_keys_path)
    print("API keys registered successfully")
except Exception as e:
    print(f"Failed to register API keys: {e}")
    sys.exit(1)

# Setup LLM config
try:
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_list_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    print("LLM config set up successfully")
except Exception as e:
    print(f"Failed to set up LLM config: {e}")
    sys.exit(1)

# Initialize Annual Report Analyzer
annual_report_analyzer = AnnualReportAnalyzer(
    "Annual_Report_Analyzer",
    llm_config,
    human_input_mode="NEVER"  # Changed from TERMINATE to NEVER to avoid auto-reply loop
)

# Get current date and date ranges for analysis
current_date = datetime.now().strftime("%Y-%m-%d")
one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")

# Get user input for stock symbol
stock_symbol = input("Enter a stock symbol to analyze (default: AAPL): ") or "AAPL"
print(f"Analyzing {stock_symbol}...")

# Create the analysis query
query = f"""
IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
- Current date: {current_date}
- Start date for annual report data: {one_year_ago}
- End date for annual report data: {current_date}

Analyze the latest annual report for {stock_symbol} and highlight key financial metrics, risks, and growth opportunities.
Also analyze the latest 10-K SEC filing for {stock_symbol}, focusing on the Risk Factors (Section 1A) and Management's Discussion (Section 7).
Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
"""

# Run the analyzer
print("Starting analysis, this may take a few minutes...")
response = annual_report_analyzer.chat(query)
print("\n=== Annual Report Analysis ===\n")
print(response)
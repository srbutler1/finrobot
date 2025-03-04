#!/usr/bin/env python
# run_investment_recommendation.py

import sys
import os
from datetime import datetime, timedelta
import autogen

# Add parent directory to path to import finrobot modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from FinRobot.finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
from FinRobot.finrobot.agents.trade_strategist import TradeStrategist
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

# Get current date and date ranges for analysis
current_date = datetime.now().strftime("%Y-%m-%d")
one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# Get user input for stock symbol
stock_symbol = input("Enter a stock symbol to analyze (default: AAPL): ") or "AAPL"
print(f"Analyzing {stock_symbol}...")

# Step 1: Run Annual Report Analysis
print("\n=== Step 1: Running Annual Report Analysis ===\n")
print("This may take a few minutes...")

# Initialize Annual Report Analyzer
annual_report_analyzer = AnnualReportAnalyzer(
    "Annual_Report_Analyzer",
    llm_config,
    human_input_mode="NEVER"
)

# Create the annual report analysis query
annual_report_query = f"""
IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
- Current date: {current_date}
- Start date for annual report data: {one_year_ago}
- End date for annual report data: {current_date}

Analyze the latest annual report for {stock_symbol} and highlight key financial metrics, risks, and growth opportunities.
Also analyze the latest 10-K SEC filing for {stock_symbol}, focusing on the Risk Factors (Section 1A) and Management's Discussion (Section 7).
Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.

Provide a concise summary that can be used by an investment strategist.
"""

# Run the annual report analyzer and capture the response
try:
    print("Starting annual report analysis...")
    annual_report_response = annual_report_analyzer.chat(annual_report_query)
    
    # Extract the first response from the conversation
    if isinstance(annual_report_response, str):
        annual_report_analysis = annual_report_response
    else:
        # If it's not a string, it might be a more complex object
        print("Warning: Unexpected response type from annual report analyzer")
        annual_report_analysis = str(annual_report_response)
    
    print("\n=== Annual Report Analysis ===\n")
    print(annual_report_analysis)
    print("\n=== End of Annual Report Analysis ===\n")
except Exception as e:
    print(f"Error during annual report analysis: {e}")
    sys.exit(1)

# Step 2: Generate Investment Recommendation based on Annual Report Analysis
print("\n=== Step 2: Generating Investment Recommendation ===\n")
print("This may take a few minutes...")

# Initialize Trade Strategist
trade_strategist = TradeStrategist(
    "Trade_Strategist",
    llm_config,
    human_input_mode="NEVER"
)

# Create the investment recommendation query
investment_recommendation_query = f"""
IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
- Current date: {current_date}
- Start date for historical data: {one_month_ago}
- End date for historical data: {current_date}

Based on the following annual report analysis for {stock_symbol}, develop a comprehensive investment recommendation:

{annual_report_analysis}

Your recommendation should include:
1. A clear investment stance (Buy, Hold, or Sell)
2. A target price range
3. Entry and exit strategies
4. Risk assessment and management strategies
5. Investment timeframe (short-term, medium-term, or long-term)

Use technical analysis to support your recommendation and provide specific price levels and indicators.
Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
"""

# Run the trade strategist
try:
    print("Starting investment recommendation generation...")
    investment_recommendation = trade_strategist.chat(investment_recommendation_query)
    
    # Print the final output
    print("\n=== Investment Recommendation for", stock_symbol, "===\n")
    print(investment_recommendation)
    print("\n=== Analysis Complete ===\n")
except Exception as e:
    print(f"Error during investment recommendation generation: {e}")
    sys.exit(1)

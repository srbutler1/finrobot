#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for a single advanced agent in FinRobot.
This script allows testing one agent at a time to verify functionality.
"""

import os
import sys
import logging
import argparse
from datetime import datetime, timedelta
import autogen

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the FinRobot directory to the path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    # Import the required modules
    from finrobot.utils import register_keys_from_json, get_current_date
    from finrobot.agents.rag_agent import RAGAgent
    from finrobot.agents.trade_strategist import TradeStrategist
    from finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
    from finrobot.agents.fingpt_forecaster import FinGPTForecaster
    
    logger.info("Successfully imported FinRobot modules")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.info("Trying alternative import path...")
    
    # Try with explicit FinRobot path
    finrobot_dir = os.path.join(current_dir, "FinRobot")
    sys.path.insert(0, finrobot_dir)
    
    try:
        from finrobot.utils import register_keys_from_json, get_current_date
        from finrobot.agents.rag_agent import RAGAgent
        from finrobot.agents.trade_strategist import TradeStrategist
        from finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
        from finrobot.agents.fingpt_forecaster import FinGPTForecaster
        
        logger.info("Successfully imported FinRobot modules using alternative path")
    except ImportError as e2:
        logger.error(f"Failed to import modules: {e2}")
        sys.exit(1)

def get_user_input():
    """Get user input for stock symbol and other parameters"""
    print("\n=== User Input Required ===")
    stock_symbol = input("Enter a stock symbol to analyze (default: AAPL): ").strip() or "AAPL"
    print(f"Using stock symbol: {stock_symbol}")
    
    current_date = get_current_date()
    print(f"Current date: {current_date}")
    print("===========================\n")
    
    return stock_symbol, current_date

def test_rag_agent(stock_symbol, current_date):
    """Test the RAG Agent"""
    logger.info("Testing RAG agent...")
    
    # Setup LLM config with correct path
    oai_config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "OAI_CONFIG_LIST")
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Initialize RAG agent
    rag_agent = RAGAgent(
        "Financial_RAG_Agent",
        llm_config,
        human_input_mode="TERMINATE"
    )
    
    # Get date ranges for analysis
    one_month_ago = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Test a query
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {one_month_ago}
    - End date for historical data: {current_date}
    
    What were the key financial metrics for {stock_symbol} in their latest earnings report?
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    """
    
    response = rag_agent.chat(query)
    logger.info(f"RAG Agent response: {response[:500]}...")
    
    return response

def test_trade_strategist(stock_symbol, current_date):
    """Test the Trade Strategist Agent"""
    logger.info("Testing Trade Strategist agent...")
    
    # Setup LLM config with correct path
    oai_config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "OAI_CONFIG_LIST")
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Initialize Trade Strategist
    trade_strategist = TradeStrategist(
        "Trade_Strategist",
        llm_config,
        human_input_mode="TERMINATE"
    )
    
    # Get date ranges for analysis
    one_month_ago = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Test a trading strategy query
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {one_month_ago}
    - End date for historical data: {current_date}
    
    Develop a trading strategy for {stock_symbol} based on recent market trends and technical indicators.
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    """
    
    response = trade_strategist.chat(query)
    logger.info(f"Trade Strategist response: {response[:500]}...")
    
    return response

def test_annual_report_analyzer(stock_symbol, current_date):
    """Test the Annual Report Analyzer Agent"""
    logger.info("Testing Annual Report Analyzer agent...")
    
    # Setup LLM config with correct path
    oai_config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "OAI_CONFIG_LIST")
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Initialize Annual Report Analyzer
    annual_report_analyzer = AnnualReportAnalyzer(
        "Annual_Report_Analyzer",
        llm_config,
        human_input_mode="TERMINATE"
    )
    
    # Get date ranges for analysis
    one_year_ago = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=365)).strftime("%Y-%m-%d")
    
    # Test an annual report analysis query
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for annual report data: {one_year_ago}
    - End date for annual report data: {current_date}
    
    Analyze the latest annual report for {stock_symbol} and highlight key financial metrics, risks, and growth opportunities.
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    """
    
    response = annual_report_analyzer.chat(query)
    logger.info(f"Annual Report Analyzer response: {response[:500]}...")
    
    return response

def test_fingpt_forecaster(stock_symbol, current_date):
    """Test the FinGPT Forecaster Agent"""
    logger.info("Testing FinGPT Forecaster agent...")
    
    # Setup LLM config with correct path
    oai_config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "OAI_CONFIG_LIST")
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    
    # Initialize FinGPT Forecaster
    fingpt_forecaster = FinGPTForecaster(
        "FinGPT_Forecaster",
        llm_config,
        human_input_mode="TERMINATE"
    )
    
    # Get date ranges for analysis
    one_month_ago = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")
    
    # Test a forecasting query
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {one_month_ago}
    - End date for historical data: {current_date}
    
    Forecast the stock price movement for {stock_symbol} over the next week based on historical data and market sentiment.
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    """
    
    response = fingpt_forecaster.chat(query)
    logger.info(f"FinGPT Forecaster response: {response[:500]}...")
    
    return response

def main():
    """Main function to run the test"""
    parser = argparse.ArgumentParser(description="Test a single advanced agent in FinRobot")
    parser.add_argument("agent", choices=["rag", "trade", "annual", "fingpt"], 
                        help="Agent to test (rag, trade, annual, fingpt)")
    args = parser.parse_args()
    
    logger.info("Starting FinRobot single agent test...")
    
    # Register API keys - use correct path to config file
    config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "config_api_keys")
    register_keys_from_json(config_path)
    logger.info(f"API keys registered successfully from {config_path}")
    
    # Get user input
    stock_symbol, current_date = get_user_input()
    
    # Test the selected agent
    if args.agent == "rag":
        logger.info("Running test: RAG Agent")
        test_rag_agent(stock_symbol, current_date)
    elif args.agent == "trade":
        logger.info("Running test: Trade Strategist")
        test_trade_strategist(stock_symbol, current_date)
    elif args.agent == "annual":
        logger.info("Running test: Annual Report Analyzer")
        test_annual_report_analyzer(stock_symbol, current_date)
    elif args.agent == "fingpt":
        logger.info("Running test: FinGPT Forecaster")
        test_fingpt_forecaster(stock_symbol, current_date)
    
    logger.info("Test completed successfully")

if __name__ == "__main__":
    main()

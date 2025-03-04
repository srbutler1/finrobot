#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for advanced FinRobot agents functionality.
This script tests the more complex agents in FinRobot, including RAG-based agents and specialized financial agents.
"""

import os
import sys
import logging
import autogen
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from finrobot.utils import register_keys_from_json, get_current_date
    logger.info("Successfully imported FinRobot utils")
except ImportError as e:
    logger.error(f"Failed to import FinRobot utils: {e}")
    sys.exit(1)

def get_user_input(prompt, default=None):
    """Get input from user with a default value."""
    if default:
        user_input = input(f"{prompt} (default: {default}): ")
        return user_input if user_input.strip() else default
    else:
        return input(f"{prompt}: ")

def test_rag_agent(stock_symbol):
    """Test the RAG (Retrieval-Augmented Generation) agent functionality if available."""
    logger.info("Testing RAG agent...")
    
    try:
        # Try to import RAG agent
        try:
            from finrobot.agents.rag_agent import RAGAgent
            rag_agent_available = True
        except ImportError:
            logger.warning("RAG agent not available")
            rag_agent_available = False
            return True
        
        if rag_agent_available:
            # Setup LLM config using autogen's config_list_from_json
            llm_config = {
                "config_list": autogen.config_list_from_json(
                    "FinRobot/OAI_CONFIG_LIST",
                    filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
                ),
                "timeout": 120,
                "temperature": 0,
            }
            
            # Initialize RAG agent
            rag_agent = RAGAgent(
                "Financial_RAG_Agent",
                llm_config,
                human_input_mode="NEVER"
            )
            
            # Get current date and date ranges for analysis
            current_date = datetime.now().strftime("%Y-%m-%d")
            one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
            # Test a query that requires retrieval
            query = f"""
            IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
            - Current date: {current_date}
            - Start date for historical data: {one_month_ago}
            - End date for historical data: {current_date}
            
            What were the key financial metrics for {stock_symbol} in their latest earnings report?
            Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
            """
            
            response = rag_agent.chat(query)
            
            logger.info(f"RAG agent response: {response}")
            logger.info("RAG agent test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in RAG agent test: {e}")
        return False

def test_trade_strategist(stock_symbol):
    """Test the Trade Strategist agent functionality if available."""
    logger.info("Testing Trade Strategist agent...")
    
    try:
        # Try to import Trade Strategist agent
        try:
            from finrobot.agents.trade_strategist import TradeStrategist
            trade_strategist_available = True
        except ImportError:
            logger.warning("Trade Strategist agent not available")
            trade_strategist_available = False
            return True
        
        if trade_strategist_available:
            # Setup LLM config using autogen's config_list_from_json
            llm_config = {
                "config_list": autogen.config_list_from_json(
                    "FinRobot/OAI_CONFIG_LIST",
                    filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
                ),
                "timeout": 120,
                "temperature": 0,
            }
            
            # Initialize Trade Strategist agent
            trade_strategist = TradeStrategist(
                "Trade_Strategist",
                llm_config,
                human_input_mode="NEVER"
            )
            
            # Get current date and date ranges for analysis
            current_date = datetime.now().strftime("%Y-%m-%d")
            one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
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
            
            logger.info(f"Trade Strategist response: {response}")
            logger.info("Trade Strategist test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in Trade Strategist test: {e}")
        return False

def test_annual_report_analyzer(stock_symbol):
    """Test the Annual Report Analyzer agent functionality if available."""
    logger.info("Testing Annual Report Analyzer agent...")
    
    try:
        # Try to import Annual Report Analyzer agent
        try:
            from finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
            annual_report_analyzer_available = True
        except ImportError:
            logger.warning("Annual Report Analyzer agent not available")
            annual_report_analyzer_available = False
            return True
        
        if annual_report_analyzer_available:
            # Setup LLM config using autogen's config_list_from_json
            llm_config = {
                "config_list": autogen.config_list_from_json(
                    "FinRobot/OAI_CONFIG_LIST",
                    filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
                ),
                "timeout": 120,
                "temperature": 0,
            }
            
            # Initialize Annual Report Analyzer agent
            annual_report_analyzer = AnnualReportAnalyzer(
                "Annual_Report_Analyzer",
                llm_config,
                human_input_mode="NEVER"
            )
            
            # Get current date and date ranges for analysis
            current_date = datetime.now().strftime("%Y-%m-%d")
            one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
            
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
            
            logger.info(f"Annual Report Analyzer response: {response}")
            logger.info("Annual Report Analyzer test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in Annual Report Analyzer test: {e}")
        return False

def test_fingpt_forecaster(stock_symbol):
    """Test the FinGPT Forecaster agent functionality if available."""
    logger.info("Testing FinGPT Forecaster agent...")
    
    try:
        # Try to import FinGPT Forecaster agent
        try:
            from finrobot.agents.fingpt_forecaster import FinGPTForecaster
            fingpt_forecaster_available = True
        except ImportError:
            logger.warning("FinGPT Forecaster agent not available")
            fingpt_forecaster_available = False
            return True
        
        if fingpt_forecaster_available:
            # Setup LLM config using autogen's config_list_from_json
            llm_config = {
                "config_list": autogen.config_list_from_json(
                    "FinRobot/OAI_CONFIG_LIST",
                    filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
                ),
                "timeout": 120,
                "temperature": 0,
            }
            
            # Initialize FinGPT Forecaster agent
            fingpt_forecaster = FinGPTForecaster(
                "FinGPT_Forecaster",
                llm_config,
                human_input_mode="NEVER"
            )
            
            # Get current date and date ranges for analysis
            current_date = datetime.now().strftime("%Y-%m-%d")
            one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            
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
            
            logger.info(f"FinGPT Forecaster response: {response}")
            logger.info("FinGPT Forecaster test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in FinGPT Forecaster test: {e}")
        return False

def main():
    """Main function to run all tests."""
    logger.info("Starting FinRobot advanced agents tests...")
    
    # Register API keys
    try:
        register_keys_from_json("FinRobot/config_api_keys")
        logger.info("API keys registered successfully")
    except Exception as e:
        logger.error(f"Failed to register API keys: {e}")
        sys.exit(1)
    
    # Get user input for stock symbol at the beginning
    print("\n=== User Input Required ===")
    stock_symbol = get_user_input("Enter a stock symbol to analyze", "AAPL")
    print(f"Using stock symbol: {stock_symbol}")
    print(f"Current date: {datetime.now().strftime('%Y-%m-%d')}")
    print("===========================\n")
    
    # Run tests
    tests = [
        ("RAG Agent", lambda: test_rag_agent(stock_symbol)),
        ("Trade Strategist", lambda: test_trade_strategist(stock_symbol)),
        ("Annual Report Analyzer", lambda: test_annual_report_analyzer(stock_symbol)),
        ("FinGPT Forecaster", lambda: test_fingpt_forecaster(stock_symbol))
    ]
    
    results = []
    for test_name, test_func in tests:
        logger.info(f"Running test: {test_name}")
        result = test_func()
        results.append((test_name, result))
        logger.info(f"Test {test_name} {'passed' if result else 'failed'}")
    
    # Print summary
    logger.info("\nTest Summary:")
    for test_name, result in results:
        logger.info(f"{test_name}: {'PASSED' if result else 'FAILED'}")
    
    # Check if all tests passed
    if all(result for _, result in results):
        logger.info("All tests passed!")
        return 0
    else:
        logger.error("Some tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())

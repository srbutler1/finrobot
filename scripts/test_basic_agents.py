#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for basic FinRobot agents functionality.
This script tests the core agents in FinRobot, including market analyst and financial advisor.
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
    from finrobot.agents.workflow import SingleAssistant, MultiAssistant
    from finrobot.utils import register_keys_from_json
    logger.info("Successfully imported FinRobot modules")
except ImportError as e:
    logger.error(f"Failed to import FinRobot modules: {e}")
    sys.exit(1)

def get_user_input(prompt, default=None):
    """Get input from user with a default value."""
    if default:
        user_input = input(f"{prompt} (default: {default}): ")
        return user_input if user_input.strip() else default
    else:
        return input(f"{prompt}: ")

def test_single_assistant():
    """Test the SingleAssistant functionality."""
    logger.info("Testing SingleAssistant...")
    
    try:
        # Setup LLM config using autogen's config_list_from_json
        llm_config = {
            "config_list": autogen.config_list_from_json(
                "FinRobot/OAI_CONFIG_LIST",
                filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
            ),
            "timeout": 120,
            "temperature": 0,
        }
        
        # Initialize a single assistant
        market_analyst = SingleAssistant(
            "Market_Analyst",
            llm_config,
            human_input_mode="NEVER"
        )
        
        # Get current date
        current_date = datetime.now().strftime("%Y-%m-%d")
        
        # Test a simple query
        response = market_analyst.chat(
            f"Today is {current_date}. Provide a brief analysis of the current market trends for tech stocks."
        )
        
        logger.info(f"SingleAssistant response: {response}")
        logger.info("SingleAssistant test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error in SingleAssistant test: {e}")
        return False

def test_group_chat(stock_symbol):
    """Test the MultiAssistant functionality with multiple agents."""
    logger.info("Testing GroupChat...")
    
    try:
        # Setup LLM config using autogen's config_list_from_json
        llm_config = {
            "config_list": autogen.config_list_from_json(
                "FinRobot/OAI_CONFIG_LIST",
                filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
            ),
            "timeout": 120,
            "temperature": 0,
        }
        
        # Define agent configurations
        market_analyst_config = {
            "name": "Market_Analyst",
            "profile": "You are a market analyst who specializes in analyzing market trends and providing insights.",
            "description": "Market analyst who specializes in analyzing market trends and providing insights."
        }
        
        financial_advisor_config = {
            "name": "Financial_Advisor",
            "profile": "You are a financial advisor who specializes in providing investment recommendations.",
            "description": "Financial advisor who specializes in providing investment recommendations."
        }
        
        # Define group configuration
        group_config = {
            "name": "Financial_Team",
            "agents": [market_analyst_config, financial_advisor_config]
        }
        
        # Create a multi-agent chat
        group_chat = MultiAssistant(
            group_config,
            llm_config=llm_config,
            human_input_mode="NEVER"
        )
        
        # Get current date and date ranges for analysis
        current_date = datetime.now().strftime("%Y-%m-%d")
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Test a query that requires collaboration
        query = f"""
        IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
        - Current date: {current_date}
        - Start date for historical data: {one_month_ago}
        - End date for historical data: {current_date}
        
        Analyze the current market conditions for {stock_symbol} and provide investment recommendations.
        Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
        """
        
        response = group_chat.chat(query)
        
        logger.info(f"GroupChat response: {response}")
        logger.info("GroupChat test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error in GroupChat test: {e}")
        return False

def test_stock_analysis(stock_symbol):
    """Test stock analysis functionality."""
    logger.info("Testing stock analysis...")
    
    try:
        # Setup LLM config using autogen's config_list_from_json
        llm_config = {
            "config_list": autogen.config_list_from_json(
                "FinRobot/OAI_CONFIG_LIST",
                filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
            ),
            "timeout": 120,
            "temperature": 0,
        }
        
        # Initialize a market analyst assistant
        market_analyst = SingleAssistant(
            "Market_Analyst",
            llm_config,
            human_input_mode="NEVER"
        )
        
        # Get current date and date ranges for analysis
        current_date = datetime.now().strftime("%Y-%m-%d")
        one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
        
        # Test stock analysis query
        query = f"""
        IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
        - Current date: {current_date}
        - Start date for historical data: {one_month_ago}
        - End date for historical data: {current_date}
        
        Use all the tools provided to retrieve information available for {stock_symbol}.
        Analyze the positive developments and potential concerns of {stock_symbol} with 2-4 most important factors
        respectively and keep them concise. Most factors should be inferred from company related news.
        Then make a rough prediction (e.g. up/down by 2-3%) of the {stock_symbol} stock price movement for next week.
        Provide a summary analysis to support your prediction.
        
        Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
        """
        
        response = market_analyst.chat(query)
        
        logger.info(f"Stock analysis response: {response}")
        logger.info("Stock analysis test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error in stock analysis test: {e}")
        return False

def main():
    """Main function to run all tests."""
    logger.info("Starting FinRobot basic agents tests...")
    
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
        ("SingleAssistant", lambda: test_single_assistant()),
        ("GroupChat", lambda: test_group_chat(stock_symbol)),
        ("Stock Analysis", lambda: test_stock_analysis(stock_symbol))
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

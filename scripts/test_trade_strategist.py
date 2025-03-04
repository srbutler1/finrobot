#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for the Trade Strategist agent in FinRobot.
This script tests the functionality of the Trade Strategist agent.
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
    from finrobot.agents.trade_strategist import TradeStrategist
    
    logger.info("Successfully imported FinRobot modules")
except ImportError as e:
    logger.error(f"Import error: {e}")
    logger.info("Trying alternative import path...")
    
    # Try with explicit FinRobot path
    finrobot_dir = os.path.join(current_dir, "FinRobot")
    sys.path.insert(0, finrobot_dir)
    
    try:
        from finrobot.utils import register_keys_from_json, get_current_date
        from finrobot.agents.trade_strategist import TradeStrategist
        
        logger.info("Successfully imported FinRobot modules using alternative path")
    except ImportError as e2:
        logger.error(f"Failed to import modules: {e2}")
        sys.exit(1)

def get_user_input():
    """Get user input for stock symbol and other parameters"""
    stock_symbol = input("Enter stock symbol (e.g., AAPL): ").strip() or "AAPL"
    
    current_date = input("Enter current date (YYYY-MM-DD) or leave blank for today: ").strip()
    if not current_date:
        current_date = get_current_date()
        logger.info(f"Using current date: {current_date}")
    
    time_period = input("Enter time period for analysis in days (default: 30): ").strip() or "30"
    time_period = int(time_period)
    
    return stock_symbol, current_date, time_period

def test_basic_strategy(trade_strategist, stock_symbol, current_date, time_period):
    """Test basic trading strategy generation"""
    logger.info("Testing basic trading strategy generation...")
    
    # Calculate start date based on time period
    start_date = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=time_period)).strftime("%Y-%m-%d")
    
    # Create a query for basic trading strategy
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {start_date}
    - End date for historical data: {current_date}
    
    Develop a basic trading strategy for {stock_symbol} based on recent market trends and technical indicators.
    Focus on SMA, EMA, and RSI indicators.
    
    IMPORTANT INSTRUCTIONS:
    1. DO NOT try to execute code directly. Instead, ASK the User_Proxy to execute functions for you.
    2. First, ask User_Proxy to fetch stock data: "Could you please fetch the stock data using get_stock_data('{stock_symbol}', '{start_date}', '{current_date}')"
    3. Then, ask User_Proxy to calculate indicators: "Could you please calculate the technical indicators using calculate_technical_indicators(stock_data)"
    4. Include the ACTUAL VALUES of indicators in your analysis (e.g., "Current RSI is 65.3")
    5. Cite specific price levels and dates in your analysis
    6. Make specific recommendations based on the actual data values
    
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    
    IMPORTANT: After providing your analysis, end with the phrase "ANALYSIS COMPLETE" to signal completion.
    """
    
    try:
        # Get response from the agent
        response = trade_strategist.chat(query)
        logger.info(f"Basic strategy response: {response[:100]}...")
        
        # Save the response to a file
        filename = f"{stock_symbol}_basic_strategy_{current_date.replace('-', '')}.txt"
        with open(filename, "w") as f:
            f.write(response)
        logger.info(f"Response saved to {filename}")
        
        return response
    except Exception as e:
        logger.error(f"Error in basic strategy test: {e}")
        return f"Error: {str(e)}"

def test_advanced_strategy(trade_strategist, stock_symbol, current_date, time_period):
    """Test advanced trading strategy generation"""
    logger.info("Testing advanced trading strategy generation...")
    
    # Calculate start date based on time period
    start_date = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=time_period)).strftime("%Y-%m-%d")
    
    # Create a query for advanced trading strategy
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {start_date}
    - End date for historical data: {current_date}
    
    Develop an advanced trading strategy for {stock_symbol} based on technical analysis and market trends.
    Include analysis of MACD, RSI, Bollinger Bands, and moving averages.
    
    IMPORTANT INSTRUCTIONS:
    1. DO NOT try to execute code directly. Instead, ASK the User_Proxy to execute functions for you.
    2. First, ask User_Proxy to fetch stock data: "Could you please fetch the stock data using get_stock_data('{stock_symbol}', '{start_date}', '{current_date}')"
    3. Then, ask User_Proxy to calculate indicators: "Could you please calculate the technical indicators using calculate_technical_indicators(stock_data)"
    4. Include the ACTUAL VALUES of indicators in your analysis (e.g., "Current MACD is -0.42")
    5. Cite specific price levels and performance metrics in your comparison
    6. Make specific recommendations based on the actual data values
    7. Include the most recent closing price and volume in your analysis
    
    Provide a comprehensive strategy with entry/exit points, stop-loss levels, and risk management considerations.
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    
    IMPORTANT: After providing your analysis, end with the phrase "ANALYSIS COMPLETE" to signal completion.
    """
    
    try:
        # Get response from the agent
        response = trade_strategist.chat(query)
        logger.info(f"Advanced strategy response: {response[:100]}...")
        
        # Save the response to a file
        filename = f"{stock_symbol}_advanced_strategy_{current_date.replace('-', '')}.txt"
        with open(filename, "w") as f:
            f.write(response)
        logger.info(f"Response saved to {filename}")
        
        return response
    except Exception as e:
        logger.error(f"Error in advanced strategy test: {e}")
        return f"Error: {str(e)}"

def test_comparative_analysis(trade_strategist, stock_symbol, current_date, time_period):
    """Test comparative trading strategy analysis"""
    logger.info("Testing comparative trading strategy analysis...")
    
    # Calculate start date based on time period
    start_date = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=time_period)).strftime("%Y-%m-%d")
    
    # Choose a competitor based on the stock symbol
    competitors = {
        "AAPL": "MSFT",
        "MSFT": "AAPL",
        "GOOGL": "META",
        "META": "GOOGL",
        "AMZN": "WMT",
        "TSLA": "F",
        "NVDA": "AMD",
        "AMD": "NVDA",
        "INTC": "AMD",
        "TSM": "INTC"
    }
    competitor = competitors.get(stock_symbol, "AAPL")
    
    # Create a query for comparative trading strategy analysis
    query = f"""
    IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {start_date}
    - End date for historical data: {current_date}
    
    Compare trading strategies for {stock_symbol} and {competitor} based on their recent performance and technical indicators.
    
    IMPORTANT INSTRUCTIONS:
    1. DO NOT try to execute code directly. Instead, ASK the User_Proxy to execute functions for you.
    2. First, ask User_Proxy to fetch stock data for both companies:
       - "Could you please fetch the stock data using get_stock_data('{stock_symbol}', '{start_date}', '{current_date}')"
       - "Could you please fetch the stock data using get_stock_data('{competitor}', '{start_date}', '{current_date}')"
    3. Then, ask User_Proxy to calculate indicators for both companies
    4. Compare the performance and technical indicators of both stocks
    5. Recommend which stock has better trading potential in the short and long term
    
    Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
    
    IMPORTANT: After providing your analysis, end with the phrase "ANALYSIS COMPLETE" to signal completion.
    """
    
    try:
        # Get response from the agent
        response = trade_strategist.chat(query)
        logger.info(f"Comparative analysis response: {response[:100]}...")
        
        # Save the response to a file
        filename = f"{stock_symbol}_vs_{competitor}_analysis_{current_date.replace('-', '')}.txt"
        with open(filename, "w") as f:
            f.write(response)
        logger.info(f"Response saved to {filename}")
        
        return response
    except Exception as e:
        logger.error(f"Error in comparative analysis test: {e}")
        return f"Error: {str(e)}"

def main():
    """Main function to run the Trade Strategist tests"""
    parser = argparse.ArgumentParser(description="Test the Trade Strategist agent in FinRobot")
    parser.add_argument("--test", choices=["basic", "advanced", "comparative", "all"], default="all", 
                      help="Test to run (basic, advanced, comparative, or all)")
    args = parser.parse_args()
    
    logger.info("Starting FinRobot Trade Strategist test...")
    
    # Register API keys - use correct path to config file
    config_path = os.path.join(os.path.join(current_dir, "FinRobot"), "config_api_keys")
    register_keys_from_json(config_path)
    logger.info(f"API keys registered successfully from {config_path}")
    
    # Get user input
    stock_symbol, current_date, time_period = get_user_input()
    
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
    
    # Initialize Trade Strategist with custom message handler
    trade_strategist = TradeStrategist(
        "Trade_Strategist",
        llm_config,
        human_input_mode="NEVER"  # Use NEVER mode to prevent auto-reply loops
    )
    
    # Create a custom message handler for the User_Proxy
    def custom_message_handler(recipient, messages, sender, config):
        """Custom message handler to process function execution requests"""
        if not messages:
            return False
        
        message = messages[-1]
        content = message.get("content", "")
        
        # Check if the message is asking to execute a function
        if "get_stock_data" in content or "calculate_technical_indicators" in content or "get_company_profile" in content:
            logger.info(f"Detected function execution request: {content[:100]}...")
            
            # Extract function name and parameters
            if "get_stock_data" in content:
                try:
                    # Execute the function
                    import re
                    match = re.search(r"get_stock_data\('([^']+)', '([^']+)', '([^']+)'\)", content)
                    if match:
                        symbol, start_date, end_date = match.groups()
                        from finrobot.data_source.yfinance_utils import YFinanceUtils
                        stock_data = YFinanceUtils.get_stock_data(symbol, start_date, end_date)
                        
                        # Send the response back to the assistant
                        response = f"Here's the stock data for {symbol} from {start_date} to {end_date}:\n{stock_data.head().to_string()}\n...\n{stock_data.tail().to_string()}"
                        recipient.receive(response, sender)
                        return True
                except Exception as e:
                    recipient.receive(f"Error executing get_stock_data: {str(e)}", sender)
                    return True
            
            if "calculate_technical_indicators" in content:
                try:
                    # Execute the function
                    from finrobot.data_source.yfinance_utils import YFinanceUtils
                    symbol = trade_strategist.last_symbol if hasattr(trade_strategist, 'last_symbol') else "MSFT"
                    start_date = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=time_period)).strftime("%Y-%m-%d")
                    stock_data = YFinanceUtils.get_stock_data(symbol, start_date, current_date)
                    
                    # Calculate indicators
                    indicators = trade_strategist._calculate_technical_indicators(stock_data)
                    
                    # Send the response back to the assistant
                    response = f"Here are the technical indicators for {symbol}:\n{indicators.head().to_string()}\n...\n{indicators.tail().to_string()}"
                    recipient.receive(response, sender)
                    return True
                except Exception as e:
                    recipient.receive(f"Error executing calculate_technical_indicators: {str(e)}", sender)
                    return True
            
            if "get_company_profile" in content:
                try:
                    # Execute the function
                    import re
                    match = re.search(r"get_company_profile\('([^']+)'\)", content)
                    if match:
                        symbol = match.groups()[0]
                        from finrobot.data_source.finnhub_utils import FinnHubUtils
                        profile = FinnHubUtils.get_company_profile(symbol)
                        
                        # Send the response back to the assistant
                        response = f"Here's the company profile for {symbol}:\n{profile}"
                        recipient.receive(response, sender)
                        return True
                except Exception as e:
                    recipient.receive(f"Error executing get_company_profile: {str(e)}", sender)
                    return True
        
        return False
    
    # Set the custom message handler for the User_Proxy
    trade_strategist.user_proxy.human_input_mode = "NEVER"
    trade_strategist.user_proxy.register_reply([custom_message_handler])
    
    # Run the selected test(s)
    results = {}
    
    if args.test in ["basic", "all"]:
        results["basic"] = test_basic_strategy(trade_strategist, stock_symbol, current_date, time_period)
        if results["basic"] and "ANALYSIS COMPLETE" in results["basic"]:
            logger.info("BASIC TEST: PASSED")
        else:
            logger.info("BASIC TEST: FAILED")
    
    if args.test in ["advanced", "all"]:
        results["advanced"] = test_advanced_strategy(trade_strategist, stock_symbol, current_date, time_period)
        if results["advanced"] and "ANALYSIS COMPLETE" in results["advanced"]:
            logger.info("ADVANCED TEST: PASSED")
        else:
            logger.info("ADVANCED TEST: FAILED")
    
    if args.test in ["comparative", "all"]:
        results["comparative"] = test_comparative_analysis(trade_strategist, stock_symbol, current_date, time_period)
        if results["comparative"] and "ANALYSIS COMPLETE" in results["comparative"]:
            logger.info("COMPARATIVE TEST: PASSED")
        else:
            logger.info("COMPARATIVE TEST: FAILED")
    
    # Print test results summary
    logger.info("\n===== TEST RESULTS SUMMARY =====")
    if "basic" in results:
        logger.info(f"BASIC TEST: {'PASSED' if results['basic'] and 'ANALYSIS COMPLETE' in results['basic'] else 'FAILED'}")
    if "advanced" in results:
        logger.info(f"ADVANCED TEST: {'PASSED' if results['advanced'] and 'ANALYSIS COMPLETE' in results['advanced'] else 'FAILED'}")
    if "comparative" in results:
        logger.info(f"COMPARATIVE TEST: {'PASSED' if results['comparative'] and 'ANALYSIS COMPLETE' in results['comparative'] else 'FAILED'}")
    
    logger.info("Trade Strategist tests completed successfully")

if __name__ == "__main__":
    main()

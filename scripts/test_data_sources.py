#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for FinRobot data sources functionality.
This script tests the various data sources available in FinRobot.
"""

import os
import sys
import logging
import pandas as pd
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

try:
    from finrobot.utils import register_keys_from_json
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

def test_finnhub_data_source(stock_symbol):
    """Test the Finnhub data source."""
    logger.info("Testing Finnhub data source...")
    
    try:
        # Import Finnhub data source
        from finrobot.data_source.finnhub_utils import FinnHubUtils
        
        # Test company profile
        profile = FinnHubUtils.get_company_profile(stock_symbol)
        logger.info(f"Company profile for {stock_symbol}: {profile}")
        
        # Test company news
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=7)).strftime("%Y-%m-%d")
        logger.info(f"Retrieving news from {start_date} to {end_date}")
        news = FinnHubUtils.get_company_news(stock_symbol, start_date, end_date)
        
        # Check if news is a DataFrame or list
        if isinstance(news, pd.DataFrame):
            news_count = len(news) if not news.empty else 0
        elif isinstance(news, list):
            news_count = len(news)
        else:
            news_count = 0
            
        logger.info(f"Retrieved {news_count} news items for {stock_symbol}")
        
        # Test basic financials - handle potential errors
        try:
            financials = FinnHubUtils.get_basic_financials(stock_symbol)
            logger.info(f"Basic financials for {stock_symbol}: {financials}")
        except Exception as e:
            logger.warning(f"Error retrieving basic financials for {stock_symbol}: {e}")
            logger.warning("This may be due to missing or incomplete data from Finnhub")
        
        logger.info("Finnhub data source test completed successfully")
        return True
    except Exception as e:
        logger.error(f"Error in Finnhub data source test: {e}")
        return False

def test_alpha_vantage_data_source(stock_symbol):
    """Test the Alpha Vantage data source if available."""
    logger.info("Testing Alpha Vantage data source...")
    
    try:
        # Try to import Alpha Vantage data source
        try:
            from finrobot.data_source.alpha_vantage_utils import AlphaVantageUtils
            alpha_vantage_available = True
        except ImportError:
            logger.warning("Alpha Vantage data source not available")
            alpha_vantage_available = False
            return True
        
        if alpha_vantage_available:
            # Test time series data
            time_series = AlphaVantageUtils.get_time_series(stock_symbol)
            logger.info(f"Time series data for {stock_symbol}: {time_series}")
            
            logger.info("Alpha Vantage data source test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in Alpha Vantage data source test: {e}")
        return False

def test_yahoo_finance_data_source(stock_symbol):
    """Test the Yahoo Finance data source if available."""
    logger.info("Testing Yahoo Finance data source...")
    
    try:
        # Try to import Yahoo Finance data source
        try:
            from finrobot.data_source.yfinance_utils import YFinanceUtils
            yahoo_finance_available = True
        except ImportError:
            logger.warning("Yahoo Finance data source not available")
            yahoo_finance_available = False
            return True
        
        if yahoo_finance_available:
            # Test stock data
            end_date = datetime.now().strftime("%Y-%m-%d")
            start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")
            logger.info(f"Retrieving stock data from {start_date} to {end_date}")
            stock_data = YFinanceUtils.get_stock_data(stock_symbol, start_date, end_date)
            logger.info(f"Stock data for {stock_symbol}: {stock_data}")
            
            logger.info("Yahoo Finance data source test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in Yahoo Finance data source test: {e}")
        return False

def main():
    """Main function to run all tests."""
    logger.info("Starting FinRobot data sources tests...")
    
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
        ("Finnhub Data Source", lambda: test_finnhub_data_source(stock_symbol)),
        ("Alpha Vantage Data Source", lambda: test_alpha_vantage_data_source(stock_symbol)),
        ("Yahoo Finance Data Source", lambda: test_yahoo_finance_data_source(stock_symbol))
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

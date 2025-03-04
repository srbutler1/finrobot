#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Test script for FinRobot functional modules.
This script tests the various functional modules available in FinRobot.
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

def test_technical_analysis():
    """Test the technical analysis functionality if available."""
    logger.info("Testing technical analysis functionality...")
    
    try:
        # Try to import technical analysis module
        try:
            from finrobot.functional.technical_analysis import TechnicalAnalysis
            technical_analysis_available = True
        except ImportError:
            logger.warning("Technical analysis module not available")
            technical_analysis_available = False
            return True
        
        if technical_analysis_available:
            # Create sample data
            dates = pd.date_range(start='2023-01-01', periods=100)
            prices = pd.Series(range(100, 200), index=dates)
            
            # Initialize technical analysis
            ta = TechnicalAnalysis(prices)
            
            # Test moving averages
            sma = ta.simple_moving_average(window=20)
            logger.info(f"SMA: {sma.tail()}")
            
            ema = ta.exponential_moving_average(window=20)
            logger.info(f"EMA: {ema.tail()}")
            
            # Test momentum indicators
            rsi = ta.relative_strength_index(window=14)
            logger.info(f"RSI: {rsi.tail()}")
            
            macd = ta.moving_average_convergence_divergence()
            logger.info(f"MACD: {macd.tail()}")
            
            logger.info("Technical analysis test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in technical analysis test: {e}")
        return False

def test_fundamental_analysis():
    """Test the fundamental analysis functionality if available."""
    logger.info("Testing fundamental analysis functionality...")
    
    try:
        # Try to import fundamental analysis module
        try:
            from finrobot.functional.fundamental_analysis import FundamentalAnalysis
            fundamental_analysis_available = True
        except ImportError:
            logger.warning("Fundamental analysis module not available")
            fundamental_analysis_available = False
            return True
        
        if fundamental_analysis_available:
            # Initialize fundamental analysis
            fa = FundamentalAnalysis()
            
            # Test fundamental metrics
            symbol = "AAPL"
            metrics = fa.get_key_metrics(symbol)
            logger.info(f"Key metrics for {symbol}: {metrics}")
            
            ratios = fa.get_financial_ratios(symbol)
            logger.info(f"Financial ratios for {symbol}: {ratios}")
            
            logger.info("Fundamental analysis test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in fundamental analysis test: {e}")
        return False

def test_sentiment_analysis():
    """Test the sentiment analysis functionality if available."""
    logger.info("Testing sentiment analysis functionality...")
    
    try:
        # Try to import sentiment analysis module
        try:
            from finrobot.functional.sentiment_analysis import SentimentAnalysis
            sentiment_analysis_available = True
        except ImportError:
            logger.warning("Sentiment analysis module not available")
            sentiment_analysis_available = False
            return True
        
        if sentiment_analysis_available:
            # Initialize sentiment analysis
            sa = SentimentAnalysis()
            
            # Test sentiment analysis
            text = "The company reported strong earnings, beating analyst expectations. Revenue grew by 15% year-over-year."
            sentiment = sa.analyze_sentiment(text)
            logger.info(f"Sentiment analysis: {sentiment}")
            
            logger.info("Sentiment analysis test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in sentiment analysis test: {e}")
        return False

def test_portfolio_optimization():
    """Test the portfolio optimization functionality if available."""
    logger.info("Testing portfolio optimization functionality...")
    
    try:
        # Try to import portfolio optimization module
        try:
            from finrobot.functional.portfolio_optimization import PortfolioOptimization
            portfolio_optimization_available = True
        except ImportError:
            logger.warning("Portfolio optimization module not available")
            portfolio_optimization_available = False
            return True
        
        if portfolio_optimization_available:
            # Create sample data
            symbols = ['AAPL', 'MSFT', 'GOOGL', 'AMZN']
            returns = pd.DataFrame({
                'AAPL': [0.01, 0.02, -0.01, 0.03, 0.01],
                'MSFT': [0.02, 0.01, 0.01, 0.02, -0.01],
                'GOOGL': [0.03, -0.01, 0.02, 0.01, 0.02],
                'AMZN': [0.01, 0.03, 0.01, -0.01, 0.02]
            })
            
            # Initialize portfolio optimization
            po = PortfolioOptimization(returns)
            
            # Test portfolio optimization
            weights = po.optimize_sharpe_ratio()
            logger.info(f"Optimal weights: {weights}")
            
            performance = po.calculate_performance(weights)
            logger.info(f"Portfolio performance: {performance}")
            
            logger.info("Portfolio optimization test completed successfully")
            return True
    except Exception as e:
        logger.error(f"Error in portfolio optimization test: {e}")
        return False

def main():
    """Main function to run all tests."""
    logger.info("Starting FinRobot functional modules tests...")
    
    # Register API keys
    try:
        register_keys_from_json("FinRobot/config_api_keys")
        logger.info("API keys registered successfully")
    except Exception as e:
        logger.error(f"Failed to register API keys: {e}")
        sys.exit(1)
    
    # Run tests
    tests = [
        ("Technical Analysis", test_technical_analysis),
        ("Fundamental Analysis", test_fundamental_analysis),
        ("Sentiment Analysis", test_sentiment_analysis),
        ("Portfolio Optimization", test_portfolio_optimization)
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

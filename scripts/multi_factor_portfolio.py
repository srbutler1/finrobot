import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# Import factor analysis modules
import value_factor_analysis as vfa
import momentum_factor_analysis as mfa
import quality_factor_analysis as qfa
import portfolio_optimization as po

def main():
    """Main function to run the multi-factor portfolio analysis"""
    print("=" * 80)
    print("MULTI-FACTOR PORTFOLIO ANALYSIS FOR DOW JONES 30")
    print("=" * 80)
    
    # Step 1: Download common data
    print("\nStep 1: Downloading Dow Jones 30 data...")
    data = vfa.download_dow_jones_data()
    print("Data download complete.")
    
    # Step 2: Run Value Factor Analysis
    print("\nStep 2: Running Value Factor Analysis...")
    value_df = vfa.calculate_value_factors(data)
    value_rankings = vfa.rank_value_stocks(value_df)
    print("Value Factor Analysis complete.")
    
    # Step 3: Run Momentum Factor Analysis
    print("\nStep 3: Running Momentum Factor Analysis...")
    momentum_df = mfa.calculate_momentum_factors(data)
    momentum_rankings = mfa.rank_momentum_stocks(momentum_df)
    print("Momentum Factor Analysis complete.")
    
    # Step 4: Run Quality Factor Analysis
    print("\nStep 4: Running Quality Factor Analysis...")
    quality_df = qfa.calculate_quality_factors()
    quality_rankings = qfa.rank_quality_stocks(quality_df)
    print("Quality Factor Analysis complete.")
    
    # Step 5: Optimize Portfolio
    print("\nStep 5: Running Portfolio Optimization...")
    
    # Load all factor rankings
    rankings = {
        'value': value_rankings,
        'momentum': momentum_rankings,
        'quality': quality_rankings
    }
    
    # Define factor weights (can be adjusted)
    factor_weights = {
        'value': 0.4,
        'momentum': 0.3,
        'quality': 0.3
    }
    
    # Download historical price data (1 year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Get unique tickers from all rankings
    all_tickers = set()
    for factor, df in rankings.items():
        all_tickers.update(df.index)
    
    print(f"Downloading price data for {len(all_tickers)} stocks...")
    price_data = po.download_price_data(list(all_tickers), start_date, end_date)
    
    # Create multi-factor portfolio
    portfolio = po.create_multi_factor_portfolio(
        rankings,
        price_data,
        weights=factor_weights,
        top_n=10,  # Top 10 stocks
        objective='sharpe'  # Maximize Sharpe ratio
    )
    
    # Print portfolio information
    print("\n" + "=" * 80)
    print("MULTI-FACTOR PORTFOLIO RESULTS")
    print("=" * 80)
    
    print(f"\nNumber of stocks: {len(portfolio['stocks'])}")
    print("\nPortfolio Composition:")
    for stock, weight in portfolio['weights'].items():
        print(f"{stock}: {weight*100:.2f}%")
    
    print("\nPortfolio Statistics:")
    print(f"Expected Annual Return: {portfolio['statistics']['return']*100:.2f}%")
    print(f"Expected Annual Volatility: {portfolio['statistics']['volatility']*100:.2f}%")
    print(f"Sharpe Ratio: {portfolio['statistics']['sharpe_ratio']:.2f}")
    
    # Save portfolio to CSV
    portfolio['weights'].to_csv('multi_factor_portfolio.csv')
    print("\nPortfolio weights saved to multi_factor_portfolio.csv")
    
    # Visualize portfolio
    po.visualize_portfolio(portfolio, price_data)
    
    print("\n" + "=" * 80)
    print("Multi-Factor Portfolio Analysis Complete!")
    print("=" * 80)

if __name__ == "__main__":
    main()

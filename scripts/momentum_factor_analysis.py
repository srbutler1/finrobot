import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta

# Function to download Dow Jones 30 data
def download_dow_jones_data():
    # Dow Jones 30 tickers
    dow_tickers = [
        'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
        'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
        'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT'
    ]
    
    # Get data for the last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Download data
    data = yf.download(dow_tickers, start=start_date, end=end_date)
    
    # Save to CSV
    data.to_csv('dow_jones_30_data.csv')
    print(f"Data saved to dow_jones_30_data.csv")
    
    return data

# Function to calculate momentum factors
def calculate_momentum_factors(data=None):
    if data is None:
        # Try to load from CSV, if not available, download
        try:
            data = pd.read_csv('dow_jones_30_data.csv', index_col=0)
            print("Data loaded from CSV file")
        except FileNotFoundError:
            print("CSV file not found, downloading data...")
            data = download_dow_jones_data()
    
    # Check data format and extract adjusted close prices
    if isinstance(data.columns, pd.MultiIndex):
        # MultiIndex format (e.g., from yf.download with multiple tickers)
        prices = data['Adj Close']
    else:
        # Single-level columns (e.g., from CSV)
        # Identify columns that contain 'Adj Close'
        adj_close_cols = [col for col in data.columns if 'Adj Close' in col]
        
        if adj_close_cols:
            # Extract ticker symbols from column names
            tickers = [col.split('_')[0] for col in adj_close_cols]
            # Create a new DataFrame with just the adjusted close prices
            prices = pd.DataFrame({ticker: data[f"{ticker}_Adj Close"] for ticker in tickers}, index=data.index)
        else:
            # If no 'Adj Close' columns, use all columns
            prices = data
    
    # Calculate momentum metrics
    momentum_metrics = {}
    
    # Calculate returns for different time periods
    returns_1m = prices.pct_change(periods=21).iloc[-1]  # ~1 month (21 trading days)
    returns_3m = prices.pct_change(periods=63).iloc[-1]  # ~3 months (63 trading days)
    returns_6m = prices.pct_change(periods=126).iloc[-1]  # ~6 months (126 trading days)
    returns_12m = prices.pct_change(periods=252).iloc[-1]  # ~12 months (252 trading days)
    
    # Calculate momentum metrics for each ticker
    for ticker in prices.columns:
        # Get price data for the ticker
        ticker_prices = prices[ticker].dropna()
        
        # Calculate momentum metrics
        momentum_metrics[ticker] = {
            '1-Month Return (%)': returns_1m[ticker] * 100,
            '3-Month Return (%)': returns_3m[ticker] * 100,
            '6-Month Return (%)': returns_6m[ticker] * 100,
            '12-Month Return (%)': returns_12m[ticker] * 100,
            'Current Price': ticker_prices.iloc[-1]
        }
        
        # Calculate 50-day and 200-day moving averages
        if len(ticker_prices) > 200:
            ma_50 = ticker_prices.rolling(window=50).mean().iloc[-1]
            ma_200 = ticker_prices.rolling(window=200).mean().iloc[-1]
            
            momentum_metrics[ticker]['50-Day MA'] = ma_50
            momentum_metrics[ticker]['200-Day MA'] = ma_200
            momentum_metrics[ticker]['Price/50-Day MA'] = ticker_prices.iloc[-1] / ma_50
            momentum_metrics[ticker]['Price/200-Day MA'] = ticker_prices.iloc[-1] / ma_200
            momentum_metrics[ticker]['50-Day MA/200-Day MA'] = ma_50 / ma_200  # Golden Cross indicator
        
        print(f"Processed momentum metrics for {ticker}")
    
    # Convert to DataFrame
    momentum_df = pd.DataFrame.from_dict(momentum_metrics, orient='index')
    
    # Save to CSV
    momentum_df.to_csv('dow_jones_momentum_metrics.csv')
    print(f"Momentum metrics saved to dow_jones_momentum_metrics.csv")
    
    return momentum_df

# Function to rank stocks based on momentum factors
def rank_momentum_stocks(momentum_df=None):
    if momentum_df is None:
        try:
            momentum_df = pd.read_csv('dow_jones_momentum_metrics.csv', index_col=0)
            print("Momentum metrics loaded from CSV file")
        except FileNotFoundError:
            print("Momentum metrics CSV file not found, calculating metrics...")
            momentum_df = calculate_momentum_factors()
    
    # Create a copy to avoid modifying the original
    df = momentum_df.copy()
    
    # For all return metrics, higher is better (ascending=False)
    rankings = {}
    
    # Rank returns (higher is better)
    rankings['1-Month Rank'] = df['1-Month Return (%)'].rank(ascending=False)
    rankings['3-Month Rank'] = df['3-Month Return (%)'].rank(ascending=False)
    rankings['6-Month Rank'] = df['6-Month Return (%)'].rank(ascending=False)
    rankings['12-Month Rank'] = df['12-Month Return (%)'].rank(ascending=False)
    
    # Rank moving average indicators (higher is better)
    if 'Price/50-Day MA' in df.columns:
        rankings['Price/50-Day MA Rank'] = df['Price/50-Day MA'].rank(ascending=False)
    
    if 'Price/200-Day MA' in df.columns:
        rankings['Price/200-Day MA Rank'] = df['Price/200-Day MA'].rank(ascending=False)
    
    if '50-Day MA/200-Day MA' in df.columns:
        rankings['50/200 MA Rank'] = df['50-Day MA/200-Day MA'].rank(ascending=False)
    
    # Combine rankings
    for rank_col, rank_series in rankings.items():
        df[rank_col] = rank_series
    
    # Calculate composite momentum score (average of all ranks)
    rank_columns = [col for col in df.columns if 'Rank' in col]
    df['Composite Momentum Rank'] = df[rank_columns].mean(axis=1)
    
    # Sort by composite rank
    df_sorted = df.sort_values('Composite Momentum Rank')
    
    # Save to CSV
    df_sorted.to_csv('dow_jones_momentum_rankings.csv')
    print(f"Momentum rankings saved to dow_jones_momentum_rankings.csv")
    
    return df_sorted

# Main execution
if __name__ == "__main__":
    print("Starting Momentum Factor Analysis for Dow Jones 30 stocks...")
    
    # Download data
    data = download_dow_jones_data()
    
    # Calculate momentum metrics
    momentum_df = calculate_momentum_factors(data)
    
    # Rank stocks
    ranked_stocks = rank_momentum_stocks(momentum_df)
    
    # Print top 5 momentum stocks
    print("\nTop 5 Momentum Stocks:")
    print(ranked_stocks.head(5)[['Current Price', '1-Month Return (%)', '6-Month Return (%)', '12-Month Return (%)', 'Composite Momentum Rank']])
    
    # Print bottom 5 momentum stocks
    print("\nBottom 5 Momentum Stocks:")
    print(ranked_stocks.tail(5)[['Current Price', '1-Month Return (%)', '6-Month Return (%)', '12-Month Return (%)', 'Composite Momentum Rank']])
    
    print("\nMomentum Factor Analysis Complete!")

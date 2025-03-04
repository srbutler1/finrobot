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

# Function to calculate value factors
def calculate_value_factors(data=None):
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
        latest_data = data['Adj Close'].iloc[-1]
    else:
        # Single-level columns (e.g., from CSV)
        # Identify columns that contain 'Adj Close'
        adj_close_cols = [col for col in data.columns if 'Adj Close' in col]
        
        if adj_close_cols:
            # Extract ticker symbols from column names
            tickers = [col.split('_')[0] for col in adj_close_cols]
            latest_data = pd.Series({ticker: data[f"{ticker}_Adj Close"].iloc[-1] for ticker in tickers})
        else:
            # If no 'Adj Close' columns, try to get the last row of all columns
            latest_data = data.iloc[-1]
    
    # Initialize a dictionary to store value metrics
    value_metrics = {}
    
    # Get fundamental data for each ticker
    for ticker in latest_data.index:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Calculate value metrics
            value_metrics[ticker] = {
                'Price': latest_data[ticker],
                'P/E Ratio': info.get('trailingPE', np.nan),
                'P/B Ratio': info.get('priceToBook', np.nan),
                'Dividend Yield': info.get('dividendYield', np.nan) * 100 if info.get('dividendYield') else np.nan,
                'EV/EBITDA': info.get('enterpriseToEbitda', np.nan),
                'Market Cap (B)': info.get('marketCap', np.nan) / 1e9
            }
            
            print(f"Processed {ticker}")
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
    
    # Convert to DataFrame
    value_df = pd.DataFrame.from_dict(value_metrics, orient='index')
    
    # Save to CSV
    value_df.to_csv('dow_jones_value_metrics.csv')
    print(f"Value metrics saved to dow_jones_value_metrics.csv")
    
    return value_df

# Function to rank stocks based on value factors
def rank_value_stocks(value_df=None):
    if value_df is None:
        try:
            value_df = pd.read_csv('dow_jones_value_metrics.csv', index_col=0)
            print("Value metrics loaded from CSV file")
        except FileNotFoundError:
            print("Value metrics CSV file not found, calculating metrics...")
            value_df = calculate_value_factors()
    
    # Create a copy to avoid modifying the original
    df = value_df.copy()
    
    # For P/E, P/B, and EV/EBITDA, lower is better (ascending=True)
    # For Dividend Yield, higher is better (ascending=False)
    rankings = {}
    
    # Rank P/E Ratio (lower is better)
    df_pe = df[df['P/E Ratio'] > 0]  # Filter out negative P/E
    rankings['P/E Rank'] = df_pe['P/E Ratio'].rank(ascending=True)
    
    # Rank P/B Ratio (lower is better)
    df_pb = df[df['P/B Ratio'] > 0]  # Filter out negative P/B
    rankings['P/B Rank'] = df_pb['P/B Ratio'].rank(ascending=True)
    
    # Rank Dividend Yield (higher is better)
    df_div = df[df['Dividend Yield'] > 0]  # Filter out zero dividend
    rankings['Dividend Rank'] = df_div['Dividend Yield'].rank(ascending=False)
    
    # Rank EV/EBITDA (lower is better)
    df_ev = df[df['EV/EBITDA'] > 0]  # Filter out negative EV/EBITDA
    rankings['EV/EBITDA Rank'] = df_ev['EV/EBITDA'].rank(ascending=True)
    
    # Combine rankings
    for rank_col, rank_series in rankings.items():
        df.loc[rank_series.index, rank_col] = rank_series
    
    # Calculate composite value score (average of all ranks)
    rank_columns = [col for col in df.columns if 'Rank' in col]
    df['Composite Value Rank'] = df[rank_columns].mean(axis=1)
    
    # Sort by composite rank
    df_sorted = df.sort_values('Composite Value Rank')
    
    # Save to CSV
    df_sorted.to_csv('dow_jones_value_rankings.csv')
    print(f"Value rankings saved to dow_jones_value_rankings.csv")
    
    return df_sorted

# Main execution
if __name__ == "__main__":
    print("Starting Value Factor Analysis for Dow Jones 30 stocks...")
    
    # Download data
    data = download_dow_jones_data()
    
    # Calculate value metrics
    value_df = calculate_value_factors(data)
    
    # Rank stocks
    ranked_stocks = rank_value_stocks(value_df)
    
    # Print top 5 value stocks
    print("\nTop 5 Value Stocks:")
    print(ranked_stocks.head(5)[['Price', 'P/E Ratio', 'P/B Ratio', 'Dividend Yield', 'Composite Value Rank']])
    
    # Print bottom 5 value stocks
    print("\nBottom 5 Value Stocks:")
    print(ranked_stocks.tail(5)[['Price', 'P/E Ratio', 'P/B Ratio', 'Dividend Yield', 'Composite Value Rank']])
    
    print("\nValue Factor Analysis Complete!")

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta

def download_dow_jones_data():
    """
    Download historical data for Dow Jones 30 stocks and save to CSV
    """
    # Dow Jones 30 tickers
    dow_tickers = [
        'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
        'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
        'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT'
    ]
    
    # Get data for the last 2 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)
    
    print(f"Downloading data for {len(dow_tickers)} stocks from {start_date.date()} to {end_date.date()}...")
    
    # Download data
    data = yf.download(dow_tickers, start=start_date, end=end_date)
    
    # Save to CSV
    data.to_csv('dow_jones_30_data.csv')
    print(f"Data saved to dow_jones_30_data.csv")
    
    return data

if __name__ == "__main__":
    print("Downloading Dow Jones 30 data...")
    download_dow_jones_data()
    print("Download complete!")

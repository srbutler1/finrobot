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

def calculate_growth_factors():
    """
    Calculate growth factors for Dow Jones 30 stocks
    """
    # Try to load data from CSV, if not available, download
    try:
        data = pd.read_csv('dow_jones_30_data.csv', index_col=0, header=[0, 1])
        print("Data loaded from CSV file")
    except FileNotFoundError:
        print("CSV file not found, downloading data...")
        data = download_dow_jones_data()
    
    # Dow Jones 30 tickers
    dow_tickers = [
        'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
        'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
        'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT'
    ]
    
    # Initialize a dictionary to store growth metrics
    growth_metrics = {}
    
    # Get fundamental data for each ticker
    for ticker in dow_tickers:
        try:
            print(f"Processing {ticker}...")
            stock = yf.Ticker(ticker)
            
            # Get financial data
            financials = stock.financials
            
            if financials.empty:
                print(f"No financial data available for {ticker}")
                continue
            
            # Calculate revenue growth
            if 'Total Revenue' in financials.index:
                revenues = financials.loc['Total Revenue']
                if len(revenues) >= 2:
                    revenue_growth_1yr = (revenues.iloc[0] / revenues.iloc[1]) - 1
                else:
                    revenue_growth_1yr = np.nan
            else:
                revenue_growth_1yr = np.nan
            
            # Calculate earnings growth
            if 'Net Income' in financials.index:
                earnings = financials.loc['Net Income']
                if len(earnings) >= 2:
                    earnings_growth_1yr = (earnings.iloc[0] / earnings.iloc[1]) - 1
                else:
                    earnings_growth_1yr = np.nan
            else:
                earnings_growth_1yr = np.nan
            
            # Get quarterly data for more recent growth
            quarterly = stock.quarterly_financials
            
            # Calculate quarterly revenue growth
            if not quarterly.empty and 'Total Revenue' in quarterly.index:
                q_revenues = quarterly.loc['Total Revenue']
                if len(q_revenues) >= 2:
                    revenue_growth_q = (q_revenues.iloc[0] / q_revenues.iloc[1]) - 1
                else:
                    revenue_growth_q = np.nan
            else:
                revenue_growth_q = np.nan
            
            # Calculate quarterly earnings growth
            if not quarterly.empty and 'Net Income' in quarterly.index:
                q_earnings = quarterly.loc['Net Income']
                if len(q_earnings) >= 2:
                    earnings_growth_q = (q_earnings.iloc[0] / q_earnings.iloc[1]) - 1
                else:
                    earnings_growth_q = np.nan
            else:
                earnings_growth_q = np.nan
            
            # Store metrics
            growth_metrics[ticker] = {
                'Revenue Growth (1Y)': revenue_growth_1yr,
                'Earnings Growth (1Y)': earnings_growth_1yr,
                'Revenue Growth (Q)': revenue_growth_q,
                'Earnings Growth (Q)': earnings_growth_q
            }
            
            print(f"Processed growth metrics for {ticker}")
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            growth_metrics[ticker] = {
                'Revenue Growth (1Y)': np.nan,
                'Earnings Growth (1Y)': np.nan,
                'Revenue Growth (Q)': np.nan,
                'Earnings Growth (Q)': np.nan
            }
    
    # Convert to DataFrame
    growth_df = pd.DataFrame.from_dict(growth_metrics, orient='index')
    
    # Save to CSV
    growth_df.to_csv('dow_jones_growth_metrics.csv')
    print(f"Growth metrics saved to dow_jones_growth_metrics.csv")
    
    return growth_df

def rank_growth_stocks(growth_df=None):
    """
    Rank stocks based on growth factors
    """
    if growth_df is None:
        try:
            growth_df = pd.read_csv('dow_jones_growth_metrics.csv', index_col=0)
            print("Growth metrics loaded from CSV file")
        except FileNotFoundError:
            print("Growth metrics CSV file not found, calculating metrics...")
            growth_df = calculate_growth_factors()
    
    # Create a copy to avoid modifying the original
    df = growth_df.copy()
    
    # For all growth metrics, higher is better (ascending=False)
    rankings = {}
    
    # Rank Revenue Growth (1Y)
    df_rev_1y = df[df['Revenue Growth (1Y)'] > 0]  # Filter out negative growth
    rankings['Revenue Growth (1Y) Rank'] = df_rev_1y['Revenue Growth (1Y)'].rank(ascending=False)
    
    # Rank Earnings Growth (1Y)
    df_earn_1y = df[df['Earnings Growth (1Y)'] > 0]  # Filter out negative growth
    rankings['Earnings Growth (1Y) Rank'] = df_earn_1y['Earnings Growth (1Y)'].rank(ascending=False)
    
    # Rank Revenue Growth (Q)
    df_rev_q = df[df['Revenue Growth (Q)'] > 0]  # Filter out negative growth
    rankings['Revenue Growth (Q) Rank'] = df_rev_q['Revenue Growth (Q)'].rank(ascending=False)
    
    # Rank Earnings Growth (Q)
    df_earn_q = df[df['Earnings Growth (Q)'] > 0]  # Filter out negative growth
    rankings['Earnings Growth (Q) Rank'] = df_earn_q['Earnings Growth (Q)'].rank(ascending=False)
    
    # Combine rankings
    for rank_col, rank_series in rankings.items():
        df.loc[rank_series.index, rank_col] = rank_series
    
    # Calculate composite growth score (average of all ranks)
    rank_columns = [col for col in df.columns if 'Rank' in col]
    df['Composite Growth Rank'] = df[rank_columns].mean(axis=1)
    
    # Sort by composite rank
    df_sorted = df.sort_values('Composite Growth Rank')
    
    # Save to CSV
    df_sorted.to_csv('dow_jones_growth_rankings.csv')
    print(f"Growth rankings saved to dow_jones_growth_rankings.csv")
    
    return df_sorted

if __name__ == "__main__":
    print("Starting Growth Factor Analysis for Dow Jones 30 stocks...")
    
    # Download data if needed
    try:
        data = pd.read_csv('dow_jones_30_data.csv')
        print("Data loaded from CSV file")
    except FileNotFoundError:
        print("CSV file not found, downloading data...")
        download_dow_jones_data()
    
    # Calculate growth metrics
    growth_df = calculate_growth_factors()
    
    # Rank stocks
    ranked_stocks = rank_growth_stocks(growth_df)
    
    # Print top 5 growth stocks
    print("\nTop 5 Growth Stocks:")
    print(ranked_stocks.head(5)[['Revenue Growth (1Y)', 'Earnings Growth (1Y)', 'Composite Growth Rank']])
    
    # Print bottom 5 growth stocks
    print("\nBottom 5 Growth Stocks:")
    print(ranked_stocks.tail(5)[['Revenue Growth (1Y)', 'Earnings Growth (1Y)', 'Composite Growth Rank']])
    
    print("\nGrowth Factor Analysis Complete!")

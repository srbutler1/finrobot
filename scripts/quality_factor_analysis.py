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

# Function to calculate quality factors
def calculate_quality_factors():
    # Dow Jones 30 tickers
    dow_tickers = [
        'AAPL', 'AMGN', 'AXP', 'BA', 'CAT', 'CRM', 'CSCO', 'CVX', 'DIS', 'DOW',
        'GS', 'HD', 'HON', 'IBM', 'INTC', 'JNJ', 'JPM', 'KO', 'MCD', 'MMM',
        'MRK', 'MSFT', 'NKE', 'PG', 'TRV', 'UNH', 'V', 'VZ', 'WBA', 'WMT'
    ]
    
    # Initialize a dictionary to store quality metrics
    quality_metrics = {}
    
    # Get fundamental data for each ticker
    for ticker in dow_tickers:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Get financial data
            try:
                balance_sheet = stock.balance_sheet
                income_stmt = stock.income_stmt
                cash_flow = stock.cashflow
                
                # Calculate quality metrics if financial data is available
                if not balance_sheet.empty and not income_stmt.empty and not cash_flow.empty:
                    # Get the most recent financial data
                    latest_bs = balance_sheet.iloc[:, 0]
                    latest_is = income_stmt.iloc[:, 0]
                    latest_cf = cash_flow.iloc[:, 0]
                    
                    # Calculate ROE (Return on Equity)
                    if 'Net Income' in latest_is and 'Total Stockholder Equity' in latest_bs:
                        roe = latest_is['Net Income'] / latest_bs['Total Stockholder Equity']
                    else:
                        roe = np.nan
                    
                    # Calculate ROA (Return on Assets)
                    if 'Net Income' in latest_is and 'Total Assets' in latest_bs:
                        roa = latest_is['Net Income'] / latest_bs['Total Assets']
                    else:
                        roa = np.nan
                    
                    # Calculate Debt-to-Equity ratio
                    if 'Total Debt' in latest_bs and 'Total Stockholder Equity' in latest_bs:
                        debt_to_equity = latest_bs['Total Debt'] / latest_bs['Total Stockholder Equity']
                    else:
                        debt_to_equity = np.nan
                    
                    # Calculate Operating Margin
                    if 'Operating Income' in latest_is and 'Total Revenue' in latest_is:
                        operating_margin = latest_is['Operating Income'] / latest_is['Total Revenue']
                    else:
                        operating_margin = np.nan
                    
                    # Calculate Free Cash Flow Yield
                    if 'Free Cash Flow' in latest_cf and 'marketCap' in info:
                        fcf_yield = latest_cf['Free Cash Flow'] / info['marketCap']
                    else:
                        fcf_yield = np.nan
                    
                    # Store metrics
                    quality_metrics[ticker] = {
                        'ROE': roe,
                        'ROA': roa,
                        'Debt-to-Equity': debt_to_equity,
                        'Operating Margin': operating_margin,
                        'FCF Yield': fcf_yield,
                        'Market Cap (B)': info.get('marketCap', np.nan) / 1e9
                    }
                else:
                    # Use alternative metrics from info if financial statements are not available
                    quality_metrics[ticker] = {
                        'ROE': info.get('returnOnEquity', np.nan),
                        'ROA': info.get('returnOnAssets', np.nan),
                        'Debt-to-Equity': info.get('debtToEquity', np.nan) / 100 if info.get('debtToEquity') else np.nan,
                        'Operating Margin': info.get('operatingMargins', np.nan),
                        'FCF Yield': np.nan,  # Not available in info
                        'Market Cap (B)': info.get('marketCap', np.nan) / 1e9
                    }
            except Exception as e:
                print(f"Error processing financial data for {ticker}: {e}")
                # Use alternative metrics from info
                quality_metrics[ticker] = {
                    'ROE': info.get('returnOnEquity', np.nan),
                    'ROA': info.get('returnOnAssets', np.nan),
                    'Debt-to-Equity': info.get('debtToEquity', np.nan) / 100 if info.get('debtToEquity') else np.nan,
                    'Operating Margin': info.get('operatingMargins', np.nan),
                    'FCF Yield': np.nan,  # Not available in info
                    'Market Cap (B)': info.get('marketCap', np.nan) / 1e9
                }
            
            print(f"Processed quality metrics for {ticker}")
        except Exception as e:
            print(f"Error processing {ticker}: {e}")
            quality_metrics[ticker] = {
                'ROE': np.nan,
                'ROA': np.nan,
                'Debt-to-Equity': np.nan,
                'Operating Margin': np.nan,
                'FCF Yield': np.nan,
                'Market Cap (B)': np.nan
            }
    
    # Convert to DataFrame
    quality_df = pd.DataFrame.from_dict(quality_metrics, orient='index')
    
    # Save to CSV
    quality_df.to_csv('dow_jones_quality_metrics.csv')
    print(f"Quality metrics saved to dow_jones_quality_metrics.csv")
    
    return quality_df

# Function to rank stocks based on quality factors
def rank_quality_stocks(quality_df=None):
    if quality_df is None:
        try:
            quality_df = pd.read_csv('dow_jones_quality_metrics.csv', index_col=0)
            print("Quality metrics loaded from CSV file")
        except FileNotFoundError:
            print("Quality metrics CSV file not found, calculating metrics...")
            quality_df = calculate_quality_factors()
    
    # Create a copy to avoid modifying the original
    df = quality_df.copy()
    
    # For ROE, ROA, Operating Margin, and FCF Yield, higher is better (ascending=False)
    # For Debt-to-Equity, lower is better (ascending=True)
    rankings = {}
    
    # Rank ROE (higher is better)
    df_roe = df[df['ROE'] > 0]  # Filter out negative ROE
    rankings['ROE Rank'] = df_roe['ROE'].rank(ascending=False)
    
    # Rank ROA (higher is better)
    df_roa = df[df['ROA'] > 0]  # Filter out negative ROA
    rankings['ROA Rank'] = df_roa['ROA'].rank(ascending=False)
    
    # Rank Debt-to-Equity (lower is better)
    df_de = df[df['Debt-to-Equity'] > 0]  # Filter out negative D/E
    rankings['D/E Rank'] = df_de['Debt-to-Equity'].rank(ascending=True)
    
    # Rank Operating Margin (higher is better)
    df_om = df[df['Operating Margin'] > 0]  # Filter out negative margins
    rankings['Operating Margin Rank'] = df_om['Operating Margin'].rank(ascending=False)
    
    # Rank FCF Yield (higher is better)
    df_fcf = df[df['FCF Yield'] > 0]  # Filter out negative FCF yield
    rankings['FCF Yield Rank'] = df_fcf['FCF Yield'].rank(ascending=False)
    
    # Combine rankings
    for rank_col, rank_series in rankings.items():
        df.loc[rank_series.index, rank_col] = rank_series
    
    # Calculate composite quality score (average of all ranks)
    rank_columns = [col for col in df.columns if 'Rank' in col]
    df['Composite Quality Rank'] = df[rank_columns].mean(axis=1)
    
    # Sort by composite rank
    df_sorted = df.sort_values('Composite Quality Rank')
    
    # Save to CSV
    df_sorted.to_csv('dow_jones_quality_rankings.csv')
    print(f"Quality rankings saved to dow_jones_quality_rankings.csv")
    
    return df_sorted

# Main execution
if __name__ == "__main__":
    print("Starting Quality Factor Analysis for Dow Jones 30 stocks...")
    
    # Calculate quality metrics
    quality_df = calculate_quality_factors()
    
    # Rank stocks
    ranked_stocks = rank_quality_stocks(quality_df)
    
    # Print top 5 quality stocks
    print("\nTop 5 Quality Stocks:")
    print(ranked_stocks.head(5)[['ROE', 'ROA', 'Debt-to-Equity', 'Operating Margin', 'Composite Quality Rank']])
    
    # Print bottom 5 quality stocks
    print("\nBottom 5 Quality Stocks:")
    print(ranked_stocks.tail(5)[['ROE', 'ROA', 'Debt-to-Equity', 'Operating Margin', 'Composite Quality Rank']])
    
    print("\nQuality Factor Analysis Complete!")

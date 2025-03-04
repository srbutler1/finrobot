import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime, timedelta
import scipy.optimize as sco

# Function to load factor rankings
def load_factor_rankings():
    """Load all factor rankings from CSV files"""
    rankings = {}
    
    # Try to load value rankings
    try:
        value_df = pd.read_csv('dow_jones_value_rankings.csv', index_col=0)
        rankings['value'] = value_df
        print("Value rankings loaded successfully")
    except FileNotFoundError:
        print("Value rankings file not found")
    
    # Try to load momentum rankings
    try:
        momentum_df = pd.read_csv('dow_jones_momentum_rankings.csv', index_col=0)
        rankings['momentum'] = momentum_df
        print("Momentum rankings loaded successfully")
    except FileNotFoundError:
        print("Momentum rankings file not found")
    
    # Add more factors as they become available
    # try:
    #     quality_df = pd.read_csv('dow_jones_quality_rankings.csv', index_col=0)
    #     rankings['quality'] = quality_df
    #     print("Quality rankings loaded successfully")
    # except FileNotFoundError:
    #     print("Quality rankings file not found")
    
    return rankings

# Function to combine factor rankings
def combine_factor_rankings(rankings, weights=None):
    """
    Combine multiple factor rankings into a single composite ranking
    
    Parameters:
    rankings (dict): Dictionary of factor rankings DataFrames
    weights (dict): Dictionary of weights for each factor (default: equal weights)
    
    Returns:
    DataFrame: Combined rankings
    """
    if not rankings:
        raise ValueError("No rankings provided")
    
    # Default to equal weights if not provided
    if weights is None:
        weights = {factor: 1/len(rankings) for factor in rankings}
    
    # Normalize weights to sum to 1
    total_weight = sum(weights.values())
    weights = {k: v/total_weight for k, v in weights.items()}
    
    # Get all tickers from all rankings
    all_tickers = set()
    for factor, df in rankings.items():
        all_tickers.update(df.index)
    
    # Initialize combined ranking DataFrame
    combined_df = pd.DataFrame(index=list(all_tickers))
    
    # Add composite ranks from each factor
    for factor, df in rankings.items():
        if factor == 'value' and 'Composite Value Rank' in df.columns:
            combined_df[f'{factor}_rank'] = df['Composite Value Rank']
        elif factor == 'momentum' and 'Composite Momentum Rank' in df.columns:
            combined_df[f'{factor}_rank'] = df['Composite Momentum Rank']
        # Add more factors as they become available
    
    # Fill NaN values with the median rank
    for col in combined_df.columns:
        median_rank = combined_df[col].median()
        combined_df[col].fillna(median_rank, inplace=True)
    
    # Calculate weighted composite rank
    combined_df['Weighted Composite Rank'] = 0
    for factor in rankings:
        combined_df['Weighted Composite Rank'] += combined_df[f'{factor}_rank'] * weights[factor]
    
    # Sort by weighted composite rank
    combined_df = combined_df.sort_values('Weighted Composite Rank')
    
    return combined_df

# Function to download historical price data
def download_price_data(tickers, start_date, end_date):
    """Download historical price data for a list of tickers"""
    data = yf.download(tickers, start=start_date, end=end_date)
    return data['Adj Close']

# Function to calculate portfolio statistics
def calculate_portfolio_statistics(returns, weights):
    """Calculate portfolio statistics (return, volatility, Sharpe ratio)"""
    # Expected portfolio return
    portfolio_return = np.sum(returns.mean() * weights) * 252  # Annualized
    
    # Expected portfolio volatility
    portfolio_volatility = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
    
    # Sharpe ratio (assuming risk-free rate of 0 for simplicity)
    sharpe_ratio = portfolio_return / portfolio_volatility
    
    return {
        'return': portfolio_return,
        'volatility': portfolio_volatility,
        'sharpe_ratio': sharpe_ratio
    }

# Function to optimize portfolio weights
def optimize_portfolio(returns, objective='sharpe', constraints=None):
    """
    Optimize portfolio weights based on the specified objective
    
    Parameters:
    returns (DataFrame): Historical returns
    objective (str): Optimization objective ('sharpe', 'min_volatility', 'max_return')
    constraints (dict): Additional constraints
    
    Returns:
    array: Optimal weights
    """
    n_assets = len(returns.columns)
    
    # Initial guess (equal weights)
    initial_weights = np.array([1/n_assets] * n_assets)
    
    # Constraints
    bounds = tuple((0, 1) for _ in range(n_assets))  # Weights between 0 and 1
    
    # Constraint: weights sum to 1
    constraints = [{'type': 'eq', 'fun': lambda x: np.sum(x) - 1}]
    
    # Objective function
    if objective == 'sharpe':
        # Maximize Sharpe ratio (negative because we're minimizing)
        def objective_function(weights):
            stats = calculate_portfolio_statistics(returns, weights)
            return -stats['sharpe_ratio']
    elif objective == 'min_volatility':
        # Minimize volatility
        def objective_function(weights):
            stats = calculate_portfolio_statistics(returns, weights)
            return stats['volatility']
    elif objective == 'max_return':
        # Maximize return (negative because we're minimizing)
        def objective_function(weights):
            stats = calculate_portfolio_statistics(returns, weights)
            return -stats['return']
    else:
        raise ValueError(f"Unknown objective: {objective}")
    
    # Optimize
    result = sco.minimize(
        objective_function,
        initial_weights,
        method='SLSQP',
        bounds=bounds,
        constraints=constraints
    )
    
    if not result['success']:
        raise ValueError(f"Optimization failed: {result['message']}")
    
    return result['x']

# Function to create and evaluate a multi-factor portfolio
def create_multi_factor_portfolio(rankings, price_data, weights=None, top_n=10, objective='sharpe'):
    """
    Create and evaluate a multi-factor portfolio
    
    Parameters:
    rankings (dict): Dictionary of factor rankings DataFrames
    price_data (DataFrame): Historical price data
    weights (dict): Dictionary of weights for each factor (default: equal weights)
    top_n (int): Number of top stocks to include in the portfolio
    objective (str): Portfolio optimization objective
    
    Returns:
    dict: Portfolio information
    """
    # Combine factor rankings
    combined_df = combine_factor_rankings(rankings, weights)
    
    # Select top N stocks
    top_stocks = combined_df.head(top_n).index.tolist()
    
    # Calculate daily returns
    returns = price_data[top_stocks].pct_change().dropna()
    
    # Optimize portfolio weights
    try:
        optimal_weights = optimize_portfolio(returns, objective)
        
        # Create portfolio with optimal weights
        portfolio = pd.Series(optimal_weights, index=top_stocks)
        
        # Calculate portfolio statistics
        stats = calculate_portfolio_statistics(returns, optimal_weights)
        
        return {
            'stocks': top_stocks,
            'weights': portfolio,
            'statistics': stats,
            'combined_rankings': combined_df
        }
    except Exception as e:
        print(f"Portfolio optimization failed: {e}")
        # Fallback to equal weights
        equal_weights = np.array([1/len(top_stocks)] * len(top_stocks))
        portfolio = pd.Series(equal_weights, index=top_stocks)
        stats = calculate_portfolio_statistics(returns, equal_weights)
        
        return {
            'stocks': top_stocks,
            'weights': portfolio,
            'statistics': stats,
            'combined_rankings': combined_df,
            'error': str(e)
        }

# Function to visualize portfolio
def visualize_portfolio(portfolio, price_data):
    """Create visualizations for the portfolio"""
    # Portfolio composition pie chart
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    portfolio['weights'].plot(kind='pie', autopct='%1.1f%%', title='Portfolio Composition')
    
    # Portfolio performance
    plt.subplot(1, 2, 2)
    
    # Calculate portfolio value over time
    portfolio_stocks = portfolio['stocks']
    portfolio_weights = portfolio['weights'].values
    
    # Normalize price data to start at 100
    normalized_prices = price_data[portfolio_stocks] / price_data[portfolio_stocks].iloc[0] * 100
    
    # Calculate portfolio value (weighted sum)
    portfolio_value = normalized_prices.dot(portfolio_weights)
    
    # Plot portfolio value
    portfolio_value.plot(title='Portfolio Performance', label='Multi-Factor Portfolio')
    
    # Plot benchmark (equal-weighted)
    benchmark = normalized_prices.mean(axis=1)
    benchmark.plot(label='Equal-Weighted Benchmark')
    
    plt.legend()
    plt.tight_layout()
    plt.savefig('portfolio_visualization.png')
    plt.close()
    
    print("Portfolio visualization saved to portfolio_visualization.png")

# Main execution
if __name__ == "__main__":
    print("Starting Multi-Factor Portfolio Optimization...")
    
    # Load factor rankings
    rankings = load_factor_rankings()
    
    if not rankings:
        print("No factor rankings found. Please run factor analysis scripts first.")
        exit(1)
    
    # Define factor weights (can be adjusted)
    factor_weights = {
        'value': 0.5,
        'momentum': 0.5,
        # Add more factors as they become available
    }
    
    # Download historical price data (1 year)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Get unique tickers from all rankings
    all_tickers = set()
    for factor, df in rankings.items():
        all_tickers.update(df.index)
    
    print(f"Downloading price data for {len(all_tickers)} stocks...")
    price_data = download_price_data(list(all_tickers), start_date, end_date)
    
    # Create multi-factor portfolio
    portfolio = create_multi_factor_portfolio(
        rankings,
        price_data,
        weights=factor_weights,
        top_n=10,  # Top 10 stocks
        objective='sharpe'  # Maximize Sharpe ratio
    )
    
    # Print portfolio information
    print("\n=== Multi-Factor Portfolio ===")
    print(f"Number of stocks: {len(portfolio['stocks'])}")
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
    visualize_portfolio(portfolio, price_data)
    
    print("\nMulti-Factor Portfolio Optimization Complete!")

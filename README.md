# FinRobot - Financial Analysis and Investment Recommendation System

## Attribution
This project is based on the original FinRobot project. All credit for the core functionality and architecture goes to the original authors. This is a personal fork with organizational improvements and additional features.

## Overview
FinRobot is an AI-powered financial analysis system that leverages large language models to analyze annual reports, SEC filings, and market data to provide investment recommendations.

## Features
- **Annual Report Analysis**: Extracts and analyzes key financial metrics and risks from company annual reports
- **SEC Filing Analysis**: Analyzes 10-K filings, focusing on Risk Factors (Section 1A) and Management's Discussion (Section 7)
- **Investment Recommendations**: Generates comprehensive investment recommendations based on fundamental and technical analysis
- **Multi-Agent Workflow**: Coordinates between specialized agents for a complete investment analysis pipeline

## Scripts

### Investment Workflow
`scripts/run_investment_workflow.py` - Runs a coordinated workflow that analyzes a company's annual report and provides investment recommendations based on that analysis.

### Annual Report Analyzer
`scripts/run_annual_report_analyzer.py` - Analyzes a company's annual report and SEC filings to extract key financial metrics, risks, and growth opportunities.

### Investment Recommendation
`scripts/run_investment_recommendation.py` - Generates investment recommendations based on annual report analysis.

### Trade Strategist
`scripts/run_trade_strategist.py` - Provides trading strategies and investment recommendations based on financial data.

## Setup

### Prerequisites
- Python 3.8+
- Required API keys:
  - OpenAI API key
  - SEC API key
  - Finnhub API key (optional)
  - Alpha Vantage API key (optional)

### Installation
1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up API keys:
   - Copy `config_template.json` to `FinRobot/config_api_keys`
   - Copy `OAI_CONFIG_LIST.template.json` to `FinRobot/OAI_CONFIG_LIST`
   - Add your API keys to these files
   - Alternatively, run `python scripts/setup_api_keys.py` for a guided setup

### Security Note
API key files are included in `.gitignore` to prevent accidental commits of sensitive information. Never commit your actual API keys to the repository.

## Usage
```bash
# Run the menu-based interface
./run.sh

# Or run individual scripts directly
python scripts/run_investment_workflow.py
```

## License
MIT License

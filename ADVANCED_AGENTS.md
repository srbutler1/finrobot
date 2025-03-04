# FinRobot Advanced Agents

This document provides an overview of the advanced agents implemented in the FinRobot system and instructions on how to use them.

## Overview

FinRobot now includes four advanced agents for financial analysis and forecasting:

1. **RAG Agent**: A Retrieval-Augmented Generation agent that provides comprehensive financial insights by retrieving and analyzing financial data from various sources.

2. **Trade Strategist**: An agent that develops trading strategies based on technical indicators, market trends, and fundamental data.

3. **Annual Report Analyzer**: An agent that analyzes company annual reports to extract key financial metrics, risks, and growth opportunities.

4. **FinGPT Forecaster**: An agent that predicts stock price movements based on historical data and market sentiment.

## Usage

### Testing Individual Agents

You can test each agent individually using the `test_single_agent.py` script:

```bash
# Test the RAG Agent
python test_single_agent.py rag

# Test the Trade Strategist
python test_single_agent.py trade

# Test the Annual Report Analyzer
python test_single_agent.py annual

# Test the FinGPT Forecaster
python test_single_agent.py fingpt
```

### Testing All Agents

You can test all advanced agents using the `test_advanced_agents.py` script:

```bash
python test_advanced_agents.py
```

### Using Agents in Your Code

Here's an example of how to use the advanced agents in your code:

```python
import autogen
from FinRobot.utils import register_keys_from_json, get_current_date
from FinRobot.finrobot.agents.rag_agent import RAGAgent
from FinRobot.finrobot.agents.trade_strategist import TradeStrategist
from FinRobot.finrobot.agents.annual_report_analyzer import AnnualReportAnalyzer
from FinRobot.finrobot.agents.fingpt_forecaster import FinGPTForecaster
from datetime import datetime, timedelta

# Register API keys
register_keys_from_json("config_api_keys")

# Setup LLM config
llm_config = {
    "config_list": autogen.config_list_from_json(
        "FinRobot/OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
    ),
    "timeout": 120,
    "temperature": 0,
}

# Initialize an agent (e.g., RAG Agent)
rag_agent = RAGAgent(
    "Financial_RAG_Agent",
    llm_config,
    human_input_mode="TERMINATE"
)

# Get current date and date ranges for analysis
current_date = get_current_date()
one_month_ago = (datetime.strptime(current_date, "%Y-%m-%d") - timedelta(days=30)).strftime("%Y-%m-%d")

# Create a query
query = f"""
IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
- Current date: {current_date}
- Start date for historical data: {one_month_ago}
- End date for historical data: {current_date}

What were the key financial metrics for AAPL in their latest earnings report?
Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
"""

# Get response from the agent
response = rag_agent.chat(query)
print(f"RAG Agent response: {response}")
```

## Agent Capabilities

### RAG Agent

- Retrieving company profiles and basic information
- Fetching recent news about companies
- Analyzing financial metrics and ratios
- Retrieving and analyzing stock price data

### Trade Strategist

- Analyzing technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands)
- Identifying trend patterns and potential reversal points
- Suggesting entry and exit points based on technical analysis
- Incorporating fundamental data into trading decisions
- Developing risk management strategies

### Annual Report Analyzer

- Analyzing key financial metrics and ratios
- Identifying trends in company performance
- Assessing risk factors and their potential impact
- Evaluating management's strategic initiatives
- Identifying growth opportunities and challenges

### FinGPT Forecaster

- Analyzing historical price trends and patterns
- Evaluating technical indicators for trading signals
- Assessing market sentiment from news and social media
- Combining technical and sentiment analysis for price forecasting
- Providing probability-based forecasts with confidence levels

## Configuration

All agents require API keys to be configured in the `config_api_keys` file. Make sure to set up your API keys before using the agents.

## Dependencies

The advanced agents rely on the following dependencies:

- autogen
- pandas
- numpy
- datetime
- logging

Make sure these dependencies are installed in your environment before using the agents.

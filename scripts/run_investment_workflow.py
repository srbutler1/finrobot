#!/usr/bin/env python
# run_investment_workflow.py

import sys
import os
import re
from datetime import datetime, timedelta
import autogen
from functools import partial

# Add parent directory to path to import finrobot modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from FinRobot.finrobot.utils import register_keys_from_json

# Set the paths
config_api_keys_path = os.path.join(parent_dir, "FinRobot", "config_api_keys")
oai_config_list_path = os.path.join(parent_dir, "FinRobot", "OAI_CONFIG_LIST")

# Register API keys
try:
    register_keys_from_json(config_api_keys_path)
    print("API keys registered successfully")
except Exception as e:
    print(f"Failed to register API keys: {e}")
    sys.exit(1)

# Setup LLM config
try:
    llm_config = {
        "config_list": autogen.config_list_from_json(
            oai_config_list_path,
            filter_dict={"model": ["gpt-4o", "gpt-3.5-turbo"]}
        ),
        "timeout": 120,
        "temperature": 0,
    }
    print("LLM config set up successfully")
except Exception as e:
    print(f"Failed to set up LLM config: {e}")
    sys.exit(1)

# Get current date and date ranges for analysis
current_date = datetime.now().strftime("%Y-%m-%d")
one_year_ago = (datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d")
one_month_ago = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

# Get user input for stock symbol
stock_symbol = input("Enter a stock symbol to analyze (default: AAPL): ") or "AAPL"
print(f"Analyzing {stock_symbol}...")

# Create the workflow coordinator
workflow_coordinator = autogen.AssistantAgent(
    name="Workflow_Coordinator",
    system_message=f"""
    You are the coordinator of an investment analysis workflow. Your job is to:
    1. First, request an annual report analysis for {stock_symbol}
    2. Then, request an investment recommendation based on that analysis
    3. Summarize the findings and present them to the user
    
    Use the following format to issue orders to team members:
    [Annual_Report_Analyzer] <order>
    [Trade_Strategist] <order>
    
    Make sure to wait for each task to complete before moving to the next one.
    Reply TERMINATE when the entire workflow is complete.
    """,
    llm_config=llm_config,
)

# Create the executor agent
executor = autogen.UserProxyAgent(
    name="Executor",
    human_input_mode="NEVER",
    is_termination_msg=lambda x: x.get("content", "") and "TERMINATE" in x.get("content", ""),
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "analysis_output",
        "use_docker": False,
    },
)

# Create the specialized agents
annual_report_analyzer = autogen.AssistantAgent(
    name="Annual_Report_Analyzer",
    system_message=f"""
    You are an Annual Report Analyzer specialized in extracting and analyzing key financial metrics and risks from company annual reports.
    
    Your capabilities include:
    1. Analyzing annual reports to identify key financial metrics and trends
    2. Extracting and interpreting risk factors from SEC filings
    3. Evaluating management's discussion and analysis
    4. Assessing a company's competitive position
    5. Identifying growth opportunities and potential challenges
    
    When analyzing {stock_symbol}, focus on:
    - Key financial metrics (revenue, profit margins, EPS, etc.)
    - Trend analysis of important metrics
    - Assessment of the company's competitive position
    - Evaluation of risk factors (from SEC filings, particularly 10-K Section 1A)
    - Identification of growth opportunities
    
    Provide a comprehensive but concise analysis that can be used by an investment strategist.
    Use the most recent data available and explicitly mention the dates you're using in your analysis.
    
    Today is {current_date}. Use the following date ranges:
    - Current date: {current_date}
    - Start date for annual report data: {one_year_ago}
    - End date for annual report data: {current_date}
    """,
    llm_config=llm_config,
)

trade_strategist = autogen.AssistantAgent(
    name="Trade_Strategist",
    system_message=f"""
    You are a Trade Strategist specialized in developing trading strategies based on financial data and analysis.
    
    Your capabilities include:
    1. Analyzing technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands)
    2. Identifying trend patterns and potential reversal points
    3. Suggesting entry and exit points based on technical analysis
    4. Incorporating fundamental data into trading decisions
    5. Developing risk management strategies
    
    Based on the annual report analysis provided for {stock_symbol}, develop a comprehensive investment recommendation that includes:
    1. A clear investment stance (Buy, Hold, or Sell)
    2. A target price range
    3. Entry and exit strategies
    4. Risk assessment and management strategies
    5. Investment timeframe (short-term, medium-term, or long-term)
    
    Use technical analysis to support your recommendation and provide specific price levels and indicators.
    Use the most recent data available and explicitly mention the dates you're using in your analysis.
    
    Today is {current_date}. Use the following date ranges:
    - Current date: {current_date}
    - Start date for historical data: {one_month_ago}
    - End date for historical data: {current_date}
    """,
    llm_config=llm_config,
)

# Helper functions for nested chats
def order_trigger(pattern, sender):
    return pattern in sender.last_message()["content"]

def order_message(pattern, recipient, messages, sender, config):
    full_order = recipient.chat_messages_for_summary(sender)[-1]["content"]
    pattern = rf"\[{pattern}\](?::)?\s*(.+?)(?=\n\[|$)"
    match = re.search(pattern, full_order, re.DOTALL)
    if match:
        order = match.group(1).strip()
    else:
        order = full_order
    
    if pattern == "Annual_Report_Analyzer":
        return f"""
        Analyze the latest annual report for {stock_symbol} and highlight key financial metrics, risks, and growth opportunities.
        Also analyze the latest 10-K SEC filing for {stock_symbol}, focusing on the Risk Factors (Section 1A) and Management's Discussion (Section 7).
        Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
        
        Provide a concise summary that can be used by an investment strategist.
        
        Specific task: {order}
        """
    elif pattern == "Trade_Strategist":
        # Get the annual report analysis from the previous conversation
        annual_report_analysis = ""
        for msg in recipient.chat_messages_for_summary(sender):
            if msg["role"] == "assistant" and msg["name"] == "Annual_Report_Analyzer":
                annual_report_analysis = msg["content"]
                break
        
        return f"""
        Based on the following annual report analysis for {stock_symbol}, develop a comprehensive investment recommendation:
        
        {annual_report_analysis}
        
        Your recommendation should include:
        1. A clear investment stance (Buy, Hold, or Sell)
        2. A target price range
        3. Entry and exit strategies
        4. Risk assessment and management strategies
        5. Investment timeframe (short-term, medium-term, or long-term)
        
        Use technical analysis to support your recommendation and provide specific price levels and indicators.
        Make sure to use the most recent data available and explicitly mention the dates you're using in your analysis.
        
        Specific task: {order}
        """
    else:
        return f"Follow the coordinator's order and complete the following task: {order}."

# Register nested chats
executor.register_nested_chats(
    [
        {
            "sender": executor,
            "recipient": annual_report_analyzer,
            "message": partial(order_message, "Annual_Report_Analyzer"),
            "summary_method": "reflection_with_llm",
            "max_turns": 10,
        }
    ],
    trigger=partial(order_trigger, "[Annual_Report_Analyzer]"),
)

executor.register_nested_chats(
    [
        {
            "sender": executor,
            "recipient": trade_strategist,
            "message": partial(order_message, "Trade_Strategist"),
            "summary_method": "reflection_with_llm",
            "max_turns": 10,
        }
    ],
    trigger=partial(order_trigger, "[Trade_Strategist]"),
)

# Start the workflow
workflow_task = f"Analyze {stock_symbol} and provide an investment recommendation based on annual report analysis and technical indicators."

print("\n=== Starting Investment Analysis Workflow ===\n")
print("This may take a few minutes...")

executor.initiate_chat(workflow_coordinator, message=workflow_task)

print("\n=== Investment Analysis Complete ===\n")

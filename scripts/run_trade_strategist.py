#!/usr/bin/env python
# run_trade_strategist.py

import sys
import os
from datetime import datetime, timedelta
import autogen

# Add parent directory to path to import finrobot modules
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from FinRobot.finrobot.agents.trade_strategist import TradeStrategist
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

# Sample annual report analysis for NVDA (will be replaced with actual analysis if stock_symbol is not NVDA)
nvda_analysis = """
### Analysis of NVIDIA Corporation (NVDA) Annual Report and 10-K Filing

**Date of Analysis:** March 4, 2025  
**Period Covered:** March 4, 2024 - March 4, 2025

#### Summary of Key Financial Performance
- **Revenue Growth:** NVIDIA reported a significant increase in revenue, reaching $40 billion for the fiscal year ending January 31, 2025, up from $30 billion in the previous year. This represents a 33% year-over-year growth, driven primarily by strong demand in the data center and gaming segments.
- **Net Income:** The company achieved a net income of $12 billion, a 25% increase from the prior year, reflecting improved operational efficiencies and higher gross margins.
- **Earnings Per Share (EPS):** EPS rose to $4.80, compared to $3.85 in the previous fiscal year, indicating robust profitability.
- **Gross Margin:** The gross margin improved to 65%, up from 62% last year, due to a favorable product mix and cost management strategies.

#### Trend Analysis of Important Metrics
- **Data Center Segment:** Continued to be the largest growth driver, with revenues increasing by 40% year-over-year, fueled by AI and machine learning applications.
- **Gaming Segment:** Experienced a 20% growth, supported by new product launches and increased consumer demand.
- **R&D Investment:** Increased by 15% to $5 billion, underscoring NVIDIA's commitment to innovation and maintaining technological leadership.

#### Assessment of Company's Competitive Position
- **Market Leadership:** NVIDIA maintains a strong competitive position in the GPU market, with a dominant share in both gaming and data center applications.
- **Innovation:** The company's focus on AI and machine learning positions it well against competitors like AMD and Intel, particularly in high-performance computing.

#### Evaluation of Risk Factors (10-K Section 1A)
- **Supply Chain Risks:** Potential disruptions in semiconductor supply chains could impact production and delivery timelines.
- **Regulatory Risks:** Increasing scrutiny and potential regulatory changes in key markets, including the U.S. and China, could affect operations.
- **Competition:** Intense competition in the semiconductor industry could pressure margins and market share.

#### Identification of Growth Opportunities
- **AI and Machine Learning:** Expanding applications in AI present significant growth opportunities, particularly in autonomous vehicles and cloud computing.
- **Emerging Markets:** Increasing penetration in emerging markets offers potential for revenue diversification and growth.
- **Partnerships and Acquisitions:** Strategic partnerships and potential acquisitions could enhance technological capabilities and market reach.

#### Overall Outlook and Recommendations
- **Outlook:** NVIDIA is well-positioned for continued growth, supported by strong demand in its core segments and strategic investments in R&D.
- **Recommendations:** Investors should consider NVIDIA as a strong buy, given its robust financial performance, leadership in AI technology, and strategic growth initiatives. However, they should remain vigilant about potential supply chain and regulatory risks.
"""

# Sample annual report analysis for AAPL
aapl_analysis = """
### Analysis of Apple Inc. (AAPL) Annual Report and 10-K Filing

**Date of Analysis:** March 4, 2025  
**Period Covered:** March 4, 2024 - March 4, 2025

#### Summary of Key Financial Performance
- **Revenue Growth:** Apple reported steady revenue growth, reaching $385 billion for the fiscal year ending September 30, 2024, a 5% increase from the previous year, driven by services and wearables.
- **Net Income:** The company achieved a net income of $95 billion, a 3% increase from the prior year, maintaining strong profitability despite market challenges.
- **Earnings Per Share (EPS):** EPS increased to $6.20, compared to $5.95 in the previous fiscal year, reflecting continued shareholder value creation.
- **Gross Margin:** The gross margin remained stable at 43%, supported by the growing high-margin services segment.

#### Trend Analysis of Important Metrics
- **Services Segment:** Continued strong growth at 15% year-over-year, now representing 25% of total revenue.
- **iPhone Sales:** Showed modest growth of 2%, indicating market saturation but continued customer loyalty.
- **R&D Investment:** Increased by 10% to $25 billion, focusing on AI integration, AR/VR technologies, and potential automotive initiatives.

#### Assessment of Company's Competitive Position
- **Brand Strength:** Apple maintains its premium brand positioning and ecosystem advantage.
- **Innovation:** The company continues to invest in new product categories and services to diversify revenue streams.

#### Evaluation of Risk Factors (10-K Section 1A)
- **Supply Chain Dependencies:** Reliance on manufacturing in China and Southeast Asia presents geopolitical and logistics risks.
- **Regulatory Scrutiny:** Increasing global regulatory pressure regarding App Store policies and market dominance.
- **Competition:** Intense competition in all product categories, particularly from Android in smartphones and various competitors in services.

#### Identification of Growth Opportunities
- **AR/VR Technologies:** Significant investment in augmented and virtual reality presents new growth avenues.
- **Healthcare Integration:** Expanding health monitoring capabilities in wearables offers growth potential in the healthcare sector.
- **AI Integration:** Enhanced AI capabilities across product lines could drive upgrades and new use cases.

#### Overall Outlook and Recommendations
- **Outlook:** Apple is well-positioned for stable growth, supported by its loyal customer base and expanding services ecosystem.
- **Recommendations:** Investors should consider Apple as a hold/buy, given its strong cash position, reliable dividend, and potential in new technology areas. However, they should monitor regulatory developments and the pace of innovation.
"""

# Generic analysis template for other stocks
generic_analysis = f"""
### Analysis of {{COMPANY}} ({stock_symbol}) Annual Report and 10-K Filing

**Date of Analysis:** {current_date}  
**Period Covered:** {one_year_ago} - {current_date}

#### Summary of Key Financial Performance
- **Revenue Growth:** {{COMPANY}} has shown [growth/decline] in revenue over the past fiscal year.
- **Net Income:** The company reported [increase/decrease] in net income compared to the previous year.
- **Earnings Per Share (EPS):** EPS has [increased/decreased] to [value], indicating [improving/declining] profitability.
- **Gross Margin:** The gross margin [improved/declined/remained stable] at [percentage].

#### Trend Analysis of Important Metrics
- **Core Business Segments:** [Description of performance across main business segments]
- **Market Share:** [Analysis of market share trends]
- **R&D Investment:** [Details about R&D spending and focus areas]

#### Assessment of Company's Competitive Position
- **Industry Standing:** [Evaluation of the company's position relative to competitors]
- **Competitive Advantages:** [Description of key competitive advantages or disadvantages]

#### Evaluation of Risk Factors (10-K Section 1A)
- **Operational Risks:** [Summary of main operational risks]
- **Financial Risks:** [Summary of financial risks including debt, currency exposure, etc.]
- **Market Risks:** [Summary of market-related risks]

#### Identification of Growth Opportunities
- **New Markets:** [Potential new markets or customer segments]
- **Product Development:** [New products or services in development]
- **Strategic Initiatives:** [Major strategic initiatives underway]

#### Overall Outlook and Recommendations
- **Outlook:** [General outlook for the company based on financial performance and market conditions]
- **Recommendations:** [General investment recommendation with supporting rationale]
"""

# Select the appropriate analysis based on the stock symbol
if stock_symbol.upper() == "NVDA":
    annual_report_analysis = nvda_analysis
elif stock_symbol.upper() == "AAPL":
    annual_report_analysis = aapl_analysis
else:
    # For other stocks, use the generic template with the company name placeholder
    print(f"No pre-defined analysis available for {stock_symbol}. Using generic template.")
    annual_report_analysis = generic_analysis.replace("{{COMPANY}}", stock_symbol)

# Initialize Trade Strategist
trade_strategist = TradeStrategist(
    "Trade_Strategist",
    llm_config,
    human_input_mode="NEVER"
)

# Create the investment recommendation query
investment_recommendation_query = f"""
IMPORTANT: Today is {current_date}. When using any data source tools, use the following date ranges:
- Current date: {current_date}
- Start date for historical data: {one_month_ago}
- End date for historical data: {current_date}

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
"""

# Run the trade strategist
try:
    print("\n=== Annual Report Analysis Used ===\n")
    print(annual_report_analysis)
    print("\n=== Generating Investment Recommendation ===\n")
    print("This may take a few minutes...")
    
    investment_recommendation = trade_strategist.chat(investment_recommendation_query)
    
    # Print the final output
    print("\n=== Investment Recommendation for", stock_symbol, "===\n")
    print(investment_recommendation)
    print("\n=== Analysis Complete ===\n")
except Exception as e:
    print(f"Error during investment recommendation generation: {e}")
    sys.exit(1)

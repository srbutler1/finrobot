import autogen
from finrobot.utils import get_current_date, register_keys_from_json
from finrobot.agents.workflow import SingleAssistant

# Read OpenAI API keys from a JSON file
llm_config = {
    "config_list": autogen.config_list_from_json(
        "FinRobot/OAI_CONFIG_LIST",
        filter_dict={"model": ["gpt-4o"]},
    ),
    "timeout": 120,
    "temperature": 0,
}

# Register FINNHUB API keys
register_keys_from_json("FinRobot/config_api_keys")

# Define the company to analyze
company = "AAPL"

# Create a market analyst assistant
assistant = SingleAssistant(
    "Market_Analyst",
    llm_config,
    # Set to "ALWAYS" if you want to chat instead of simply receiving the prediction
    human_input_mode="NEVER",
)

# Run the analysis
assistant.chat(
    f"Use all the tools provided to retrieve information available for {company} upon {get_current_date()}. "
    f"Analyze the positive developments and potential concerns of {company} "
    "with 2-4 most important factors respectively and keep them concise. "
    "Most factors should be inferred from company related news. "
    f"Then make a rough prediction (e.g. up/down by 2-3%) of the {company} stock price movement for next week. "
    "Provide a summary analysis to support your prediction."
)

# FinRobot - Financial Analysis and Investment Recommendation System

## Attribution
This project is based on the original FinRobot project. All credit for the core functionality and architecture goes to the original authors. This is a personal fork with organizational improvements and additional features.

### Original Papers

1. Zhou, T., Wang, P., Wu, Y., & Yang, H. (2024). FinRobot: AI Agent for Equity Research and Valuation with Large Language Models. *ICAIF 2024: The 1st Workshop on Large Language Models and Generative AI for Finance*.

2. Yang, H., Zhang, B., Wang, N., Guo, C., Zhang, X., Lin, L., Wang, J., Zhou, T., Guan, M., Zhang, R., et al. (2024). FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models. *arXiv preprint arXiv:2405.14767*.

3. Han, X., Wang, N., Che, S., Yang, H., Zhang, K., & Xu, S. X. (2024). Enhancing Investment Analysis: Optimizing AI-Agent Collaboration in Financial Research. *ICAIF 2024: Proceedings of the 5th ACM International Conference on AI in Finance*, 538-546.

### Academic Citations
```bibtex
@inproceedings{zhou2024finrobot,
  title={FinRobot: {AI} Agent for Equity Research and Valuation with Large Language Models},
  author={Tianyu Zhou and Pinqiao Wang and Yilin Wu and Hongyang Yang},
  booktitle={ICAIF 2024: The 1st Workshop on Large Language Models and Generative AI for Finance},
  year={2024}
}

@article{yang2024finrobot,
  title={FinRobot: An Open-Source AI Agent Platform for Financial Applications using Large Language Models},
  author={Yang, Hongyang and Zhang, Boyu and Wang, Neng and Guo, Cheng and Zhang, Xiaoli and Lin, Likun and Wang, Junlin and Zhou, Tianyu and Guan, Mao and Zhang, Runjia and others},
  journal={arXiv preprint arXiv:2405.14767},
  year={2024}
}

@inproceedings{han2024enhancing,
  title={Enhancing Investment Analysis: Optimizing AI-Agent Collaboration in Financial Research},
  author={Han, Xuewen and Wang, Neng and Che, Shangkun and Yang, Hongyang and Zhang, Kunpeng and Xu, Sean Xin},
  booktitle={ICAIF 2024: Proceedings of the 5th ACM International Conference on AI in Finance},
  pages={538--546},
  year={2024}
}
```

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

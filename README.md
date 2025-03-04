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

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Quick Setup (Recommended)

We provide a setup script that automates the entire installation process:

```bash
# Clone the repository
git clone https://github.com/srbutler1/finrobot.git
cd finrobot

# Run the setup script
./setup_environment.sh
```

This script will:
1. Create and activate a virtual environment
2. Install all dependencies
3. Clone the original FinRobot repository if needed
4. Guide you through API key setup

### Manual Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/srbutler1/finrobot.git
   cd finrobot
   ```

2. **Create and activate a virtual environment (recommended)**
   ```bash
   python -m venv finrobot_venv
   source finrobot_venv/bin/activate  # On Windows: finrobot_venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r scripts/requirements.txt
   pip install -e .
   ```

4. **Set up API keys**
   ```bash
   python scripts/setup_config.py
   ```
   You will be prompted to enter your API keys for:
   - OpenAI API
   - SEC API
   - Finnhub API
   - Alpha Vantage API

### Important Note on Dependencies

This repository contains scripts that depend on the original FinRobot package. To use these scripts, you need to:

1. **Clone the original FinRobot repository**
   ```bash
   git clone https://github.com/AI4Finance-Foundation/FinRobot.git
   ```

2. **Install the original FinRobot package**
   ```bash
   cd FinRobot
   pip install -e .
   cd ..
   ```

3. **Ensure both repositories are at the same directory level**
   The scripts expect the FinRobot directory to be in the same parent directory as this repository.

## Usage

You can run the scripts using the shell script or directly with Python:

### Using the shell script

```bash
./run.sh
```

This will present a menu with various options to run different components of the system.

### Running scripts directly

```bash
# Run investment recommendation
python scripts/run_investment_recommendation.py

# Run annual report analyzer
python scripts/run_annual_report_analyzer.py

# Run trade strategist
python scripts/run_trade_strategist.py

# Run investment workflow
python scripts/run_investment_workflow.py
```

## Security Note
API key files are included in `.gitignore` to prevent accidental commits of sensitive information. Never commit your actual API keys to the repository.

## License
MIT License

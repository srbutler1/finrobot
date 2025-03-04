#!/bin/bash

# Display menu
echo "===== FinRobot ====="
echo "1. Setup API Keys"
echo "2. Run Investment Workflow"
echo "3. Run Annual Report Analyzer"
echo "4. Run Trade Strategist"
echo "5. Run Basic Tests"
echo "6. Run All Tests"
echo "7. Exit"
echo "==================="

# Get user choice
read -p "Enter your choice (1-7): " choice

# Execute based on choice
case $choice in
    1)
        python scripts/setup_config.py
        ;;
    2)
        python scripts/run_investment_workflow.py
        ;;
    3)
        python scripts/run_annual_report_analyzer.py
        ;;
    4)
        python scripts/run_trade_strategist.py
        ;;
    5)
        echo "Running basic import tests..."
        python scripts/test_imports.py
        ;;
    6)
        echo "Running all tests..."
        python scripts/run_all_tests.py
        ;;
    7)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac

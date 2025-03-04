# FinRobot Test Suite

This directory contains a comprehensive test suite for the FinRobot platform. These tests are designed to verify the functionality of various components and ensure that the system is working as expected.

## Test Scripts Overview

1. **test_imports.py**
   - Tests the basic import functionality of FinRobot modules
   - Verifies that all required packages are installed correctly
   - Checks API key registration

2. **test_basic_agents.py**
   - Tests the core agent functionality
   - Includes tests for SingleAssistant and GroupChat
   - Tests basic stock analysis capabilities

3. **test_data_sources.py**
   - Tests various data sources used by FinRobot
   - Includes tests for Finnhub, Alpha Vantage, and Yahoo Finance data sources
   - Verifies data retrieval for company profiles, news, financials, and stock data

4. **test_functional.py**
   - Tests the functional modules of FinRobot
   - Includes tests for technical analysis, fundamental analysis, sentiment analysis, and portfolio optimization
   - Verifies calculations and analysis capabilities

5. **test_advanced_agents.py**
   - Tests advanced agent functionality
   - Includes tests for RAG-based agents, trade strategists, annual report analyzers, and forecasters
   - Verifies complex financial analysis capabilities

6. **run_all_tests.py**
   - Master script that runs all the individual test scripts
   - Provides a comprehensive test summary
   - Logs all test results to a file for later review

## Running the Tests

### Running All Tests

To run all tests at once, execute the following command:

```bash
python run_all_tests.py
```

This will run all test scripts and provide a summary of the results. The test results will also be logged to a file named `finrobot_test_results_YYYYMMDD_HHMMSS.log`.

### Running Individual Tests

You can also run individual test scripts as needed:

```bash
python test_imports.py
python test_basic_agents.py
python test_data_sources.py
python test_functional.py
python test_advanced_agents.py
```

## Test Requirements

- All tests require the FinRobot package to be installed in development mode
- API keys should be properly configured in the `FinRobot/config_api_keys` file
- Some tests may require internet access to retrieve data from external sources

## Troubleshooting

If you encounter any issues while running the tests:

1. Ensure that all required packages are installed correctly
2. Verify that API keys are properly configured
3. Check the log file for detailed error messages
4. Make sure you have internet access for tests that require external data

## Contributing

When adding new features to FinRobot, please also add corresponding tests to ensure the functionality works as expected. Follow the existing test structure and patterns when adding new tests.

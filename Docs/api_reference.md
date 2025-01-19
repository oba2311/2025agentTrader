# API Reference

## Trading Agent API

### `TradingAgent` Class

The main class for interacting with the trading agent system.

#### Methods

##### `__init__()`

Initializes a new trading agent instance.

```python
agent = TradingAgent()
```

##### `process_user_input(user_input: str) -> str`

Process natural language input to create and validate trading strategies.

Parameters:

- `user_input`: A string containing the user's trading strategy description

Returns:

- A string containing the agent's response

```python
response = agent.process_user_input("Track NVIDIA stock and alert me when RSI goes below 30")
```

##### `_analyze_stock_data(ticker: str) -> Dict[str, Any]`

Analyzes stock data for patterns and signals.

Parameters:

- `ticker`: Stock symbol to analyze

Returns:

- Dictionary containing analysis results:
  - `technical_indicators`: RSI, MACD, Bollinger Bands
  - `statistics`: Current price, volume, returns
  - `signals`: Trading signals based on indicators

##### `_validate_strategy(strategy: Dict[str, Any]) -> Dict[str, Any]`

Validates trading strategy parameters.

Parameters:

- `strategy`: Dictionary containing:
  - `ticker`: Stock symbol
  - `indicator`: Technical indicator to use
  - `condition`: Comparison condition
  - `threshold`: Trigger value

Returns:

- Dictionary containing validation results:
  - `is_valid`: Boolean indicating validity
  - `messages`: List of validation messages
  - `suggested_parameters`: Optional parameter suggestions

## Technical Indicators

### Available Indicators

1. **RSI (Relative Strength Index)**

   - Range: 0-100
   - Default periods: 14
   - Oversold threshold: 30
   - Overbought threshold: 70

2. **MACD (Moving Average Convergence Divergence)**

   - Components:
     - MACD line
     - Signal line
     - Histogram

3. **Bollinger Bands**

   - Components:
     - Upper band
     - Middle band (20-day SMA)
     - Lower band
   - Default deviation: 2

4. **Volume Analysis**
   - Volume comparison
   - On-Balance Volume (OBV)
   - Volume moving averages

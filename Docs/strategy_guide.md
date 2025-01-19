# Trading Strategy Guide

## Overview

This guide explains how to create and implement trading strategies using the AI Trading Agent. The system supports both technical and fundamental analysis approaches, with a focus on automated signal generation and monitoring.

## Creating Strategies

### Natural Language Input

The agent accepts natural language descriptions of trading strategies. Examples:

1. Simple RSI strategy:

```
"Alert me when NVIDIA stock's RSI drops below 30"
```

2. Volume-based strategy:

```
"Track unusual volume spikes in AMD stock above 1.5 times average"
```

3. Multiple indicator strategy:

```
"Monitor TSLA and alert me when RSI is oversold and MACD shows a bullish crossover"
```

### Strategy Components

Each strategy consists of four main components:

1. **Ticker Symbol**

   - Valid stock or ETF symbol
   - Example: AAPL, NVDA, SPY

2. **Technical Indicator**

   - RSI (Relative Strength Index)
   - MACD (Moving Average Convergence Divergence)
   - Bollinger Bands
   - Volume metrics

3. **Condition**

   - `above`: Value exceeds threshold
   - `below`: Value falls under threshold
   - `crosses_above`: Value transitions above threshold
   - `crosses_below`: Value transitions below threshold

4. **Threshold**
   - Numeric value or relative measure
   - Examples:
     - RSI: 30 (oversold), 70 (overbought)
     - Volume: "1.5x_average"

## Strategy Templates

### 1. Oversold RSI Strategy

```python
{
    "ticker": "NVDA",
    "indicator": "RSI",
    "condition": "below",
    "threshold": 30
}
```

### 2. Volume Spike Detection

```python
{
    "ticker": "AAPL",
    "indicator": "Volume",
    "condition": "above",
    "threshold": "1.5x_average"
}
```

### 3. MACD Crossover

```python
{
    "ticker": "TSLA",
    "indicator": "MACD",
    "condition": "crosses_above",
    "threshold": "signal_line"
}
```

## Best Practices

1. **Risk Management**

   - Always set appropriate stop-loss levels
   - Don't rely on a single indicator
   - Consider market conditions

2. **Strategy Validation**

   - Test strategies with historical data
   - Start with simple conditions
   - Gradually add complexity

3. **Monitoring**
   - Regular strategy performance review
   - Adjust parameters based on market conditions
   - Keep track of false signals

## Common Patterns

### Trend Following

```python
"Alert me when {stock} trends above its 20-day moving average with increasing volume"
```

### Reversal Detection

```python
"Monitor {stock} for oversold RSI conditions with bullish MACD divergence"
```

### Volatility Breakouts

```python
"Track when {stock} breaks out of Bollinger Bands with high volume"
```

## Customization

The agent supports strategy customization through:

1. Multiple indicator combinations
2. Custom timeframes
3. Adjustable thresholds
4. Complex conditional logic

## Backtesting

To validate your strategy:

1. Use historical data
2. Test across different market conditions
3. Analyze false signals
4. Measure performance metrics

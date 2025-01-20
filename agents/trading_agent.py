from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any, Optional, Tuple
import os
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import talib
from .prompts import TradingPrompts

# Load environment variables
load_dotenv()

class TradingAgent:
    def __init__(self):
        # Initialize the language model
        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="gpt-4"
        )
        
        # Initialize conversation memory
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        # Initialize prompts
        self.prompts = TradingPrompts()
        
        # Initialize tools
        self.tools = self._initialize_tools()
        
        # Initialize the agent
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
            memory=self.memory,
            verbose=True
        )
        
        # Store active strategies
        self.active_strategies = {}
    
    def _initialize_tools(self) -> List[Tool]:
        """Initialize the tools that the agent can use"""
        tools = [
            Tool(
                name="StockDataAnalyzer",
                func=self._analyze_stock_data,
                description="Analyzes historical stock data to identify patterns and signals. Input should be a stock ticker symbol."
            ),
            Tool(
                name="StrategyValidator",
                func=self._validate_strategy,
                description="Validates if a given trading strategy is well-formed and feasible. Input should be a dictionary containing strategy parameters."
            ),
            Tool(
                name="BacktestStrategy",
                func=self._backtest_strategy,
                description="Backtests a trading strategy using historical data."
            )
        ]
        return tools
    
    def _extract_strategy(self, user_input: str) -> Tuple[Dict[str, Any], List[str]]:
        """Extract trading strategy from user input"""
        try:
            # Create strategy extraction prompt
            prompt = self.prompts.create_strategy_extraction_prompt(
                user_input,
                context={"history": self.memory.chat_memory.messages}
            )
            
            # Get strategy from LLM
            response = self.llm(prompt.format(user_input=user_input, context=""))
            
            # Parse response
            strategy = self._parse_llm_response(response)
            
            # Validate strategy
            validation_result = self._validate_strategy(strategy)
            
            return strategy, validation_result['messages']
            
        except Exception as e:
            return None, [f"Error extracting strategy: {str(e)}"]
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into a structured strategy"""
        try:
            # Extract strategy dictionary from response
            # This is a simple implementation - you might want to make it more robust
            import json
            start_idx = response.find('{')
            end_idx = response.rfind('}') + 1
            strategy_str = response[start_idx:end_idx]
            return json.loads(strategy_str)
        except Exception as e:
            raise ValueError(f"Failed to parse LLM response: {str(e)}")
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Calculate various technical indicators"""
        close_prices = data['Close'].values
        high_prices = data['High'].values
        low_prices = data['Low'].values
        volume = data['Volume'].values

        indicators = {}
        
        # RSI
        indicators['RSI'] = talib.RSI(close_prices, timeperiod=14)[-1]
        
        # MACD
        macd, signal, hist = talib.MACD(close_prices)
        indicators['MACD'] = {
            'macd': macd[-1],
            'signal': signal[-1],
            'histogram': hist[-1]
        }
        
        # Bollinger Bands
        upper, middle, lower = talib.BBANDS(close_prices)
        indicators['BB'] = {
            'upper': upper[-1],
            'middle': middle[-1],
            'lower': lower[-1]
        }
        
        # Volume indicators
        indicators['OBV'] = talib.OBV(close_prices, volume)[-1]
        
        # Trend indicators
        indicators['SMA_20'] = talib.SMA(close_prices, timeperiod=20)[-1]
        indicators['SMA_50'] = talib.SMA(close_prices, timeperiod=50)[-1]
        indicators['EMA_20'] = talib.EMA(close_prices, timeperiod=20)[-1]
        
        # Volatility
        indicators['ATR'] = talib.ATR(high_prices, low_prices, close_prices, timeperiod=14)[-1]
        
        return indicators
    
    def _analyze_stock_data(self, ticker: str) -> Dict[str, Any]:
        """Analyze stock data for patterns and signals"""
        try:
            # Fetch data
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=60)  # Get 60 days of data
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                return {"error": f"No data found for ticker {ticker}"}
            
            # Calculate technical indicators
            indicators = self._calculate_technical_indicators(df)
            
            # Get current price
            current_price = df['Close'].iloc[-1]
            
            # Basic statistics
            stats = {
                'current_price': current_price,
                'daily_return': ((current_price / df['Close'].iloc[-2]) - 1) * 100,
                'volume': df['Volume'].iloc[-1],
                'avg_volume_10d': df['Volume'].tail(10).mean(),
                'volatility': df['Close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
            }
            
            # Combine all analysis
            analysis = {
                'ticker': ticker,
                'timestamp': datetime.now().isoformat(),
                'technical_indicators': indicators,
                'statistics': stats,
                'signals': self._generate_signals(indicators, stats)
            }
            
            return analysis
            
        except Exception as e:
            return {"error": f"Error analyzing {ticker}: {str(e)}"}
    
    def _backtest_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Backtest a trading strategy"""
        try:
            ticker = strategy['ticker']
            
            # Fetch historical data
            stock = yf.Ticker(ticker)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)  # 1 year of data
            df = stock.history(start=start_date, end=end_date)
            
            if df.empty:
                return {"error": f"No historical data found for {ticker}"}
            
            # Initialize results
            signals = []
            performance = []
            
            # Simulate strategy
            for i in range(20, len(df)):  # Start after enough data for indicators
                window = df.iloc[:i+1]
                indicators = self._calculate_technical_indicators(window)
                stats = {
                    'volume': window['Volume'].iloc[-1],
                    'avg_volume_10d': window['Volume'].tail(10).mean()
                }
                
                signal = self._generate_signals(indicators, stats)
                signals.append(signal)
                
                # Calculate returns if signal triggered
                if self._should_trigger_signal(signal, strategy):
                    next_return = df['Close'].iloc[min(i+5, len(df)-1)] / df['Close'].iloc[i] - 1
                    performance.append(next_return)
            
            # Calculate performance metrics
            results = {
                'total_signals': len([s for s in signals if self._should_trigger_signal(s, strategy)]),
                'avg_return': np.mean(performance) if performance else 0,
                'win_rate': len([p for p in performance if p > 0]) / len(performance) if performance else 0,
                'sharpe_ratio': np.mean(performance) / np.std(performance) if performance else 0
            }
            
            return results
            
        except Exception as e:
            return {"error": f"Error backtesting strategy: {str(e)}"}
    
    def _should_trigger_signal(self, signal: Dict[str, str], strategy: Dict[str, Any]) -> bool:
        """Check if current signals match strategy conditions"""
        indicator = strategy['indicator']
        condition = strategy['condition']
        
        if indicator not in signal:
            return False
            
        if indicator == 'RSI':
            if condition == 'below' and 'Oversold' in signal[indicator]:
                return True
            if condition == 'above' and 'Overbought' in signal[indicator]:
                return True
                
        return False
    
    def _generate_signals(self, indicators: Dict[str, Any], stats: Dict[str, Any]) -> Dict[str, str]:
        """Generate trading signals based on technical indicators"""
        signals = {}
        
        # RSI signals
        if indicators['RSI'] < 30:
            signals['RSI'] = 'Oversold - Potential Buy'
        elif indicators['RSI'] > 70:
            signals['RSI'] = 'Overbought - Potential Sell'
        else:
            signals['RSI'] = 'Neutral'
            
        # MACD signals
        if indicators['MACD']['macd'] > indicators['MACD']['signal']:
            signals['MACD'] = 'Bullish'
        else:
            signals['MACD'] = 'Bearish'
            
        # Volume signals
        if stats['volume'] > stats['avg_volume_10d'] * 1.5:
            signals['Volume'] = 'Unusual volume - High'
        elif stats['volume'] < stats['avg_volume_10d'] * 0.5:
            signals['Volume'] = 'Unusual volume - Low'
        else:
            signals['Volume'] = 'Normal'
            
        return signals
    
    def _validate_strategy(self, strategy: Dict[str, Any]) -> Dict[str, Any]:
        """Validate if a given strategy is well-formed and feasible"""
        validation_result = {
            'is_valid': True,
            'messages': [],
            'suggested_parameters': {}
        }
        
        required_fields = ['ticker', 'indicator', 'condition', 'threshold']
        
        # Check required fields
        for field in required_fields:
            if field not in strategy:
                validation_result['is_valid'] = False
                validation_result['messages'].append(f"Missing required field: {field}")
        
        if not validation_result['is_valid']:
            return validation_result
            
        # Validate indicator
        valid_indicators = ['RSI', 'MACD', 'BB', 'Volume']
        if strategy['indicator'] not in valid_indicators:
            validation_result['is_valid'] = False
            validation_result['messages'].append(f"Invalid indicator. Must be one of: {', '.join(valid_indicators)}")
            
        # Validate condition
        valid_conditions = ['above', 'below', 'crosses_above', 'crosses_below']
        if strategy['condition'] not in valid_conditions:
            validation_result['is_valid'] = False
            validation_result['messages'].append(f"Invalid condition. Must be one of: {', '.join(valid_conditions)}")
            
        # Validate and suggest parameters based on indicator
        if strategy['indicator'] == 'RSI':
            if not (0 <= float(strategy['threshold']) <= 100):
                validation_result['is_valid'] = False
                validation_result['messages'].append("RSI threshold must be between 0 and 100")
                validation_result['suggested_parameters'] = {
                    'oversold': 30,
                    'overbought': 70
                }
        
        return validation_result
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input and return agent's response"""
        try:
            # Extract strategy from user input
            strategy, messages = self._extract_strategy(user_input)
            
            if not strategy:
                return "\n".join(messages)
            
            # Validate strategy
            validation_result = self._validate_strategy(strategy)
            
            # If strategy is valid, run backtesting
            if validation_result['is_valid']:
                backtest_results = self._backtest_strategy(strategy)
                validation_result['backtest_results'] = backtest_results
            
            # Format response
            response = self.prompts.format_strategy_response(strategy, validation_result)
            
            # Store valid strategies
            if validation_result['is_valid']:
                strategy_id = f"{strategy['ticker']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                self.active_strategies[strategy_id] = strategy
            
            return response
            
        except Exception as e:
            return f"Error processing input: {str(e)}"

if __name__ == "__main__":
    # Example usage
    agent = TradingAgent()
    
    # Test input
    test_input = "I want to track NVIDIA stock and get alerts when the RSI indicates oversold conditions"
    response = agent.process_user_input(test_input)
    print(f"Response: {response}") 
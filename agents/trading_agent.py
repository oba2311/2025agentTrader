from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import talib

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
            )
        ]
        return tools
    
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
        macd, signal, _ = talib.MACD(close_prices)
        indicators['MACD'] = {
            'macd': macd[-1],
            'signal': signal[-1]
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
                'avg_volume_10d': df['Volume'].tail(10).mean()
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
            response = self.agent.run(input=user_input)
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
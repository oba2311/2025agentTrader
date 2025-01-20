from typing import Dict, Any
from langchain.prompts import PromptTemplate

STRATEGY_EXTRACTION_TEMPLATE = """
You are a professional trading assistant. Your task is to extract a well-defined trading strategy from the user's input.

User Input: {user_input}

Please extract the following components:
1. Stock ticker symbol
2. Technical indicators to monitor
3. Conditions for alerts
4. Threshold values

The strategy should be returned in the following format:
{
    "ticker": "SYMBOL",
    "indicators": ["INDICATOR1", "INDICATOR2"],
    "conditions": ["CONDITION1", "CONDITION2"],
    "thresholds": [VALUE1, VALUE2],
    "timeframe": "TIMEFRAME"
}

Current Context:
{context}

Response should include:
1. The structured strategy
2. Any clarifying questions if the input is ambiguous
3. Suggested refinements to make the strategy more robust

Response:"""

STRATEGY_VALIDATION_TEMPLATE = """
Analyze the following trading strategy for potential issues:

Strategy: {strategy}

Consider:
1. Technical indicator compatibility
2. Historical effectiveness
3. Risk management concerns
4. Market condition requirements

Response should include:
1. Validation results
2. Specific concerns
3. Suggested improvements
4. Risk assessment

Response:"""

class TradingPrompts:
    @staticmethod
    def create_strategy_extraction_prompt(user_input: str, context: Dict[str, Any] = None) -> PromptTemplate:
        """Create a prompt for extracting trading strategy from user input"""
        if context is None:
            context = {}
            
        return PromptTemplate(
            input_variables=["user_input", "context"],
            template=STRATEGY_EXTRACTION_TEMPLATE
        )
    
    @staticmethod
    def create_strategy_validation_prompt(strategy: Dict[str, Any]) -> PromptTemplate:
        """Create a prompt for validating a trading strategy"""
        return PromptTemplate(
            input_variables=["strategy"],
            template=STRATEGY_VALIDATION_TEMPLATE
        )
    
    @staticmethod
    def format_strategy_response(strategy: Dict[str, Any], validation_result: Dict[str, Any]) -> str:
        """Format the strategy and validation results into a user-friendly response"""
        response = []
        
        # Strategy summary
        response.append("📈 Strategy Summary:")
        response.append(f"- Stock: {strategy['ticker']}")
        response.append(f"- Indicators: {', '.join(strategy['indicators'])}")
        response.append(f"- Conditions: {', '.join(strategy['conditions'])}")
        response.append(f"- Timeframe: {strategy.get('timeframe', 'Default')}")
        
        # Validation results
        if validation_result['is_valid']:
            response.append("\n✅ Strategy Validation:")
        else:
            response.append("\n⚠️ Strategy Concerns:")
            
        for message in validation_result['messages']:
            response.append(f"- {message}")
            
        # Backtesting results
        if validation_result.get('backtest_results'):
            response.append("\n📊 Backtest Results:")
            results = validation_result['backtest_results']
            
            if isinstance(results, dict) and 'error' not in results:
                response.append(f"- Total Signals: {results['total_signals']}")
                response.append(f"- Average Return: {results['avg_return']:.2f}%")
                response.append(f"- Win Rate: {results['win_rate']:.1%}")
                response.append(f"- Sharpe Ratio: {results['sharpe_ratio']:.2f}")
            elif isinstance(results, dict) and 'error' in results:
                response.append(f"⚠️ {results['error']}")
            
        # Suggestions
        if validation_result.get('suggested_parameters'):
            response.append("\n💡 Suggested Parameters:")
            for param, value in validation_result['suggested_parameters'].items():
                response.append(f"- {param}: {value}")
                
        return "\n".join(response) 
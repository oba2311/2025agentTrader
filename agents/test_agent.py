from trading_agent import TradingAgent
import json

def test_agent():
    agent = TradingAgent()
    
    # Test cases
    test_cases = [
        # Simple RSI strategy
        {
            "description": "Simple RSI Strategy",
            "input": "Alert me when NVIDIA stock's RSI goes below 30"
        },
        # Complex multi-indicator strategy
        {
            "description": "Complex Strategy",
            "input": "Monitor Tesla stock and alert me when RSI is below 30 and MACD shows a bullish crossover"
        },
        # Volume-based strategy
        {
            "description": "Volume Strategy",
            "input": "Track unusual volume spikes in AMD stock that are 50% above average"
        },
        # Invalid input test
        {
            "description": "Invalid Input",
            "input": "Just buy some good stocks"
        }
    ]
    
    print("🤖 Testing Trading Agent\n")
    
    for case in test_cases:
        print(f"\n📝 Test Case: {case['description']}")
        print(f"Input: {case['input']}")
        print("\nResponse:")
        print("-" * 50)
        
        response = agent.process_user_input(case['input'])
        print(response)
        print("-" * 50)

if __name__ == "__main__":
    test_agent() 
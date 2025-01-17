import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_stock_data():
    # Calculate dates
    end_date = datetime.now()
    start_date = end_date - timedelta(days=3*365)  # 3 years of data
    
    # List of tickers to fetch
    tickers = {
        'SPY': 'S&P 500 ETF',
        'SMH': 'Semiconductor ETF',
        'NVDA': 'NVIDIA',
        'AMD': 'AMD'
    }
    
    # Dictionary to store the data
    stock_data = {}
    
    try:
        for ticker, name in tickers.items():
            # Fetch data from Yahoo Finance
            stock = yf.Ticker(ticker)
            df = stock.history(start=start_date, end=end_date)
            
            # Store data
            stock_data[ticker] = df
            
            # Save to CSV
            df.to_csv(f'data/{ticker}_historical.csv')
            
        # Calculate the number of months of data
        months = (end_date.year - start_date.year) * 12 + (end_date.month - start_date.month)
        
        logger.info(f"Just got the data for {months} months from Yahoo Finance")
        return stock_data
        
    except Exception as e:
        logger.error(f"Error fetching data: {str(e)}")
        raise

if __name__ == "__main__":
    # Create data directory if it doesn't exist
    import os
    os.makedirs('data', exist_ok=True)
    
    # Fetch the data
    get_stock_data()

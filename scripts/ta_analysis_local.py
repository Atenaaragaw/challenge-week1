import pandas as pd
import talib
import numpy as np
import os
from typing import List

# --- Configuration ---
BASE_PATH = r'C:\Users\Home-User\Downloads\data\Data'
TICKER_FILES = {
    'AAPL': 'AAPL.csv', 
    'MSFT': 'MSFT.csv', 
    'GOOG': 'GOOG.csv', 
    'AMZN': 'AMZN.csv', 
    'NVDA': 'NVDA.csv', 
    'META': 'META.csv'
}
PROJECT_ROOT = r'C:\Users\Home-User\challenge-week1' 
OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'all_tickers_indicators.csv')

def load_local_stock_data(ticker: str, filename: str) -> pd.DataFrame:
    """Loads a single CSV file, ensuring standard OHLCV format."""
    file_path = os.path.join(BASE_PATH, filename)
    print(f"Loading data for {ticker} from {file_path}...")
    try:
        # Assuming the CSV files have a date column and standard columns like 'Close'
        df = pd.read_csv(file_path)
        
        # Standardize the Date/Index (Crucial for time series analysis)
        if 'Date' in df.columns:
             df.set_index('Date', inplace=True)
        elif 'date' in df.columns:
             df.set_index('date', inplace=True)
             
        df.index = pd.to_datetime(df.index)
        
        # Standardize OHLCV columns (adjust as necessary for your files)
        df.columns = [col.capitalize() for col in df.columns]
        
        # Add the ticker symbol
        df['Ticker'] = ticker
        
        # Ensure we have the required 'Close' column
        if 'Close' not in df.columns:
            print(f"Warning: 'Close' column not found for {ticker}. Skipping.")
            return pd.DataFrame()
            
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df[['Open', 'High', 'Low', 'Close', 'Volume', 'Ticker']].copy()
        
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}. Please check the path.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error processing data for {ticker}: {e}")
        return pd.DataFrame()

def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """Calculates key technical indicators using TA-Lib."""
    if df.empty:
        return df
    
    close_prices = df['Close'].values
    
    # 1. Moving Averages (MA)
    df['SMA_20'] = talib.SMA(close_prices, timeperiod=20)
    df['EMA_50'] = talib.EMA(close_prices, timeperiod=50)

    # 2. Relative Strength Index (RSI)
    df['RSI_14'] = talib.RSI(close_prices, timeperiod=14)

    # 3. MACD
    macd, macdsignal, macdhist = talib.MACD(
        close_prices, fastperiod=12, slowperiod=26, signalperiod=9
    )
    df['MACD'] = macd
    df['MACD_Signal'] = macdsignal
    df['MACD_Hist'] = macdhist
    
    # Drop initial NaN rows created by the indicators
    df.dropna(inplace=True) 
    return df

def run_local_multi_ticker_analysis(ticker_files: dict) -> pd.DataFrame:
    """Loops through all files, loads, calculates indicators, and combines results."""
    all_data = []
    
    for ticker, filename in ticker_files.items():
        stock_df = load_local_stock_data(ticker, filename)
        if not stock_df.empty:
            stock_df_indicators = calculate_indicators(stock_df)
            all_data.append(stock_df_indicators)
            
    if all_data:
        final_df = pd.concat(all_data)
        return final_df
    else:
        print("No data processed successfully.")
        return pd.DataFrame()

if __name__ == '__main__':
    final_df_with_indicators = run_local_multi_ticker_analysis(TICKER_FILES)

    if not final_df_with_indicators.empty:
        print(f"\n--- Combined Data Summary ---")
        print(f"Total rows: {len(final_df_with_indicators)}")
        print(f"Tickers processed: {final_df_with_indicators['Ticker'].nunique()}")
        
        # Save the result
        final_df_with_indicators.to_csv(OUTPUT_FILE, index=True)
        print(f"\nData saved successfully to: {OUTPUT_FILE}")
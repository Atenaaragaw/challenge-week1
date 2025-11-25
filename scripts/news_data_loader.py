import pandas as pd
import os
from typing import Optional

RAW_NEWS_FILE_PATH = r'C:\Users\Home-User\Downloads\data\raw_analyst_ratings.csv'
PROJECT_ROOT = r'C:\Users\Home-User\challenge-week1' 

CLEANED_OUTPUT_FILE = os.path.join(PROJECT_ROOT, 'data', 'cleaned_financial_news.csv') 

def load_and_clean_news_data() -> Optional[pd.DataFrame]:
    """
    Loads the raw news data from the specified path, performs initial cleaning,
    and processes the date field.
    """
    print(f"Loading raw news data from {RAW_NEWS_FILE_PATH}...")
    
    try:
        # Load the CSV file
        df = pd.read_csv(RAW_NEWS_FILE_PATH)
        
        # --- Data Cleaning and Standardization ---
        
        # 1. Standardize column names (lowercase for consistency)
        df.columns = df.columns.str.lower()
        
        # NOTE: Assuming the column names match the challenge description:
        # 'headline', 'publisher', 'date', 'stock' (or similar)
        
        # If the stock column is named 'stock', rename for clarity:
        if 'stock' in df.columns:
            df.rename(columns={'stock': 'stock_symbol'}, inplace=True) 

        # 2. Convert 'date' to datetime object, handling the known timezone (UTC-4)
        # We use 'errors='coerce' to turn bad dates into NaT and then drop them, improving data quality.
        df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce')
        df.dropna(subset=['date'], inplace=True)
        
        # 3. Create key features for Task 1 EDA
        df['publication_date'] = df['date'].dt.date
        df['publication_hour'] = df['date'].dt.hour
        df['headline_len'] = df['headline'].str.len()
        
        print("Initial cleaning successful.")
        print(f"Cleaned data shape: {df.shape}")
        
        return df
        
    except FileNotFoundError:
        print(f"ERROR: News file not found at {RAW_NEWS_FILE_PATH}. Please check the path.")
        return None
    except Exception as e:
        print(f"An unexpected error occurred during data processing: {e}")
        return None

def run_news_data_preparation():
    """Runs the news data loading and saves the cleaned file for subsequent use."""
    
    cleaned_df = load_and_clean_news_data()
    
    if cleaned_df is not None and not cleaned_df.empty:
        # Ensure the output directory exists
        os.makedirs(os.path.dirname(CLEANED_OUTPUT_FILE), exist_ok=True)
        
        cleaned_df.to_csv(CLEANED_OUTPUT_FILE, index=False)
        print(f"\nCleaned news data saved successfully to: {CLEANED_OUTPUT_FILE}")
        
        return cleaned_df
    else:
        print("News data preparation failed.")
        return pd.DataFrame()

if __name__ == '__main__':
    # Execute the script
    run_news_data_preparation()
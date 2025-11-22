import pandas as pd

def load_financial_data(file_path: str = 'C:\Users\Home-User\Downloads\data\raw_analyst_ratings.csv') -> pd.DataFrame:
    try:
        df = pd.read_csv(file_path)
        print(f"Data loaded successfully. Shape: {df.shape}")
        return df
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return pd.DataFrame()

if __name__ == '__main__':
    # NOTE: This will fail until you add the data file
    # df = load_financial_data() 
    print("Data loader module configured.")
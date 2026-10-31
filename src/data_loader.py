import os
import pandas as pd

DEFAULT_URL = "https://docs.google.com/spreadsheets/d/1JQbd2LFo1ubi43SLw2xTW2v4Qk8Z_NtoD_DdQCnsegQ/export?format=csv"

def load_raw_data(source_url: str = DEFAULT_URL, save_raw_path: str = None) -> pd.DataFrame:
    """Ingests raw churn dataset from URL or local path."""
    df = pd.read_csv(source_url)
    
    if save_raw_path:
        os.makedirs(os.path.dirname(save_raw_path), exist_ok=True)
        df.to_csv(save_raw_path, index=False)
        print(f"[DataLoader] Raw data saved to: {save_raw_path}")
        
    print(f"[DataLoader] Loaded dataset with shape: {df.shape}")
    return df

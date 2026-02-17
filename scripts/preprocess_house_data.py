"""
Preprocess Land Registry 2024 data for house price model training.
"""

import pandas as pd
import numpy as np
from pathlib import Path

def main():
    print("="*60)
    print("KALMAN - House Price Data Preprocessing")
    print("="*60)
    
    raw_file = "data/training/raw/pp-2024.csv"
    
    print(f"\nLoading data from {raw_file}...")
    
    column_names = [
        'transaction_id', 'price', 'date_of_transfer', 'postcode',
        'property_type', 'old_new', 'duration', 'paon', 'saon',
        'street', 'locality', 'town_city', 'district', 'county',
        'ppd_category_type', 'record_status'
    ]
    
    df = pd.read_csv(raw_file, names=column_names, header=None)
    print(f"✅ Loaded {len(df):,} transactions")
    
    print(f"\n📊 Dataset Overview:")
    print(f"  Columns: {len(df.columns)}")
    print(f"  Memory: {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
    
    print(f"\n💰 Price Statistics:")
    print(df['price'].describe())
    
    print(f"\n🏠 Property Types:")
    print(df['property_type'].value_counts())
    
    print(f"\n📍 Top 10 Locations:")
    print(df['town_city'].value_counts().head(10))

if __name__ == "__main__":
    main()

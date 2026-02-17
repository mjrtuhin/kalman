"""
Clean data and save for training.
"""

import pandas as pd
from pathlib import Path

print("Loading data...")

column_names = [
    'transaction_id', 'price', 'date_of_transfer', 'postcode',
    'property_type', 'old_new', 'duration', 'paon', 'saon',
    'street', 'locality', 'town_city', 'district', 'county',
    'ppd_category_type', 'record_status'
]

df = pd.read_csv("data/training/raw/pp-2024.csv", names=column_names, header=None)
initial = len(df)

print(f"Initial: {initial:,}")

df = df[df['price'] > 10000]
df = df[df['price'] < 10000000]

df = df[df['property_type'].isin(['D', 'S', 'T', 'F'])]

df = df[df['postcode'].notna()]

df['postcode_sector'] = df['postcode'].str.extract(r'^([A-Z]{1,2}\d{1,2})')

print(f"Cleaned: {len(df):,} ({len(df)/initial*100:.1f}% retained)")

Path("data/training/processed").mkdir(parents=True, exist_ok=True)

df.to_parquet("data/training/processed/house_2024_cleaned.parquet", index=False)

print(f"✅ Saved to data/training/processed/house_2024_cleaned.parquet")
print(f"📊 Ready for training: {len(df):,} transactions")

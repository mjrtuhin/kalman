"""
Improved model with more features.
"""

import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import json
from datetime import datetime

print("="*70)
print("KALMAN - IMPROVED House Price Model")
print("="*70)

print("\n📂 Loading data...")
df = pd.read_parquet("data/training/processed/house_2024_cleaned.parquet")
print(f"✅ Loaded {len(df):,} transactions")

print("\n🔧 Feature Engineering...")

df['date_of_transfer'] = pd.to_datetime(df['date_of_transfer'])
df['month'] = df['date_of_transfer'].dt.month
df['quarter'] = df['date_of_transfer'].dt.quarter
df['is_new_build'] = (df['old_new'] == 'Y').astype(int)
df['is_freehold'] = (df['duration'] == 'F').astype(int)

postcode_sector_median = df.groupby('postcode_sector')['price'].median()
df['sector_median_price'] = df['postcode_sector'].map(postcode_sector_median)

town_median = df.groupby('town_city')['price'].median()
df['town_median_price'] = df['town_city'].map(town_median)

property_type_median = df.groupby('property_type')['price'].median()
df['property_type_median'] = df['property_type'].map(property_type_median)

categorical_features = ['property_type', 'duration', 'postcode_sector', 'town_city', 'county']
numerical_features = ['month', 'quarter', 'is_new_build', 'is_freehold', 
                     'sector_median_price', 'town_median_price', 'property_type_median']

for col in categorical_features:
    df[col] = df[col].fillna('UNKNOWN').astype(str)

for col in numerical_features:
    df[col] = df[col].fillna(df[col].median())

feature_cols = categorical_features + numerical_features
target = 'price'

print(f"✅ Total features: {len(feature_cols)}")

print("\n✂️ Train/Val/Test split...")
train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

print(f"   Train: {len(train_df):,}")
print(f"   Val:   {len(val_df):,}")
print(f"   Test:  {len(test_df):,}")

train_pool = Pool(train_df[feature_cols], train_df[target], cat_features=categorical_features)
val_pool = Pool(val_df[feature_cols], val_df[target], cat_features=categorical_features)

print("\n🤖 Training improved model...")

model = CatBoostRegressor(
    iterations=1000,
    learning_rate=0.05,
    depth=8,
    loss_function='RMSE',
    eval_metric='R2',
    random_seed=42,
    verbose=100,
    early_stopping_rounds=50
)

model.fit(train_pool, eval_set=val_pool, plot=False)

print("\n📊 Final Evaluation...")

test_pred = model.predict(test_df[feature_cols])
r2 = r2_score(test_df[target], test_pred)
mae = mean_absolute_error(test_df[target], test_pred)
rmse = np.sqrt(mean_squared_error(test_df[target], test_pred))

print(f"\n{'='*70}")
print("IMPROVED MODEL PERFORMANCE")
print(f"{'='*70}")
print(f"R² Score:  {r2:.4f} (vs 0.5108 baseline)")
print(f"MAE:       £{mae:,.0f} (vs £102,977 baseline)")
print(f"RMSE:      £{rmse:,.0f} (vs £231,465 baseline)")
print(f"{'='*70}")

model.save_model("models/house_2024_improved_v1.cbm")
print(f"\n💾 Saved: models/house_2024_improved_v1.cbm")

metadata = {
    "model_name": "house_2024_improved_v1",
    "version": "1.0",
    "training_date": datetime.now().isoformat(),
    "features": feature_cols,
    "metrics": {"r2_score": float(r2), "mae": float(mae), "rmse": float(rmse)}
}

with open("models/house_2024_improved_v1_metadata.json", 'w') as f:
    json.dump(metadata, f, indent=2)

print("✅ Training complete!")

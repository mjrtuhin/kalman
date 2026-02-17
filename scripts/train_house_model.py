"""
Train CatBoost model for house price prediction.
866K transactions from 2024.
"""

import pandas as pd
import numpy as np
from catboost import CatBoostRegressor, Pool
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import json
from pathlib import Path
from datetime import datetime

print("="*70)
print("KALMAN - House Price Model Training")
print("="*70)

print("\n📂 Loading preprocessed data...")
df = pd.read_parquet("data/training/processed/house_2024_cleaned.parquet")
print(f"✅ Loaded {len(df):,} transactions")

print("\n🔧 Preparing features...")

categorical_features = ['property_type', 'duration', 'postcode_sector', 'town_city', 'county']
target = 'price'

feature_cols = categorical_features.copy()

for col in categorical_features:
    if col in df.columns:
        df[col] = df[col].fillna('UNKNOWN').astype(str)

print(f"✅ Features: {len(feature_cols)}")
print(f"   Categorical: {categorical_features}")

print("\n✂️ Train/Val/Test split (70/15/15)...")

train_df, temp_df = train_test_split(df, test_size=0.3, random_state=42)
val_df, test_df = train_test_split(temp_df, test_size=0.5, random_state=42)

print(f"   Train: {len(train_df):,}")
print(f"   Val:   {len(val_df):,}")
print(f"   Test:  {len(test_df):,}")

train_pool = Pool(
    data=train_df[feature_cols],
    label=train_df[target],
    cat_features=categorical_features
)

val_pool = Pool(
    data=val_df[feature_cols],
    label=val_df[target],
    cat_features=categorical_features
)

print("\n🤖 Training CatBoost model...")
print("   (This will take 10-30 minutes...)")

model = CatBoostRegressor(
    iterations=500,
    learning_rate=0.1,
    depth=6,
    loss_function='RMSE',
    eval_metric='R2',
    random_seed=42,
    verbose=50,
    early_stopping_rounds=50
)

model.fit(
    train_pool,
    eval_set=val_pool,
    plot=False
)

print("\n📊 Evaluating on test set...")

test_pred = model.predict(test_df[feature_cols])

r2 = r2_score(test_df[target], test_pred)
mae = mean_absolute_error(test_df[target], test_pred)
rmse = np.sqrt(mean_squared_error(test_df[target], test_pred))

print(f"\n{'='*70}")
print("MODEL PERFORMANCE")
print(f"{'='*70}")
print(f"R² Score:  {r2:.4f}")
print(f"MAE:       £{mae:,.0f}")
print(f"RMSE:      £{rmse:,.0f}")
print(f"{'='*70}")

Path("models").mkdir(exist_ok=True)

model_path = "models/house_2024_v1.cbm"
model.save_model(model_path)
print(f"\n💾 Model saved: {model_path}")

metadata = {
    "model_name": "house_2024_v1",
    "version": "1.0",
    "training_date": datetime.now().isoformat(),
    "data_size": len(df),
    "train_size": len(train_df),
    "val_size": len(val_df),
    "test_size": len(test_df),
    "features": feature_cols,
    "categorical_features": categorical_features,
    "metrics": {
        "r2_score": float(r2),
        "mae": float(mae),
        "rmse": float(rmse)
    }
}

metadata_path = "models/house_2024_v1_metadata.json"
with open(metadata_path, 'w') as f:
    json.dump(metadata, f, indent=2)

print(f"📄 Metadata saved: {metadata_path}")

print("\n✅ Training complete!")

"""
Test the trained model with sample predictions.
"""

import pandas as pd
from catboost import CatBoostRegressor

print("="*70)
print("KALMAN - Model Prediction Test")
print("="*70)

print("\n📂 Loading model...")
model = CatBoostRegressor()
model.load_model("models/house_2024_improved_v1.cbm")
print("✅ Model loaded")

print("\n🏠 Test Predictions:\n")

test_cases = [
    {
        "name": "London Semi-Detached",
        "property_type": "S",
        "duration": "F",
        "postcode_sector": "SW1",
        "town_city": "LONDON",
        "county": "GREATER LONDON",
        "month": 6,
        "quarter": 2,
        "is_new_build": 0,
        "is_freehold": 1,
        "sector_median_price": 750000,
        "town_median_price": 650000,
        "property_type_median": 400000
    },
    {
        "name": "Manchester Terraced",
        "property_type": "T",
        "duration": "F",
        "postcode_sector": "M1",
        "town_city": "MANCHESTER",
        "county": "GREATER MANCHESTER",
        "month": 3,
        "quarter": 1,
        "is_new_build": 0,
        "is_freehold": 1,
        "sector_median_price": 220000,
        "town_median_price": 240000,
        "property_type_median": 230000
    },
    {
        "name": "Birmingham Flat",
        "property_type": "F",
        "duration": "L",
        "postcode_sector": "B1",
        "town_city": "BIRMINGHAM",
        "county": "WEST MIDLANDS",
        "month": 9,
        "quarter": 3,
        "is_new_build": 1,
        "is_freehold": 0,
        "sector_median_price": 180000,
        "town_median_price": 190000,
        "property_type_median": 160000
    }
]

for test in test_cases:
    name = test.pop("name")
    df = pd.DataFrame([test])
    
    prediction = model.predict(df)[0]
    
    print(f"{name}:")
    print(f"  Location: {test['town_city']}, {test['postcode_sector']}")
    print(f"  Type: {test['property_type']} ({test['duration']})")
    print(f"  💰 Predicted Price: £{prediction:,.0f}")
    print()

print("="*70)
print("✅ Model is working!")
print("="*70)

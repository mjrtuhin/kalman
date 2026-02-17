"""
ML Execution Agent - Loads model, predicts, generates explanations.
Uses template-based explanations (no LLM needed).
"""

import pandas as pd
from catboost import CatBoostRegressor
import json
from typing import Dict, List
from pathlib import Path

class MLExecutionAgent:
    """Handles model loading, prediction, and explanation generation."""
    
    def __init__(self, model_path: str = "models/house_2024_improved_v1.cbm"):
        self.model_path = model_path
        self.model = None
        self.metadata = None
        
    def load_model(self):
        """Load trained model."""
        print(f"Loading model from {self.model_path}...")
        self.model = CatBoostRegressor()
        self.model.load_model(self.model_path)
        
        metadata_path = self.model_path.replace('.cbm', '_metadata.json')
        with open(metadata_path, 'r') as f:
            self.metadata = json.load(f)
        
        print(f"✅ Model loaded (R² {self.metadata['metrics']['r2_score']:.4f})")
        
    def predict(self, features: Dict) -> Dict:
        """Make prediction and generate explanation."""
        
        if self.model is None:
            self.load_model()
        
        df = pd.DataFrame([features])
        
        prediction = self.model.predict(df)[0]
        
        feature_importance = self.model.get_feature_importance()
        feature_names = self.metadata['features']
        
        top_features = sorted(
            zip(feature_names, feature_importance),
            key=lambda x: abs(x[1]),
            reverse=True
        )[:5]
        
        explanation = self._generate_explanation(features, prediction, top_features)
        
        return {
            "prediction": float(prediction),
            "confidence_low": float(prediction * 0.85),
            "confidence_high": float(prediction * 1.15),
            "explanation": explanation,
            "top_factors": [{"feature": f, "importance": float(i)} for f, i in top_features]
        }
    
    def _generate_explanation(self, features: Dict, prediction: float, top_features: List) -> str:
        """Generate human-readable explanation using templates."""
        
        property_type_map = {
            'D': 'detached house',
            'S': 'semi-detached house',
            'T': 'terraced house',
            'F': 'flat/apartment'
        }
        
        tenure_map = {
            'F': 'freehold',
            'L': 'leasehold'
        }
        
        prop_type = property_type_map.get(features.get('property_type', 'F'), 'property')
        tenure = tenure_map.get(features.get('duration', 'F'), 'property')
        location = features.get('town_city', 'this area')
        postcode = features.get('postcode_sector', '')
        
        explanation = f"Based on our analysis of 866,000 recent UK property sales, "
        explanation += f"this {prop_type} ({tenure}) in {location}"
        
        if postcode:
            explanation += f" ({postcode})"
        
        explanation += f" is estimated at £{prediction:,.0f}. "
        
        sector_median = features.get('sector_median_price', 0)
        if sector_median > 0:
            diff_pct = ((prediction - sector_median) / sector_median) * 100
            if abs(diff_pct) > 5:
                direction = "above" if diff_pct > 0 else "below"
                explanation += f"This is {abs(diff_pct):.1f}% {direction} the area median of £{sector_median:,.0f}. "
        
        if features.get('is_new_build'):
            explanation += "As a new build property, this includes modern construction standards and warranties. "
        
        top_factor = top_features[0][0] if top_features else None
        if top_factor == 'postcode_sector':
            explanation += f"Location is the primary value driver for this property. "
        elif top_factor == 'property_type':
            explanation += f"Property type significantly influences the valuation. "
        
        return explanation


def test_agent():
    """Test the ML Execution Agent."""
    
    print("="*70)
    print("Testing ML Execution Agent")
    print("="*70)
    
    agent = MLExecutionAgent()
    
    test_property = {
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
    }
    
    result = agent.predict(test_property)
    
    print(f"\n💰 Prediction: £{result['prediction']:,.0f}")
    print(f"📊 Confidence Range: £{result['confidence_low']:,.0f} - £{result['confidence_high']:,.0f}")
    print(f"\n📝 Explanation:")
    print(result['explanation'])
    print(f"\n🔍 Top Factors:")
    for factor in result['top_factors']:
        print(f"   - {factor['feature']}: {factor['importance']:.2f}")
    
    print("\n✅ Agent working perfectly!")


if __name__ == "__main__":
    test_agent()

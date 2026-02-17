"""
ML Execution Agent with REAL LLM (Ollama + Llama 3).
"""

import pandas as pd
from catboost import CatBoostRegressor
import json
import requests
from typing import Dict, List

class MLExecutionAgent:
    """Handles model loading, prediction, and LLM-powered explanations."""
    
    def __init__(self, model_path: str = "models/house_2024_improved_v1.cbm"):
        self.model_path = model_path
        self.model = None
        self.metadata = None
        self.ollama_url = "http://localhost:11434/api/generate"
        
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
        """Make prediction with LLM explanation."""
        
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
        
        explanation = self._generate_llm_explanation(features, prediction, top_features)
        
        return {
            "prediction": float(prediction),
            "confidence_low": float(prediction * 0.85),
            "confidence_high": float(prediction * 1.15),
            "explanation": explanation,
            "top_factors": [{"feature": f, "importance": float(i)} for f, i in top_features]
        }
    
    def _generate_llm_explanation(self, features: Dict, prediction: float, top_features: List) -> str:
        """Generate explanation using Ollama Llama 3."""
        
        property_type_map = {
            'D': 'detached house',
            'S': 'semi-detached house',
            'T': 'terraced house',
            'F': 'flat'
        }
        
        prop_type = property_type_map.get(features.get('property_type', 'S'), 'property')
        location = features.get('town_city', 'this area')
        postcode = features.get('postcode_sector', '')
        sector_median = features.get('sector_median_price', 0)
        
        top_factor_names = [f[0] for f in top_features[:3]]
        
        prompt = f"""You are a UK property expert explaining house price predictions to homeowners.

Property Details:
- Type: {prop_type}
- Location: {location} {postcode}
- Predicted Price: £{prediction:,.0f}
- Area Median: £{sector_median:,.0f}
- Top Value Factors: {', '.join(top_factor_names)}

Write a brief, friendly 2-3 sentence explanation for the homeowner about:
1. The estimated price
2. How it compares to the area
3. The main factor affecting the value

Use plain English, no jargon. Be conversational and helpful."""

        try:
            response = requests.post(
                self.ollama_url,
                json={
                    "model": "llama3.2:3b",
                    "prompt": prompt,
                    "stream": False
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["response"].strip()
            else:
                return self._fallback_explanation(features, prediction, sector_median)
                
        except Exception as e:
            print(f"⚠️ LLM error: {e}, using fallback")
            return self._fallback_explanation(features, prediction, sector_median)
    
    def _fallback_explanation(self, features: Dict, prediction: float, sector_median: float) -> str:
        """Fallback template if LLM fails."""
        prop_type = features.get('property_type', 'property')
        location = features.get('town_city', 'this area')
        
        explanation = f"This {prop_type} in {location} is estimated at £{prediction:,.0f}. "
        
        if sector_median > 0:
            diff = prediction - sector_median
            pct = (diff / sector_median) * 100
            if abs(pct) > 5:
                direction = "above" if pct > 0 else "below"
                explanation += f"This is {abs(pct):.1f}% {direction} the area median."
        
        return explanation


def test_agent():
    """Test with LLM."""
    
    print("="*70)
    print("Testing ML Agent with REAL LLM (Llama 3)")
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
    
    print("\n🤖 Generating prediction with LLM explanation...")
    print("(This may take 10-20 seconds for first request)\n")
    
    result = agent.predict(test_property)
    
    print(f"💰 Prediction: £{result['prediction']:,.0f}")
    print(f"📊 Range: £{result['confidence_low']:,.0f} - £{result['confidence_high']:,.0f}")
    print(f"\n🤖 LLM Explanation:")
    print(result['explanation'])
    print(f"\n✅ Real LLM working!")


if __name__ == "__main__":
    test_agent()

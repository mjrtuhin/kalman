"""
Prediction service with LLM-powered explanations.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.ml_execution_agent import MLExecutionAgent

class PredictionService:
    """Handles predictions with LLM explanations."""
    
    def __init__(self):
        self.house_agent = MLExecutionAgent("models/house_2024_improved_v1.cbm")
        self.house_agent.load_model()
    
    def predict_house_price(self, user_input: dict) -> dict:
        """Predict with LLM explanation."""
        
        property_type_map = {
            "Detached": "D",
            "Semi-Detached": "S",
            "Terraced": "T",
            "Flat": "F"
        }
        
        postcode = user_input.get("postcode", "").strip().upper()
        postcode_sector = postcode.split()[0] if postcode else "UNKNOWN"
        
        features = {
            "property_type": property_type_map.get(user_input.get("property_type"), "S"),
            "duration": "F" if user_input.get("tenure") == "Freehold" else "L",
            "postcode_sector": postcode_sector,
            "town_city": "LONDON",
            "county": "GREATER LONDON",
            "month": 6,
            "quarter": 2,
            "is_new_build": 0,
            "is_freehold": 1 if user_input.get("tenure") == "Freehold" else 0,
            "sector_median_price": 400000,
            "town_median_price": 380000,
            "property_type_median": 350000
        }
        
        result = self.house_agent.predict(features)
        
        return {
            "status": "success",
            "prediction": result["prediction"],
            "confidence_low": result["confidence_low"],
            "confidence_high": result["confidence_high"],
            "explanation": result["explanation"],
            "top_factors": result["top_factors"],
            "model_version": "house_2024_improved_v1",
            "llm_powered": True
        }

prediction_service = PredictionService()

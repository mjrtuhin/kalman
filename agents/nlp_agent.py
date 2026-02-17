"""
NLP Agent - Extracts structured data from natural language queries.
"""

import re
from typing import Dict, Optional, List

class NLPAgent:
    """Converts natural language to structured prediction inputs."""
    
    def __init__(self):
        self.property_types = {
            'detached': 'Detached',
            'semi': 'Semi-Detached',
            'semi-detached': 'Semi-Detached',
            'terraced': 'Terraced',
            'terrace': 'Terraced',
            'flat': 'Flat',
            'apartment': 'Flat',
            'bungalow': 'Detached'
        }
        
        self.tenure_keywords = {
            'freehold': 'Freehold',
            'leasehold': 'Leasehold'
        }
    
    def parse_query(self, query: str) -> Dict:
        """Extract prediction parameters from natural language."""
        
        query_lower = query.lower().strip()
        
        result = {
            "category": "house_price",
            "input_data": {},
            "missing_fields": []
        }
        
        postcode_match = re.search(r'\b([A-Z]{1,2}\d{1,2}[A-Z]?)\s*(\d[A-Z]{2})?\b', query.upper())
        if postcode_match:
            result["input_data"]["postcode"] = postcode_match.group(0)
        else:
            result["missing_fields"].append("postcode")
        
        found_type = False
        for keyword, prop_type in self.property_types.items():
            if keyword in query_lower:
                result["input_data"]["property_type"] = prop_type
                found_type = True
                break
        
        if not found_type:
            result["missing_fields"].append("property_type")
        
        found_tenure = False
        for keyword, tenure in self.tenure_keywords.items():
            if keyword in query_lower:
                result["input_data"]["tenure"] = tenure
                found_tenure = True
                break
        
        bedroom_match = re.search(r'(\d+)[\s-]*(bed|bedroom)', query_lower)
        if bedroom_match:
            result["input_data"]["bedrooms"] = int(bedroom_match.group(1))
        
        return result
    
    def extract_intent(self, query: str) -> str:
        """Determine what the user wants to do."""
        
        query = query.lower()
        
        if any(word in query for word in ['worth', 'value', 'price', 'cost', 'much', 'sell']):
            return "predict_price"
        elif any(word in query for word in ['compare', 'similar', 'nearby']):
            return "compare"
        elif any(word in query for word in ['what if', 'if i', 'renovate', 'improve']):
            return "scenario"
        else:
            return "predict_price"
    
    def get_missing_fields_prompt(self, missing: List[str]) -> str:
        """Generate a friendly prompt asking for missing information."""
        
        prompts = {
            "postcode": "📍 What's the postcode? (e.g., SW1A 1AA, M1 2AB)",
            "property_type": "🏠 What type? (detached, semi-detached, terraced, or flat)"
        }
        
        questions = [prompts.get(field, field) for field in missing]
        
        return "I'd love to help! I just need:\n\n" + "\n".join(questions)

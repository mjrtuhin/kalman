"""
NLP Agent - Extracts structured data from natural language queries.
"""

import re
from typing import Dict, Optional

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
        
        query = query.lower().strip()
        
        result = {
            "category": "house_price",
            "input_data": {}
        }
        
        # Extract postcode (e.g., SW1A 1AA, M1 1AA)
        postcode_match = re.search(r'\b([A-Z]{1,2}\d{1,2}[A-Z]?)\s*(\d[A-Z]{2})?\b', query.upper())
        if postcode_match:
            result["input_data"]["postcode"] = postcode_match.group(0)
        
        # Extract property type
        for keyword, prop_type in self.property_types.items():
            if keyword in query:
                result["input_data"]["property_type"] = prop_type
                break
        
        # Extract tenure
        for keyword, tenure in self.tenure_keywords.items():
            if keyword in query:
                result["input_data"]["tenure"] = tenure
                break
        
        # Extract bedrooms (e.g., "3 bed", "3-bed", "three bedroom")
        bedroom_match = re.search(r'(\d+)[\s-]*(bed|bedroom)', query)
        if bedroom_match:
            result["input_data"]["bedrooms"] = int(bedroom_match.group(1))
        
        # Default values if not found
        if "property_type" not in result["input_data"]:
            result["input_data"]["property_type"] = "Semi-Detached"
        
        if "tenure" not in result["input_data"]:
            result["input_data"]["tenure"] = "Freehold"
        
        return result
    
    def extract_intent(self, query: str) -> str:
        """Determine what the user wants to do."""
        
        query = query.lower()
        
        if any(word in query for word in ['worth', 'value', 'price', 'cost', 'much']):
            return "predict_price"
        elif any(word in query for word in ['compare', 'similar', 'nearby']):
            return "compare"
        elif any(word in query for word in ['what if', 'if i', 'renovate', 'improve']):
            return "scenario"
        else:
            return "predict_price"


def test_nlp():
    """Test NLP parsing."""
    
    print("="*70)
    print("Testing NLP Agent")
    print("="*70)
    
    agent = NLPAgent()
    
    test_queries = [
        "How much is a 3 bed semi in SW1A 1AA worth?",
        "What's the value of a terraced house in Manchester M1?",
        "Price for detached freehold in London",
        "I have a flat in Birmingham B1 2AA, what's it worth?"
    ]
    
    for query in test_queries:
        print(f"\n📝 Query: {query}")
        result = agent.parse_query(query)
        intent = agent.extract_intent(query)
        print(f"   Intent: {intent}")
        print(f"   Extracted: {result['input_data']}")
    
    print("\n✅ NLP Agent working!")


if __name__ == "__main__":
    test_nlp()

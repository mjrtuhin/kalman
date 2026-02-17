"""
Pydantic models for API requests and responses.
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime


class PredictionRequest(BaseModel):
    """Request model for prediction endpoint."""
    
    category: str = Field(..., description="Prediction category: house_price, business_viability, product_launch")
    type: str = Field(..., description="Specific type within category (e.g., 'general', 'restaurant')")
    
    # Common fields
    location: Optional[str] = Field(None, description="Postcode for location-based predictions")
    
    # House price specific
    property_type: Optional[str] = Field(None, description="D=Detached, S=Semi, T=Terraced, F=Flat")
    bedrooms: Optional[int] = Field(None, ge=1, le=20)
    floor_area: Optional[float] = Field(None, ge=10, le=1000, description="Floor area in m²")
    epc_rating: Optional[str] = Field(None, pattern="^[A-G]$")
    tenure: Optional[str] = Field(None, description="F=Freehold, L=Leasehold")
    
    # Business viability specific
    business_type: Optional[str] = Field(None, description="Type of business")
    startup_budget: Optional[float] = Field(None, ge=0)
    monthly_rent: Optional[float] = Field(None, ge=0)
    experience_years: Optional[int] = Field(None, ge=0, le=50)
    
    # Product launch specific
    product_category: Optional[str] = Field(None, description="Product category")
    target_price: Optional[float] = Field(None, ge=0)
    target_demographic: Optional[str] = None
    launch_channel: Optional[str] = Field(None, description="online, retail, both")
    
    class Config:
        json_schema_extra = {
            "example": {
                "category": "house_price",
                "type": "general",
                "location": "SW1A 1AA",
                "property_type": "S",
                "bedrooms": 3,
                "floor_area": 120.0,
                "epc_rating": "C",
                "tenure": "F"
            }
        }


class PredictionResponse(BaseModel):
    """Response model for prediction endpoint."""
    
    request_id: str
    timestamp: datetime
    category: str
    type: str
    
    prediction: float
    confidence_low: float
    confidence_high: float
    
    shap_values: Dict[str, Any]
    explanation: str
    
    comparables: Optional[List[Dict[str, Any]]] = None
    map_data: Optional[Dict[str, Any]] = None
    
    status: str = "success"
    warnings: Optional[List[str]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_123456",
                "timestamp": "2024-02-17T10:30:00Z",
                "category": "house_price",
                "type": "general",
                "prediction": 285000.0,
                "confidence_low": 270000.0,
                "confidence_high": 300000.0,
                "shap_values": {
                    "top_features": [
                        {"name": "location", "contribution": 12000},
                        {"name": "floor_area", "contribution": 8000}
                    ]
                },
                "explanation": "Your property is estimated at £285,000...",
                "status": "success"
            }
        }

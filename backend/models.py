"""
Pydantic models with Chat support.
"""

from pydantic import BaseModel
from typing import Optional, Dict, Any

class PredictionRequest(BaseModel):
    """Standard prediction request."""
    category: str
    input_data: Dict[str, Any]

class PredictionResponse(BaseModel):
    """Standard prediction response."""
    category: str
    prediction: float
    confidence_low: float
    confidence_high: float
    explanation: str
    metadata: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    """Natural language chat request."""
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    """Chat response with conversation tracking."""
    message: str
    prediction: Optional[float] = None
    confidence_low: Optional[float] = None
    confidence_high: Optional[float] = None
    conversation_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

"""
API routes for predictions.
"""

from fastapi import APIRouter, HTTPException
from backend.models import PredictionRequest, PredictionResponse
from backend.orchestrator import PredictionOrchestrator
import logging
from datetime import datetime
import uuid

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Generate prediction based on user input.
    
    Args:
        request: Prediction request with category, type, and relevant parameters
        
    Returns:
        Prediction response with results and explanation
    """
    logger.info(f"Prediction request: {request.category}/{request.type}")
    
    try:
        # Create orchestrator
        orchestrator = PredictionOrchestrator()
        
        # Execute prediction pipeline
        result = await orchestrator.execute(request)
        
        # Add metadata
        result["request_id"] = str(uuid.uuid4())
        result["timestamp"] = datetime.utcnow()
        result["category"] = request.category
        result["type"] = request.type
        
        return PredictionResponse(**result)
        
    except Exception as e:
        logger.error(f"Prediction failed: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/models")
async def list_models():
    """List available prediction models."""
    return {
        "models": [
            {
                "category": "house_price",
                "types": ["general"],
                "status": "planned"
            },
            {
                "category": "business_viability",
                "types": ["restaurant", "convenience_shop"],
                "status": "planned"
            },
            {
                "category": "product_launch",
                "types": ["energy_drink"],
                "status": "planned"
            }
        ]
    }

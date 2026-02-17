"""
Energy Performance Certificate (EPC) schema.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class EPCCertificate(BaseModel):
    """Schema for EPC Register data."""
    
    lmk_key: str = Field(description="Unique certificate identifier")
    address: str
    postcode: str
    current_energy_rating: str = Field(pattern="^[A-G]$", description="Current EPC rating A-G")
    potential_energy_rating: str = Field(pattern="^[A-G]$")
    current_energy_efficiency: int = Field(ge=0, le=100)
    total_floor_area: Optional[float] = Field(None, ge=0, description="Floor area in m²")
    property_type: str
    built_form: Optional[str] = None
    construction_age_band: Optional[str] = None
    lodgement_date: date
    
    class Config:
        json_schema_extra = {
            "example": {
                "lmk_key": "1234567890123456789012345678",
                "address": "10 DOWNING STREET, WESTMINSTER, LONDON, SW1A 1AA",
                "postcode": "SW1A 1AA",
                "current_energy_rating": "C",
                "potential_energy_rating": "B",
                "current_energy_efficiency": 72,
                "total_floor_area": 120.5,
                "property_type": "House",
                "built_form": "Semi-Detached",
                "construction_age_band": "1900-1929",
                "lodgement_date": "2023-06-15"
            }
        }

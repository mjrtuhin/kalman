"""
Postcodes.io API response schema.
"""

from pydantic import BaseModel, Field
from typing import Optional


class PostcodeData(BaseModel):
    """Schema for Postcodes.io data."""
    
    postcode: str
    latitude: float
    longitude: float
    region: Optional[str] = None
    district: Optional[str] = None
    lsoa: Optional[str] = Field(None, description="Lower Layer Super Output Area")
    msoa: Optional[str] = Field(None, description="Middle Layer Super Output Area")
    parliamentary_constituency: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "postcode": "SW1A 1AA",
                "latitude": 51.5033,
                "longitude": -0.1276,
                "region": "London",
                "district": "Westminster",
                "lsoa": "Westminster 018A",
                "msoa": "Westminster 018",
                "parliamentary_constituency": "Cities of London and Westminster"
            }
        }

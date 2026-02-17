"""
Land Registry Price Paid Data schema.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class LandRegistryPPD(BaseModel):
    """Schema for HM Land Registry Price Paid Data."""
    
    transaction_id: str
    price: float = Field(gt=0, description="Sale price in GBP")
    transaction_date: date
    postcode: str
    property_type: str = Field(pattern="^[DSTF]$", description="D=Detached, S=Semi, T=Terraced, F=Flat")
    old_new: str = Field(pattern="^[YN]$", description="Y=New build, N=Existing")
    duration: str = Field(pattern="^[FL]$", description="F=Freehold, L=Leasehold")
    paon: Optional[str] = Field(None, description="Primary Addressable Object Name")
    saon: Optional[str] = Field(None, description="Secondary Addressable Object Name")
    street: Optional[str] = None
    locality: Optional[str] = None
    town_city: Optional[str] = None
    district: Optional[str] = None
    county: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "transaction_id": "{12345678-1234-1234-1234-123456789012}",
                "price": 250000.0,
                "transaction_date": "2024-01-15",
                "postcode": "SW1A 1AA",
                "property_type": "S",
                "old_new": "N",
                "duration": "F",
                "paon": "10",
                "saon": None,
                "street": "DOWNING STREET",
                "locality": "WESTMINSTER",
                "town_city": "LONDON",
                "district": "CITY OF WESTMINSTER",
                "county": "GREATER LONDON"
            }
        }

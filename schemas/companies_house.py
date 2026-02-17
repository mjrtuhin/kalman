"""
Companies House data schema.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CompaniesHouseCompany(BaseModel):
    """Schema for Companies House company data."""
    
    company_number: str
    company_name: str
    company_status: str
    sic_code: str = Field(description="Standard Industrial Classification code")
    incorporation_date: Optional[date] = None
    dissolution_date: Optional[date] = None
    registered_address_postcode: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "company_number": "12345678",
                "company_name": "EXAMPLE RESTAURANT LTD",
                "company_status": "active",
                "sic_code": "56.10",
                "incorporation_date": "2020-01-15",
                "dissolution_date": None,
                "registered_address_postcode": "B1 1AA"
            }
        }

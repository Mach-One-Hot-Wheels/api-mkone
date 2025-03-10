from pydantic import BaseModel, Field, HttpUrl, UUID4
from typing import Optional, List
from datetime import datetime

class HotwheelsBase(BaseModel):
    """Base schema with common Hotwheels attributes"""
    model_name: str = Field(..., description="Name of the Hotwheels model", max_length=255)
    image_url: Optional[HttpUrl] = Field(None, description="URL to the model image")
    collector_number: Optional[str] = Field(None, description="Collector number", max_length=255)
    series_number: Optional[str] = Field(None, description="Series number", max_length=255)
    release_year: Optional[int] = Field(None, description="Year the model was released")
    series: Optional[str] = Field(None, description="Series name", max_length=255)
    color: Optional[str] = Field(None, description="Model color", max_length=255)
    tampo: Optional[str] = Field(None, description="Model tampo/decals", max_length=255)
    wheel_type: Optional[str] = Field(None, description="Type of wheels", max_length=100)
    base_type: Optional[str] = Field(None, description="Type of base", max_length=100)
    base_color: Optional[str] = Field(None, description="Color of the base", max_length=100)
    window_color: Optional[str] = Field(None, description="Color of windows", max_length=100)
    interior_color: Optional[str] = Field(None, description="Interior color", max_length=100)
    toy_number: Optional[str] = Field(None, description="Toy number", max_length=100)
    assortment_number: Optional[str] = Field(None, description="Assortment number", max_length=100)
    scale: Optional[str] = Field(None, description="Model scale", max_length=100)
    country: Optional[str] = Field(None, description="Country of manufacture", max_length=100)
    base_codes: Optional[str] = Field(None, description="Base codes", max_length=100)
    case_number: Optional[str] = Field(None, description="Case number", max_length=100)
    notes: Optional[str] = Field(None, description="Additional notes", max_length=1000)
    treasure_hunt_year: Optional[int] = Field(None, description="Year of treasure hunt designation")
    super_treasure_hunt_year: Optional[int] = Field(None, description="Year of super treasure hunt designation")

class HotwheelsCreate(HotwheelsBase):
    """Schema for creating a new Hotwheels model"""
    pass

class HotwheelsUpdate(BaseModel):
    """Schema for updating an existing Hotwheels model"""
    model_name: Optional[str] = Field(None, description="Name of the Hotwheels model", max_length=255)
    image_url: Optional[HttpUrl] = Field(None, description="URL to the model image")
    collector_number: Optional[str] = Field(None, description="Collector number", max_length=255)
    series_number: Optional[str] = Field(None, description="Series number", max_length=255)
    release_year: Optional[int] = Field(None, description="Year the model was released")
    series: Optional[str] = Field(None, description="Series name", max_length=255)
    color: Optional[str] = Field(None, description="Model color", max_length=255)
    tampo: Optional[str] = Field(None, description="Model tampo/decals", max_length=255)
    wheel_type: Optional[str] = Field(None, description="Type of wheels", max_length=100)
    base_type: Optional[str] = Field(None, description="Type of base", max_length=100)
    base_color: Optional[str] = Field(None, description="Color of the base", max_length=100)
    window_color: Optional[str] = Field(None, description="Color of windows", max_length=100)
    interior_color: Optional[str] = Field(None, description="Interior color", max_length=100)
    toy_number: Optional[str] = Field(None, description="Toy number", max_length=100)
    assortment_number: Optional[str] = Field(None, description="Assortment number", max_length=100)
    scale: Optional[str] = Field(None, description="Model scale", max_length=100)
    country: Optional[str] = Field(None, description="Country of manufacture", max_length=100)
    base_codes: Optional[str] = Field(None, description="Base codes", max_length=100)
    case_number: Optional[str] = Field(None, description="Case number", max_length=100)
    notes: Optional[str] = Field(None, description="Additional notes", max_length=1000)
    treasure_hunt_year: Optional[int] = Field(None, description="Year of treasure hunt designation")
    super_treasure_hunt_year: Optional[int] = Field(None, description="Year of super treasure hunt designation")

class HotwheelsResponse(HotwheelsBase):
    """Schema for Hotwheels response including DB fields"""
    id: UUID4
    created_at: datetime
    update_at: datetime
    
    class Config:
        orm_mode = True
        from_attributes = True

class HotwheelsSearchParams(BaseModel):
    """Schema for search parameters"""
    model_name: Optional[str] = None
    release_year: Optional[int] = None
    series: Optional[str] = None 
    color: Optional[str] = None
    treasure_hunt: Optional[bool] = None
    super_treasure_hunt: Optional[bool] = None

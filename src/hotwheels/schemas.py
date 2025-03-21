from pydantic import BaseModel, Field, HttpUrl, UUID4
from typing import List, Generic, TypeVar
from datetime import datetime

class HotwheelsBase(BaseModel):
    """Base schema with common Hotwheels attributes"""
    model_name: str = Field(..., description="Name of the Hotwheels model", max_length=255)
    image_url: HttpUrl | None = Field(None, description="URL to the model image")
    collector_number: str | None = Field(None, description="Collector number", max_length=255)
    series_number: str | None = Field(None, description="Series number", max_length=255)
    release_year: int | None = Field(None, description="Year the model was released")
    series: str | None = Field(None, description="Series name", max_length=255)
    color: str | None = Field(None, description="Model color", max_length=255)
    tampo: str | None = Field(None, description="Model tampo/decals", max_length=255)
    wheel_type: str | None = Field(None, description="Type of wheels", max_length=100)
    base_type: str | None = Field(None, description="Type of base", max_length=100)
    base_color: str | None = Field(None, description="Color of the base", max_length=100)
    window_color: str | None = Field(None, description="Color of windows", max_length=100)
    interior_color: str | None = Field(None, description="Interior color", max_length=100)
    toy_number: str | None = Field(None, description="Toy number", max_length=100)
    assortment_number: str | None = Field(None, description="Assortment number", max_length=100)
    scale: str | None = Field(None, description="Model scale", max_length=100)
    country: str | None = Field(None, description="Country of manufacture", max_length=100)
    base_codes: str | None = Field(None, description="Base codes", max_length=100)
    case_number: str | None = Field(None, description="Case number", max_length=100)
    notes: str | None = Field(None, description="Additional notes", max_length=1000)
    treasure_hunt_year: int | None = Field(None, description="Year of treasure hunt designation")
    super_treasure_hunt_year: int | None = Field(None, description="Year of super treasure hunt designation")

class HotwheelsCreate(HotwheelsBase):
    """Schema for creating a new Hotwheels model"""
    pass

class HotwheelsUpdate(BaseModel):
    """Schema for updating an existing Hotwheels model"""
    model_name: str | None = Field(None, description="Name of the Hotwheels model", max_length=255)
    image_url: HttpUrl | None = Field(None, description="URL to the model image")
    collector_number: str | None = Field(None, description="Collector number", max_length=255)
    series_number: str | None = Field(None, description="Series number", max_length=255)
    release_year: int | None = Field(None, description="Year the model was released")
    series: str | None = Field(None, description="Series name", max_length=255)
    color: str | None = Field(None, description="Model color", max_length=255)
    tampo: str | None = Field(None, description="Model tampo/decals", max_length=255)
    wheel_type: str | None = Field(None, description="Type of wheels", max_length=100)
    base_type: str | None = Field(None, description="Type of base", max_length=100)
    base_color: str | None = Field(None, description="Color of the base", max_length=100)
    window_color: str | None = Field(None, description="Color of windows", max_length=100)
    interior_color: str | None = Field(None, description="Interior color", max_length=100)
    toy_number: str | None = Field(None, description="Toy number", max_length=100)
    assortment_number: str | None = Field(None, description="Assortment number", max_length=100)
    scale: str | None = Field(None, description="Model scale", max_length=100)
    country: str | None = Field(None, description="Country of manufacture", max_length=100)
    base_codes: str | None = Field(None, description="Base codes", max_length=100)
    case_number: str | None = Field(None, description="Case number", max_length=100)
    notes: str | None = Field(None, description="Additional notes", max_length=1000)
    treasure_hunt_year: int | None = Field(None, description="Year of treasure hunt designation")
    super_treasure_hunt_year: int | None = Field(None, description="Year of super treasure hunt designation")

class HotwheelsResponse(HotwheelsBase):
    """Schema for Hotwheels response including DB fields"""
    id: UUID4
    created_at: datetime
    update_at: datetime
    
    class Config:
        from_attributes = True

class HotwheelsSearchParams(BaseModel):
    """Schema for search parameters"""
    model_name: str | None = None
    release_year: int | None = None
    series: str | None = None 
    color: str | None = None
    treasure_hunt: bool | None = None
    super_treasure_hunt: bool | None = None

class HotwheelsSearchResponse(BaseModel):
    id: UUID4
    model_name: str
    image_url: str | None
    series: str | None
    color: str | None
    release_year: int | None

class PaginationMeta(BaseModel):
    """Metadata for pagination"""
    total_items: int
    total_pages: int
    current_page: int
    page_size: int
    has_next: bool
    has_prev: bool

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response with items and metadata"""
    items: List[T]
    meta: PaginationMeta
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.user_hotwheels.models import UserHotwheelsModality
from decimal import Decimal

class UserHotwheelsCreate(BaseModel):
    user_id: UUID
    hotwheels_id: UUID

class UserHotwheelsResponse(BaseModel):
    user_id: UUID
    hotwheels_id: UUID
    modality: UserHotwheelsModality
    favorite: bool
    price: Decimal
    description: str | None = None
    sold: bool
    quantity: int
    visit_count: int
    is_negotiable: bool
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class UserHotwheelsListResponse(BaseModel):
    total: int
    items: list[UserHotwheelsResponse]

class UserHotwheelsUpdate(BaseModel):
    modality: UserHotwheelsModality | None = None
    price: Decimal | None = None
    description: str | None = None
    sold: bool | None = None
    is_negotiable: bool | None = None
    quantity: int | None = None
    favorite: bool | None = None
    visit_count: int | None = None

class HotwheelsCardInfo(BaseModel):
    # Hotwheels info
    id: UUID
    model_name: str
    image_url: str
    collector_number: str | None = None
    series: str | None = None
    color: str | None = None
    release_year: int | None = None
    
    # UserHotwheels info
    modality: UserHotwheelsModality
    favorite: bool
    price: Decimal
    description: str | None = None
    sold: bool
    quantity: int
    is_negotiable: bool
    visit_count: int
    
    class Config:
        from_attributes = True

class UserHotwheelsCardListResponse(BaseModel):
    total: int
    items: list[HotwheelsCardInfo]
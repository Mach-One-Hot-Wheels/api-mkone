from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.user_hotwheels.models import UserHotwheelsModality

class UserHotwheelsCreate(BaseModel):
    user_id: UUID
    hotwheels_id: UUID

class UserHotwheelsResponse(BaseModel):
    id: UUID
    user_id: UUID
    hotwheels_id: UUID
    modality: UserHotwheelsModality
    favorite: bool
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

class UserHotwheelsListResponse(BaseModel):
    total: int
    items: list[UserHotwheelsResponse]
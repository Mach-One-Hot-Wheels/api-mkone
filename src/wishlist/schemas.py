from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class WishlistCreate(BaseModel):
    user_id: UUID
    hotwheels_id: UUID

class WishlistResponse(BaseModel):
    user_id: UUID
    hotwheels_id: UUID
    created_at: datetime
    update_at: datetime

    class Config:
        from_attributes = True

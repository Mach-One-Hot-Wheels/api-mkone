from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.auth.models import UserRole
from typing import Optional, Dict

class UserResponse(BaseModel):
    id: UUID
    avatar_url: Optional[str]
    name: Optional[str]
    bio: Optional[str]
    nickname: str
    phone: Optional[str]
    social_networks: Optional[Dict]
    role: UserRole
    email: str
    is_active: bool
    visit_count: int
    created_at: datetime
    updated_at: datetime
    last_seen: datetime

    class Config:
        from_attributes = True

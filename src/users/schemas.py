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

class UserUpdate(BaseModel):
    avatar_url: Optional[str] = None
    name: Optional[str] = None
    bio: Optional[str] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    social_networks: Optional[Dict] = None
    email: Optional[str] = None
    is_active: Optional[bool] = None
    visit_count: Optional[int] = None
    last_seen: Optional[datetime] = None
    role: Optional[UserRole] = None
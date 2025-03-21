from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from src.auth.models import UserRole
from typing import Dict
from typing import Optional

class UserResponse(BaseModel):
    id: UUID
    avatar_url: str | None
    name: str | None
    bio: str | None
    nickname: str
    phone: str | None
    social_networks: Dict | None
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
    avatar_url: str | None = None
    name: str | None = None
    bio: str | None = None
    nickname: str | None = None
    phone: str | None = None
    social_networks: Dict | None = None
    email: str | None = None
    is_active: bool | None = None
    visit_count: int | None = None
    last_seen: datetime | None = None
    role: UserRole | None
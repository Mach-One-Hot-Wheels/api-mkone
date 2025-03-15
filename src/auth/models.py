from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, TIMESTAMP, JSON, Index, Boolean, Enum, UUID
from sqlalchemy.sql import func
from uuid import uuid4
import enum
from src.base import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    USER = "user"

class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    avatar_url = Column(String(255)) 
    name = Column(String(100))
    bio = Column(String(500))
    nickname = Column(String(50), unique=True)
    phone = Column(String(20))
    social_networks = Column(JSON) 
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    visit_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    last_seen = Column(TIMESTAMP, server_default=func.now())
    
    wishlists = relationship("Wishlist", back_populates="user")
    user_hotwheels = relationship("UserHotwheels", back_populates="user")
    collections = relationship("Collection", back_populates="user")
    
    __table_args__ = (
        Index('idx_user_email', email),
        Index('idx_user_role', role),
    )
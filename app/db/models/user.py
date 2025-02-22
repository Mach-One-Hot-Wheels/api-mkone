from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.sql import func
from ..database import Base

class User(Base):
    __tablename__ = "user_data"

    id = Column(Integer, primary_key=True, index=True)
    avatar_url = Column(String(255))
    email = Column(String(255), unique=True)
    nome = Column(String(255))
    bio = Column(Text)
    nickname = Column(String(255), unique=True)
    phone = Column(String(20))
    password = Column(String(255))
    social_networks = Column(JSON)
    role = Column(String(50))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

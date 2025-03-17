from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, UUID, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from uuid import uuid4
from src.base import Base


class Wishlist(Base):
    __tablename__ = "wishlist"
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)
    hotwheels_id = Column(UUID(as_uuid=True), ForeignKey('hotwheels.id'), primary_key=True)
    
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="wishlists")
    hotwheels = relationship("Hotwheels", back_populates="wishlists")
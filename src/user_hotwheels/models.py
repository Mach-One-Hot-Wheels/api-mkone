from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Boolean, Enum, DECIMAL, Integer
from sqlalchemy.sql import func
from uuid import uuid4
from src.base import Base
import enum

class UserHotwheelsModality(enum.Enum):
    COLLECTION = "collection"
    SALE = "sale"
    TRADE = "trade"


class UserHotwheels(Base):
    __tablename__ = "user_hotwheels"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    hotwheels_id = Column(UUID(as_uuid=True), ForeignKey("hotwheels.id"), nullable=False)
    modality = Column(Enum(UserHotwheelsModality), nullable=False, default=UserHotwheelsModality.COLLECTION)
    favorite = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="user_hotwheels")
    hotwheels = relationship("Hotwheels", back_populates="user_hotwheels")
    user_hotwheels_sale = relationship("UserHotwheelsSale", back_populates="user_hotwheels")

class UserHotwheelsSale(Base):
    __tablename__ = "user_hotwheels_sale"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_hotwheels_id = Column(UUID(as_uuid=True), ForeignKey("user_hotwheels.id"), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    description = Column(String(1000))
    sold = Column(Boolean, default=False)
    visit_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user_hotwheels = relationship("UserHotwheels", back_populates="user_hotwheels_sale")
    
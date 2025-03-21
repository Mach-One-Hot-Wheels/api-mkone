from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, UUID, TIMESTAMP, ForeignKey, Boolean, Enum, DECIMAL, Integer
from sqlalchemy.sql import func
from src.base import Base
import enum

class UserHotwheelsModality(enum.Enum):
    COLLECTION = "collection"
    SALE = "sale"


class UserHotwheels(Base):
    __tablename__ = "user_hotwheels"

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, primary_key=True)
    hotwheels_id = Column(UUID(as_uuid=True), ForeignKey("hotwheels.id"), nullable=False, primary_key=True)
    modality = Column(Enum(UserHotwheelsModality), nullable=False, default=UserHotwheelsModality.COLLECTION)
    favorite = Column(Boolean, default=False)
    price = Column(DECIMAL(10, 2), default=0.0, nullable=False)
    description = Column(String(1000), nullable=True)
    sold = Column(Boolean, default=False)
    quantity = Column(Integer, default=1, nullable=False)
    visit_count = Column(Integer, default=0, nullable=False)
    is_negotiable = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="user_hotwheels")
    hotwheels = relationship("Hotwheels", back_populates="user_hotwheels")
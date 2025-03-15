from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, UUID, TIMESTAMP, Index
from sqlalchemy.sql import func
from uuid import uuid4
from src.base import Base


class Hotwheels(Base):
    __tablename__ = "hotwheels"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    model_name = Column(String(255))
    image_url = Column(String(255))
    collector_number = Column(String(255))
    series_number = Column(String(255))
    release_year = Column(Integer)
    series = Column(String(255))
    color = Column(String(255))
    tampo = Column(String(255))
    wheel_type = Column(String(100))
    base_type = Column(String(100))
    base_color = Column(String(100))
    window_color = Column(String(100))
    interior_color = Column(String(100))
    toy_number = Column(String(100))
    assortment_number = Column(String(100))
    scale = Column(String(100))
    country = Column(String(100))
    base_codes = Column(String(100))
    case_number = Column(String(100))
    notes = Column(String(1000))
    treasure_hunt_year = Column(Integer)
    super_treasure_hunt_year = Column(Integer)
    visit_count = Column(Integer, default=0, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    wishlists = relationship("Wishlist", back_populates="hotwheels")
    user_hotwheels = relationship("UserHotwheels", back_populates="hotwheels")
    collections_items = relationship("CollectionItem", back_populates="hotwheels")
    
    __table_args__ = (
        Index('idx_hotwheels_model_name', model_name),
    )
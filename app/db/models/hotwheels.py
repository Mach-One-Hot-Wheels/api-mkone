from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from ..database import Base

class Hotwheels(Base):
    __tablename__ = "hotwheels"

    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255))
    image_url = Column(String(255))
    collector_number = Column(String(50))
    series_number = Column(String(50))
    release_year = Column(Integer)
    series = Column(String(255))
    color = Column(String(50))
    tampo = Column(String(255))
    wheel_type = Column(String(100))
    base_type = Column(String(100))
    base_color = Column(String(50))
    window_color = Column(String(50))
    interior_color = Column(String(50))
    toy_number = Column(String(50))
    assortment_number = Column(String(50))
    scale = Column(String(50))
    country = Column(String(100))
    base_codes = Column(String(255))
    case_number = Column(String(50))
    notes = Column(Text)
    treasure_hunt_year = Column(Integer)
    super_treasure_hunt_year = Column(Integer)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from ..database import Base

class UserHotwheels(Base):
    __tablename__ = "user_hotwheels"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_data.id', ondelete='CASCADE'))
    hotwheels_id = Column(Integer, ForeignKey('hotwheels.id', ondelete='CASCADE'))
    modality = Column(String(50))
    favorite = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class Collection(Base):
    __tablename__ = "collections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_data.id', ondelete='CASCADE'))
    title = Column(String(255), nullable=False)
    display_order = Column(Integer, nullable=False)

class CollectionItem(Base):
    __tablename__ = "collection_items"

    id = Column(Integer, primary_key=True, index=True)
    collection_id = Column(Integer, ForeignKey('collections.id', ondelete='CASCADE'))
    hotwheels_id = Column(Integer, ForeignKey('hotwheels.id', ondelete='CASCADE'))
    position = Column(Integer)

class Wishlist(Base):
    __tablename__ = "wishlist"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user_data.id', ondelete='CASCADE'))
    hotwheels_id = Column(Integer, ForeignKey('hotwheels.id', ondelete='CASCADE'))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class UserHotwheelsSale(Base):
    __tablename__ = "user_hotwheels_sale"

    id = Column(Integer, primary_key=True, index=True)
    user_hotwheels_id = Column(Integer, ForeignKey('user_hotwheels.id', ondelete='CASCADE'))
    price = Column(Numeric(10, 2))

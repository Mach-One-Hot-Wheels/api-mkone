from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, UUID, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from uuid import uuid4
from src.base import Base


class Collection(Base):
    __tablename__ = "collection"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    display_order = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    __table_args__ = (
        UniqueConstraint('user_id', 'display_order', name='unique_user_display_order'),
    )
    
    user = relationship("User", back_populates="collections")
    items = relationship("CollectionItem", back_populates="collection")
    
class CollectionItem(Base):
    __tablename__ = "collection_item"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    collection_id = Column(UUID(as_uuid=True), ForeignKey('collection.id'), nullable=False)
    hotwheel_id = Column(UUID(as_uuid=True), ForeignKey('hotwheels.id'), nullable=False)
    position = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    update_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
    
    collection = relationship("Collection", back_populates="items")
    hotwheels = relationship("Hotwheels", back_populates="collections_items")
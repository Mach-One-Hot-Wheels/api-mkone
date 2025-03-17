from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from src.database import get_session
from src.wishlist.models import Wishlist
from src.wishlist.schemas import WishlistCreate, WishlistResponse
from src.hotwheels.schemas import HotwheelsSearchResponse
from src.hotwheels.models import Hotwheels
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=WishlistResponse)
def create_wishlist_item(wishlist: WishlistCreate, db: Session = Depends(get_session)):
    db_wishlist = Wishlist(
        user_id=wishlist.user_id,
        hotwheels_id=wishlist.hotwheels_id
    )
    db.add(db_wishlist)
    try:
        db.commit()
        db.refresh(db_wishlist)
        return db_wishlist
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Item already exists in wishlist or invalid IDs"
        )

@router.delete("/{user_id}/{hotwheels_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_wishlist_item(user_id: UUID, hotwheels_id: UUID, db: Session = Depends(get_session)):
    wishlist_item = db.query(Wishlist).filter(Wishlist.user_id == user_id, Wishlist.hotwheels_id == hotwheels_id).first()
    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )
    
    db.delete(wishlist_item)
    db.commit()
    return None

@router.get("/check")
def check_wishlist_item(user_id: UUID, hotwheels_id: UUID, db: Session = Depends(get_session)):
    wishlist_item = db.query(Wishlist).filter(
        Wishlist.user_id == user_id,
        Wishlist.hotwheels_id == hotwheels_id
    ).first()
    
    return {"exists": wishlist_item is not None}

@router.get("/user/{user_id}", response_model=List[HotwheelsSearchResponse])
def get_user_wishlist(user_id: UUID, db: Session = Depends(get_session)):
    wishlist_items = db.query(
        Hotwheels.id,
        Hotwheels.model_name,
        Hotwheels.image_url,
        Hotwheels.series,
        Hotwheels.color,
        Hotwheels.release_year
    ).join(
        Wishlist, Wishlist.hotwheels_id == Hotwheels.id
    ).filter(
        Wishlist.user_id == user_id
    ).all()
    
    return wishlist_items


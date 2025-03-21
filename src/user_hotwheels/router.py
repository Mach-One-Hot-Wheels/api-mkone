from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.user_hotwheels.schemas import (
    UserHotwheelsCreate,
    UserHotwheelsResponse,
    UserHotwheelsListResponse,
    UserHotwheelsUpdate,
    HotwheelsCardInfo,
    UserHotwheelsCardListResponse,
)
from src.user_hotwheels.models import UserHotwheels
from src.hotwheels.models import Hotwheels
from src.database import get_session
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=UserHotwheelsResponse)
async def create_user_hotwheels(
    user_hotwheels: UserHotwheelsCreate, db: Session = Depends(get_session)
):
    # Check if the combination already exists
    existing = (
        db.query(UserHotwheels)
        .filter(
            UserHotwheels.user_id == user_hotwheels.user_id,
            UserHotwheels.hotwheels_id == user_hotwheels.hotwheels_id,
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This Hot Wheels is already registered for this user",
        )

    try:
        db_user_hotwheels = UserHotwheels(**user_hotwheels.model_dump())
        db.add(db_user_hotwheels)
        db.commit()
        db.refresh(db_user_hotwheels)
        return db_user_hotwheels

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user_id or hotwheels_id",
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while creating the record",
        )


@router.get("/user/{user_id}", response_model=UserHotwheelsListResponse)
async def get_user_hotwheels(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    total = db.query(UserHotwheels).filter(UserHotwheels.user_id == user_id).count()
    items = (
        db.query(UserHotwheels)
        .filter(UserHotwheels.user_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {"total": total, "items": items}


@router.get("/hotwheels/{hotwheels_id}", response_model=UserHotwheelsListResponse)
async def get_hotwheels_users(
    hotwheels_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    total = (
        db.query(UserHotwheels)
        .filter(UserHotwheels.hotwheels_id == hotwheels_id)
        .count()
    )
    items = (
        db.query(UserHotwheels)
        .filter(UserHotwheels.hotwheels_id == hotwheels_id)
        .offset(skip)
        .limit(limit)
        .all()
    )

    return {"total": total, "items": items}


@router.get("/check/{user_id}/{hotwheels_id}", response_model=UserHotwheelsResponse)
async def check_user_has_hotwheels(
    user_id: UUID,
    hotwheels_id: UUID,
    db: Session = Depends(get_session),
):
    exists = (
        db.query(UserHotwheels)
        .filter(
            UserHotwheels.user_id == user_id,
            UserHotwheels.hotwheels_id == hotwheels_id,
        )
        .first()
    )
    
    if not exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="UserHotwheels item not found",
        )
        
    return exists


@router.delete("/{user_id}/{hotwheels_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_hotwheels_item(
    user_id: UUID, hotwheels_id: UUID, db: Session = Depends(get_session)
):
    user_hotwheels_item = (
        db.query(UserHotwheels)
        .filter(
            UserHotwheels.user_id == user_id, UserHotwheels.hotwheels_id == hotwheels_id
        )
        .first()
    )
    if not user_hotwheels_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="UserHotwheels item not found"
        )

    db.delete(user_hotwheels_item)
    db.commit()
    return None


@router.patch("/{user_id}/{hotwheels_id}", response_model=UserHotwheelsResponse)
async def update_user_hotwheels(
    user_id: UUID,
    hotwheels_id: UUID,
    update_data: UserHotwheelsUpdate,
    db: Session = Depends(get_session)
):
    # Check if the item exists
    user_hotwheels_item = (
        db.query(UserHotwheels)
        .filter(
            UserHotwheels.user_id == user_id, 
            UserHotwheels.hotwheels_id == hotwheels_id
        )
        .first()
    )
    
    if not user_hotwheels_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="UserHotwheels item not found"
        )
    
    # Get non-None values from update_data
    update_values = {k: v for k, v in update_data.model_dump().items() if v is not None}
    
    if not update_values:
        return user_hotwheels_item  # Nothing to update
    
    try:
        # Update only the provided fields
        for key, value in update_values.items():
            setattr(user_hotwheels_item, key, value)
            
        db.commit()
        db.refresh(user_hotwheels_item)
        return user_hotwheels_item
        
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the record: {str(e)}"
        )


@router.get("/user/{user_id}/cards", response_model=UserHotwheelsCardListResponse)
async def get_user_hotwheels_cards(
    user_id: UUID,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_session),
):
    """
    Get all hotwheels card information for a specific user.
    Returns combined data from UserHotwheels and Hotwheels tables.
    """
    query = (
        db.query(UserHotwheels, Hotwheels)
        .join(Hotwheels, UserHotwheels.hotwheels_id == Hotwheels.id)
        .filter(UserHotwheels.user_id == user_id)
    )
    
    total = query.count()
    results = query.offset(skip).limit(limit).all()
    
    # Combine the data from both tables
    items = []
    for user_hw, hw in results:
        card_info = {
            # Hotwheels info
            "id": hw.id,
            "model_name": hw.model_name,
            "image_url": hw.image_url,
            "collector_number": hw.collector_number,
            "series": hw.series,
            "color": hw.color,
            "release_year": hw.release_year,
            
            # UserHotwheels info
            "modality": user_hw.modality,
            "favorite": user_hw.favorite,
            "price": user_hw.price,
            "description": user_hw.description,
            "sold": user_hw.sold,
            "quantity": user_hw.quantity,
            "is_negotiable": user_hw.is_negotiable,
            "visit_count": user_hw.visit_count,
        }
        items.append(card_info)
    
    return {"total": total, "items": items}

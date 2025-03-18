from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from src.user_hotwheels.schemas import (
    UserHotwheelsCreate,
    UserHotwheelsResponse,
    UserHotwheelsListResponse,
)
from src.user_hotwheels.models import UserHotwheels
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


@router.get("/check/{user_id}/{hotwheels_id}")
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
        is not None
    )

    return {"exists": exists}


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

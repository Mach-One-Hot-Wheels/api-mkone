from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import get_session
from src.auth.models import User
from src.auth.router import get_current_user
from .schemas import UserResponse, UserUpdate
from uuid import UUID

router = APIRouter()


@router.get("/{user_id}", response_model=UserResponse)
def get_current_user(user_id: UUID, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_session),
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user_update.email and user_update.email != user.email:
        existing_email = db.execute(
            select(User).where(User.email == user_update.email)
        ).first()
        if existing_email:
            raise HTTPException(status_code=409, detail="Email already registered")

    if user_update.nickname and user_update.nickname != user.nickname:
        existing_nickname = db.execute(
            select(User).where(User.nickname == user_update.nickname)
        ).first()
        if existing_nickname:
            raise HTTPException(status_code=409, detail="Nickname already taken")

    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    db.commit()
    db.refresh(user)
    return user

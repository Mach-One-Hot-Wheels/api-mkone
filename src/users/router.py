from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.database import get_session
from src.auth.models import User
from .schemas import UserResponse
from uuid import UUID

router = APIRouter()

@router.get("/{user_id}", response_model=UserResponse)
def get_current_user(user_id: UUID, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
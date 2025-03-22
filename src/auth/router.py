from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import get_session
from src.auth.models import User
from src.auth.schemas import UserLogin, UserRegister, UserPublic, TokenResponse
from src.auth.utils import (
    hash_password,
    encode_jwt,
    verify_password,
    generate_payload,
    decode_jwt,
)
from src.auth.service import AuthenticationService
from src.auth.dependencies import get_auth_service

security = HTTPBearer()
router = APIRouter()

@router.post("/register", response_model=TokenResponse)
def register(
    user: UserRegister,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    user_db, token = auth_service.register(user)
    return {
        "user": UserPublic(id=user_db.id, email=user_db.email, nickname=user_db.nickname),
        "token": token
    }

@router.post("/login", response_model=TokenResponse)
def login(
    user: UserLogin,
    auth_service: AuthenticationService = Depends(get_auth_service)
):
    user_db, token = auth_service.login(user)
    return {
        "user": UserPublic(id=user_db.id, email=user_db.email, nickname=user_db.nickname),
        "token": token
    }

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session)
):
    try:
        token = credentials.credentials

        payload = decode_jwt(token)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")

        user = session.execute(select(User).where(User.id == user_id)).scalars().first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")

        return user
    except Exception as e:
        raise HTTPException(
            status_code=401, detail="Invalid authentication credentials"
        )


@router.get("/me", response_model=UserPublic)
async def get_me(
    current_user: User = Depends(get_current_user)
):
    return UserPublic(
        id=current_user.id, email=current_user.email, nickname=current_user.nickname
    )
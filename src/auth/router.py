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

security = HTTPBearer()
router = APIRouter()




@router.post("/register", response_model=TokenResponse)
def register(
    user: UserRegister, session: Session = Depends(get_session)
):
    result = session.execute(select(User).where(User.email == user.email)).first()
    if result:
        raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

    result2 = session.execute(
        select(User).where(User.nickname == user.nickname)
    ).first()
    if result2:
        raise HTTPException(status_code=409, detail="Apelido já cadastrado.")

    user.password = hash_password(user.password)

    user_db = User(**user.model_dump())
    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    payload = generate_payload(user_db)
    token = encode_jwt(payload)

    return {
        "user": UserPublic(id=user_db.id, email=user_db.email, nickname=user_db.nickname),
        "token": token
    }


@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    user_db = session.execute(statement).scalars().first()

    if user_db and verify_password(user.password, user_db.password):
        payload = generate_payload(user_db)
        token = encode_jwt(payload)

        return {
            "user": UserPublic(id=user_db.id, email=user_db.email, nickname=user_db.nickname),
            "token": token
        }

    raise HTTPException(status_code=401, detail="E-mail e/ou senha inválidas.")

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
async def get_me(current_user: User = Depends(get_current_user)):
    return UserPublic(
        id=current_user.id, email=current_user.email, nickname=current_user.nickname
    )
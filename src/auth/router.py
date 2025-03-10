from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.database import get_session
from src.auth.models import User
from src.auth.schemas import UserLogin, UserRegister, UserPublic
from src.auth.utils import hash_password, encode_jwt, verify_password, generate_payload


router = APIRouter()


@router.post("/register", response_model=UserPublic)
def register(
    user: UserRegister, response: Response, session: Session = Depends(get_session)
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
    jwt = encode_jwt(payload)
    response.set_cookie(
        key="token", value=jwt, max_age=60 * 60, httponly=True, samesite="strict"
    )

    return user_db


@router.post("/login", response_model=UserPublic)
def login(user: UserLogin, response: Response, session: Session = Depends(get_session)):
    statement = select(User).where(User.email == user.email)
    user_db = session.execute(statement).scalars().first()
    if user_db and verify_password(user.password, user_db.password):
        payload = generate_payload(user_db)
        jwt = encode_jwt(payload)
        response.set_cookie(
            key="token", value=jwt, max_age=60 * 60, httponly=True, samesite="strict"
        )
        return UserPublic(id=user_db.id, email=user_db.email)
    raise HTTPException(status_code=401, detail="E-mail e/ou senha inválidas.")

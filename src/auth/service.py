from typing import Protocol
from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException

from src.auth.models import User
from src.auth.schemas import UserLogin, UserRegister, UserPublic, TokenResponse
from src.auth.utils import hash_password, verify_password, generate_payload, encode_jwt


class AuthenticationService(Protocol):
    """
    Interface para os serviços de autenticação:
    
    Register -- cadastro de usuário
    Login -- login de usuário
    """

    def register(self, user: UserRegister) -> tuple[User, str]: ...

    def login(self, user: UserLogin) -> tuple[User, str]: ...


class SQLAlchemyAuthService:
    """Implementação dos serviços de autenticação."""

    def __init__(self, session: Session):
        """Inicializa o serviço com uma sessão do banco de dados."""
        self.session = session

    def register(self, user: UserRegister) -> tuple[User, str]:
        """Registra um novo usuário no banco de dados."""
        result = self.session.execute(
            select(User).where(User.email == user.email)
        ).first()
        if result:
            """Verifica se o e-mail já está cadastrado."""
            raise HTTPException(status_code=409, detail="E-mail já cadastrado.")

        result2 = self.session.execute(
            select(User).where(User.nickname == user.nickname)
        ).first()
        if result2:
            """Verifica se o apelido já está cadastrado."""
            raise HTTPException(status_code=409, detail="Apelido já cadastrado.")

        user.password = hash_password(user.password)
        user_db = User(**user.model_dump())

        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)

        payload = generate_payload(user_db)
        token = encode_jwt(payload)

        return user_db, token

    def login(self, user: UserLogin) -> tuple[User, str]:
        """Realiza o login de um usuário no sistema"""
        statement = select(User).where(User.email == user.email)
        user_db = self.session.execute(statement).scalars().first()

        if user_db and verify_password(user.password, user_db.password):
            """Verifica se o usuário existe e se a senha está correta."""
            payload = generate_payload(user_db)
            token = encode_jwt(payload)
            return user_db, token

        """Caso o usuário não exista ou a senha esteja incorreta."""
        raise HTTPException(status_code=401, detail="E-mail e/ou senha inválidas.")

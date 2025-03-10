import bcrypt
from dotenv import load_dotenv
import os
import jwt
from datetime import datetime, timedelta, timezone
from uuid import uuid4

load_dotenv()

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def hash_password(password: str) -> str:
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(
        bytes(password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )


def encode_jwt(payload):
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_jwt(token):
    return jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)


def generate_payload(user_db):
    payload = {
        "sub": str(user_db.id),
        "role": str(user_db.role.value),
        "email": user_db.email,
        "iat": datetime.now(timezone.utc).timestamp(),
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        "jti": str(uuid4()),
    }
    return payload

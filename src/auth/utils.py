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
    """
    Realiza o hash de senha usando bcrypt diretamente.
    
    Args:
        password (str): Senha a passar pelo hasher.
        
    Returns:
        str: Senha hasheada.
    """
    return bcrypt.hashpw(
        bytes(password, encoding="utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    """
    Verifica se a senha passada é igual a senha armazenada no banco de dados.
    
    Args:
        password (str): Senha a ser verificada.
        hashed_password (str): Senha armazenada no banco.
        
    Returns:
        bool: True se a senha for igual, False caso contrário.
    """
    return bcrypt.checkpw(
        bytes(password, encoding="utf-8"),
        bytes(hashed_password, encoding="utf-8"),
    )


def encode_jwt(payload):
    """
    Codifica o JWT com variáveis de ambiente.
    
    Args:
        payload (dict): Payload a ser codificado.
        
    Returns:
        str: Token JWT gerado.
    """
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)


def decode_jwt(token):
    """
    Decodifica o JWT com variáveis de ambiente.
    
    Args:
        token (str): token a ser decodificado.
    """
    return jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)


def generate_payload(user_db):
    """
    Gera o payload para o JWT.
    
    Args:
        user_db (User): Usuário do banco a ser codificado.
        
    Returns:
        dict: Payload gerado.
    """
    payload = {
        "sub": str(user_db.id),
        "role": str(user_db.role.value),
        "email": user_db.email,
        "iat": datetime.now(timezone.utc).timestamp(),
        "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        "jti": str(uuid4()),
    }
    return payload

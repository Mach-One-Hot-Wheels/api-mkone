from fastapi import Request, Depends, HTTPException, Response
from typing import Annotated, Any
from src.auth.utils import decode_jwt
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database import get_session
from src.auth.service import AuthenticationService, SQLAlchemyAuthService

def get_token_info(request: Request, response: Response):
    token = request.cookies.get("token")
    if token == None:
        return token
    try:
        payload = decode_jwt(token)
        print(payload)
        return payload
    except Exception as e:
        response.delete_cookie("token")
        return None
    
    
UserDependecie = Annotated[Any, Depends(get_token_info)]

def get_auth_service(
    session: Session = Depends(get_session)
) -> AuthenticationService:
    return SQLAlchemyAuthService(session)
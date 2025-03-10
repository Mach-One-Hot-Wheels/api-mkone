from pydantic import BaseModel, EmailStr, UUID4


class UserRegister(BaseModel):
    email: EmailStr
    nickname: str
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: UUID4
    email: EmailStr
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.enums.roles import Roles


class UserBase(BaseModel):
    email: EmailStr
    is_superuser: bool = False


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(UserBase):
    password: str
    role: Optional[Roles]


class UserAddUpdate(UserBase):
    role: Roles


class ShowUser(UserBase):
    id: Optional[int] = None
    email: EmailStr
    role: str

    class Config:
        orm_mode = True

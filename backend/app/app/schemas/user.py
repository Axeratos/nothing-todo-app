from pydantic import BaseModel, EmailStr

from .base import BaseDBSchema


class UserBase(BaseModel):
    email: EmailStr | None
    username: str | None
    password: str | None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str


class UserLogin(UserBase):
    login: str | EmailStr
    password: str


class UserUpdate(UserBase):
    pass


class UserDB(UserBase, BaseDBSchema):
    email: EmailStr
    username: str

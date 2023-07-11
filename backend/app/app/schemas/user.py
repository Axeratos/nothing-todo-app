from pydantic import BaseModel, EmailStr

from .base import BaseDBSchema
from ..core.security import hash_password


class UserBase(BaseModel):
    email: EmailStr | None
    username: str | None
    password: str | None


class UserCreate(UserBase):
    email: EmailStr
    username: str
    password: str

    def hash_password(self):
        self.password = hash_password(self.password)


class UserUpdate(UserBase):
    pass


class UserDB(UserBase, BaseDBSchema):
    email: EmailStr
    username: str

from sqlalchemy import String
from sqlalchemy.orm import Mapped, validates, mapped_column

from .base_model import Base


class User(Base):
    __tablename__ = "user"
    email: Mapped[str] = mapped_column(String, unique=True)
    username: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str]
    is_verified: Mapped[bool] = mapped_column(default=True)

    @validates("password")
    def validate_password(self, key, password):
        if 8 > len(password):
            raise ValueError("password is too short")
        return password

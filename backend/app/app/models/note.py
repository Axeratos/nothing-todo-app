from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column

from .base_model import Base
from app.models import User


class Note(Base):
    __tablename__ = "note"
    text: Mapped[str]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship(back_populates="tasks")

from datetime import date, time
from typing import Optional

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base_model import Base
from app.models import User


class Task(Base):
    __tablename__ = "task"
    title: Mapped[str] = mapped_column(String(100))
    deadline_date: Mapped[date]
    deadline_time: Mapped[Optional[time]]
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    owner: Mapped[User] = relationship(back_populates="tasks")

from datetime import date, time
from typing import Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Task(Base):
    title: Mapped[str] = mapped_column(String(100))
    deadline_date: Mapped[date]
    deadline_time: Mapped[Optional[time]]

from sqlalchemy.orm import Mapped

from app.db import Base


class Note(Base):
    text: Mapped[str]


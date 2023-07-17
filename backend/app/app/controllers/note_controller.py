from sqlalchemy.ext.asyncio import AsyncSession

from app.mixins.controller import OwnerOperationsMixin
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate
from .base_controller import BaseDatabaseController


class NoteDatabaseController(BaseDatabaseController[Note, NoteCreate, NoteUpdate], OwnerOperationsMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(Note, session)

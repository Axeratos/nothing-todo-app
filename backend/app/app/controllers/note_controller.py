from app.mixins.controller import OwnerOperationsMixin
from app.models import Note
from app.schemas import NoteCreate, NoteUpdate
from .base_controller import BaseDatabaseController


class NoteDatabaseController(BaseDatabaseController[Note, NoteCreate, NoteUpdate], OwnerOperationsMixin):
    pass

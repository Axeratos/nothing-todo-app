from app.models import Note
from app.schemas import NoteCreate, NoteUpdate
from .base_controller import BaseDatabaseController


class NoteDatabaseController(BaseDatabaseController[Note, NoteCreate, NoteUpdate]):
    pass

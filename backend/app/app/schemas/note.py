from pydantic import BaseModel

from .base import BaseDBSchema


class NoteBase(BaseModel):
    text: str | None


class NoteCreate(NoteBase):
    text: str


class NoteUpdate(NoteBase):
    pass


class NoteDB(NoteBase, BaseDBSchema):
    text: str

from datetime import date, time

from pydantic import BaseModel

from .base import BaseDBSchema


class TaskBase(BaseModel):
    title: str | None
    deadline_date: date | None
    deadline_time: time | None


class TaskCreate(TaskBase):
    title: str
    deadline_date: date


class TaskUpdate(TaskBase):
    pass


class TaskDB(TaskBase, BaseDBSchema):
    pk: int
    title: str
    deadline_date: date

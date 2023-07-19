from sqlalchemy.ext.asyncio import AsyncSession

from app.mixins.controller import OwnerOperationsMixin
from app.models import Task
from app.schemas import TaskUpdate, TaskCreate
from .base_controller import BaseDatabaseController


class TaskDatabaseController(BaseDatabaseController[Task, TaskCreate, TaskUpdate], OwnerOperationsMixin):
    def __init__(self, session: AsyncSession):
        super().__init__(Task, session)

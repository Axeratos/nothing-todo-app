from .base_controller import BaseDatabaseController
from ..models import User
from ..schemas import UserCreate, UserUpdate


class UserDatabaseController(BaseDatabaseController[User, UserCreate, UserUpdate]):
    pass

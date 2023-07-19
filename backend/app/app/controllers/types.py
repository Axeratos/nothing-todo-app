from typing import TypeVar

from .base_controller import BaseDatabaseController

Controller = TypeVar("Controller", bound=BaseDatabaseController)

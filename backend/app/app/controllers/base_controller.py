from sqlalchemy.ext.asyncio import AsyncSession

from app.db import Base


class BaseDatabaseController:
    def __init__(self, model: Base, session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, **kwargs):
        pass

    async def create(self, data):
        pass

    async def update(self, data):
        pass

    async def delete(self, pk: int):
        pass

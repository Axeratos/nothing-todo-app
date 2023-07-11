from pydantic import BaseModel
from sqlalchemy import select, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base_model import Base


class BaseDatabaseController:
    def __init__(self, model: Base, session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, **kwargs):
        queryset = await self.session.scalars(select(self.model).filter_by(**kwargs))
        return queryset.first()

    async def get_all(self):
        pass

    async def get_with_options(self, **kwargs):
        queryset = await self.session.scalars(select(self.model).where(or_(
            getattr(self.model, column) == value for column, value in kwargs.items()
        )))
        return queryset.all()

    async def create(self, data: dict | BaseModel):
        if isinstance(data, BaseModel):
            data = data.dict()
        new_object = self.model(**data)
        self.session.add(new_object)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object

    async def update(self, data):
        pass

    async def delete(self, pk: int):
        pass

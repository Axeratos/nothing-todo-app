from typing import Type, Generic, Sequence

from pydantic import BaseModel
from sqlalchemy import select, or_, ScalarResult, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.types.controller import ModelType, CreateSchemaType, UpdateSchemaType


class BaseDatabaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, **kwargs) -> ModelType | None:
        queryset = await self.session.scalars(select(self.model).filter_by(**kwargs))
        return queryset.first()

    async def get_all(self, **kwargs) -> Sequence[ModelType]:
        statement = select(self.model)
        if kwargs:
            statement = statement.filter_by(**kwargs)
        queryset = await self.session.scalars(statement)
        return queryset.all()

    async def get_options_queryset(self, **kwargs) -> ScalarResult:
        return await self.session.scalars(select(self.model).where(or_(
            getattr(self.model, column) == value for column, value in kwargs.items()
        )))

    async def get_paginated(self, page: int, page_size: int, **kwargs):
        queryset = await self.session.scalars(
            select(self.model).filter_by(**kwargs).offset((page - 1) * page_size).limit(page_size)
        )
        return queryset.all()

    async def create(self, data: dict | CreateSchemaType) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.dict()
        new_object = self.model(**data)
        self.session.add(new_object)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object

    async def update(self, pk: int, new_object_data: dict | UpdateSchemaType, owner_id: int) -> ModelType:
        if isinstance(new_object_data, dict):
            update_data = new_object_data
        else:
            update_data = new_object_data.dict(exclude_unset=True)
        query = await self.session.scalars(update(self.model).filter_by(id=pk, owner_id=owner_id).values(**update_data)
                                           .returning(self.model))
        await self.session.commit()
        return query.first()

    async def delete(self, **kwargs) -> ModelType | None:
        query = await self.session.scalars(delete(self.model).filter_by(**kwargs).returning(self.model))
        await self.session.commit()
        return query.first()

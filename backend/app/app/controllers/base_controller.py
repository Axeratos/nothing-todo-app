from typing import Type, Generic, Sequence

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, or_, ScalarResult
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.types import ModelType, CreateSchemaType, UpdateSchemaType


class BaseDatabaseController(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, **kwargs) -> ModelType | None:
        queryset = await self.session.scalars(select(self.model).filter_by(**kwargs))
        return queryset.first()

    async def get_all(self) -> Sequence[ModelType]:
        queryset = await self.session.scalars(select(self.model))
        return queryset.all()

    async def get_options_queryset(self, **kwargs) -> ScalarResult:
        return await self.session.scalars(select(self.model).where(or_(
            getattr(self.model, column) == value for column, value in kwargs.items()
        )))

    async def create(self, data: dict | CreateSchemaType) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.dict()
        new_object = self.model(**data)
        self.session.add(new_object)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object

    async def update(self, new_object_data: dict | UpdateSchemaType, old_object: ModelType) -> ModelType:
        old_obj_data = jsonable_encoder(old_object)
        if isinstance(new_object_data, dict):
            update_data = new_object_data
        else:
            update_data = new_object_data.dict(exclude_unset=True)
        for field in old_obj_data:
            if field in update_data:
                setattr(old_object, field, update_data[field])

        await self.session.commit()
        return old_object

    async def delete(self, **kwargs) -> ModelType | None:
        object_delete = await self.get(**kwargs)
        if not object_delete:
            return
        await self.session.delete(object_delete)
        await self.session.commit()
        return object_delete

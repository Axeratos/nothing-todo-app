from pydantic import BaseModel

from app.controllers import BaseDatabaseController
from app.types.controller import CreateSchemaType, ModelType


class OwnerOperationsMixin:
    async def create_with_owner(self: BaseDatabaseController, data: dict | CreateSchemaType,
                                owner_id: int) -> ModelType:
        if isinstance(data, BaseModel):
            data = data.dict()
        new_object = self.model(**data, owner_id=owner_id)
        self.session.add(new_object)
        await self.session.flush()
        await self.session.commit()
        await self.session.refresh(new_object)
        return new_object

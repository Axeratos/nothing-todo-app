from datetime import datetime

from pydantic import BaseModel


class BaseDBSchema(BaseModel):
    pk: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

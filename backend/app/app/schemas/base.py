from datetime import datetime

from pydantic import BaseModel


class BaseDBSchema(BaseModel):
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
    
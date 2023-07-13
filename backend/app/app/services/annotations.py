from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import get_session, get_current_verified_user
from app.schemas import UserDB

DBSession = Annotated[AsyncSession, Depends(get_session)]
CurrentVerifiedUser = Annotated[UserDB, Depends(get_current_verified_user)]

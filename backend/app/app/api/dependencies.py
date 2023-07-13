from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import async_sessionmaker
from starlette import status

from app.controllers import UserDatabaseController
from app.core.security import decode_token
from app.db.database_core import engine
from app.models import User

oauth2 = OAuth2PasswordBearer(tokenUrl="access-token")


async def get_session():
    session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e


async def get_current_user(session: Depends(get_session), token: str = Depends(oauth2)) -> User:
    token_data = decode_token(token)
    controller = UserDatabaseController(User, session)
    user = await controller.get(id=token_data.subject)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_current_verified_user(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user. Verify your account",
        )
    return current_user

from fastapi.security import OAuth2PasswordBearer, OAuth2
from sqlalchemy.ext.asyncio import async_sessionmaker

from app.db.database_core import engine

oauth2 = OAuth2PasswordBearer(tokenUrl="access-token")


async def get_session():
    session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)
    async with session_maker() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            raise e

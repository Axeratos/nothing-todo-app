from sqlalchemy.ext.asyncio import create_async_engine

from app.core.settings import app_config

engine = create_async_engine(app_config.DB_URL, echo=True)

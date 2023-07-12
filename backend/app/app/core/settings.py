from pathlib import Path

from pydantic import BaseSettings

env_path = Path(__file__).resolve().parents[2].joinpath(".env")
print(env_path)


class Settings(BaseSettings):
    DB_URL: str
    JWT_SECRET_KEY: str

    class Config:
        env_file = env_path


app_config = Settings()

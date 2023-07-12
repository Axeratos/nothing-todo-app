from datetime import datetime, timezone, timedelta

from fastapi import HTTPException
from jose import jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from app.core.settings import app_config
from app.schemas import TokenData

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def hash_password(plain_password: str):
    return pwd_context.hash(plain_password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def create_token(subject: int, expires_delta: timedelta):
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode_data = {"subject": subject, "exp": expire}
    return jwt.encode(
        to_encode_data,
        app_config.JWT_SECRET_KEY,
        algorithm=ALGORITHM,
    )


def decode_token(token: str | None) -> TokenData:
    try:
        payload = jwt.decode(
            token,
            app_config.JWT_SECRET_KEY,
            algorithms=[ALGORITHM],
        )
        return TokenData(**payload)
    except (jwt.JWTError, ValidationError, AttributeError) as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        ) from exc

from fastapi import APIRouter, HTTPException

from app.controllers import BaseDatabaseController
from app.core.security import hash_password
from app.models import User
from app.schemas import UserCreate
from app.services.annotations import DBSession

router = APIRouter()


@router.post("/sign-up")
async def sign_up(user_data: UserCreate, db: DBSession):
    controller = BaseDatabaseController(User, db)
    old_users_queryset = await controller.get_options_queryset(email=user_data.email, username=user_data.username)
    if old_users_queryset.first():
        raise HTTPException(status_code=400)
    user_data.password = hash_password(user_data.password)
    await controller.create(user_data)
    return {"msg": "User created successfully"}

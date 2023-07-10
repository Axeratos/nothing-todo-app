from fastapi import APIRouter, HTTPException

from app.controllers import BaseDatabaseController
from app.models import User
from app.schemas import UserCreate
from app.services.annotations import DBSession

router = APIRouter()


@router.post("/sign-up")
async def sign_up(user_data: UserCreate, db: DBSession):
    controller = BaseDatabaseController(User, db)
    old_user = await controller.get_with_options(email=user_data.email, username=user_data.username)
    if old_user:
        raise HTTPException(status_code=400)
    new_user = controller.create(user_data)
    return {"msg": "User created successfully"}

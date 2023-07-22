from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers import BaseDatabaseController
from app.core.security import verify_password, create_token
from app.models import User
from app.services.annotations import DBSession

router = APIRouter()


@router.post("/access-token")
async def login_access_token(login_data: Annotated[OAuth2PasswordRequestForm, Depends()], session: DBSession):
    controller = BaseDatabaseController(User, session)
    queryset = await controller.get_options_queryset(email=login_data.username, username=login_data.username)
    user = queryset.first()
    if not user:
        raise HTTPException(status_code=404, detail={"field": "username", "msg": "User does not exists"})
    elif not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=400, detail={"field": "password", "msg": "Password is incorrect"})

    access_token_expires = timedelta(minutes=10)

    return {
        "access_token": create_token(user.id, access_token_expires),
        "token_type": "bearer",
    }

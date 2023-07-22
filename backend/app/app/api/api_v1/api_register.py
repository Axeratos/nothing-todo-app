from fastapi import APIRouter

from app.api.api_v1.endpoints import user, notes, tasks, tokens

api_router = APIRouter()

api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(tokens.router, tags=["login"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
api_router.include_router(tasks.router, prefix="/tasks", tags=["tasks"])

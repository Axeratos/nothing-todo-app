from fastapi import APIRouter, HTTPException

from app.controllers import TaskDatabaseController
from app.schemas import TaskCreate, TaskUpdate, TaskDB
from app.services.annotations import CurrentVerifiedUser, DBSession
from app.structs import Page

router = APIRouter()


@router.get("/all", response_model=list[TaskDB])
async def get_all_tasks(session: DBSession, user: CurrentVerifiedUser):
    task_controller = TaskDatabaseController(session)
    return await task_controller.get_all(owner_id=user.id)


@router.post("/")
async def create_task(task_data: TaskCreate, user: CurrentVerifiedUser, session: DBSession):
    task_controller = TaskDatabaseController(session)
    return await task_controller.create_with_owner(task_data, user.id)


@router.get("/{pk}")
async def get_task(pk: int, session: DBSession, user: CurrentVerifiedUser):
    task_controller = TaskDatabaseController(session)
    task = await task_controller.get(id=pk, owner_id=user.id)
    if not task:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return task


@router.get("/")
async def get_tasks_paginated(session: DBSession, user: CurrentVerifiedUser, page: int = 1, page_size: int = 5):
    task_controller = TaskDatabaseController(session)
    page = await Page.create_new_page(task_controller, page, page_size, owner_id=user.id)
    return page


@router.put("/{pk}")
async def update_task(pk: int, update_data: TaskUpdate, session: DBSession, user: CurrentVerifiedUser):
    task_controller = TaskDatabaseController(session)
    updated_task = await task_controller.update(pk, update_data, user.id)
    if not updated_task:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return updated_task


@router.delete("/{pk}")
async def delete_task(pk: int, session: DBSession, user: CurrentVerifiedUser):
    task_controller = TaskDatabaseController(session)
    deleted_task = await task_controller.delete(id=pk, owner_id=user.id)
    if not deleted_task:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return deleted_task

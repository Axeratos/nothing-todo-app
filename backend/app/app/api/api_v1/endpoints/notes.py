from fastapi import APIRouter, HTTPException

from app.controllers import NoteDatabaseController
from app.schemas import NoteCreate, NoteUpdate, NoteDB
from app.services.annotations import DBSession, CurrentVerifiedUser
from app.structs import Page

router = APIRouter()


@router.get("/all", response_model=list[NoteDB])
async def get_all_notes(session: DBSession, user: CurrentVerifiedUser):
    note_controller = NoteDatabaseController(session)
    return await note_controller.get_all(owner_id=user.id)


@router.post("/", response_model=NoteDB)
async def create_note(note_data: NoteCreate, user: CurrentVerifiedUser, session: DBSession):
    note_controller = NoteDatabaseController(session)
    return await note_controller.create_with_owner(note_data, user.id)


@router.get("/{pk}", response_model=NoteDB)
async def get_note(pk: int, session: DBSession, user: CurrentVerifiedUser):
    note_controller = NoteDatabaseController(session)
    note = await note_controller.get(id=pk, owner_id=user.id)
    if not note:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return note


@router.get("/", response_model=Page)
async def get_notes_paginated(session: DBSession, user: CurrentVerifiedUser, page: int = 1, page_size: int = 5):
    note_controller = NoteDatabaseController(session)
    page = await Page.create_new_page(note_controller, page, page_size, owner_id=user.id)
    return page


@router.put("/{pk}", response_model=NoteDB)
async def update_note(pk: int, update_data: NoteUpdate, session: DBSession, user: CurrentVerifiedUser):
    note_controller = NoteDatabaseController(session)
    updated_note = await note_controller.update(pk, update_data, user.id)
    if not updated_note:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return updated_note


@router.delete("/{pk}", response_model=NoteDB)
async def delete_note(pk: int, session: DBSession, user: CurrentVerifiedUser):
    note_controller = NoteDatabaseController(session)
    deleted_note = await note_controller.delete(id=pk, owner_id=user.id)
    if not deleted_note:
        raise HTTPException(status_code=404, detail={"msg": "Note not found"})
    return deleted_note

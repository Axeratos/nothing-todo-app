from dataclasses import dataclass
from math import ceil

from fastapi import HTTPException

from app.controllers.types import Controller


@dataclass
class Page:
    items: list
    pages_count: int
    has_next: int

    @classmethod
    async def create_new_page(cls, controller: Controller, page: int, page_size: int, **kwargs):
        items_count = await controller.get_count(**kwargs)
        pages_count = ceil(items_count / page_size)
        if page > pages_count:
            raise HTTPException(status_code=404, detail={"msg": "Page does not exists"})
        return cls(
            await controller.get_paginated(page, page_size, **kwargs),
            pages_count,
            page < pages_count
        )

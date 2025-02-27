from __future__ import annotations as _annotations

from api import router_books
from api import router_users
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(router_users.router, prefix="/user", tags=["User"])
api_router.include_router(router_books.router, prefix="/book", tags=["Book"])
from fastapi import APIRouter

from app.views.auth import login
from app.views.data import data
from app.views.users import register, users

views_router = APIRouter()
views_router.include_router(users.router, prefix="", tags=["users-view"])
views_router.include_router(login.router, prefix="", tags=["auth-view"])
views_router.include_router(data.router, prefix="", tags=["data-view"])
views_router.include_router(register.router, prefix="", tags=["register-view"])

from fastapi import APIRouter, Request
from src.di.providers import provide_async_session
from src.database.repos.user import UserRepository
from .user import user_router

base_router = APIRouter()
base_router.include_router(user_router)

    
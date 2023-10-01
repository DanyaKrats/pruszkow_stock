import logging
from typing import Any, Callable
from starlette.middleware.base import BaseHTTPMiddleware
import asyncio
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.di.providers import provide_async_session, provide_db


DB_URL = "postgresql+asyncpg://postgres:postgres@localhost/pruszkow_stock"
DB_MAX_CONNECTION_COUNT = 10


class AssyncSessionMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: Any) -> None:
        self.app = app

    async def dispatch_func(self, request, call_next:Callable[..., Any]) -> Any:  
        engine = provide_db()
        session_maker = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)
        async with session_maker as session:
            setattr(request, 'db_session', session) 
            response = await call_next(request)
            return response
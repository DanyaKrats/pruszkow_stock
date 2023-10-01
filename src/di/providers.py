from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncEngine
from .db import Database

DB_URL = "postgresql+asyncpg://postgres:postgres@localhost/pruszkow_stock"
DB_MAX_CONNECTION_COUNT = 10

def provide_db_stub() -> None:  # pragma: no cover
    ...


def provide_db(database_url: str = DB_URL, max_connection_count: int = DB_MAX_CONNECTION_COUNT) -> AsyncEngine:
    return Database(
        database_url=database_url, max_connection_count=max_connection_count
    ).engine


def provide_db_only(database_url: str, max_connection_count: int) -> Database:
    return Database(
        database_url=database_url, max_connection_count=max_connection_count
    )
def provide_async_session(engine: AsyncEngine = None) -> AsyncSession:
    if engine is None:
        engine = provide_db()
    return sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)()




class ProviderSession:
    def __init__(self, session_factory: sessionmaker) -> None:
        self._session_factory = session_factory

    async def __call__(self):
        async with self._session_factory() as session:
            try:
                yield session
            except:
                await session.close()
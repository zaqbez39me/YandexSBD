"""
The engine module - the engine module that provides the class working
with asynchronous database.

Classes:
    DatabaseEngine - class that provides the interface for the database management.

Notes:
    The main feature of this module is simplification of working with
    database engine and sessions.
"""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession, async_sessionmaker,
                                    create_async_engine)

from app.database.base import Base


class DatabaseEngine:
    """
    A database engine class.

    Used to initialize async engine on creation, to define session_maker
    and provide an ability to open sessions when it is needed. Moreover,
    this class contains methods for starting and finalizing behavior.

    __engine(AsyncEngine):
        The async engine instance
    __session_maker(async_sessionmaker):
        The sessionmaker class. Used to create new database sessions.
    """

    def __init__(self, database_url: str):
        self.__engine = create_async_engine(database_url)
        self.__session_maker = async_sessionmaker(
            bind=self.__engine,
            autocommit=False,
            class_=AsyncSession,
            autoflush=False,
        )

    async def start(self) -> None:
        """
        Prepares database for usage.

        The method to create all the tables in the database. Usually, it is
        done on initialization of app stage.
        """
        async with self.__engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all, checkfirst=True)

    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        """
        Creates a new session.

        Yields:
            session: async session generator
        """
        async with self.__session_maker() as session:
            yield session

    async def finalize(self) -> None:
        """Finalizes the engine instance."""
        await self.__engine.dispose()

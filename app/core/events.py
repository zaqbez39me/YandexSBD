from typing import Callable

from app.database import DatabaseEngine


def create_startup_handler(db_engine: DatabaseEngine) -> Callable:
    async def startup() -> None:
        await db_engine.start()

    return startup


def create_shutdown_handler(db_engine: DatabaseEngine) -> Callable:
    async def shutdown() -> None:
        await db_engine.finalize()

    return shutdown

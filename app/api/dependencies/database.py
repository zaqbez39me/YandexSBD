from typing import Type, Callable

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import db_engine
from app.database.repositories.base import BaseRepository


def get_repository(
    repo: Type[BaseRepository]
) -> Callable[[AsyncSession], BaseRepository]:
    def _get_repo(
            session: AsyncSession = Depends(db_engine.session)
    ):
        return repo(session)
    return _get_repo

from typing import Callable

from fastapi.exceptions import RequestValidationError
from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from app.database.error import ConflictWithRequestDBError, NotFoundInDBError


def create_validation_exception_handler() -> Callable:
    async def validation_exception_handler(
        _: Request, exc: RequestValidationError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"errors": exc.errors()},
        )

    return validation_exception_handler


def create_not_found_handler() -> Callable:
    async def not_found_handler(
        _: Request, exc: NotFoundInDBError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": exc.message},
        )

    return not_found_handler


def create_request_db_conflict_handler() -> Callable:
    async def not_found_handler(
        _: Request, exc: ConflictWithRequestDBError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )

    return not_found_handler

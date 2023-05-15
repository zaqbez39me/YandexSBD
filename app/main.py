from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.middlewares import get_middleware
from app.api.utils import get_limiter, get_router
from app.core.config import settings
from app.core.events import create_shutdown_handler, create_startup_handler
from app.core.exceptions import (create_not_found_handler,
                                 create_request_db_conflict_handler,
                                 create_validation_exception_handler)
from app.database import db_engine
from app.database.error import ConflictWithRequestDBError, NotFoundInDBError


def get_application() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION
    )
    application.state.limiter = get_limiter()
    application.add_middleware(get_middleware())

    application.add_event_handler(
        event_type="startup", func=create_startup_handler(db_engine)
    )

    application.add_event_handler(
        event_type="shutdown", func=create_shutdown_handler(db_engine)
    )

    application.add_exception_handler(
        exc_class_or_status_code=RateLimitExceeded,
        handler=_rate_limit_exceeded_handler,
    )

    application.add_exception_handler(
        exc_class_or_status_code=NotFoundInDBError,
        handler=create_not_found_handler(),
    )

    application.add_exception_handler(
        exc_class_or_status_code=ConflictWithRequestDBError,
        handler=create_request_db_conflict_handler(),
    )

    application.add_exception_handler(
        exc_class_or_status_code=RequestValidationError,
        handler=create_validation_exception_handler(),
    )

    application.include_router(get_router())

    return application


app: FastAPI = get_application()

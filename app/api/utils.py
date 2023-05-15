from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.endpoints import orders, couriers


def get_limiter() -> Limiter:
    return Limiter(key_func=get_remote_address, default_limits=["10/second"])


def get_router() -> APIRouter:
    router = APIRouter()
    router.include_router(couriers.router)
    router.include_router(orders.router)
    return router

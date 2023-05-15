from fastapi import APIRouter
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.api.endpoints import couriers, orders


def get_limiter() -> Limiter:
    """
    Returns a limiter that limits requests to 10 per second per remote address.

    Returns:
        Limiter: A limiter that limits requests to 10 per second per remote address.
    """
    return Limiter(key_func=get_remote_address, default_limits=["10/second"])


def get_router() -> APIRouter:
    """
    Returns an API router that includes the `orders` and `couriers` routers.

    Returns:
        APIRouter: An API router that includes the `orders` and `couriers` routers.
    """
    router = APIRouter()
    router.include_router(couriers.router)
    router.include_router(orders.router)
    return router

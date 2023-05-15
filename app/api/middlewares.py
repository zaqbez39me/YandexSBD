from typing import Type

from slowapi.middleware import SlowAPIMiddleware


def get_middleware() -> Type[SlowAPIMiddleware]:
    return SlowAPIMiddleware

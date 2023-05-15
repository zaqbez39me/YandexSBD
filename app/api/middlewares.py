"""
This module provides a function for getting the SlowAPIMiddleware class.

The `get_middleware()` function returns the `SlowAPIMiddleware` class.
This class can be used to add slow request handling to a FastAPI application.
"""

from typing import Type

from slowapi.middleware import SlowAPIMiddleware


def get_middleware() -> Type[SlowAPIMiddleware]:
    """
    Returns the SlowAPIMiddleware class.

    Returns:
        The SlowAPIMiddleware class.
    """
    return SlowAPIMiddleware

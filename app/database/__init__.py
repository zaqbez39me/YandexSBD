"""
This module provides a function for creating a `DatabaseEngine` instance.

The `DatabaseEngine` class provides a connection to the database.
"""

from app.core.config import settings
from app.database.engine import DatabaseEngine

db_engine = DatabaseEngine(settings.SQLALCHEMY_DATABASE_URI)

"""
This module provides a base repository class for interacting with couriers in the database.
The `BaseRepository` class provides a connection to the database for its subclasses to use.
This allows for a consistent way to interact with the database across all repositories.
The `connection` property provides a way to get the current connection to the database.
This can be used to execute queries and perform other database operations.
"""

from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    """
    A base repository class that provides a connection to the database.

    Args:
        conn: An asynchronous session to the database.

    Attributes:
        conn: The connection to the database.
    """

    def __init__(self, conn: AsyncSession) -> None:
        """
        Initialize the repository with a connection to the database.

        Args:
            conn: An asynchronous session to the database.
        """
        self._conn = conn

    @property
    def connection(self) -> AsyncSession:
        """
        Get the connection to the database.

        Returns:
            The connection to the database.
        """
        return self._conn

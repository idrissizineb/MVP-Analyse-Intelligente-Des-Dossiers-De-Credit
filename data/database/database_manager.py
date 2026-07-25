"""
Database management module.

This module initializes and manages the database schema.
"""

from data.database.connection import DatabaseConnection
from data.database.models import CREATE_CLIENT_TABLE


class DatabaseManager:
    """
    Manage database initialization and operations.
    """

    def __init__(
        self,
        database_connection: DatabaseConnection
    ):
        """
        Initialize the database manager.

        Parameters
        ----------
        database_connection : DatabaseConnection
            Database connection manager.
        """

        self.database_connection = database_connection

    def initialize_database(self) -> None:
        """
        Create the database tables if they do not exist.
        """

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(CREATE_CLIENT_TABLE)

        connection.commit()

        cursor.close()
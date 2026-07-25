"""
Database connection module.

This module is responsible for creating and managing
the connection to the SQLite database.
"""

import sqlite3
from pathlib import Path


class DatabaseConnection:
    """
    Manage the connection to the SQLite database.
    """

    def __init__(
        self,
        database_path: str = "data/database/credit_analysis.db"
    ):
        """
        Initialize the database connection manager.

        Parameters
        ----------
        database_path : str
            Path to the SQLite database file.
        """

        self.database_path = Path(database_path)

        # Create the parent directory if it does not exist
        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection = None

    def connect(self) -> sqlite3.Connection:
        """
        Establish a connection to the SQLite database.

        Returns
        -------
        sqlite3.Connection
            Active SQLite database connection.
        """

        if self.connection is None:

            self.connection = sqlite3.connect(
                self.database_path
            )

        return self.connection

    def close(self) -> None:
        """
        Close the database connection.
        """

        if self.connection is not None:

            self.connection.close()

            self.connection = None
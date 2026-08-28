"""
Database connection module.

This module is responsible for creating and managing
the connection to the SQLite database.
"""

import sqlite3
from pathlib import Path
from typing import Any, Optional, Sequence


class DatabaseConnection:
    """
    Manage the connection to the SQLite database.

    This class centralizes all low-level SQLite connection
    and query execution operations.
    """

    def __init__(
        self,
        database_path: str = "data/database/credit_analysis.db"
    ) -> None:
        """
        Initialize the database connection manager.

        Parameters
        ----------
        database_path : str
            Path to the SQLite database file.
        """

        self.database_path = Path(database_path)

        self.database_path.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.connection: Optional[sqlite3.Connection] = None

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

    def execute(
        self,
        query: str,
        parameters: Sequence[Any] = ()
    ) -> sqlite3.Cursor:
        """
        Execute a SQL query.

        This method is used for INSERT, UPDATE, DELETE,
        and other SQL statements that modify the database.

        Parameters
        ----------
        query : str
            SQL query to execute.

        parameters : Sequence[Any]
            Values used in the SQL query.

        Returns
        -------
        sqlite3.Cursor
            Cursor containing the execution result.
        """

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        connection.commit()

        return cursor

    def fetch_one(
        self,
        query: str,
        parameters: Sequence[Any] = ()
    ) -> Optional[tuple]:
        """
        Execute a SELECT query and return one result.

        Parameters
        ----------
        query : str
            SQL SELECT query.

        parameters : Sequence[Any]
            Values used in the SQL query.

        Returns
        -------
        Optional[tuple]
            One database row if found, otherwise None.
        """

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchone()

    def fetch_all(
        self,
        query: str,
        parameters: Sequence[Any] = ()
    ) -> list[tuple]:
        """
        Execute a SELECT query and return all results.

        Parameters
        ----------
        query : str
            SQL SELECT query.

        parameters : Sequence[Any]
            Values used in the SQL query.

        Returns
        -------
        list[tuple]
            List of database rows.
        """

        connection = self.connect()

        cursor = connection.cursor()

        cursor.execute(
            query,
            parameters
        )

        return cursor.fetchall()

    def close(self) -> None:
        """
        Close the database connection.
        """

        if self.connection is not None:

            self.connection.close()

            self.connection = None
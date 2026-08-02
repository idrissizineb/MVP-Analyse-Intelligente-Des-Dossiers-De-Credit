import sqlite3


class SQLExecutor:
    """
    Execute validated SQL queries on the SQLite database.
    """

    def __init__(self, database_path: str):

        self.database_path = database_path

    def execute(self, sql: str) -> list[dict]:
        """
        Execute a SELECT query and return the results
        as a list of dictionaries.

        Parameters
        ----------
        sql : str
            Validated SQL query.

        Returns
        -------
        list[dict]
        """

        connection = sqlite3.connect(self.database_path)

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(sql)

        rows = cursor.fetchall()

        connection.close()

        return [dict(row) for row in rows]
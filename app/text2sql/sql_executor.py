import sqlite3

class SQLExecutor:

    def __init__(self, database_path: str):
        self.database_path = database_path

    def execute(
        self,
        sql: str,
        parameters: dict | None = None,
    ) -> list[dict]:

        connection = sqlite3.connect(self.database_path)
        connection.row_factory = sqlite3.Row

        print("\nSQL:")
        print(sql)
        print("\nParameters:")
        print(parameters)

        cursor = connection.cursor()
        cursor.execute(sql, parameters)
        rows = cursor.fetchall()
        connection.close()
        return [dict(row) for row in rows]
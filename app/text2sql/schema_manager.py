import sqlite3


class SchemaManager:
    """
    Reads the SQLite database schema and returns
    a human-readable description that can be injected
    into LLM prompts.
    """

    def __init__(self, database_path: str):

        self.database_path = database_path

    def get_schema(self) -> dict:
        """
        Returns the complete database schema.

        Example
        -------
        {
            "clients": [
                "id_client",
                "nom_prenom",
                "numero_compte"
            ],
            ...
        }
        """

        connection = sqlite3.connect(self.database_path)

        cursor = connection.cursor()

        # ------------------------------------------
        # Retrieve all table names
        # ------------------------------------------

        cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tables = cursor.fetchall()

        schema = {}

        for (table_name,) in tables:

            cursor.execute(
                f"PRAGMA table_info({table_name})"
            )

            columns = cursor.fetchall()

            schema[table_name] = [

                column[1]

                for column in columns

            ]

        connection.close()

        return schema

    def schema_as_text(self) -> str:
        """
        Converts the schema into a prompt-friendly format.

        Example:

        Table: clients
            - id_client
            - nom_prenom
            - numero_compte
        """

        schema = self.get_schema()

        lines = []

        for table, columns in schema.items():

            lines.append(f"Table: {table}")

            for column in columns:

                lines.append(f"    - {column}")

            lines.append("")

        return "\n".join(lines)
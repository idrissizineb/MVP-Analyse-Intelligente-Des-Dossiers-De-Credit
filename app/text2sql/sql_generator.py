from app.llm.groq_client import GroqClient
from app.text2sql.prompts import TEXT_TO_SQL_PROMPT
from app.text2sql.schema_manager import SchemaManager


class SQLGenerator:
    """
    Convert a pseudonymized natural-language question
    into a SQLite SELECT query.

    Sensitive values must already be pseudonymized
    before this class is called.
    """

    def __init__(
        self,
        database_path: str,
    ):

        self.llm = GroqClient()

        self.schema_manager = SchemaManager(
            database_path
        )

    def generate_sql(
        self,
        question: str,
    ) -> str:

        schema = (
            self.schema_manager.schema_as_text()
        )

        system_prompt = (
            TEXT_TO_SQL_PROMPT.format(
                schema=schema
            )
        )

        print(
            "\n========== SQL GENERATION =========="
        )

        print(
            "Question sent to Groq:"
        )

        print(
            question
        )

        sql = self.llm.chat(
            prompt=question,
            system_prompt=system_prompt,
            temperature=0
        )

        print(
            "\nGenerated SQL:"
        )

        print(
            sql
        )

        return sql.strip()
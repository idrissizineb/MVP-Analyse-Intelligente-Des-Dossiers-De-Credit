from app.text2sql.sql_generator import SQLGenerator
from app.text2sql.sql_validator import SQLValidator
from app.text2sql.sql_executor import SQLExecutor
from app.text2sql.answer_generator import AnswerGenerator


class Text2SQLPipeline:
    """
    Complete Text-to-SQL pipeline.

    Workflow
    --------
    1. Receive a question in natural language.
    2. Generate an SQL query using the LLM.
    3. Validate the generated SQL.
    4. Execute the SQL query.
    5. Convert the SQL results into a natural-language answer.
    """

    def __init__(self):

        self.database_path = "data/database/credit_analysis.db"

        self.sql_generator = SQLGenerator(
            database_path=self.database_path
        )

        self.sql_validator = SQLValidator()

        self.sql_executor = SQLExecutor(
            database_path=self.database_path
        )

        self.answer_generator = AnswerGenerator()

    def ask(
        self,
        question: str
    ) -> dict:
        """
        Execute the complete Text-to-SQL pipeline.

        Parameters
        ----------
        question : str
            User question.

        Returns
        -------
        dict
        """

        # =====================================================
        # STEP 1 - Generate SQL
        # =====================================================

        sql = self.sql_generator.generate_sql(question)

        # =====================================================
        # STEP 2 - Validate SQL
        # =====================================================

        valid, reason = self.sql_validator.validate(sql)

        if not valid:

            return {
                "success": False,
                "question": question,
                "generated_sql": sql,
                "error": reason,
            }

        # =====================================================
        # STEP 3 - Execute SQL
        # =====================================================

        results = self.sql_executor.execute(sql)

        # =====================================================
        # STEP 4 - Generate answer
        # =====================================================

        answer = self.answer_generator.generate(
            question,
            results
        )

        # =====================================================
        # RETURN
        # =====================================================

        return {
            "success": True,
            "question": question,
            "generated_sql": sql,
            "results": results,
            "answer": answer,
        }
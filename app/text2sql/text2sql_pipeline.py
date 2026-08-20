from app.text2sql.sql_generator import SQLGenerator
from app.text2sql.sql_validator import SQLValidator
from app.text2sql.sql_executor import SQLExecutor
from app.text2sql.answer_generator import AnswerGenerator
from app.text2sql.entity_extractor import EntityExtractor
from app.security.pseudonymizer import Pseudonymizer


class Text2SQLPipeline:
    """
    Complete secure Text-to-SQL pipeline.

    Security workflow
    -----------------
    1. Receive original question.
    2. Pseudonymize sensitive values locally.
    3. Send ONLY pseudonymized question to Groq.
    4. Generate SQL using placeholders.
    5. Extract pseudonymized entities locally.
    6. Restore real values locally for SQLite parameters.
    7. Execute SQL locally.
    8. Pseudonymize SQL results locally.
    9. Send ONLY pseudonymized results to Groq.
    10. Restore sensitive values locally in the final answer.
    """

    def __init__(self):

        self.database_path = (
            "data/database/credit_analysis.db"
        )

        # --------------------------------------------------
        # Shared pseudonymizer
        # --------------------------------------------------

        self.pseudonymizer = Pseudonymizer()

        # --------------------------------------------------
        # Components
        # --------------------------------------------------

        self.sql_generator = SQLGenerator(
            database_path=self.database_path
        )

        self.sql_validator = SQLValidator()

        self.sql_executor = SQLExecutor(
            database_path=self.database_path
        )

        self.answer_generator = AnswerGenerator()

        self.entity_extractor = EntityExtractor()

    # ======================================================
    # ASK
    # ======================================================

    def ask(
        self,
        question: str
    ) -> dict:

        # ==================================================
        # STEP 1 - PSEUDONYMIZE QUESTION LOCALLY
        # ==================================================

        print(
            "\n========== TEXT-TO-SQL SECURITY =========="
        )

        print(
            "\nOriginal question:"
        )

        print(question)

        pseudonymized_question = (
            self.pseudonymizer.pseudonymize_query(
                question
            )
        )

        print(
            "\nQuestion sent to Groq:"
        )

        print(
            pseudonymized_question
        )

        # ==================================================
        # STEP 2 - GENERATE SQL
        # ==================================================

        sql = self.sql_generator.generate_sql(
            pseudonymized_question
        )

        # ==================================================
        # STEP 3 - VALIDATE SQL
        # ==================================================

        valid, reason = (
            self.sql_validator.validate(sql)
        )

        if not valid:

            return {
                "success": False,
                "question": question,
                "generated_sql": sql,
                "error": reason,
            }

        # ==================================================
        # STEP 4 - EXTRACT ENTITIES FROM ORIGINAL QUESTION
        # ==================================================

        # IMPORTANT:
        #
        # EntityExtractor works on the ORIGINAL question.
        #
        # This gives us the real values locally.
        #
        # Example:
        #
        # Original:
        # "Quel est le crédit de IDRISSI ZINEB ?"
        #
        # Parameters:
        # {
        #     "client_name": "IDRISSI ZINEB"
        # }

        parameters = (
            self.entity_extractor.extract(
                question
            )
        )

        print(
            "\nLocal parameters:"
        )

        print(
            parameters
        )

        # ==================================================
        # STEP 5 - EXECUTE SQL LOCALLY
        # ==================================================

        # The SQL contains placeholders such as:
        #
        # WHERE nom_prenom = :client_name
        #
        # The real value stays local.
        #
        results = self.sql_executor.execute(
            sql,
            parameters
        )

        print(
            "\n========== SQL RESULTS =========="
        )

        print(
            results
        )

        # ==================================================
        # STEP 6 - PSEUDONYMIZE SQL RESULTS
        # ==================================================

        pseudonymized_results = (
            self.pseudonymizer.pseudonymize_records(
                results
            )
        )

        print(
            "\n========== RESULTS SENT TO GROQ =========="
        )

        print(
            pseudonymized_results
        )

        # ==================================================
        # STEP 7 - GENERATE ANSWER
        # ==================================================

        answer = (
            self.answer_generator.generate(
                question=pseudonymized_question,
                sql_results=pseudonymized_results
            )
        )

        # ==================================================
        # STEP 8 - RESTORE SENSITIVE VALUES LOCALLY
        # ==================================================

        restored_answer = (
            self.pseudonymizer.restore_query_placeholders(
                answer
            )
        )

        print(
            "\n========== FINAL ANSWER =========="
        )

        print(
            restored_answer
        )

        # ==================================================
        # RETURN
        # ==================================================

        return {
            "success": True,

            # Original question is kept locally
            "question": question,

            # SQL generated from pseudonymized question
            "generated_sql": sql,

            # Original DB results stay local
            "results": results,

            # Final answer is restored locally
            "answer": restored_answer,
        }
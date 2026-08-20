import json

from app.llm.groq_client import GroqClient
from app.text2sql.prompts import ANSWER_GENERATION_PROMPT


class AnswerGenerator:
    """
    Transform pseudonymized SQL results into
    a natural-language answer.

    Sensitive values must already be pseudonymized
    before calling this class.
    """

    def __init__(self):

        self.llm = GroqClient()

    def generate(
        self,
        question: str,
        sql_results: list[dict],
    ) -> str:

        results = json.dumps(
            sql_results,
            indent=4,
            ensure_ascii=False
        )

        user_prompt = f"""
Question:

{question}

SQL Results:

{results}
"""

        print(
            "\n========== ANSWER GENERATION =========="
        )

        print(
            "Data sent to Groq:"
        )

        print(
            user_prompt
        )

        answer = self.llm.chat(
            prompt=user_prompt,
            system_prompt=ANSWER_GENERATION_PROMPT,
            temperature=0
        )

        return answer.strip()
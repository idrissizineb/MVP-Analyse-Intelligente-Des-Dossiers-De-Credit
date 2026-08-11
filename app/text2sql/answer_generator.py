import json

from app.llm.groq_client import GroqClient

from app.text2sql.prompts import ANSWER_GENERATION_PROMPT


class AnswerGenerator:
    """
    Transform SQL results into a natural-language answer.
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

        answer = self.llm.chat(

            prompt=user_prompt,

            system_prompt=ANSWER_GENERATION_PROMPT,

            temperature=0

        )

        return answer.strip()
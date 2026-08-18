import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:
    """
    Client used to communicate with Groq API.

    GPT-OSS 120B is used for:
    - OCR correction
    - Structured field extraction

    Field extraction uses Groq Structured Outputs with
    strict JSON Schema to guarantee valid JSON.
    """

    def __init__(
        self,
        model: str = "openai/gpt-oss-120b",
    ):

        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is not configured."
            )

        self.client = Groq(
            api_key=api_key
        )

        self.model = model

    # ======================================================
    # GENERIC CHAT
    # ======================================================

    def chat(
        self,
        prompt: str,
        system_prompt: str = "",
        temperature: float = 0.0,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],

            temperature=temperature,

            # GPT-OSS reasoning
            reasoning_effort="low",
            reasoning_format="hidden",
        )

        return response.choices[0].message.content or ""

    # ======================================================
    # OCR CORRECTION
    # ======================================================

    def correct_ocr(
        self,
        prompt: str,
        document: str,
    ) -> str:

        return self.chat(
            prompt=document,
            system_prompt=prompt,
            temperature=0,
        )

    # ======================================================
    # FIELD EXTRACTION
    # ======================================================

    def extract_fields(
        self,
        prompt: str,
        document: str,
    ) -> str:

        print("\n========== GROQ FIELD EXTRACTION DEBUG ==========")
        print(f"MODEL: {self.model}")
        print("STRUCTURED OUTPUT: ENABLED")
        print("STRICT JSON SCHEMA: ENABLED")
        print("REASONING: LOW")
        print("=================================================\n")

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[
                {
                    "role": "system",
                    "content": prompt,
                },
                {
                    "role": "user",
                    "content": document,
                },
            ],

            # ==================================================
            # STRICT STRUCTURED OUTPUT
            # ==================================================

            response_format={
                "type": "json_schema",
                "json_schema": {
                    "name": "credit_file_fields",

                    "strict": True,

                    "schema": {
                        "type": "object",

                        "properties": {

                            "cin": {
                                "type": "string"
                            },

                            "nom_prenom": {
                                "type": "string"
                            },

                            "numero_compte": {
                                "type": "string"
                            },

                            "nature_credit": {
                                "type": "string"
                            },

                            "montant_credit": {
                                "type": "string"
                            },

                            "date_de_decision": {
                                "type": "string"
                            },

                            "date_archivage": {
                                "type": "string"
                            },
                        },

                        "required": [
                            "cin",
                            "nom_prenom",
                            "numero_compte",
                            "nature_credit",
                            "montant_credit",
                            "date_de_decision",
                            "date_archivage",
                        ],

                        "additionalProperties": False,
                    },
                },
            },

            # GPT-OSS supports low / medium / high reasoning.
            # Low is enough for this extraction task.
            reasoning_effort="low",

            # Hide reasoning tokens from the returned content.
            reasoning_format="hidden",

            temperature=0,
        )

        content = response.choices[0].message.content or ""

        print("========== GROQ RESPONSE ==========")
        print(content)
        print("===================================\n")

        return content
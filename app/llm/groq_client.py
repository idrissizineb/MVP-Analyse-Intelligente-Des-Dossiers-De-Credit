import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:
    """
    Client used to communicate with Groq API.
    """

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
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

        return self.chat(
            prompt=document,
            system_prompt=prompt,
            temperature=0,
        )
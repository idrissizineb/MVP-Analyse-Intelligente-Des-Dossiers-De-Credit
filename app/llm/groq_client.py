"""
Groq API client.

This module centralizes every interaction with the Groq API.

Current capabilities
--------------------
- OCR correction
- Banking field extraction

Future capabilities
-------------------
- Document classification
- Document summarization
- Validation
"""

from groq import Groq  # pyright: ignore[reportMissingImports]

from app.llm.config import GROQ_API_KEY
from app.llm.prompts import OCR_CORRECTION_PROMPT


class GroqClient:
    """
    Wrapper around the Groq API.

    This class is responsible only for communicating with Groq.
    It does not contain business logic.
    """

    def __init__(
        self,
        model: str = "llama-3.3-70b-versatile",
    ):
        """
        Initialize the Groq client.
        """

        self.client = Groq(api_key=GROQ_API_KEY)
        self.model = model

    # ==========================================================
    # Internal helper
    # ==========================================================

    def _generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
    ) -> str:
        """
        Send a prompt to Groq and return the generated text.

        Parameters
        ----------
        system_prompt : str
            Instructions for the model.

        user_prompt : str
            User content.

        temperature : float
            Generation temperature.

        Returns
        -------
        str
            Model response.
        """

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=temperature,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
        )

        return completion.choices[0].message.content.strip()

    # ==========================================================
    # OCR Correction
    # ==========================================================

    def correct_ocr(self, ocr_text: str) -> str:
        """
        Correct OCR output.

        Parameters
        ----------
        ocr_text : str

        Returns
        -------
        str
            Corrected OCR text.
        """

        return self._generate(
            system_prompt=OCR_CORRECTION_PROMPT,
            user_prompt=ocr_text,
            temperature=0,
        )

    # ==========================================================
    # Field Extraction
    # ==========================================================

    def extract_fields(
        self,
        prompt: str,
        document: str,
    ) -> str:
        """
        Extract structured banking fields.

        Parameters
        ----------
        prompt : str
            Extraction prompt.

        document : str
            OCR text from the complete dossier.

        Returns
        -------
        str
            JSON returned by Groq.
        """

        return self._generate(
            system_prompt=prompt,
            user_prompt=document,
            temperature=0,
        )
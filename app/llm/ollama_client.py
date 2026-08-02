"""
Generic Ollama client.

This module centralizes every interaction with the local Ollama model.

Current capabilities
--------------------
- OCR correction
- Banking field extraction

Future capabilities
-------------------
- SQL generation
- Summarization
- Validation
"""

from ollama import chat  # pyright: ignore[reportMissingImports]

from app.llm.prompts import (
    OCR_CORRECTION_PROMPT,
)


class OllamaClient:
    """
    Wrapper around a local Ollama model.

    This class is responsible only for communicating
    with the language model.
    """

    def __init__(
        self,
        model: str = "qwen2.5:7b",
    ):

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

        response = chat(
            model=self.model,
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
            options={
                "temperature": temperature,
            },
        )

        return response["message"]["content"].strip()

    # ==========================================================
    # OCR Correction
    # ==========================================================

    def correct_ocr(
        self,
        ocr_text: str,
    ) -> str:

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

        return self._generate(
            system_prompt=prompt,
            user_prompt=document,
            temperature=0,
        )

    def chat(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.0,
    ) -> str:
        """Generic chat interface used by every LLM task."""


        return self._generate(
            system_prompt=system_prompt or "",
            user_prompt=prompt,
            temperature=temperature,
        )
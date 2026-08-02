"""
Field extraction module.

This module extracts structured banking information from the corrected
OCR text of an entire credit file.

Workflow
--------
1. Merge OCR text from all pages.
2. Send the complete document to Groq.
3. Parse the returned JSON.
4. Return a Python dictionary.
"""

import json
import re

from app.llm.ollama_client import OllamaClient
from app.llm.prompts import FIELD_EXTRACTION_PROMPT


class FieldExtractor:
    """
    Extract structured banking fields from corrected OCR text.
    """

    def __init__(self, client: OllamaClient):
        """
        Initialize the field extractor.

        Parameters
        ----------
        client : GroqClient
            Shared Groq client.
        """

        self.client = client

    def extract(self, corrected_pages: list[str]) -> dict:
        """
        Extract banking fields from a complete credit file.

        Parameters
        ----------
        corrected_pages : list[str]
            List containing the corrected OCR text for every page
            of the PDF.

        Returns
        -------
        dict
            Dictionary containing the extracted banking fields.
        """

        # ---------------------------------------------------------
        # Merge all pages into one document
        # ---------------------------------------------------------

        full_document = self._merge_pages(corrected_pages)

        # ---------------------------------------------------------
        # Ask Groq to extract the fields
        # ---------------------------------------------------------

        response = self.client.extract_fields(
            prompt=FIELD_EXTRACTION_PROMPT,
            document=full_document,
        )

        # ---------------------------------------------------------
        # Convert Groq response into Python dictionary
        # ---------------------------------------------------------

        return self._parse_json(response)

    def _merge_pages(self, pages: list[str]) -> str:
        """
        Merge multiple OCR pages into one document.

        Parameters
        ----------
        pages : list[str]
            Corrected OCR text for every page.

        Returns
        -------
        str
            Complete document.
        """

        merged_document = []

        for page_number, page in enumerate(pages, start=1):

            merged_document.append(
                f"================ PAGE {page_number} ================\n"
            )

            merged_document.append(page.strip())

            merged_document.append("\n")

        return "\n".join(merged_document)

    def _parse_json(self, response: str) -> dict:
        """
        Parse the JSON returned by Groq.

        Groq may sometimes surround the JSON with Markdown
        or additional text.

        This method extracts only the JSON object.

        Parameters
        ----------
        response : str
            Raw Groq response.

        Returns
        -------
        dict
            Parsed JSON.

        Raises
        ------
        ValueError
            If no valid JSON is found.
        """

        # ---------------------------------------------------------
        # Remove Markdown code blocks
        # ---------------------------------------------------------

        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.strip()

        # ---------------------------------------------------------
        # Extract the JSON object
        # ---------------------------------------------------------

        match = re.search(r"\{.*\}", response, re.DOTALL)

        if not match:
            raise ValueError(
                "No JSON object found in Groq response."
            )

        json_string = match.group()

        # ---------------------------------------------------------
        # Parse JSON
        # ---------------------------------------------------------

        try:
            return json.loads(json_string)

        except json.JSONDecodeError as error:

            raise ValueError(
                f"Groq returned invalid JSON:\n\n{json_string}"
            ) from error
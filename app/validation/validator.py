"""
Validation module.

This module validates the banking fields extracted by the LLM
before they are stored in the database.
"""

import re
from datetime import datetime


class Validator:
    """
    Validate extracted banking fields.
    """

    def validate(self, fields: dict) -> dict:
        """
        Validate every extracted field.

        Parameters
        ----------
        fields : dict

        Returns
        -------
        dict
        """

        results = {
            "nom_prenom": self._validate_name(
                fields.get("nom_prenom", "")
            ),

            "numero_compte": self._validate_account(
                fields.get("numero_compte", "")
            ),

            "nature_credit": self._validate_credit_type(
                fields.get("nature_credit", "")
            ),

            "montant_credit": self._validate_amount(
                fields.get("montant_credit", "")
            ),

            "date_production": self._validate_date(
                fields.get("date_production", "")
            ),

            "date_archivage": self._validate_date(
                fields.get("date_archivage", "")
            ),
        }

        is_valid = all(
            field["valid"]
            for field in results.values()
        )

        return {
            "fields": results,
            "is_valid": is_valid,
        }

    # ==========================================================
    # Individual validators
    # ==========================================================

    def _validate_name(self, value: str) -> dict:
        """
        Validate the customer's full name.

        Rules
        -----
        - Cannot be empty.
        - Must contain at least one letter.
        - Cannot contain digits.
        """

        value = value.strip()

        # Empty field
        if not value:
            return {
                "value": value,
                "valid": False,
                "error": "Customer name is missing."
            }

        # Contains numbers
        if any(char.isdigit() for char in value):
            return {
                "value": value,
                "valid": False,
                "error": "Customer name must not contain digits."
            }

        # Must contain at least one letter
        if not re.search(r"[A-Za-zÀ-ÿ]", value):
            return {
                "value": value,
                "valid": False,
                "error": "Customer name must contain letters."
            }

        return {
            "value": value,
            "valid": True,
            "error": None
        }

    def _validate_account(self, value: str) -> dict:
        raise NotImplementedError

    def _validate_credit_type(self, value: str) -> dict:
        raise NotImplementedError

    def _validate_amount(self, value: str) -> dict:
        raise NotImplementedError

    def _validate_date(self, value: str) -> dict:
        raise NotImplementedError
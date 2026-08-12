"""
Validation module.

This module validates the banking fields extracted from
the complete credit dossier before they are stored.
"""

import re
from datetime import datetime


class Validator:
    """
    Validate extracted banking fields.
    """

    def validate(self, fields: dict) -> dict:
        """
        Validate all extracted fields.

        Parameters
        ----------
        fields : dict
            Dictionary containing the extracted banking fields.

        Returns
        -------
        dict
            Validation results for every field and a global status.
        """

        results = {
            # ==================================================
            # CIN
            # ==================================================

            "cin": self._validate_cin(
                fields.get("cin", "")
            ),

            # ==================================================
            # Client name
            # ==================================================

            "nom_prenom": self._validate_name(
                fields.get("nom_prenom", "")
            ),

            # ==================================================
            # Account number
            # ==================================================

            "numero_compte": self._validate_account(
                fields.get("numero_compte", "")
            ),

            # ==================================================
            # Credit type
            # ==================================================

            "nature_credit": self._validate_credit_type(
                fields.get("nature_credit", "")
            ),

            # ==================================================
            # Credit amount
            # ==================================================

            "montant_credit": self._validate_amount(
                fields.get("montant_credit", "")
            ),

            # ==================================================
            # Decision date
            # ==================================================

            "date_de_decision": self._validate_date(
                fields.get("date_de_decision", "")
            ),

            # ==================================================
            # Archive date
            # ==================================================

            "date_archivage": self._validate_optional_date(
                fields.get("date_archivage", "")
            ),
        }

        is_valid = all(
            field["status"] == "valid"
            for field in results.values()
        )

        return {
            "fields": results,
            "is_valid": is_valid,
        }

    # ==========================================================
    # CIN validation
    # ==========================================================

    def _validate_cin(self, value: str) -> dict:
        """
        Validate the customer's CIN.

        Expected format:
        - One or two letters
        - Followed by digits

        Examples:
        - A123456
        - AB123456

        The validation is case-insensitive.
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "CIN is missing."
            }

        # Normalize letters to uppercase.
        normalized_value = value.upper()

        # Expected format:
        # 1 or 2 letters + one or more digits
        if not re.fullmatch(
            r"[A-Z]{1,2}\d+",
            normalized_value
        ):
            return {
                "value": value,
                "status": "invalid",
                "error": (
                    "Invalid CIN format. "
                    "Expected one or two letters followed by digits."
                )
            }

        return {
            "value": normalized_value,
            "status": "valid",
            "error": None
        }

    # ==========================================================
    # Name validation
    # ==========================================================

    def _validate_name(self, value: str) -> dict:
        """
        Validate the customer's full name.

        Rules:
        - Cannot be empty.
        - Must contain at least one letter.
        - Cannot contain digits.
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "Customer name is missing."
            }

        if any(char.isdigit() for char in value):
            return {
                "value": value,
                "status": "invalid",
                "error": "Customer name must not contain digits."
            }

        if not re.search(
            r"[A-Za-zÀ-ÿ]",
            value
        ):
            return {
                "value": value,
                "status": "invalid",
                "error": "Customer name must contain letters."
            }

        return {
            "value": value,
            "status": "valid",
            "error": None
        }

    # ==========================================================
    # Account number validation
    # ==========================================================

    def _validate_account(self, value: str) -> dict:
        """
        Validate the bank account number.

        Rules:
        - Cannot be empty.
        - Must contain exactly 16 digits.
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "Account number is missing."
            }

        if not value.isdigit():
            return {
                "value": value,
                "status": "invalid",
                "error": (
                    "Account number must contain digits only."
                )
            }

        if len(value) != 16:
            return {
                "value": value,
                "status": "invalid",
                "error": (
                    "Account number must contain exactly "
                    "16 digits."
                )
            }

        return {
            "value": value,
            "status": "valid",
            "error": None
        }

    # ==========================================================
    # Credit type validation
    # ==========================================================

    def _validate_credit_type(self, value: str) -> dict:
        """
        Validate the nature of the credit.

        The credit type is not compared against a fixed list,
        because credit types may vary between documents.

        Rules:
        - Cannot be empty.
        - Must contain at least one letter.
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "Credit type is missing."
            }

        if not re.search(
            r"[A-Za-zÀ-ÿ]",
            value
        ):
            return {
                "value": value,
                "status": "invalid",
                "error": (
                    "Credit type must contain letters."
                )
            }

        return {
            "value": value,
            "status": "valid",
            "error": None
        }

    # ==========================================================
    # Amount validation
    # ==========================================================

    def _validate_amount(self, value: str) -> dict:
        """
        Validate the credit amount.

        Accepted examples:
        - 740000
        - 740000,00
        - 740 000,00
        - 740 000,00 DHs
        - 740000.00
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "Credit amount is missing."
            }

        # Remove currency symbols and letters.
        cleaned_value = re.sub(
            r"[^\d,.\s]",
            "",
            value
        ).strip()

        # Remove spaces used as thousands separators.
        cleaned_value = cleaned_value.replace(
            " ",
            ""
        )

        # Accept:
        # 740000
        # 740000,00
        # 740000.00
        valid_format = re.fullmatch(
            r"\d+(?:[,.]\d{1,2})?",
            cleaned_value
        )

        if not valid_format:
            return {
                "value": value,
                "status": "invalid",
                "error": "Invalid credit amount format."
            }

        try:
            numeric_value = float(
                cleaned_value.replace(
                    ",",
                    "."
                )
            )

        except ValueError:
            return {
                "value": value,
                "status": "invalid",
                "error": "Credit amount must be numeric."
            }

        if numeric_value <= 0:
            return {
                "value": value,
                "status": "invalid",
                "error": (
                    "Credit amount must be greater than zero."
                )
            }

        return {
            "value": value,
            "status": "valid",
            "error": None
        }

    # ==========================================================
    # Required date validation
    # ==========================================================

    def _validate_date(self, value: str) -> dict:
        """
        Validate a required date.

        Accepted formats:
        - DD/MM/YYYY
        - DD-MM-YYYY
        - YYYY-MM-DD
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "invalid",
                "error": "Date is missing."
            }

        accepted_formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%Y-%m-%d",
        ]

        for date_format in accepted_formats:

            try:
                datetime.strptime(
                    value,
                    date_format
                )

                return {
                    "value": value,
                    "status": "valid",
                    "error": None
                }

            except ValueError:
                continue

        return {
            "value": value,
            "status": "invalid",
            "error": (
                "Invalid date format. Expected "
                "DD/MM/YYYY, DD-MM-YYYY, or YYYY-MM-DD."
            )
        }

    # ==========================================================
    # Optional date validation
    # ==========================================================

    def _validate_optional_date(
        self,
        value: str
    ) -> dict:
        """
        Validate an optional date.

        An empty value is valid because the field
        is not mandatory.
        """

        value = str(value).strip()

        if not value:
            return {
                "value": value,
                "status": "valid",
                "error": None
            }

        return self._validate_date(value)
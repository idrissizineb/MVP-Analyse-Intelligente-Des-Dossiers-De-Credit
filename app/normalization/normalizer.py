"""
Normalization module.

This module converts validated extracted values into
standard Python types before database storage.
"""

import re


class Normalizer:
    """
    Normalize validated banking fields.
    """

    def normalize(
        self,
        fields: dict
    ) -> dict:
        """
        Normalize all extracted banking fields.

        Parameters
        ----------
        fields : dict
            Validated extracted fields.

        Returns
        -------
        dict
            Normalized fields.
        """

        return {
            # ==================================================
            # CIN
            # ==================================================

            "cin": self._normalize_cin(
                fields["cin"]
            ),

            # ==================================================
            # Name
            # ==================================================

            "nom_prenom": self._normalize_name(
                fields["nom_prenom"]
            ),

            # ==================================================
            # Account number
            # ==================================================

            "numero_compte": self._normalize_account(
                fields["numero_compte"]
            ),

            # ==================================================
            # Credit type
            # ==================================================

            "nature_credit": self._normalize_credit_type(
                fields["nature_credit"]
            ),

            # ==================================================
            # Amount
            # ==================================================

            "montant_credit": self._normalize_amount(
                fields["montant_credit"]
            ),

            # ==================================================
            # Decision date
            # ==================================================

            "date_de_decision": self._normalize_date(
                fields["date_de_decision"]
            ),

            # ==================================================
            # Archive date
            # ==================================================

            "date_archivage": self._normalize_date(
                fields["date_archivage"]
            ),
        }

    # ==========================================================
    # CIN
    # ==========================================================

    def _normalize_cin(
        self,
        value: str
    ) -> str:

        """
        Normalize the CIN.

        The CIN is converted to uppercase and
        surrounding spaces are removed.

        Example:
            ab123456 -> AB123456
        """

        return str(value).strip().upper()

    # ==========================================================
    # Name
    # ==========================================================

    def _normalize_name(
        self,
        value: str
    ) -> str:

        return value.strip()

    # ==========================================================
    # Account number
    # ==========================================================

    def _normalize_account(
        self,
        value: str
    ) -> str:

        return value.strip()

    # ==========================================================
    # Credit type
    # ==========================================================

    def _normalize_credit_type(
        self,
        value: str
    ) -> str:

        return value.strip()

    # ==========================================================
    # Amount
    # ==========================================================

    def _normalize_amount(
        self,
        value: str
    ) -> float:

        normalized_value = value.strip()

        # Remove currency text
        normalized_value = (
            normalized_value
            .replace("DHs", "")
            .replace("Dhs", "")
            .replace("DH", "")
            .replace("dh", "")
            .strip()
        )

        # Remove regular and Unicode spaces used as thousands
        # separators (NBSP, narrow NBSP, thin space, etc.)
        normalized_value = re.sub(r"\s+", "", normalized_value)

        # Convert French decimal separator
        normalized_value = (
            normalized_value
            .replace(",", ".")
        )

        return float(normalized_value)

    # ==========================================================
    # Date
    # ==========================================================

    def _normalize_date(
        self,
        value: str | None
    ) -> str | None:

        if not value:
            return None

        return value.strip()
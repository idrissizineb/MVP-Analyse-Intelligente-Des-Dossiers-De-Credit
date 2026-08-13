"""
Pseudonymization module.

Replaces sensitive customer information with temporary tokens
before sending OCR text to external LLM services.

Sensitive fields:
- CIN
- Customer name
- Bank account number
"""

import re
from typing import Dict, Tuple


class Pseudonymizer:
    """
    Pseudonymize sensitive banking information locally.
    """

    def __init__(self):
        self.mapping: Dict[str, str] = {}

    # ==========================================================
    # Pseudonymize
    # ==========================================================

    def pseudonymize(self, text: str) -> Tuple[str, Dict[str, str]]:
        """
        Replace sensitive values with pseudonym tokens.

        Returns:
            pseudonymized_text
            mapping used to restore original values
        """

        self.mapping = {}

        # ------------------------------------------------------
        # Account numbers
        # ------------------------------------------------------

        text = self._replace_accounts(text)

        # ------------------------------------------------------
        # CIN
        # ------------------------------------------------------

        text = self._replace_cins(text)

        # ------------------------------------------------------
        # Customer names
        # ------------------------------------------------------

        text = self._replace_names(text)

        return text, self.mapping

    # ==========================================================
    # Restore
    # ==========================================================

    def restore(self, text: str) -> str:
        """
        Restore original sensitive values.
        """

        # Replace longest tokens first
        for token, original in sorted(
            self.mapping.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):
            text = text.replace(token, original)

        return text

    # ==========================================================
    # Account number
    # ==========================================================

    def _replace_accounts(self, text: str) -> str:
        """
        Replace 16-digit bank account numbers.

        Example:
            1234567891234567
            ->
            [ACCOUNT_001]
        """

        pattern = r"\b\d{16}\b"

        def replacement(match):

            original = match.group(0)

            token = self._create_token(
                "ACCOUNT",
                original
            )

            return token

        return re.sub(
            pattern,
            replacement,
            text
        )

    # ==========================================================
    # CIN
    # ==========================================================

    def _replace_cins(self, text: str) -> str:
        """
        Replace Moroccan CIN-like identifiers.

        Expected format:
            one or two letters followed by digits.

        Examples:
            CIN_001
            AB123456
        """

        pattern = r"\b[A-Za-z]{1,2}\d{4,8}\b"

        def replacement(match):

            original = match.group(0)

            token = self._create_token(
                "CIN",
                original
            )

            return token

        return re.sub(
            pattern,
            replacement,
            text
        )

    # ==========================================================
    # Customer name
    # ==========================================================

    def _replace_names(self, text: str) -> str:
        """
        Replace customer names appearing after identity labels.

        Only capture the name on the same line.
        """

        patterns = [
            r"(?im)(Nom\s+et\s+prénom\s*:\s*)([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",
            r"(?im)(Nom\s*:\s*)([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",
        ]

        for pattern in patterns:

            def replacement(match):

                prefix = match.group(1)
                original = match.group(2).strip()

                token = self._create_token(
                    "PERSON",
                    original
                )

                return prefix + token

            text = re.sub(
                pattern,
                replacement,
                text
            )

        return text

    # ==========================================================
    # Token creation
    # ==========================================================

    def _create_token(
        self,
        category: str,
        original: str
    ) -> str:

        # Reuse existing token if value was already encountered
        for token, value in self.mapping.items():

            if value == original:

                return token

        number = sum(
            1
            for token in self.mapping
            if token.startswith(f"[{category}_")
        ) + 1

        token = f"[{category}_{number:03d}]"

        self.mapping[token] = original

        return token
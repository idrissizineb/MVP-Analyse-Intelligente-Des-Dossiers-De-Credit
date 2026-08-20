"""
Pseudonymization module.

Replaces sensitive customer information with temporary tokens
before sending OCR text to external LLM services.

Sensitive fields:
- CIN
- Customer name
- Bank account number

The pseudonymization mapping is shared across the entire
document so the same sensitive value always receives the
same pseudonym.
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
    # PSEUDONYMIZE
    # ==========================================================

    def pseudonymize(
        self,
        text: str
    ) -> Tuple[str, Dict[str, str]]:
        """
        Replace sensitive values with pseudonym tokens.

        The existing mapping is preserved so information detected
        on a previous page can be recognized on later pages.

        Returns:
            pseudonymized_text
            mapping used to restore original values
        """

        # IMPORTANT:
        # Do NOT reset self.mapping here.
        #
        # The mapping must survive between pages.
        #
        # Page 1:
        #   IDRISSI ZINEB -> [PERSON_001]
        #
        # Page 2:
        #   ZINEB IDRISSI -> [PERSON_001]

        # ------------------------------------------------------
        # Existing known PERSON values
        # ------------------------------------------------------

        text = self._replace_known_persons(text)

        # ------------------------------------------------------
        # Account numbers
        # ------------------------------------------------------

        text = self._replace_accounts(text)

        # ------------------------------------------------------
        # CIN
        # ------------------------------------------------------

        text = self._replace_cins(text)

        # ------------------------------------------------------
        # Customer names after labels
        # ------------------------------------------------------

        text = self._replace_names(text)

        # ------------------------------------------------------
        # Name split across multiple OCR lines
        # ------------------------------------------------------

        text = self._replace_known_person_parts(text)

        return text, self.mapping.copy()

    # ==========================================================
    # RESTORE
    # ==========================================================

    def restore(self, text: str) -> str:
        """
        Restore original sensitive values.
        """

        for token, original in sorted(
            self.mapping.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):
            text = text.replace(
                token,
                original
            )

        return text

    # ==========================================================
    # ACCOUNT NUMBER
    # ==========================================================

    def _replace_accounts(
        self,
        text: str
    ) -> str:
        """
        Replace 16-digit bank account numbers.
        """

        pattern = r"\b\d{16}\b"

        def replacement(match):

            original = match.group(0)

            return self._create_token(
                "ACCOUNT",
                original
            )

        return re.sub(
            pattern,
            replacement,
            text
        )

    # ==========================================================
    # CIN
    # ==========================================================

    def _replace_cins(
        self,
        text: str
    ) -> str:
        """
        Replace Moroccan CIN-like identifiers.
        """

        pattern = r"\b[A-Za-z]{1,2}\d{4,8}\b"

        def replacement(match):

            original = match.group(0)

            return self._create_token(
                "CIN",
                original
            )

        return re.sub(
            pattern,
            replacement,
            text
        )

    # ==========================================================
    # CUSTOMER NAME AFTER LABEL
    # ==========================================================

    def _replace_names(
        self,
        text: str
    ) -> str:
        """
        Replace customer names appearing after identity labels.
        """

        patterns = [

            r"(?im)"
            r"(Nom\s+et\s+prénom\s*:\s*)"
            r"([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",

            r"(?im)"
            r"(Nom\s*:\s*)"
            r"([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",
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
    # REPLACE KNOWN PERSON VALUES
    # ==========================================================

    def _replace_known_persons(
        self,
        text: str
    ) -> str:
        """
        Replace person names already discovered on a previous page.

        Example:

        Existing mapping:
            [PERSON_001] -> IDRISSI ZINEB

        New page:
            ZINEB IDRISSI

        This method also recognizes the reversed order.
        """

        person_entries = [
            (token, value)
            for token, value in self.mapping.items()
            if token.startswith("[PERSON_")
        ]

        # Longest names first
        person_entries.sort(
            key=lambda item: len(item[1]),
            reverse=True
        )

        for token, original in person_entries:

            normalized_original = self._normalize_name(
                original
            )

            parts = normalized_original.split()

            if len(parts) < 2:
                continue

            # --------------------------------------------------
            # Original order
            # --------------------------------------------------

            original_pattern = self._name_pattern(
                parts
            )

            text = re.sub(
                original_pattern,
                token,
                text,
                flags=re.IGNORECASE
            )

            # --------------------------------------------------
            # Reversed order
            # --------------------------------------------------

            reversed_parts = list(
                reversed(parts)
            )

            reversed_pattern = self._name_pattern(
                reversed_parts
            )

            text = re.sub(
                reversed_pattern,
                token,
                text,
                flags=re.IGNORECASE
            )

        return text

    # ==========================================================
    # REPLACE SPLIT NAME
    # ==========================================================

    def _replace_known_person_parts(
        self,
        text: str
    ) -> str:
        """
        Handles OCR where the name is split across lines.

        Example:

            ZINEB
            IDRISSI

        becomes:

            [PERSON_001]
        """

        person_entries = [
            (token, value)
            for token, value in self.mapping.items()
            if token.startswith("[PERSON_")
        ]

        for token, original in person_entries:

            parts = self._normalize_name(
                original
            ).split()

            if len(parts) < 2:
                continue

            first = re.escape(parts[0])
            second = re.escape(parts[1])

            # --------------------------------------------------
            # Same line
            # --------------------------------------------------

            pattern_same_line = (
                rf"\b{first}\s+{second}\b"
            )

            text = re.sub(
                pattern_same_line,
                token,
                text,
                flags=re.IGNORECASE
            )

            # --------------------------------------------------
            # Reversed same line
            # --------------------------------------------------

            pattern_reversed = (
                rf"\b{second}\s+{first}\b"
            )

            text = re.sub(
                pattern_reversed,
                token,
                text,
                flags=re.IGNORECASE
            )

            # --------------------------------------------------
            # Split across lines
            # --------------------------------------------------

            pattern_split = (
                rf"\b{first}\s*\n\s*{second}\b"
            )

            text = re.sub(
                pattern_split,
                token,
                text,
                flags=re.IGNORECASE
            )

            # --------------------------------------------------
            # Reversed split
            # --------------------------------------------------

            pattern_split_reversed = (
                rf"\b{second}\s*\n\s*{first}\b"
            )

            text = re.sub(
                pattern_split_reversed,
                token,
                text,
                flags=re.IGNORECASE
            )

        return text

    # ==========================================================
    # NORMALIZE NAME
    # ==========================================================

    def _normalize_name(
        self,
        name: str
    ) -> str:
        """
        Normalize spaces and case for name comparison.
        """

        return " ".join(
            name.strip().split()
        )

    # ==========================================================
    # NAME REGEX
    # ==========================================================

    def _name_pattern(
        self,
        parts
    ) -> str:
        """
        Build a regex allowing spaces or line breaks.
        """

        escaped_parts = [
            re.escape(part)
            for part in parts
        ]

        return (
            r"\b"
            + r"\s+".join(escaped_parts)
            + r"\b"
        )

    # ==========================================================
    # TOKEN CREATION
    # ==========================================================

    def _create_token(
        self,
        category: str,
        original: str
    ) -> str:
        """
        Create or reuse a token.
        """

        normalized_original = (
            self._normalize_name(original)
            if category == "PERSON"
            else original
        )

        # ------------------------------------------------------
        # Reuse existing token
        # ------------------------------------------------------

        for token, value in self.mapping.items():

            existing_value = (
                self._normalize_name(value)
                if token.startswith("[PERSON_")
                else value
            )

            if existing_value.lower() == (
                normalized_original.lower()
            ):

                return token

        # ------------------------------------------------------
        # Create new token
        # ------------------------------------------------------

        number = sum(
            1
            for token in self.mapping
            if token.startswith(
                f"[{category}_"
            )
        ) + 1

        token = (
            f"[{category}_{number:03d}]"
        )

        self.mapping[token] = original

        return token
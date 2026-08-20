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

    # ==========================================================
    # TEXT-TO-SQL
    # ==========================================================

    SENSITIVE_COLUMNS = {
        "cin": "CIN",
        "nom_prenom": "PERSON",
        "numero_compte": "ACCOUNT",
    }

    QUERY_NAME_STOPWORDS = {
        "quel", "quelle", "quels", "quelles",
        "est", "sont", "le", "la", "les", "du", "de", "des",
        "un", "une", "et", "ou", "pour", "par", "sur",
        "type", "nature", "montant", "credit", "crédit",
        "credits", "crédits", "client", "clients",
        "dossier", "dossiers", "document", "documents",
        "compte", "comptes", "date", "decision", "décision",
        "archivage", "enregistre", "enregistrés", "enregistres",
    }

    def pseudonymize_query(
        self,
        text: str
    ) -> str:
        """
        Mask identifiers in a natural-language question.

        Used before sending a Text-to-SQL question to Groq.
        """

        text = self._replace_known_persons(text)
        text = self._replace_accounts(text)
        text = self._replace_cins(text)
        text = self._replace_uppercase_names(text)
        text = self._replace_names_after_client_keyword(text)
        text = self._replace_known_person_parts(text)

        return text

    def apply_mapping_to_text(
        self,
        text: str
    ) -> str:
        """
        Replace already-known sensitive values inside text.
        """

        text = self._replace_known_persons(text)
        text = self._replace_accounts(text)
        text = self._replace_cins(text)
        text = self._replace_known_person_parts(text)

        return text

    def restore_query_placeholders(
        self,
        text: str
    ) -> str:
        """
        Restore original values in an LLM answer.

        Also recovers tokens if the model dropped the brackets.
        """

        restored = self.restore(text)

        for token, original in sorted(
            self.mapping.items(),
            key=lambda item: len(item[0]),
            reverse=True
        ):
            inner = token[1:-1]
            restored = restored.replace(inner, original)

        return restored

    def pseudonymize_records(
        self,
        records: list
    ) -> list:
        """
        Mask sensitive fields in SQL result rows.
        """

        return [
            self._pseudonymize_record(record)
            for record in records
        ]

    def _pseudonymize_record(
        self,
        record: dict
    ) -> dict:

        if not isinstance(record, dict):
            return record

        masked = {}

        priority_keys = [
            key
            for key in record
            if key.lower() in self.SENSITIVE_COLUMNS
        ]

        other_keys = [
            key
            for key in record
            if key not in priority_keys
        ]

        for key in priority_keys + other_keys:
            masked[key] = self._pseudonymize_field(
                key,
                record[key]
            )

        return masked

    def _pseudonymize_field(
        self,
        key: str,
        value
    ):

        if value is None:
            return None

        if isinstance(value, dict):
            return self._pseudonymize_record(value)

        if isinstance(value, list):
            return [
                self._pseudonymize_record(item)
                if isinstance(item, dict)
                else self._pseudonymize_field(key, item)
                for item in value
            ]

        if not isinstance(value, str):
            return value

        category = self.SENSITIVE_COLUMNS.get(
            key.lower()
        )

        if category:
            return self._create_token(
                category,
                value
            )

        masked = self._replace_known_persons(value)
        masked = self._replace_accounts(masked)
        masked = self._replace_cins(masked)
        masked = self._replace_known_person_parts(masked)

        return masked

    def _replace_uppercase_names(
        self,
        text: str
    ) -> str:
        """
        Replace ALL-CAPS multi-word names in questions.

        Example:
            IDRISSI ZINEB -> [PERSON_001]
        """

        pattern = (
            r"\b([A-ZÀ-Ÿ]{2,}"
            r"(?:[ \t]+[A-ZÀ-Ÿ]{2,}){1,3})\b"
        )

        def replacement(match):

            original = match.group(1)

            words = original.split()

            if all(
                word.lower() in self.QUERY_NAME_STOPWORDS
                for word in words
            ):
                return original

            return self._create_token(
                "PERSON",
                original
            )

        return re.sub(
            pattern,
            replacement,
            text
        )

    def _replace_names_after_client_keyword(
        self,
        text: str
    ) -> str:
        """
        Replace a name that follows the word 'client'.

        Example:
            client Idrissi Zineb -> client [PERSON_001]
        """

        pattern = (
            r"(?i)(\bclient(?:e)?s?\s+)"
            r"(?!\[)"
            r"([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+){0,3})"
        )

        def replacement(match):

            prefix = match.group(1)
            original = match.group(2).strip()

            words = original.split()

            if all(
                word.lower() in self.QUERY_NAME_STOPWORDS
                for word in words
            ):
                return match.group(0)

            token = self._create_token(
                "PERSON",
                original
            )

            return prefix + token

        return re.sub(
            pattern,
            replacement,
            text
        )
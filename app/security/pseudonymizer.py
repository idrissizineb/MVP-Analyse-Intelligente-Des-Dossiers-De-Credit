"""
Pseudonymization module.

Replaces sensitive customer information with temporary tokens
before sending OCR text to external LLM services.

Sensitive fields:
- CIN
- Customer name
- Bank account number

The pseudonymization is performed at document level.

Once a sensitive value is detected, all occurrences of that
value are replaced throughout the complete OCR text.

The module also handles OCR line breaks inside customer names.

Example:

    Mapping:
        [PERSON_001] -> ZINEB IDRISSI

    OCR:
        ZINEB
        IDRISSI

    Result:
        [PERSON_001]
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
        Detect and replace sensitive information.

        The process is:

        1. Detect account numbers.
        2. Detect CINs.
        3. Detect customer names.
        4. Replace all detected values globally.
        5. Verify that no original sensitive value remains.

        Returns:
            pseudonymized_text
            mapping used to restore original values
        """

        # Reset mapping for every document
        self.mapping = {}

        # ------------------------------------------------------
        # 1. Bank account numbers
        # ------------------------------------------------------

        text = self._replace_accounts(text)

        # ------------------------------------------------------
        # 2. CIN
        # ------------------------------------------------------

        text = self._replace_cins(text)

        # ------------------------------------------------------
        # 3. Customer names
        # ------------------------------------------------------

        text = self._replace_names(text)

        # ------------------------------------------------------
        # 4. Replace all known sensitive values globally
        # ------------------------------------------------------

        text = self._replace_known_values(text)

        # ------------------------------------------------------
        # 5. Security verification
        # ------------------------------------------------------

        self._verify_no_sensitive_data(text)

        return text, self.mapping

    # ==========================================================
    # RESTORE
    # ==========================================================

    def restore(self, text: str) -> str:
        """
        Restore original sensitive values using the local mapping.

        This should only be used locally.
        The mapping must never be sent to the external LLM.
        """

        # Replace longest tokens first
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
        Detect and replace 16-digit bank account numbers.

        Example:

            1234567891234567

        becomes:

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

    def _replace_cins(
        self,
        text: str
    ) -> str:
        """
        Detect and replace Moroccan CIN-like identifiers.

        Expected format:

            One or two letters followed by digits.

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
    # CUSTOMER NAME
    # ==========================================================

    def _replace_names(
        self,
        text: str
    ) -> str:
        """
        Detect customer names appearing after identity labels.

        Supported examples:

            Nom et prénom : ZINEB IDRISSI
            Nom et prenom : ZINEB IDRISSI
            Nom : ZINEB IDRISSI

        The detected name is stored in the mapping.

        It is then replaced globally by _replace_known_values().
        """

        patterns = [

            # --------------------------------------------------
            # Nom et prénom : ZINEB IDRISSI
            # --------------------------------------------------

            r"(?im)"
            r"(Nom\s+et\s+prénom\s*:\s*)"
            r"([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",

            # --------------------------------------------------
            # Nom et prenom : ZINEB IDRISSI
            # --------------------------------------------------

            r"(?im)"
            r"(Nom\s+et\s+prenom\s*:\s*)"
            r"([A-Za-zÀ-ÿ]+(?:[ \t]+[A-Za-zÀ-ÿ]+)*)",

            # --------------------------------------------------
            # Nom : ZINEB IDRISSI
            # --------------------------------------------------

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
    # GLOBAL REPLACEMENT
    # ==========================================================

    def _replace_known_values(
        self,
        text: str
    ) -> str:
        """
        Replace every previously detected sensitive value
        throughout the complete OCR text.

        This is particularly important when the same customer
        appears on several pages.

        Example:

            Page 1:
                Nom et prénom : ZINEB IDRISSI

            Page 2:
                CARTE NATIONALE D'IDENTITE
                ZINEB
                IDRISSI

        Result:

            Page 1:
                Nom et prénom : [PERSON_001]

            Page 2:
                CARTE NATIONALE D'IDENTITE
                [PERSON_001]

        The \\s+ pattern allows OCR whitespace and line breaks.
        """

        # ------------------------------------------------------
        # Process longest original values first
        # ------------------------------------------------------

        known_values = sorted(
            self.mapping.items(),
            key=lambda item: len(item[1]),
            reverse=True
        )

        for token, original in known_values:

            if not original:
                continue

            # ==================================================
            # PERSON NAME
            # ==================================================

            if token.startswith("[PERSON_"):

                name_parts = original.split()

                # --------------------------------------------------
                # Multi-part name
                # --------------------------------------------------

                if len(name_parts) >= 2:

                    # Convert:
                    #
                    # ZINEB IDRISSI
                    #
                    # into:
                    #
                    # ZINEB\s+IDRISSI
                    #
                    # which matches:
                    #
                    # ZINEB IDRISSI
                    # ZINEB  IDRISSI
                    # ZINEB
                    # IDRISSI

                    pattern = r"\s+".join(
                        re.escape(part)
                        for part in name_parts
                    )

                    text = re.sub(
                        pattern,
                        token,
                        text,
                        flags=re.IGNORECASE
                    )

                # --------------------------------------------------
                # Single-part name
                # --------------------------------------------------

                else:

                    text = re.sub(
                        re.escape(original),
                        token,
                        text,
                        flags=re.IGNORECASE
                    )

            # ==================================================
            # CIN
            # ==================================================

            elif token.startswith("[CIN_"):

                text = re.sub(
                    re.escape(original),
                    token,
                    text,
                    flags=re.IGNORECASE
                )

            # ==================================================
            # ACCOUNT
            # ==================================================

            elif token.startswith("[ACCOUNT_"):

                text = text.replace(
                    original,
                    token
                )

        return text

    # ==========================================================
    # SECURITY CHECK
    # ==========================================================

    def _verify_no_sensitive_data(
        self,
        text: str
    ) -> None:
        """
        Verify that no original sensitive value remains
        in the text before it is sent to an external LLM.

        Raises:
            ValueError:
                If sensitive information is still detected.
        """

        for token, original in self.mapping.items():

            if not original:
                continue

            # ==================================================
            # PERSON NAME
            # ==================================================

            if token.startswith("[PERSON_"):

                name_parts = original.split()

                if len(name_parts) >= 2:

                    pattern = r"\s+".join(
                        re.escape(part)
                        for part in name_parts
                    )

                    if re.search(
                        pattern,
                        text,
                        flags=re.IGNORECASE
                    ):

                        raise ValueError(
                            "PII leakage detected before "
                            f"external LLM transmission: "
                            f"{token}"
                        )

                else:

                    if re.search(
                        re.escape(original),
                        text,
                        flags=re.IGNORECASE
                    ):

                        raise ValueError(
                            "PII leakage detected before "
                            f"external LLM transmission: "
                            f"{token}"
                        )

            # ==================================================
            # CIN
            # ==================================================

            elif token.startswith("[CIN_"):

                if re.search(
                    re.escape(original),
                    text,
                    flags=re.IGNORECASE
                ):

                    raise ValueError(
                        "PII leakage detected before "
                        f"external LLM transmission: "
                        f"{token}"
                    )

            # ==================================================
            # ACCOUNT
            # ==================================================

            elif token.startswith("[ACCOUNT_"):

                if original in text:

                    raise ValueError(
                        "PII leakage detected before "
                        f"external LLM transmission: "
                        f"{token}"
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
        Create a pseudonym token.

        If the same sensitive value has already been detected,
        reuse its existing token.
        """

        # ------------------------------------------------------
        # Reuse existing token
        # ------------------------------------------------------

        for token, value in self.mapping.items():

            if value == original:

                return token

        # ------------------------------------------------------
        # Generate next token number
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
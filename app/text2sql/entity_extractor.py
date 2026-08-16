import re


class EntityExtractor:
    """
    Extract entities from user questions.

    The client is identified using their CIN.
    """

    def extract(self, question: str) -> dict:
        """
        Extract the CIN from the user's question.

        Expected CIN format:
        - 1 or 2 letters
        - followed by digits

        Examples:
        AS123456
        AB123456
        """

        # Remove punctuation
        cleaned_question = re.sub(
            r"[?.!,;:]",
            "",
            question
        )

        # Search for a CIN anywhere in the question.
        #
        # Examples:
        # AS123456
        # AB123456
        #
        cin_pattern = r"\b[A-Za-z]{1,2}\d{5,8}\b"

        match = re.search(
            cin_pattern,
            cleaned_question
        )

        if match:

            cin = match.group(0)

            return {
                "cin": cin
            }

        return {}
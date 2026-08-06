import re


class EntityExtractor:
    """
    Extract client names from user questions.
    """

    def extract(self, question: str) -> dict:

        question = re.sub(r"[?.!,;:]", "", question)

        parts = re.split(r"\bde\b", question, flags=re.IGNORECASE)

        if len(parts) > 1:

            client_name = parts[-1].strip()

            return {
                "client_name": client_name
            }

        return {}
"""
Test the banking field extraction module.
"""

import json

from app.llm.field_extractor import FieldExtractor


def main():

    # Simulated OCR output from a multi-page credit file
    corrected_pages = [

        """
        BANQUE POPULAIRE

        DEMANDE DE CREDIT

        Nature du crédit :
        Crédit Immobilier

        Date de production :
        12/06/2026
        """,

        """
        Informations du client

        Nom et prénom :
        IDRISSI ZINEB

        Numéro du compte :
        123456789123456789
        """,

        """
        Montant du crédit

        450000 MAD

        Date d'archivage

        20/06/2026
        """
    ]

    extractor = FieldExtractor()

    fields = extractor.extract(corrected_pages)

    print("\n")
    print("=" * 70)
    print("EXTRACTED FIELDS")
    print("=" * 70)

    print(json.dumps(fields, indent=4, ensure_ascii=False))


if __name__ == "__main__":
    main()
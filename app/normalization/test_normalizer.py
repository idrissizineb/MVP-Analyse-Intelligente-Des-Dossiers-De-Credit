from app.normalization.normalizer import Normalizer


def main():

    normalizer = Normalizer()

    fields = {
        "nom_prenom": "TEST CLIENT",
        "numero_compte": "2111112345670001",
        "nature_credit": "Acquisition logement",
        "montant_credit": "740 000,00 DHs",
        "date_production": "19/05/2026",
        "date_archivage": "",
    }

    normalized_fields = normalizer.normalize(
        fields
    )

    print("\n========== NORMALIZED FIELDS ==========\n")

    for field, value in normalized_fields.items():

        print(
            f"{field}: {value}"
        )

        print(
            f"Type: {type(value).__name__}"
        )


if __name__ == "__main__":
    main()
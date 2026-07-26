from app.pipeline import DocumentPipeline


def main():

    pipeline = DocumentPipeline(
        pdf_path="data/input/FICHE DE DECISION TEST.pdf",
        save_intermediate=True
    )

    result = pipeline.run()

    processed_pages = result["pages"]

    print(processed_pages[0])

    extracted_fields = result["fields"]
    validation_result = result["validation"]
    normalized_fields = result["normalized_fields"]
    dossier_id = result["dossier_id"]

    print(
        f"\nTotal processed pages: "
        f"{len(processed_pages)}"
    )

    print(
        "\n========== EXTRACTED FIELDS ==========\n"
    )

    for field, value in extracted_fields.items():

        print(
            f"{field}: {value}"
        )

    print(
        "\n========== VALIDATION RESULTS ==========\n"
    )

    for field, field_result in validation_result["fields"].items():

        print(
            f"{field}:"
        )

        print(
            f"  Value: "
            f"{field_result['value']}"
        )

        print(
            f"  Status: "
            f"{field_result['status']}"
        )

        if field_result["error"]:

            print(
                f"  Error: "
                f"{field_result['error']}"
            )

        print()

    print(
        "Overall document validity: "
        f"{validation_result['is_valid']}"
    )

    print(
        "\n========== NORMALIZED FIELDS ==========\n"
    )

    for field, value in normalized_fields.items():

        print(
            f"{field}: {value}"
        )

    print(
        "\n========== DATABASE ==========\n"
    )

    print(
        "Credit dossier saved successfully."
    )

    print(
        f"Dossier ID: {dossier_id}"
    )

    stored_dossier = pipeline.database_manager.get_dossier(dossier_id)

    print(
        "\n========== STORED DOSSIER ==========\n"
    )

    if stored_dossier:

        print(
            f"Dossier ID: {stored_dossier[0]}"
        )

        print(
            f"Client ID: {stored_dossier[1]}"
        )

        print(
            f"Account Number: {stored_dossier[2]}"
        )

        print(
            f"Credit Type: {stored_dossier[3]}"
        )

        print(
            f"Amount: {stored_dossier[4]}"
        )

        print(
            f"Production Date: {stored_dossier[5]}"
        )

        print(
            f"Archive Date: {stored_dossier[6]}"
        )

        print(
            f"Status: {stored_dossier[7]}"
        )

    else:

        print(
            "Dossier not found."
        )

    print(
        f"Document ID: {result['document_id']}"
    )

    print(
        "\n========== OCR RESULTS ==========\n"
    )

    for page_number, page in enumerate(
        processed_pages,
        start=1
    ):

        print(
            f"\n===== PAGE {page_number} =====\n"
        )

        print(
            page["corrected_text"]
        )


if __name__ == "__main__":

    main()
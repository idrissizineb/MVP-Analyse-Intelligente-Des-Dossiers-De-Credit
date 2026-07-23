from app.pipeline import DocumentPipeline


def main():

    pipeline = DocumentPipeline(
        pdf_path="data/input/FICHE DE DECISION TEST.pdf",
        save_intermediate=True
    )

    result = pipeline.run()

    processed_pages = result["pages"]
    extracted_fields = result["fields"]
    validation_result = result["validation"]

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

    for field, result in validation_result["fields"].items():

        print(
            f"{field}:"
        )

        print(
            f"  Value: {result['value']}"
        )

        status = result["status"]

        print(
            f"  Status: {status}"
        )

        if result["error"]:

            print(
                f"  Error: {result['error']}"
            )

        print()

    print(
        f"Overall document validity: "
        f"{validation_result['is_valid']}"
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
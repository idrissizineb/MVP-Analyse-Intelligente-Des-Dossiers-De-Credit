from app.pipeline import DocumentPipeline


def main():

    print(
        "\n"
        "==============================================\n"
        " PIPELINE + DATABASE INTEGRATION TEST\n"
        "==============================================\n"
    )

    # ==========================================================
    # 1. RUN THE COMPLETE PIPELINE
    # ==========================================================

    print(
        "\n========== 1. RUNNING PIPELINE ==========\n"
    )

    pipeline = DocumentPipeline(

        pdf_path="data/input/FICHE DE DECISION TEST.pdf",

        save_intermediate=True

    )

    result = pipeline.run()

    print(
        "\n✓ Pipeline executed successfully."
    )


    # ==========================================================
    # 2. VERIFY THE MAIN RESULT
    # ==========================================================

    print(
        "\n========== 2. VERIFYING PIPELINE RESULT ==========\n"
    )

    required_keys = [

        "pages",

        "fields",

        "validation",

        "normalized_fields",

        "dossier_id",

        "document_id"

    ]

    for key in required_keys:

        if key in result:

            print(
                f"✓ Result contains: {key}"
            )

        else:

            print(
                f"✗ Missing result key: {key}"
            )

            raise Exception(
                f"Pipeline result is missing: {key}"
            )


    # ==========================================================
    # 3. VERIFY DOSSIER
    # ==========================================================

    print(
        "\n========== 3. VERIFYING DOSSIER ==========\n"
    )

    dossier_id = result["dossier_id"]

    stored_dossier = (

        pipeline.database_manager.get_dossier(

            dossier_id

        )

    )

    if stored_dossier is None:

        raise Exception(
            "✗ Dossier was not found in the database."
        )

    print(
        "✓ Dossier exists in database."
    )

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


    # ==========================================================
    # 4. VERIFY DOCUMENT
    # ==========================================================

    print(
        "\n========== 4. VERIFYING DOCUMENT ==========\n"
    )

    document_id = result["document_id"]

    document = (

        pipeline.database_manager.get_document(

            document_id

        )

    )

    if document is None:

        raise Exception(
            "✗ Document was not found in the database."
        )

    print(
        "✓ Document exists in database."
    )

    print(
        f"Document ID: {document[0]}"
    )

    print(
        f"Dossier ID: {document[1]}"
    )

    print(
        f"File name: {document[2]}"
    )


    # ==========================================================
    # 5. VERIFY DOCUMENT PAGES
    # ==========================================================

    print(
        "\n========== 5. VERIFYING DOCUMENT PAGES ==========\n"
    )

    processed_pages = result["pages"]

    if len(processed_pages) == 0:

        raise Exception(
            "✗ No processed pages found."
        )

    print(
        f"✓ {len(processed_pages)} page(s) processed."
    )

    for page_number, page in enumerate(

        processed_pages,

        start=1

    ):

        print(
            f"✓ Page {page_number} processed."
        )


    # ==========================================================
    # 6. VERIFY EXTRACTED FIELDS
    # ==========================================================

    print(
        "\n========== 6. VERIFYING EXTRACTED FIELDS ==========\n"
    )

    extracted_fields = result["fields"]

    if not extracted_fields:

        raise Exception(
            "✗ No extracted fields found."
        )

    for field_name, field_value in extracted_fields.items():

        print(
            f"✓ {field_name}: {field_value}"
        )


    # ==========================================================
    # 7. VERIFY VALIDATION RESULTS
    # ==========================================================

    print(
        "\n========== 7. VERIFYING VALIDATION RESULTS ==========\n"
    )

    validation_result = result["validation"]

    validation_fields = (

        validation_result.get(

            "fields",

            {}

        )

    )

    if not validation_fields:

        raise Exception(
            "✗ No validation results found."
        )

    for field_name, field_result in validation_fields.items():

        print(
            f"✓ {field_name}"
        )

        print(
            f"  Status: "
            f"{field_result['status']}"
        )


    print(
        "\nOverall document validity: "
        f"{validation_result['is_valid']}"
    )


    # ==========================================================
    # 8. VERIFY NORMALIZED FIELDS
    # ==========================================================

    print(
        "\n========== 8. VERIFYING NORMALIZED FIELDS ==========\n"
    )

    normalized_fields = result["normalized_fields"]

    for field_name, value in normalized_fields.items():

        print(
            f"✓ {field_name}: {value}"
        )


    # ==========================================================
    # 9. VERIFY OCR RESULTS
    # ==========================================================

    print(
        "\n========== 9. VERIFYING OCR RESULTS ==========\n"
    )

    for page_number, page in enumerate(

        processed_pages,

        start=1

    ):

        if "corrected_text" not in page:

            raise Exception(

                f"✗ OCR result missing for page {page_number}"

            )

        print(

            f"✓ OCR result exists for page {page_number}"

        )

        print(

            f"Text length: "
            f"{len(page['corrected_text'])} characters"

        )


    # ==========================================================
    # 10. FINAL RESULT
    # ==========================================================

    print(
        "\n"
        "==============================================\n"
        "✓ PIPELINE + DATABASE INTEGRATION TEST PASSED\n"
        "==============================================\n"
    )


if __name__ == "__main__":

    main()
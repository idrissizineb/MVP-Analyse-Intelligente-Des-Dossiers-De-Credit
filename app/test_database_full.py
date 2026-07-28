from app.pipeline import DocumentPipeline


def main():

    print(
        "\n"
        "==============================================\n"
        "       FULL DATABASE INTEGRATION TEST\n"
        "==============================================\n"
    )

    # ==========================================================
    # 1. RUN PIPELINE
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
    # 2. GET IDENTIFIERS
    # ==========================================================

    dossier_id = result["dossier_id"]

    document_id = result["document_id"]

    print(
        "\n========== 2. IDENTIFIERS ==========\n"
    )

    print(
        f"Dossier ID: {dossier_id}"
    )

    print(
        f"Document ID: {document_id}"
    )

    # ==========================================================
    # 3. VERIFY DOSSIER
    # ==========================================================

    print(
        "\n========== 3. CREDIT DOSSIER ==========\n"
    )

    dossier = pipeline.database_manager.get_dossier(

        dossier_id

    )

    if dossier is None:

        raise Exception(
            "✗ Credit dossier was not found in the database."
        )

    print(
        "✓ Credit dossier found in database."
    )

    print(
        dossier
    )

    # ==========================================================
    # 4. VERIFY DOCUMENT
    # ==========================================================

    print(
        "\n========== 4. DOCUMENT ==========\n"
    )

    document = pipeline.database_manager.get_document(

        document_id

    )

    if document is None:

        raise Exception(
            "✗ Document was not found in the database."
        )

    print(
        "✓ Document found in database."
    )

    print(
        document
    )

    # ==========================================================
    # 5. VERIFY OCR RESULTS
    # ==========================================================

    print(
        "\n========== 5. OCR RESULTS ==========\n"
    )

    ocr_results = (

        pipeline.database_manager
        .get_ocr_results_by_document(
            document_id
        )

    )

    if not ocr_results:

        raise Exception(
            "✗ No OCR results found in the database."
        )

    print(
        f"✓ {len(ocr_results)} OCR result(s) found."
    )

    for ocr_result in ocr_results:

        print(
            "\nOCR RESULT:"
        )

        print(
            f"ID: {ocr_result[0]}"
        )

        print(
            f"Page ID: {ocr_result[1]}"
        )

        print(
            f"Raw text: {ocr_result[2]}"
        )

        print(
            f"Corrected text: {ocr_result[3]}"
        )

        print(
            f"Confidence: {ocr_result[5]}"
        )

    # ==========================================================
    # 6. VERIFY EXTRACTED FIELDS
    # ==========================================================

    print(
        "\n========== 6. EXTRACTED FIELDS ==========\n"
    )

    extracted_fields = (

        pipeline.database_manager
        .get_extracted_fields_by_document(
            document_id
        )

    )

    if not extracted_fields:

        raise Exception(
            "✗ No extracted fields found in the database."
        )

    print(
        f"✓ {len(extracted_fields)} extracted field(s) found."
    )

    for field in extracted_fields:

        print(
            "\nFIELD:"
        )

        print(
            f"Name: {field[2]}"
        )

        print(
            f"Value: {field[3]}"
        )

        print(
            f"Normalized value: {field[4]}"
        )

    # ==========================================================
    # 7. VERIFY VALIDATION RESULTS
    # ==========================================================

    print(
        "\n========== 7. VALIDATION RESULTS ==========\n"
    )

    validation_results = (

        pipeline.database_manager
        .get_validation_results_by_document(
            document_id
        )

    )

    if not validation_results:

        raise Exception(
            "✗ No validation results found in the database."
        )

    print(
        f"✓ {len(validation_results)} validation result(s) found."
    )

    for validation in validation_results:

        print(
            "\nVALIDATION:"
        )

        print(
            f"Field: {validation[2]}"
        )

        print(
            f"Value: {validation[3]}"
        )

        print(
            f"Status: {validation[4]}"
        )

        print(
            f"Error: {validation[5]}"
        )

    # ==========================================================
    # 8. FINAL RESULT
    # ==========================================================

    print(
        "\n"
        "==============================================\n"
        "✓ COMPLETE DATABASE VERIFICATION PASSED\n"
        "==============================================\n"
    )


if __name__ == "__main__":

    main()
from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


def main():

    print("\n========== DATABASE RELATIONSHIP TEST ==========\n")

    # ======================================================
    # 1. DATABASE CONNECTION
    # ======================================================

    database_connection = DatabaseConnection()

    database_manager = DatabaseManager(
        database_connection=database_connection
    )

    database_manager.initialize_database()

    # ======================================================
    # 2. CREATE CLIENT
    # ======================================================

    print("\n========== 1. CLIENT ==========\n")

    client_id = database_manager.create_client(
        nom_prenom="TEST CLIENT"
    )

    print(
        f"✓ Client created successfully."
    )

    print(
        f"Client ID: {client_id}"
    )

    # ======================================================
    # 3. CREATE CREDIT DOSSIER
    # ======================================================

    print("\n========== 2. CREDIT DOSSIER ==========\n")

    dossier_id = database_manager.create_dossier(

        client_id=client_id,

        numero_compte="TEST123456789",

        nature_credit="Acquisition logement",

        montant_credit=740000.0,

        date_production="19/05/2026",

        date_archivage=None,

        statut="en_analyse"

    )

    print(
        "✓ Credit dossier created successfully."
    )

    print(
        f"Dossier ID: {dossier_id}"
    )

    # ======================================================
    # 4. CREATE DOCUMENT
    # ======================================================

    print("\n========== 3. DOCUMENT ==========\n")

    document_id = database_manager.create_document(

        dossier_id=dossier_id,

        nom_fichier="test_fiche_decision.pdf",

        type_document="fiche_decision",

        nombre_pages=1,

        chemin_fichier="data/test/test_fiche_decision.pdf"

    )

    print(
        "✓ Document created successfully."
    )

    print(
        f"Document ID: {document_id}"
    )

    # ======================================================
    # 5. CREATE DOCUMENT PAGE
    # ======================================================

    print("\n========== 4. DOCUMENT PAGE ==========\n")

    page_id = database_manager.create_document_page(

        document_id=document_id,

        numero_page=1,

        chemin_image="data/processed/page_1_resized.png"

    )

    print(
        "✓ Document page created successfully."
    )

    print(
        f"Page ID: {page_id}"
    )

    # ======================================================
    # 6. SAVE OCR RESULT
    # ======================================================

    print("\n========== 5. OCR RESULT ==========\n")

    ocr_result_id = database_manager.save_ocr_result(

        page_id=page_id,

        raw_text="TEST RAW OCR TEXT",

        corrected_text="TEST CORRECTED OCR TEXT",

        raw_ocr_json='{"text": "TEST RAW OCR TEXT"}',

        average_confidence=0.95,

        ocr_engine="PaddleOCR"

    )

    print(
        "✓ OCR result saved successfully."
    )

    print(
        f"OCR Result ID: {ocr_result_id}"
    )

    # ======================================================
    # 7. SAVE EXTRACTED FIELDS
    # ======================================================

    print("\n========== 6. EXTRACTED FIELDS ==========\n")

    fields = {

        "nom_prenom": "TEST CLIENT",

        "numero_compte": "TEST123456789",

        "nature_credit": "Acquisition logement",

        "montant_credit": "740 000,00 DHs",

        "date_production": "19/05/2026",

        "date_archivage": None

    }

    normalized_fields = {

        "nom_prenom": "TEST CLIENT",

        "numero_compte": "TEST123456789",

        "nature_credit": "Acquisition logement",

        "montant_credit": "740000.0",

        "date_production": "19/05/2026",

        "date_archivage": None

    }

    extracted_field_ids = database_manager.save_extracted_fields(

        document_id=document_id,

        fields=fields,

        normalized_fields=normalized_fields

    )

    print(
        "✓ Extracted fields saved successfully."
    )

    print(
        f"Extracted field IDs: {extracted_field_ids}"
    )

    # ======================================================
    # 8. SAVE VALIDATION RESULTS
    # ======================================================

    print("\n========== 7. VALIDATION RESULTS ==========\n")

    validation_result = {

        "fields": {

            "nom_prenom": {

                "value": "TEST CLIENT",

                "status": "valid",

                "error": None

            },

            "numero_compte": {

                "value": "TEST123456789",

                "status": "valid",

                "error": None

            },

            "nature_credit": {

                "value": "Acquisition logement",

                "status": "valid",

                "error": None

            },

            "montant_credit": {

                "value": "740 000,00 DHs",

                "status": "valid",

                "error": None

            },

            "date_production": {

                "value": "19/05/2026",

                "status": "valid",

                "error": None

            },

            "date_archivage": {

                "value": None,

                "status": "valid",

                "error": None

            }

        },

        "is_valid": True

    }

    validation_ids = database_manager.save_validation_results(

        document_id=document_id,

        validation_result=validation_result

    )

    print(
        "✓ Validation results saved successfully."
    )

    print(
        f"Validation IDs: {validation_ids}"
    )

    # ======================================================
    # 9. RETRIEVE DATA
    # ======================================================

    print("\n========== RETRIEVING DATA ==========\n")

    client = database_manager.get_client(

        client_id=client_id

    )

    dossier = database_manager.get_dossier(

        dossier_id=dossier_id

    )

    document = database_manager.get_document(

        document_id=document_id

    )

    page = database_manager.get_document_page(

        page_id=page_id

    )

    ocr_result = database_manager.get_ocr_result_by_page(

        page_id=page_id

    )

    print(
        "CLIENT:"
    )

    print(
        client
    )

    print(
        "\nDOSSIER:"
    )

    print(
        dossier
    )

    print(
        "\nDOCUMENT:"
    )

    print(
        document
    )

    print(
        "\nDOCUMENT PAGE:"
    )

    print(
        page
    )

    print(
        "\nOCR RESULT:"
    )

    print(
        ocr_result
    )

    # ======================================================
    # FINAL RESULT
    # ======================================================

    print(
        "\n=============================================="
    )

    print(
        "✓ COMPLETE DATABASE RELATIONSHIP TEST PASSED"
    )

    print(
        "==============================================\n"
    )


if __name__ == "__main__":

    main()
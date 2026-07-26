from data.database.connection import DatabaseConnection
from data.database.database_manager import DatabaseManager


def main():

    database_connection = DatabaseConnection()

    database_manager = DatabaseManager(
        database_connection=database_connection
    )

    database_manager.initialize_database()

    dossier_id = 8

    document_id = database_manager.create_document(
        dossier_id=dossier_id,
        nom_fichier="FICHE DE DECISION TEST.pdf",
        type_document="FICHE_DE_DECISION",
        nombre_pages=1,
        chemin_fichier="data/input/FICHE DE DECISION TEST.pdf"
    )

    print(
        f"Document created successfully."
    )

    print(
        f"Document ID: {document_id}"
    )

    document = database_manager.get_document(
        document_id=document_id
    )

    print(
        "\n========== STORED DOCUMENT =========="
    )

    print(
        f"Document ID: {document[0]}"
    )

    print(
        f"Dossier ID: {document[1]}"
    )

    print(
        f"File Name: {document[2]}"
    )

    print(
        f"Document Type: {document[3]}"
    )

    print(
        f"Number of Pages: {document[4]}"
    )

    print(
        f"File Path: {document[5]}"
    )

    database_connection.close()

    print(
        "\nDatabase connection closed."
    )

    page_id = database_manager.create_document_page(
        document_id=1,
        numero_page=1,
        chemin_image="data/processed/page_1_resized.png"
    )

    print(
        f"Page created successfully."
    )

    print(
        f"Page ID: {page_id}"
    )

    page = database_manager.get_document_page(
        page_id=page_id
    )

    print(page)

if __name__ == "__main__":
    main()
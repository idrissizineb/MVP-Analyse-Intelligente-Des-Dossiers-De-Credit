"""
Database management module.

This module initializes and manages the database schema and
provides CRUD operations for clients, credit dossiers,
documents, pages, OCR results, extracted fields, and
validation results.
"""

from data.database.connection import DatabaseConnection  # pyright: ignore[reportMissingImports]

from data.database.models import (
    CREATE_CLIENT_TABLE,
    CREATE_DOSSIER_CREDIT_TABLE,
    CREATE_DOCUMENT_TABLE,
    CREATE_DOCUMENT_PAGE_TABLE,
)


class DatabaseManager:
    """
    Manage database initialization and database operations.
    """

    def __init__(
        self,
        database_connection: DatabaseConnection
    ):
        """
        Initialize the database manager.

        Parameters
        ----------
        database_connection : DatabaseConnection
            Database connection manager.
        """

        self.database_connection = database_connection

    # ==========================================================
    # DATABASE INITIALIZATION
    # ==========================================================

    def initialize_database(self) -> None:
        """
        Create all database tables if they do not already exist.
        """

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        # ------------------------------------------------------
        # Existing tables
        # ------------------------------------------------------

        cursor.execute(
            CREATE_CLIENT_TABLE
        )

        cursor.execute(
            CREATE_DOSSIER_CREDIT_TABLE
        )

        cursor.execute(
            CREATE_DOCUMENT_TABLE
        )

        cursor.execute(
            CREATE_DOCUMENT_PAGE_TABLE
        )

        # ------------------------------------------------------
        # OCR RESULTS TABLE
        # ------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS ocr_results (

                ocr_result_id INTEGER PRIMARY KEY AUTOINCREMENT,

                page_id INTEGER NOT NULL,

                raw_text TEXT,

                corrected_text TEXT,

                raw_ocr_json TEXT,

                average_confidence REAL,

                ocr_engine TEXT DEFAULT 'PaddleOCR',

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (page_id)
                    REFERENCES document_page(page_id)
                    ON DELETE CASCADE
            )
            """
        )

        # ------------------------------------------------------
        # EXTRACTED FIELDS TABLE
        # ------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS extracted_fields (

                extracted_field_id INTEGER PRIMARY KEY AUTOINCREMENT,

                document_id INTEGER NOT NULL,

                field_name TEXT NOT NULL,

                field_value TEXT,

                normalized_value TEXT,

                confidence REAL,

                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (document_id)
                    REFERENCES document(document_id)
                    ON DELETE CASCADE
            )
            """
        )

        # ------------------------------------------------------
        # VALIDATION RESULTS TABLE
        # ------------------------------------------------------

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS validation_results (

                validation_id INTEGER PRIMARY KEY AUTOINCREMENT,

                document_id INTEGER NOT NULL,

                field_name TEXT NOT NULL,

                field_value TEXT,

                status TEXT NOT NULL,

                error_message TEXT,

                validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                FOREIGN KEY (document_id)
                    REFERENCES document(document_id)
                    ON DELETE CASCADE
            )
            """
        )

        connection.commit()

        cursor.close()

        print(
            "✓ Database initialized successfully."
        )

    # ==========================================================
    # CLIENT
    # ==========================================================

    def create_client(
        self,
        nom_prenom: str
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO client (
                nom_prenom
            )
            VALUES (?)
            """,
            (
                nom_prenom,
            )
        )

        connection.commit()

        client_id = cursor.lastrowid

        cursor.close()

        return client_id

    def get_client(
        self,
        client_id: int
    ) -> tuple | None:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                client_id,
                nom_prenom,
                created_at
            FROM client
            WHERE client_id = ?
            """,
            (
                client_id,
            )
        )

        client = cursor.fetchone()

        cursor.close()

        return client

    def get_client_by_name(
        self,
        nom_prenom: str
    ) -> tuple | None:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                client_id,
                nom_prenom,
                created_at
            FROM client
            WHERE nom_prenom = ?
            """,
            (
                nom_prenom,
            )
        )

        client = cursor.fetchone()

        cursor.close()

        return client

    def get_or_create_client(
        self,
        nom_prenom: str
    ) -> int:

        client = self.get_client_by_name(
            nom_prenom
        )

        if client is not None:

            return client[0]

        return self.create_client(
            nom_prenom=nom_prenom
        )

    # ==========================================================
    # CREDIT DOSSIER
    # ==========================================================

    def create_dossier(
        self,
        client_id: int,
        numero_compte: str,
        nature_credit: str,
        montant_credit: float,
        date_production: str | None = None,
        date_archivage: str | None = None,
        statut: str = "en_analyse",
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO dossier_credit (

                client_id,

                numero_compte,

                nature_credit,

                montant_credit,

                date_production,

                date_archivage,

                statut

            )

            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                client_id,
                numero_compte,
                nature_credit,
                montant_credit,
                date_production,
                date_archivage,
                statut,
            )
        )

        connection.commit()

        dossier_id = cursor.lastrowid

        cursor.close()

        return dossier_id

    def get_dossier(
        self,
        dossier_id: int
    ) -> tuple | None:

        query = """

        SELECT

            dossier_id,

            client_id,

            numero_compte,

            nature_credit,

            montant_credit,

            date_production,

            date_archivage,

            statut,

            created_at

        FROM dossier_credit

        WHERE dossier_id = ?

        """

        return self.database_connection.fetch_one(
            query,
            (
                dossier_id,
            )
        )

    def get_client_dossiers(
        self,
        client_id: int
    ) -> list[tuple]:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT

                dossier_id,

                client_id,

                numero_compte,

                nature_credit,

                montant_credit,

                date_production,

                date_archivage,

                statut,

                created_at

            FROM dossier_credit

            WHERE client_id = ?

            """,
            (
                client_id,
            )
        )

        dossiers = cursor.fetchall()

        cursor.close()

        return dossiers

    def save_credit_dossier(
        self,
        fields: dict
    ) -> int:

        client_id = self.get_or_create_client(
            nom_prenom=fields["nom_prenom"]
        )

        dossier_id = self.create_dossier(

            client_id=client_id,

            numero_compte=fields["numero_compte"],

            nature_credit=fields["nature_credit"],

            montant_credit=fields["montant_credit"],

            date_production=fields["date_production"],

            date_archivage=fields["date_archivage"],

        )

        return dossier_id

    # ==========================================================
    # DOCUMENT
    # ==========================================================

    def create_document(
        self,
        dossier_id: int,
        nom_fichier: str,
        type_document: str | None,
        nombre_pages: int,
        chemin_fichier: str
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO document (

                dossier_id,

                nom_fichier,

                type_document,

                nombre_pages,

                chemin_fichier

            )

            VALUES (?, ?, ?, ?, ?)

            """,
            (
                dossier_id,
                nom_fichier,
                type_document,
                nombre_pages,
                chemin_fichier
            )
        )

        connection.commit()

        document_id = cursor.lastrowid

        cursor.close()

        return document_id

    def get_document(
        self,
        document_id: int
    ) -> tuple | None:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT

                document_id,

                dossier_id,

                nom_fichier,

                type_document,

                nombre_pages,

                chemin_fichier,

                created_at

            FROM document

            WHERE document_id = ?

            """,
            (
                document_id,
            )
        )

        document = cursor.fetchone()

        cursor.close()

        return document

    # ==========================================================
    # DOCUMENT PAGE
    # ==========================================================

    def create_document_page(
        self,
        document_id: int,
        numero_page: int,
        chemin_image: str
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO document_page (

                document_id,

                numero_page,

                chemin_image

            )

            VALUES (?, ?, ?)

            """,
            (
                document_id,
                numero_page,
                chemin_image
            )
        )

        connection.commit()

        page_id = cursor.lastrowid

        cursor.close()

        return page_id

    def get_document_page(
        self,
        page_id: int
    ) -> tuple | None:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT

                page_id,

                document_id,

                numero_page,

                chemin_image,

                created_at

            FROM document_page

            WHERE page_id = ?

            """,
            (
                page_id,
            )
        )

        page = cursor.fetchone()

        cursor.close()

        return page

    # ==========================================================
    # OCR RESULTS
    # ==========================================================

    def save_ocr_result(
        self,
        page_id: int,
        raw_text: str,
        corrected_text: str,
        raw_ocr_json: str,
        average_confidence: float,
        ocr_engine: str = "PaddleOCR"
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO ocr_results (

                page_id,

                raw_text,

                corrected_text,

                raw_ocr_json,

                average_confidence,

                ocr_engine

            )

            VALUES (?, ?, ?, ?, ?, ?)

            """,
            (
                page_id,
                raw_text,
                corrected_text,
                raw_ocr_json,
                average_confidence,
                ocr_engine
            )
        )

        connection.commit()

        ocr_result_id = cursor.lastrowid

        cursor.close()

        return ocr_result_id

    def get_ocr_result_by_page(
        self,
        page_id: int
    ) -> tuple | None:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            SELECT

                ocr_result_id,

                page_id,

                raw_text,

                corrected_text,

                raw_ocr_json,

                average_confidence,

                ocr_engine,

                created_at

            FROM ocr_results

            WHERE page_id = ?

            ORDER BY created_at DESC

            LIMIT 1

            """,
            (
                page_id,
            )
        )

        result = cursor.fetchone()

        cursor.close()

        return result

    # ==========================================================
    # EXTRACTED FIELDS
    # ==========================================================

    def save_extracted_field(
        self,
        document_id: int,
        field_name: str,
        field_value: str | None,
        normalized_value: str | None = None,
        confidence: float | None = None
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO extracted_fields (

                document_id,

                field_name,

                field_value,

                normalized_value,

                confidence

            )

            VALUES (?, ?, ?, ?, ?)

            """,
            (
                document_id,
                field_name,
                field_value,
                normalized_value,
                confidence
            )
        )

        connection.commit()

        extracted_field_id = cursor.lastrowid

        cursor.close()

        return extracted_field_id

    def save_extracted_fields(
        self,
        document_id: int,
        fields: dict,
        normalized_fields: dict | None = None
    ) -> list[int]:

        extracted_field_ids = []

        normalized_fields = normalized_fields or {}

        for field_name, field_value in fields.items():

            normalized_value = normalized_fields.get(
                field_name
            )

            field_id = self.save_extracted_field(

                document_id=document_id,

                field_name=field_name,

                field_value=field_value,

                normalized_value=normalized_value,

                confidence=None

            )

            extracted_field_ids.append(
                field_id
            )

        return extracted_field_ids

    # ==========================================================
    # VALIDATION RESULTS
    # ==========================================================

    def save_validation_result(
        self,
        document_id: int,
        field_name: str,
        field_value: str | None,
        status: str,
        error_message: str | None = None
    ) -> int:

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """

            INSERT INTO validation_results (

                document_id,

                field_name,

                field_value,

                status,

                error_message

            )

            VALUES (?, ?, ?, ?, ?)

            """,
            (
                document_id,
                field_name,
                field_value,
                status,
                error_message
            )
        )

        connection.commit()

        validation_id = cursor.lastrowid

        cursor.close()

        return validation_id

    def save_validation_results(
        self,
        document_id: int,
        validation_result: dict
    ) -> list[int]:

        validation_ids = []

        fields = validation_result.get(
            "fields",
            {}
        )

        for field_name, result in fields.items():

            validation_id = self.save_validation_result(

                document_id=document_id,

                field_name=field_name,

                field_value=result.get(
                    "value"
                ),

                status=result.get(
                    "status"
                ),

                error_message=result.get(
                    "error"
                )

            )

            validation_ids.append(
                validation_id
            )

        return validation_ids
"""
Database management module.

This module initializes and manages the database schema.
"""

from data.database.connection import DatabaseConnection  # pyright: ignore[reportMissingImports]
from data.database.models import ( CREATE_CLIENT_TABLE, CREATE_DOSSIER_CREDIT_TABLE, CREATE_DOCUMENT_TABLE, CREATE_DOCUMENT_PAGE_TABLE)  # pyright: ignore[reportMissingImports]


class DatabaseManager:
    """
    Manage database initialization and operations.
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

    def initialize_database(self) -> None:
        """
        Create the database tables if they do not exist.
        """

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(CREATE_CLIENT_TABLE)

        cursor.execute(CREATE_DOSSIER_CREDIT_TABLE)

        cursor.execute(CREATE_DOCUMENT_TABLE)

        cursor.execute(CREATE_DOCUMENT_PAGE_TABLE)

        connection.commit()

        cursor.close()

    def create_client(
        self,
        nom_prenom: str
    ) -> int:
        """
        Create a new client in the database.

        Parameters
        ----------
        nom_prenom : str
            Full name of the client.

        Returns
        -------
        int
            ID of the newly created client.
        """

        connection = self.database_connection.connect()

        cursor = connection.cursor()

        cursor.execute(
            """
            INSERT INTO client (nom_prenom)
            VALUES (?)
            """,
            (nom_prenom,)
        )

        connection.commit()

        client_id = cursor.lastrowid

        cursor.close()

        return client_id

    def get_client(
        self,
        client_id: int
    ) -> tuple | None:
        """
        Retrieve a client by its ID.

        Parameters
        ----------
        client_id : int
            Unique identifier of the client.

        Returns
        -------
        tuple | None
            Client record if found.
        """

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
            (client_id,)
        )

        client = cursor.fetchone()

        cursor.close()

        return client

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
        """
        Create a credit dossier for an existing client.

        Parameters
        ----------
        client_id : int
            ID of the client owning the dossier.

        numero_compte : str
            Client bank account number.

        nature_credit : str
            Type or purpose of the credit.

        montant_credit : float
            Credit amount.

        date_production : str | None
            Production date.

        date_archivage : str | None
            Archive date.

        statut : str
            Current dossier status.

        Returns
        -------
        int
            ID of the created credit dossier.
        """

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

    def get_client_dossiers(
        self,
        client_id: int
    ) -> list[tuple]:
        """
        Retrieve all credit dossiers belonging to a client.

        Parameters
        ----------
        client_id : int
            ID of the client.

        Returns
        -------
        list[tuple]
            Credit dossiers belonging to the client.
        """

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
            (client_id,)
        )

        dossiers = cursor.fetchall()

        cursor.close()

        return dossiers

    def get_client_by_name(
        self,
        nom_prenom: str
    ) -> tuple | None:
        """
        Retrieve a client by their full name.

        Parameters
        ----------
        nom_prenom : str
            Full name of the client.

        Returns
        -------
        tuple | None
            Client record if found, otherwise None.
        """

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
            (nom_prenom,)
        )

        client = cursor.fetchone()

        cursor.close()

        return client

    def get_or_create_client(
        self,
        nom_prenom: str
    ) -> int:
        """
        Retrieve an existing client or create a new one.

        Parameters
        ----------
        nom_prenom : str
            Full name of the client.

        Returns
        -------
        int
            ID of the existing or newly created client.
        """

        client = self.get_client_by_name(
            nom_prenom
        )

        if client is not None:

            return client[0]

        return self.create_client(
            nom_prenom=nom_prenom
        )

    def save_credit_dossier(
        self,
        fields: dict
    ) -> int:
        """
        Save an extracted credit dossier in the database.

        Parameters
        ----------
        fields : dict
            Validated extracted banking fields.

        Returns
        -------
        int
            ID of the created credit dossier.
        """

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

    def get_dossier(
        self,
        dossier_id: int
    ):
        """
        Retrieve a credit dossier by its identifier.

        Parameters
        ----------
        dossier_id : int
            Identifier of the credit dossier.

        Returns
        -------
        tuple | None
            The dossier row if found, otherwise None.
        """

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
                (dossier_id,)
            )

    def create_document(
        self,
        dossier_id: int,
        nom_fichier: str,
        type_document: str | None,
        nombre_pages: int,
        chemin_fichier: str
    ) -> int:
        """
        Create a document associated with an existing credit dossier.

        Parameters
        ----------
        dossier_id : int
            ID of the credit dossier containing the document.

        nom_fichier : str
            Original name of the document file.

        type_document : str | None
            Type of document, if known.

        nombre_pages : int
            Number of pages in the document.

        chemin_fichier : str
            Path to the original document.

        Returns
        -------
        int
            ID of the created document.
        """

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
        """
        Retrieve a document by its identifier.

        Parameters
        ----------
        document_id : int
            Unique identifier of the document.

        Returns
        -------
        tuple | None
            Document record if found, otherwise None.
        """

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
            (document_id,)
        )

        document = cursor.fetchone()

        cursor.close()

        return document


    def create_document_page(
        self,
        document_id: int,
        numero_page: int,
        chemin_image: str
    ) -> int:
        """
        Create a page associated with a document.

        Parameters
        ----------
        document_id : int
            ID of the parent document.

        numero_page : int
            Page number inside the document.

        chemin_image : str
            Path to the processed page image.

        Returns
        -------
        int
            ID of the created page.
        """

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
        """
        Retrieve a document page by its identifier.
        """

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
            (page_id,)
        )

        page = cursor.fetchone()

        cursor.close()

        return page
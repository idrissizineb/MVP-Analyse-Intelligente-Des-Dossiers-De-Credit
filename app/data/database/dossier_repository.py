import sqlite3


class DossierRepository:

    def __init__(self, database_path: str):
        self.database_path = database_path

    # ==========================================================
    # GET ALL DOSSIERS
    # ==========================================================

    def get_all_dossiers(self):

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                d.dossier_id,
                c.cin,
                c.nom_prenom,
                d.numero_compte,
                d.nature_credit,
                d.montant_credit,
                d.date_de_decision,
                d.statut,
                d.created_at
            FROM dossier_credit d
            JOIN client c
                ON d.client_id = c.client_id
            ORDER BY d.created_at DESC
            """
        )

        rows = cursor.fetchall()

        connection.close()

        return [dict(row) for row in rows]

    # ==========================================================
    # GET DOSSIERS BY CIN
    # ==========================================================

    def get_dossiers_by_cin(
        self,
        cin: str
    ):

        connection = sqlite3.connect(
            self.database_path
        )

        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        cursor.execute(
            """
            SELECT
                d.dossier_id,
                c.cin,
                c.nom_prenom,
                d.numero_compte,
                d.nature_credit,
                d.montant_credit,
                d.date_de_decision,
                d.statut,
                d.created_at
            FROM dossier_credit d
            JOIN client c
                ON d.client_id = c.client_id
            WHERE c.cin = ?
            ORDER BY d.created_at DESC
            """,
            (cin,)
        )

        rows = cursor.fetchall()

        connection.close()

        return [dict(row) for row in rows]
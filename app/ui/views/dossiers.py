import sys
from pathlib import Path

import streamlit as st
from app.pipeline import DocumentPipeline
from app.ui.components.cards import info_card
from app.ui.components.dossier_card import dossier_card

import tempfile

import sqlite3

import streamlit as st

from app.pipeline import DocumentPipeline
from app.ui.components.cards import info_card
from app.ui.components.dossier_card import dossier_card
from app.data.database.dossier_repository import DossierRepository


def show_dossiers():

    st.title("📁 Gestion des Dossiers")

    st.markdown(
        """
Déposez un ou plusieurs dossiers clients au format PDF.

Les dossiers seront analysés automatiquement puis enregistrés
dans la base de données.
"""
    )

    st.divider()

    # ==========================================================
    # Upload
    # ==========================================================

    st.subheader("Importer des dossiers")

    uploaded_files = st.file_uploader(
        "Déposez vos fichiers PDF",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded_files:

        st.success(
            f"{len(uploaded_files)} fichier(s) sélectionné(s)."
        )

        for file in uploaded_files:
            st.write(f"📄 {file.name}")

    st.write("")

    analyse = st.button(
        "🚀 Analyser les dossiers",
        use_container_width=True,
    )

    # ==========================================================
    # Analyse
    # ==========================================================

    if analyse and uploaded_files:

        progress = st.progress(0)

        status = st.empty()

        for uploaded_file in uploaded_files:

            status.write(f"Analyse de {uploaded_file.name}")

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp:

                tmp.write(uploaded_file.getbuffer())

                pdf_path = Path(tmp.name)

            progress.progress(10)
            status.write("📄 Conversion du PDF...")

            progress.progress(25)
            status.write("🖼 Prétraitement des images...")

            progress.progress(45)
            status.write("🔍 OCR...")

            progress.progress(65)
            status.write("🧠 Extraction des informations...")

            progress.progress(80)
            status.write("💾 Enregistrement dans la base...")

            pipeline = DocumentPipeline(
                pdf_path=str(pdf_path)
            )

            results = pipeline.run()

            st.session_state["analysis_results"] = results

            progress.progress(100)

            status.success(
                f"{uploaded_file.name} analysé avec succès."
            )

    # ==========================================================
    # Résumé
    # ==========================================================

    if "analysis_results" in st.session_state:

        results = st.session_state["analysis_results"]

        fields = results["normalized_fields"]

        st.divider()

        st.success("✅ Analyse terminée avec succès")

        col1, col2 = st.columns(2)

        with col1:

            info_card(
                "Client",
                fields.get("nom_prenom", "-"),
                "👤",
            )

            info_card(
                "Montant",
                fields.get("montant_credit", "-"),
                "💰",
            )

        with col2:

            info_card(
                "Nature du crédit",
                fields.get("nature_credit", "-"),
                "🏦",
            )

        # ======================================================
        # Détails
        # ======================================================

        show_details = st.toggle(
            "Afficher les détails techniques"
        )

        if show_details:

            st.divider()

            st.subheader("Informations extraites")
            st.json(results["fields"])

            st.subheader("Validation")
            st.json(results["validation"])

            st.subheader("Valeurs normalisées")
            st.json(results["normalized_fields"])

    # ==========================================================
    # Recherche par CIN
    # ==========================================================

    st.divider()

    st.subheader("🔎 Rechercher un client par CIN")

    cin = st.text_input(
        "CIN",
        placeholder="Exemple : AB123456",
    )

    if st.button("🔍 Rechercher", width="stretch"):

        if not cin.strip():

            st.warning(
                "Veuillez saisir une CIN."
            )

        else:

            repository = DossierRepository(
                "data/database/credit_analysis.db"
            )

            dossiers = repository.get_dossiers_by_cin(
                cin.strip()
            )

            if not dossiers:

                st.warning(
                    f"Aucun dossier trouvé pour la CIN : {cin}"
                )

            else:

                st.success(
                    f"{len(dossiers)} dossier(s) trouvé(s)."
                )

                for dossier in dossiers:

                    dossier_card(dossier)


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
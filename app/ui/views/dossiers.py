import tempfile
from pathlib import Path

import streamlit as st

from app.pipeline import DocumentPipeline
from app.ui.components.cards import info_card
from app.ui.components.dossier_card import dossier_card
from data.database.dossier_repository import DossierRepository


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
    # Historique
    # ==========================================================

    st.divider()

    st.subheader("Historique des dossiers")

    repository = DossierRepository(
        "data/database/credit_analysis.db"
    )

    historique = repository.get_all_dossiers()

    if len(historique) == 0:

        st.info(
            "Aucun dossier enregistré."
        )

    else:

        # If get_all_dossiers() returns a pandas DataFrame
        if hasattr(historique, "iterrows"):

            for _, dossier in historique.iterrows():

                dossier_card(dossier)

        # If it returns a list of dictionaries
        else:

            for dossier in historique:
                st.write("DEBUG:", dossier)
                dossier_card(dossier)
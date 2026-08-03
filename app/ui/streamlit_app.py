import tempfile
from pathlib import Path

import streamlit as st

from app.pipeline import DocumentPipeline
from app.text2sql.text2sql_pipeline import Text2SQLPipeline


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Banque Populaire AI",
    page_icon="🏦",
    layout="wide",
)

st.title("🏦 Banque Populaire AI Assistant")


# ==========================================================
# SIDEBAR
# ==========================================================

page = st.sidebar.selectbox(
    "Navigation",
    [
        "Analyse d'un dossier",
        "Interroger la base",
    ],
)


# ==========================================================
# DOCUMENT ANALYSIS PAGE
# ==========================================================

if page == "Analyse d'un dossier":

    st.header("Analyse d'un dossier PDF")

    uploaded_file = st.file_uploader(
        "Choisissez un fichier PDF",
        type=["pdf"],
    )

    if uploaded_file is not None:

        st.success(
            f"Fichier sélectionné : {uploaded_file.name}"
        )

        if st.button("Analyser le dossier"):

            # --------------------------------------------------
            # Save uploaded PDF temporarily
            # --------------------------------------------------

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf",
            ) as tmp_file:

                tmp_file.write(
                    uploaded_file.getbuffer()
                )

                pdf_path = Path(tmp_file.name)

            # --------------------------------------------------
            # Run pipeline
            # --------------------------------------------------

            with st.spinner(
                "Analyse du dossier en cours..."
            ):

                pipeline = DocumentPipeline(
                    pdf_path=str(pdf_path)
                )

                results = pipeline.run()

            # --------------------------------------------------
            # Display results
            # --------------------------------------------------

            st.success(
                "Analyse terminée avec succès."
            )

            st.subheader("Informations extraites")

            st.json(results["fields"])

            st.subheader("Validation")

            st.json(results["validation"])

            st.subheader("Valeurs normalisées")

            st.json(results["normalized_fields"])

            st.subheader("Base de données")

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Dossier ID",
                    results["dossier_id"],
                )

            with col2:

                st.metric(
                    "Document ID",
                    results["document_id"],
                )

            st.divider()

            # --------------------------------------------------
            # Ask immediately after analysis
            # --------------------------------------------------

            st.subheader(
                "Interroger immédiatement la base"
            )

            question = st.text_input(
                "Posez une question sur les dossiers",
                key="analysis_question",
            )

            if st.button(
                "Exécuter la requête",
                key="analysis_query",
            ):

                assistant = Text2SQLPipeline()

                response = assistant.ask(question)
                st.write(response)
                st.stop()

                st.subheader("SQL généré")

                st.code(
                    response["generated_sql"],
                    language="sql",
                )

                st.subheader("Résultats SQL")

                st.json(
                    response["results"]
                )

                st.subheader("Réponse")

                st.success(
                    response["answer"]
                )


# ==========================================================
# TEXT2SQL PAGE
# ==========================================================

else:

    st.header("Assistant Text2SQL")

    question = st.text_input(
        "Posez votre question",
        key="main_question",
    )

    if st.button(
        "Poser la question",
        key="main_query",
    ):

        if question.strip() == "":

            st.warning(
                "Veuillez saisir une question."
            )

        else:

            assistant = Text2SQLPipeline()

            response = assistant.ask(question)

            st.subheader("SQL généré")

            st.code(
                response["generated_sql"],
                language="sql",
            )

            st.subheader("Résultats SQL")

            st.json(
                response["results"]
            )

            st.subheader("Réponse")

            st.success(
                response["answer"]
            )
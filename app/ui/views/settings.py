import streamlit as st


def show_settings():

    st.title("⚙️ Paramètres")

    st.markdown(
        """
Configurez les paramètres généraux de l'application.
"""
    )

    st.divider()

    # ==========================================================
    # IA
    # ==========================================================

    st.subheader("🤖 Intelligence Artificielle")

    st.text_input(
        "Modèle LLM",
        value="llama3.1",
        disabled=True,
    )

    st.text_input(
        "Moteur OCR",
        value="PaddleOCR",
        disabled=True,
    )

    st.info(
        "Ces paramètres seront configurables dans une prochaine version."
    )

    st.divider()

    # ==========================================================
    # Base de données
    # ==========================================================

    st.subheader("🗄️ Base de données")

    st.text_input(
        "Base SQLite",
        value="data/database/credit_analysis.db",
        disabled=True,
    )

    st.divider()

    # ==========================================================
    # Pipeline
    # ==========================================================

    st.subheader("⚙️ Pipeline")

    st.checkbox(
        "Correction de l'inclinaison (Deskew)",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "Réduction du bruit",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "Amélioration du contraste",
        value=True,
        disabled=True,
    )

    st.checkbox(
        "OCR",
        value=True,
        disabled=True,
    )

    st.divider()

    # ==========================================================
    # À propos
    # ==========================================================

    st.subheader("ℹ️ À propos")

    st.markdown(
        """
**Analyse Intelligente des Dossiers de Crédit**

Développé dans le cadre d'un projet de stage chez **Banque Populaire Maroc**.

Version **1.0**
"""
    )
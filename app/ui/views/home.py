import streamlit as st


def show_home():

    st.title("🏦 Banque Populaire AI")

    st.markdown("---")

    st.header("Analyse Intelligente des Dossiers de Crédit")

    st.write(
        """
Bienvenue dans l'application d'analyse intelligente des dossiers de crédit.

Cette application permet :

- l'analyse automatique des dossiers PDF,
- l'extraction des informations importantes,
- le stockage dans une base de données,
- l'interrogation de la base en langage naturel grâce à l'IA.
"""
    )

    st.info("Sélectionnez une fonctionnalité dans le menu de gauche.")
import streamlit as st


def dossier_card(dossier):

    with st.container(border=True):

        st.subheader(f"👤 {dossier['nom_prenom']}")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"🏦 **Crédit :** {dossier['nature_credit']}"
            )

            st.write(
                f"💰 **Montant :** {dossier['montant_credit']} DH"
            )

        with col2:

            st.write(
                f"📅 **Date :** {dossier['created_at']}"
            )

            st.write(
                f"🆔 **ID :** {dossier['dossier_id']}"
            )

        st.button(
            "Voir le dossier",
            key=f"dossier_{dossier['dossier_id']}",
        )
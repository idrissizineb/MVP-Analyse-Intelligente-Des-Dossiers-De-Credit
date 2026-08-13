import streamlit as st

from app.text2sql.text2sql_pipeline import Text2SQLPipeline


def show_assistant():

    # ==========================================================
    # Header
    # ==========================================================

    st.title("💬 Credit Assistant")

    st.caption(
        "Posez vos questions sur les dossiers de crédit."
    )

    st.divider()

    # ==========================================================
    # Welcome
    # ==========================================================

    st.info(
        """
### Bienvenue 👋

Je peux répondre à vos questions concernant :

- les crédits
- les clients
- les revenus
- les montants
- les garanties
- les documents

• Quels documents sont enregistrés pour un client ?
"""
    )

    st.divider()

    # ==========================================================
    # Chat History
    # ==========================================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ==========================================================
    # Chat Input
    # ==========================================================

    question = st.chat_input(
        "Posez votre question..."
    )

    if question:

        # ---------------- USER ----------------

        st.session_state.messages.append(
            {
                "role": "user",
                "content": question,
            }
        )

        with st.chat_message("user"):
            st.markdown(question)

        # ---------------- ASSISTANT ----------------

        with st.chat_message("assistant"):

            with st.spinner("Recherche en cours..."):

                try:

                    pipeline = Text2SQLPipeline()

                    response = pipeline.ask(question)

                    st.markdown(response["answer"])

                    with st.expander("SQL généré"):
                        st.code(
                            response["generated_sql"],
                            language="sql",
                        )

                    with st.expander("Résultats SQL"):
                        st.json(
                            response["results"]
                        )

                    assistant_answer = response["answer"]

                except Exception as e:

                    import traceback

                    print("\n========== TEXT2SQL ERROR ==========")
                    print(e)
                    traceback.print_exc()

                    assistant_answer = (
                        "❌ Une erreur est survenue.\n\n"
                        f"```{e}```"
                    )

                    st.error(assistant_answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_answer,
            }
        )
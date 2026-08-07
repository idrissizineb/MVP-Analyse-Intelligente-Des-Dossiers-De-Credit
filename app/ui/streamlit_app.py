import streamlit as st
from pathlib import Path

from app.ui.views.home import show_home
from app.ui.views.dossiers import show_dossiers
from app.ui.views.assistant import show_assistant
from app.ui.views.settings import show_settings


# ==========================================================
# LOAD CUSTOM CSS
# ==========================================================

def load_css():

    css_path = Path(__file__).parent / "style.css"

    if css_path.exists():

        with open(css_path, encoding="utf-8") as f:

            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True,
            )


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Banque Populaire AI",
    page_icon="🏦",
    layout="wide",
)

# Load CSS
load_css()

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.image(
        "app/ui/assets/BCP.jfif",
        use_container_width=True,
    )

    st.markdown(
        """
        <h2 style='text-align:center;color:#E67E00;'>
        Banque Populaire
        </h2>

        <p style='text-align:center;color:gray;'>
        Analyse Intelligente<br>
        des Dossiers de Crédit
        </p>

        <hr>
        """,
        unsafe_allow_html=True,
    )

    page = st.radio(

        "Navigation",

        [

            "🏠 Accueil",

            "📁 Dossiers",

            "💬 Credit Assistant",

            "⚙️ Paramètres",

        ],

        label_visibility="collapsed",

    )

    st.markdown("<hr>", unsafe_allow_html=True)

    st.caption("Version 1.0")

# ==========================================================
# ROUTING
# ==========================================================

if page == "🏠 Accueil":

    show_home()

elif page == "📁 Dossiers":

    show_dossiers()

elif page == "💬 Credit Assistant":

    show_assistant()

elif page == "⚙️ Paramètres":

    show_settings()
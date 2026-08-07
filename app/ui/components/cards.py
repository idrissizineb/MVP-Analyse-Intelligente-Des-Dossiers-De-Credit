import streamlit as st


def info_card(title, value, icon="📄"):

    st.markdown(
        f"""
<div style="
padding:18px;
border-radius:12px;
border:1px solid #d9d9d9;
background-color:#fafafa;
margin-bottom:15px;
">

<h5>{icon} {title}</h5>

<h3>{value}</h3>

</div>
""",
        unsafe_allow_html=True,
    )
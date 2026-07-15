import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer

def teacher_screen():

    header_dashboard()
    style_background_dashboard()
    style_base_layout()

    teacher_screen_login()

    footer()


def teacher_screen_register():
    st.header("Register your teacher profile", text_alignment="center")
    

def teacher_screen_login():
    with st.container(key="portal_cards"):
        st.subheader("Login using Password", text_alignment="center")
        st.space()
        teacher_username = st.text_input("Username:", placeholder="@username")
        teacher_password = st.text_input("Password:", type="password", placeholder="Enter password")

        st.space()
        btnc1, btnc2 = st.columns(2, gap="small")
        with btnc1:
            st.button('Login', icon=":material/passkey:", width="stretch")
        with btnc2:
            st.button('Register Instead', type="tertiary", icon=":material/passkey:", width="stretch")


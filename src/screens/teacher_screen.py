import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer
import src.database.db as db
from src.database.db import check_teacher_exits, create_teacher, login_teacher

def teacher_screen():
    header_dashboard()
    style_background_dashboard()
    style_base_layout()

    if 'is_logged_in' in st.session_state:
        teacher_dashboard()

    elif 'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=="login":
        teacher_screen_login()
        
    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()

    footer()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data
    st.header(f"Welcome {teacher_data['name']}.", text_alignment="center")
        

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_name or not teacher_username or not teacher_pass:
        return False, "All fields are required!"
    if check_teacher_exits(teacher_username):
        return False, "Username already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match."
    try:
        create_teacher(teacher_username, teacher_pass, teacher_name)
        return True, "Successfully Created! Login Now"
    except Exception as e:
        return False, "Unexpected Error!"
def teacher_login(username, password):
    if not username or not password:
        return False
    teacher = db.login_teacher(username, password)

    if teacher:
        st.session_state.user_role = 'teacher'
        st.session_state.teacher_data = teacher
        st.session_state.is_logged_in = True
        return True
    return False


def teacher_screen_register():
    with st.container(key="portal_cards"):
        st.subheader("Register your teacher profile", text_alignment="center")
        st.space()
        teacher_username = st.text_input("Enter username", placeholder='@username')

        teacher_name = st.text_input("Enter name", placeholder='Ananya Roy')

        teacher_pass = st.text_input("Enter password", type='password', placeholder="Enter password")

        teacher_pass_confirm = st.text_input("Confirm your password", type='password', placeholder="Enter password")
        st.divider()

        btnc1, btnc2 = st.columns(2, gap="small")
        with btnc1:
            if st.button('Register Now', icon=":material/passkey:", width="stretch"):
                success, message = register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm)
                if success:
                    st.success(message)
                    import time
                    time.sleep(2)
                    st.session_state['teacher_login_type'] = "login"
                    st.rerun()
                else:
                    st.error(message)
        with btnc2:
            if st.button('Login Instead', type="tertiary", icon=":material/passkey:", width="stretch"):
                st.session_state['teacher_login_type'] = 'login'
                st.rerun()

    

def teacher_screen_login():
    with st.container(key="portal_cards"):
        st.subheader("Login using Password", text_alignment="center")
        st.space()
        teacher_username = st.text_input("Username:", placeholder="@username")
        teacher_password = st.text_input("Password:", type="password", placeholder="Enter password")

        st.divider()
        btnc1, btnc2 = st.columns(2, gap="small")
        with btnc1:
            if st.button('Login', icon=":material/passkey:", width="stretch"):
                if teacher_login(teacher_username, teacher_password):
                    st.toast("welcome back!", icon="👋")
                    import time
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username and password")
        
        with btnc2:
            if st.button('Register Instead', type="tertiary", icon=":material/passkey:", width="stretch"):
                st.session_state['teacher_login_type'] = 'register'
                st.rerun()


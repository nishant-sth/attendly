import streamlit as st
from src.ui.base_layout import style_background_dashboard, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer
import src.database.db as db
from .teacher_tabs import teacher_tab_manage_subjects, teacher_tab_take_attendence, teacher_tab_attendence_records




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
    
    st.space(size="xlarge")
    st.divider()
    footer()

def teacher_dashboard():
    teacher_data = st.session_state.teacher_data

    # if st.button("Logout", key='logoutbtn', shortcut='control+backspace'):
    #     st.session_state['is_logged_in'] = False
    #     del st.session_state.teacher_data
    #     st.rerun()

    st.subheader(f"Welcome, {teacher_data['name']}.", text_alignment="center")
    st.space(size="medium")

    if 'current_teacher_tab' not in st.session_state:
        st.session_state['current_teacher_tab'] = 'take_attendence'
    
    tab1, tab2, tab3 = st.columns(3, gap="small")
    with tab1:
        type1 = "primary" if st.session_state.current_teacher_tab == 'take_attendence' else 'tertiary'
        if st.button("Take Attendence", type=type1, width="stretch", icon=":material/ar_on_you:"):
            st.session_state['current_teacher_tab'] = 'take_attendence'
            st.rerun()

    with tab2:
        type2 = "primary" if st.session_state.current_teacher_tab == 'manage_subjects' else 'tertiary'
        if st.button("Manage Subjects", type=type2, width="stretch", icon=":material/book_ribbon:"):
            st.session_state['current_teacher_tab'] = 'manage_subjects'
            st.rerun()

    with tab3:
        type3 = "primary" if st.session_state.current_teacher_tab == 'attendence_records' else 'tertiary'
        if st.button("Attendence Records",type=type3, width="stretch", icon=":material/cards_stack:"):
            st.session_state['current_teacher_tab'] = 'attendence_records'
            st.rerun()
    
    if st.session_state['current_teacher_tab'] == 'take_attendence':
        teacher_tab_take_attendence()
    if st.session_state['current_teacher_tab'] == 'manage_subjects':
        teacher_tab_manage_subjects()
    if st.session_state['current_teacher_tab'] == 'attendence_records':
        teacher_tab_attendence_records()
    

def register_teacher(teacher_username, teacher_name, teacher_pass, teacher_pass_confirm):
    if not teacher_name or not teacher_username or not teacher_pass:
        return False, "All fields are required!"
    if db.check_teacher_exits(teacher_username):
        return False, "Username already taken."
    if teacher_pass != teacher_pass_confirm:
        return False, "Password doesn't match."
    try:
        db.create_teacher(teacher_username, teacher_pass, teacher_name)
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
                    st.toast(f"welcome back! {teacher_username}", icon="👋")
                    st.rerun()
                else:
                    st.error("Invalid username and password")
        
        with btnc2:
            if st.button('Register Instead', type="tertiary", icon=":material/passkey:", width="stretch"):
                st.session_state['teacher_login_type'] = 'register'
                st.rerun()


import streamlit as st
from src.components.header import header_home
from src.ui.base_layout import style_base_layout, style_background_home
from src.components.footer import footer_home

def home_screen():
    style_base_layout()
    style_background_home()
    header_home()

    with st.container(key="portal_cards"):
        col1, col2 = st.columns(2, gap="large")

        with col1:
            st.markdown('<div class="card-icon">🎓</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Student</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Mark attendance instantly</div>', unsafe_allow_html=True)
            if st.button('Student Portal', type='primary', icon=':material/arrow_outward:',
                         icon_position='right', key='student_btn', use_container_width=True):
                st.session_state['login_type'] = 'student'
                st.rerun()

        with col2:
            st.markdown('<div class="card-icon">🧑‍🏫</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-title">Teacher</div>', unsafe_allow_html=True)
            st.markdown('<div class="card-sub">Manage classes and reports</div>', unsafe_allow_html=True)
            if st.button('Teacher Portal', type='secondary', icon=':material/arrow_outward:',
                         icon_position='right', key='teacher_btn', use_container_width=True):
                st.session_state['login_type'] = 'teacher'
                st.rerun()

    # # feature strip
    # st.markdown("""
    #     <div class="feature-strip">
    #         <div class="feature-item"><span class="feature-emoji">🧠</span>Face recognition</div>
    #         <div class="feature-item"><span class="feature-emoji">📊</span>Real-time reports</div>
    #         <div class="feature-item"><span class="feature-emoji">🔒</span>Secure and fast</div>
    #     </div>
    # """, unsafe_allow_html=True)

    footer_home()
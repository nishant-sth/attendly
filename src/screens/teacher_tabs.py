import streamlit as st
from src.database import db
from src.components.subject_dialog import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_subject_qr import share_subject


def teacher_tab_take_attendence():
    st.subheader("Take AI attendence")

def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    with st.container(border=True, key="manage-subjects-container", width="stretch"):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Manage Subjects")
        with col2:
            if st.button("New Subject", type="secondary", width="stretch"):
                create_subject_dialog(teacher_id)
        
        # List all the teacher subjects
        teacher_id = st.session_state.teacher_data['teacher_id']
        subjects = db.get_teacher_subject(teacher_id)
        if subjects:
            for sub in subjects:
                stats = [
                    ("🫂", "Students", sub['total_students']),
                    ("🕰️", "Classes", sub['total_classes']),
                ]
            def share_btn():
                if st.button(f"Share Code: {sub['name']}", key=f"share_{sub['subject_code']}", icon=":material/share:", type="primary"):
                    share_subject(sub['name'], sub['subject_code'])
                st.space()

            subject_card(
                name = sub['name'],
                code = sub['subject_code'],
                section = sub['section'],
                stats=stats,
                footer_callback=share_btn
            )
        else:
            st.info("NO SUBJECTS FOUND. CREATE ONE ABOVE")

def teacher_tab_attendence_records():
    st.subheader("Attendence Records")
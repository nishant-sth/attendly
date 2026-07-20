import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_in_subject
import time


@st.dialog("Quick Enrollment")
def auto_enroll_in_subject_dialog(join_code):
    student_id = st.session_state.get('student_data')['student_id']
    result = supabase.table("subjects").select("subject_id, name").eq("subject_code", join_code).execute()
    if not result.data:
        st.error("Subject Code not found!")
        if st.button("Close"):
            st.query_params.clear()
            st.rerun()
            return 
    
    subject = result.data[0]
    check = supabase.table("subject_students").select("*").eq("subject_id", subject['subject_id']).eq("student_id", student_id).execute()

    if check.data:
        st.info("You're already enrolled.")
        st.query_params.clear()
        st.rerun()
        return 
    st.markdown(f"Would you like to enroll in **{subject['name']}**?", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button('No thanks'):
            st.query_params.clear()
            st.rerun()
    with col2:
        if st.button('Yes enroll now!', type='primary', width='stretch'):
            enroll_in_subject(subject_id=subject['subject_id'], student_id=student_id)
            st.toast('Joined succesfully!')
            st.query_params.clear()
            time.sleep(1)
            st.rerun()
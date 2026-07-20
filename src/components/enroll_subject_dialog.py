import streamlit as st
from src.database.config import supabase
from src.database.db import enroll_in_subject
import time


@st.dialog("Enroll in Subject")
def create_enroll_in_subject_dialog():
    st.write("Enter the subject code provided by your teacher to enroll ")
    join_code = st.text_input("Subject Code:", placeholder="E.g. CSC304")

    if st.button("Enroll Now", type="primary", width="stretch"):
        if join_code:
            res = supabase.table("subjects").select("subject_id, name, subject_code").eq("subject_code", join_code).execute()
            if res.data:
                subject = res.data[0]
                student_id = st.session_state.student_data['student_id']

            check = supabase.table("subject_students").select("*").eq("subject_id", subject['subject_id']).eq("student_id", student_id).execute()
            if check.data:
                st.warning(f"You are already enrolled in {subject['name']} subject")
            else:
                enroll_in_subject(subject_id=subject['subject_id'], student_id=student_id)
                st.success("Enrolled successfully")
                time.sleep(1)
                st.rerun()
            
        else:
            st.warning("Please enter the subject code")
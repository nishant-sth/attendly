import streamlit as st
from src.database.db import create_subject

@st.dialog(title="Create New Subject")
def create_subject_dialog(teacher_id):
    st.write("Enter the details of the new subject")
    sub_id = st.text_input("Subject Code:", placeholder='Eg.CSC20')
    sub_name = st.text_input("Subject Name:", placeholder="Introduction of Congnitive Science")
    sub_section = st.text_input("Section:", placeholder="A")


    if st.button("Create Subject Now", type="primary", width="content"):
        if sub_id and sub_name and sub_section:
            try:
                create_subject(subject_code=sub_id, name=sub_name, section=sub_section, teacher_id=teacher_id)
                st.toast("Subject created successfully")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")
        else:
            st.warning("Please fill all the sections")
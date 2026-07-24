import time
import numpy as np
from PIL import Image
import streamlit as st
from src.components.header import header_dashboard
from src.components.footer import footer
from src.ui.base_layout import style_background_home, style_base_layout
from src.pipelines.face_pipeline import predict_attendence
from src.database.db import get_all_students, create_student, get_student_subjects, get_student_attendence, unenroll_in_subject
from src.pipelines.face_pipeline import get_image_embeddings, train_model
from src.pipelines.voice_pipeline import get_voice_embedding
from src.components.enroll_subject_dialog import create_enroll_in_subject_dialog
from src.components.subject_card import subject_card

def student_dashboard():
    student_data = st.session_state.get('student_data')
    if isinstance(student_data, list):
        student_data = student_data[0] if student_data else None

    if not student_data:
        st.session_state['login_type'] = None
        st.session_state.pop('student_data', None)
        st.warning("Student session expired. Please log in again.")
        st.rerun()
        return

    st.subheader("Student Dashboard", text_alignment="center")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader(f"Welcome {student_data['name']}")
    with col2:
        if st.button("Enroll in Subject", type="primary", width="stretch"):
            create_enroll_in_subject_dialog()
    st.divider()

    with st.spinner("Loading your subjects.."):
        student_id = student_data['student_id']
        subjects = get_student_subjects(student_id)
        logs = get_student_attendence(student_id)
    
    stats_map = {}
    for log in logs:
        sub_id = log['subject_id']

        if sub_id not in stats_map:
            stats_map[sub_id] = {
                "total": 0,
                "attended": 0
            }
        stats_map[sub_id]['total'] += 1

        if log.get('is_present'):
            stats_map[sub_id]['attended'] += 1
    
    cols = st.columns(2)
    for i, sub_node in enumerate(subjects):
        sub = sub_node["subjects"]
        sub_id = sub['subject_id']

        stats = stats_map.get(sub_id, {"total": 0, "attended": 0})
        
        def unenroll_btn():
            if st.button("Unenroll form this course", width="stretch", type="tertiary", key=f"{sub['subject_code']}-btn", icon=":material/delete_forever:"):
                unenroll_in_subject(subject_id=sub_id, student_id=student_id)
                st.rerun()
        
        with cols[i % 2]:
            subject_card(
                name=sub['name'],
                code=sub['subject_code'],
                section=sub['section'],
                stats=[
                    ('👩🏻‍🏫', "Total:", stats['total']),
                    ('📝', "Attended:", stats['attended'])
                ],
                footer_callback=unenroll_btn
            )

def student_screen():
    header_dashboard()
    style_base_layout()
    style_background_home()

    if 'student_data' in st.session_state:
        student_dashboard()
        return 

    st.header("Login Using FaceID", text_alignment="center")

    show_registration = False
    image_source = st.camera_input("Position your face in the center", width=1060)

    if image_source:
        image = np.array(Image.open(image_source))

        with st.spinner("AI is scanning..."):
            detected, all_ids, num_faces = predict_attendence(image)
            if num_faces == 0:
                st.warning("Face not found!")
            elif num_faces > 1:
                st.warning("Multiple faces found")
            else:
                student = None
                if detected:
                    student_id = list(detected.keys())[0]
                    all_students = get_all_students()
                    student = next((s for s in all_students if s['student_id']==student_id), None)
                
                if student:
                    st.session_state.is_logged_in = True
                    st.session_state.user_role = 'student'
                    st.session_state.student_data = student
                    st.toast(f"Welcome back {student['name']}")
                    time.sleep(2)
                    st.rerun()
                else:
                    st.info("Face is not recognized! You might be a new student")
                    show_registration = True
    
    if show_registration:
        with st.container(border=True):
            st.subheader('Register new Student Profile')
            new_name = st.text_input("Enter your name", placeholder="E.g. Sourav Joshi")

            st.subheader("Optional : Voice Enrollment")
            st.info("Add your voice for attendence")

            audio_data = None

            try:
                audio_data = st.audio_input("Record a short pharse like 'I am Present, My name is @yourname.'")
            except Exception:
                st.error("Audio data failed!")

            if st.button('Create Account', type="secondary"):
                if not new_name:
                    st.error("Please enter your name")
                else:
                    with st.spinner("Creating student profile."):
                        img = np.array(Image.open(image_source))
                        embeddings = get_image_embeddings(img)

                        if embeddings:
                            face_emb = embeddings[0].tolist()
                            voice_emb = None

                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())
                            respose_data = create_student(name=new_name, face_embedding=face_emb, voice_embedding=voice_emb)

                            if respose_data:
                                train_model()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = respose_data
                                time.sleep(2)
                                st.rerun()
                                st.toast(f"Created Profile! Hi {new_name}")
                        else:
                            st.error("Couldn't capture your facial features for registration")

    footer()



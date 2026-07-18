import streamlit as st
from src.ui.base_layout import style_background_home, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer
import numpy as np
from PIL import Image
from src.pipelines.face_pipeline import predict_attendence
from src.database.db import get_all_students, create_student
import time
from src.pipelines.face_pipeline import get_image_embeddings, train_model
from src.pipelines.voice_pipeline import get_voice_embedding


def student_dashboard():
    st.subheader("Student Dashboard")


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

            if st.button('Create Account', type="primary"):
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



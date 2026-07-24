import streamlit as st
from src.database import db
from src.components.subject_dialog import create_subject_dialog
from src.components.subject_card import subject_card
from src.components.share_subject_qr import share_subject
from src.components.add_photo_dialog import add_photos_dialog
from src.pipelines.face_pipeline import predict_attendence
from src.components.atendence_result_dialog import attendence_results_dialog
from src.components.voice_attendence_dialog import voice_attendence_dialog
from src.database.config import supabase
from datetime import datetime
import numpy as np
import pandas as pd

def teacher_tab_take_attendence():
    teacher_data = st.session_state.get('teacher_data')
    teacher_id = teacher_data['teacher_id']

    st.subheader("Take AI attendence")

    if 'attendence_images' not in st.session_state:
        st.session_state.attendence_images = []

    subjects = db.get_teacher_subject(teacher_id)

    if not subjects:
        st.warning("You haven't created any subject yet! Please create one first")
        return 

    subject_options = {
        f"{sub['name']} - {sub['subject_code']}": sub['subject_id']
        for sub in subjects
    }
    
    col1, col2 = st.columns([3, 1.5], vertical_alignment="bottom")
    with col1:
        selected_subject_label = st.selectbox("Select Subject", options=list(subject_options.keys()))

    with col2:
        if st.button("Add Photos", type="primary", icon=":material/photo_prints:", width="stretch",):
            add_photos_dialog()

    selected_subject_id = subject_options[selected_subject_label]
    
    st.divider()

    if st.session_state.get('attendence_images'):
        st.subheader("Added Images:")
        gallery_cols = st.columns(4)

        for idx, img in enumerate(st.session_state.get('attendence_images', [])):
            with gallery_cols[idx % 4]:
                st.image(img, width="stretch", caption=f"Photo {idx + 1}")


    has_photos = bool(st.session_state.get('attendence_images'))
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("Clear All Photo", width="stretch", type="tertiary", icon=":material/delete:", disabled= not has_photos):
            st.session_state.attendence_images = []
            st.rerun()

    with c2:
        if st.button("Run Face Analysis", width="stretch", type="secondary", icon=":material/action_key:", disabled= not has_photos):
            with st.spinner("Deep Face analysis of classroom image...."):
                all_detected_ids = {}

                for id, img in enumerate(st.session_state.get('attendence_images')):
                    img_np = np.array(img.convert("RGB"))

                    detected, _, _ = predict_attendence(img_np)
                    if detected:
                        for sid in detected.keys():
                            all_detected_ids.setdefault(sid, []).append(f"Photo {id+1}")

                enrolled_res = supabase.table('subject_students').select("*, students(*)").eq("subject_id", selected_subject_id).execute()

                enrolled_students = enrolled_res.data
                if not enrolled_students:
                    st.warning("No students in this course")
                else:
                    results, attendence_to_log = [], []

                    current_timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            
                    for node in enrolled_students:
                        student = node['students']
                        source = all_detected_ids.get(int(student['student_id']), [])
                        is_present = len(source) > 0

                        results.append({
                            "Name": student['name'],
                            "ID": student['student_id'],
                            "Source": ",".join(source) if is_present else "-",
                            "Status": "Present" if is_present else "Absent"
                        })

                        attendence_to_log.append({
                            'student_id': student["student_id"],
                            'subject_id': selected_subject_id,
                            'timestamp': current_timestamp,
                            'is_present': bool(is_present)
                        })

                attendence_results_dialog(pd.DataFrame(results), attendence_to_log)

    with c3:
        if st.button("Use Voice Attendence", type="primary", width="stretch", icon=":material/mic:"):
            voice_attendence_dialog(selected_subject_id)





def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data['teacher_id']
    with st.container(border=True, key="manage-subjects-container", width="stretch"):
        col1, col2 = st.columns(2, gap="xxlarge")
        with col1:
            st.subheader("Manage Subjects")
        with col2:
            if st.button("Create New Subject", type="secondary", width="stretch"):
                create_subject_dialog(teacher_id)
        
        # List all the teacher subjects
        teacher_id = st.session_state.teacher_data['teacher_id']
        subjects = db.get_teacher_subject(teacher_id)

        # print(subjects)
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
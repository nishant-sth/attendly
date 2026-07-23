import streamlit as st
from PIL import Image

@st.dialog("Capture or Upload Photos")
def add_photos_dialog():
    st.write("Upload classroom photos to scan for attendence.")

    if 'photo_tab' not in st.session_state:
        st.session_state.photo_tab = 'camera'

    t1, t2 = st.columns(2)

    with t1:
        type_camera = 'primary' if st.session_state.get('photo_tab') == 'camera' else 'tertiary'
        if st.button("Camera", type=type_camera, width="stretch"):
            st.session_state.photo_type = 'camera'
    with t2:
        type_upload = 'primary' if st.session_state.get('photo_tab') == 'upload' else 'tertiary'
        if st.button('Upload Photos', type=type_upload, width="stretch"):
            st.session_state.photo_tab = 'upload'

    if st.session_state.get('photo_tab') == 'camera':
        cam_photo = st.camera_input("Take Snapshot", key="dialog_camera", width="stretch")
        if cam_photo:
            st.session_state.attendence_images.append(Image.open(cam_photo))
            st.toast("Photo Captured")
            st.rerun()

    if st.session_state.get('photo_tab') == 'upload':
        upload_files = st.file_uploader("Choose image files", type=['jpeg', 'png', 'jpg'], accept_multiple_files=True, key='dialog_upload')

        if upload_files:
            for file in upload_files:
                st.session_state.attendence_images.append(Image.open(file))
                st.toast("Photos uploaded successfully")
                st.rerun()

    st.divider()
    if st.button("Done", type="primary", width="stretch"):
        st.rerun()
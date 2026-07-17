import streamlit as st
from src.ui.base_layout import style_background_home, style_base_layout
from src.components.header import header_dashboard
from src.components.footer import footer
import numpy as np
from PIL import Image

def student_screen():
    header_dashboard()
    style_base_layout()
    style_background_home()


    st.header("Login Using FaceID", text_alignment="center")
    image_source = st.camera_input("Position your face in the center", width=1060)

    if image_source:
        np.array(Image.open(image_source))
    footer()



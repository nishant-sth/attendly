import streamlit as st


def footer():
    st.markdown(f"""
                <div style="margin-top:2rem; display:flex; gap:6px; justify-content:center; items-align:center">
                <p style="font-weight:; color:white;"> Created by <strong><u>Nishant Shrestha</u></strong></p>  
                </div>
                        
                """, unsafe_allow_html=True)

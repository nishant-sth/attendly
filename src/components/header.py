import streamlit as st


def header_home():

    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"

    # top navigation bar
    st.markdown(f"""
        <div class="navbar">
            <div class="nav-left">
                <img src='{logo_url}' />
                <span class="nav-brand">SNAPCLASS</span>
            </div>
            <div class="nav-links">
                <span>Features</span>
                <span>About</span>
                <span>Contact</span>
            </div>
            <div class="nav-cta">Sign in</div>
        </div>
    """, unsafe_allow_html=True)

    # hero section
    st.markdown("""
        <div style="text-align:left; margin-top:1rem; margin-bottom:1rem;">
            <div class="hero-badge">✨ AI-powered attendance</div>
            <h1 style="text-align:left; color:#fff;">SNAP<br/>CLASS</h1>
            <p class="hero-tagline">Mark attendance in seconds with face recognition,
            built for students and teachers.</p>
            <div class="stats-row">
                <div>
                    <div class="stat-num">2.4x</div>
                    <div class="stat-label">faster roll call</div>
                </div>
                <div>
                    <div class="stat-num">99%</div>
                    <div class="stat-label">accuracy</div>
                </div>
            </div>
        </div>
    """, unsafe_allow_html=True)
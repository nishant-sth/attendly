import streamlit as st


def style_background_home():

    st.markdown("""
        <style>

                .stApp {
                    background: radial-gradient(circle at 12% 10%, rgba(255,255,255,0.10), transparent 40%),
                                radial-gradient(circle at 90% 85%, rgba(235,69,158,0.18), transparent 45%),
                                linear-gradient(160deg, #6C5CE7 0%, #5865F2 45%, #2E22B0 100%) !important;
                    background-attachment: fixed !important;
                }

                /* glass portal cards (student / teacher) */
                .st-key-portal_cards div[data-testid="stColumn"]{
                    background-color: rgba(255,255,255,0.12) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    border: 1px solid rgba(255,255,255,0.25) !important;
                    padding: 2.2rem 1.8rem !important;
                    border-radius: 1.8rem !important;
                    text-align:center;
                    transition: transform 0.25s ease-in-out;
                }

                .st-key-portal_cards div[data-testid="stColumn"]:hover{
                    transform: translateY(-4px);
                }

        </style>

                """
            ,unsafe_allow_html=True)


def style_background_dashboard():

    st.markdown("""
        <style>

                .stApp {
                    background: radial-gradient(circle at 12% 10%, rgba(255,255,255,0.16), transparent 40%),
                                radial-gradient(circle at 88% 84%, rgba(255,95,162,0.22), transparent 46%),
                                linear-gradient(150deg, #6C5CE7 0%, #5865F2 45%, #2E22B0 100%) !important;
                    background-attachment: fixed !important;
                }

                .st-key-portal_cards{
                    background-color: rgba(250,220,245,0.22) !important;
                    backdrop-filter: blur(10px) !important;
                    -webkit-backdrop-filter: blur(10px) !important;
                    border: 1px solid rgba(255,255,255,0.25) !important;
                    padding: 2.3rem 2rem !important;
                    border-radius: 1.4rem !important;
                    text-align:center;
                    width: 54% !important;
                    transition: transform 0.25s ease-in-out;
                }

        </style>  

                """
            ,unsafe_allow_html=True)


def style_base_layout():

    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');


         /* Hide Top Bar of streamlit */

            #MainMenu, footer, header {
                visibility: hidden;
            }

            .block-container {
                padding-top:0rem !important;
                max-width: 1000px !important;
            }

            h1 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 3.5rem !important;
                color: white !important;
                line-height:1.05 !important;
                margin-bottom:0rem !important;
            }


            h2 {
                font-family: 'Climate Crisis', sans-serif !important;
                font-size: 1.6rem !important;
                line-height:1 !important;
                margin-bottom:0.2rem !important;
            }

            h3, h4, p {
                font-family:'Outfit', sans-serif !important;
                color: white !important;
            }

            /* kind="primary" */
            button{     
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                background: rgba(255,255,255,0.15);
                color: white !important;
                font-family:'Outfit', sans-serif;
                font-size:12px;
                padding:6px 16px;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            button:hover{
                transform :scale(1.05)}

            /* --- navbar --- */
            .navbar {
                display:flex;
                align-items:center;
                justify-content:space-between;
                padding: 14px 6px;
                border-bottom: 1px solid rgba(255,255,255,0.15);
                margin-bottom: 2rem;
            }
            .navbar .nav-left{
                display:flex; align-items:center; gap:10px;
            }
            .navbar .nav-left img{ height:34px; }
            .navbar .nav-brand{
                font-family:'Climate Crisis', sans-serif;
                font-size:1.3rem;
                color:#fff;
                letter-spacing:0.5px;
            }
            .navbar .nav-links{
                display:flex; gap:22px;
                font-family:'Outfit', sans-serif;
                font-size:13px;
                color: rgba(255,255,255,0.75);
            }
            .navbar .nav-cta{
                background: rgba(255,255,255,0.15);
                border: 1px solid rgba(255,255,255,0.3);
                color:#fff;
                font-family:'Outfit', sans-serif;
                font-size:15px;
                padding:6px 16px;
                border-radius:999px;
            }
            /* --- hero --- */
            .hero-badge{
                display:inline-block;
                background: rgba(255,255,255,0.14);
                border: 1px solid rgba(255,255,255,0.28);
                color:#fff;
                font-family:'Outfit', sans-serif;
                font-size:12px;
                padding:5px 14px;
                border-radius:999px;
                margin-bottom:14px;
            }
            .hero-tagline{
                font-family:'Outfit', sans-serif;
                color: rgba(255,255,255,0.75);
                font-size:15px;
                max-width:480px;
                margin: 10px auto 0;
            }
            .stats-row{
                display:flex;
                justify-content:left;
                gap:40px;
                margin-top:22px;
            }
            .stat-num{
                font-family:'Climate Crisis', sans-serif;
                font-size:1.6rem;
                color:#fff;
            }
            .stat-label{
                font-family:'Outfit', sans-serif;
                font-size:11px;
                color: rgba(255,255,255,0.6);
            }

            /* --- portal cards --- */
            .card-icon{ font-size:3.6rem; margin-bottom:0.6rem; }
            .card-title{
                font-family:'Climate Crisis', sans-serif;
                font-size:1.5rem;
                color:#fff;
            }
            .card-sub{
                font-family:'Outfit', sans-serif;
                font-size:12.5px;
                color: rgba(255,255,255,0.7);
                margin-bottom:1.2rem;
            }

            /* --- feature strip --- */
            .feature-strip{
                display:flex;
                justify-content:center;
                gap:44px;
                margin-top:2.6rem;
                padding-top:1.6rem;
                border-top: 1px solid rgba(255,255,255,0.15);
            }
            .feature-item{
                text-align:center;
                font-family:'Outfit', sans-serif;
                font-size:12px;
                color: rgba(255,255,255,0.8);
            }
            .feature-item .feature-emoji{
                font-size:1.4rem;
                display:block;
                margin-bottom:4px;
            }
                
            .st-key-home_button_container div.stButton > button {
                background: rgba(255,255,255,.15) !important;
                border: 1px solid rgba(255,255,255,.30) !important;
                border-radius: 999px !important;
                font-size: 0.8rem !important;
                padding: 4px 10px !important;
                margin-top: 3rem !important;
                min-height: 28px !important;
                line-height: 1.2 !important;
            }

            
            .st-key-manage-subjects-container {
                background-color: #4f4858 !important;
                border: 1px solid rgba(0, 112, 23, 0.18) !important;
                border-radius: 16px !important;
                padding: 1rem 1.2rem !important;
                box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06) !important;
            }
                
            div[data-testid="stToast"] {
                background-color: #c3e9f4 !important;
                color: black !important;
                border-left: 3px solid black !important;
            }
            div[data-testid="stToast"] * {
                color: black !important;
            }
            /* Camera: larger and remove white side panels */
            div[data-testid="stCameraInput"] {
                width: min(765px, 92vw) !important;
                max-width: 765px !important;
                margin: 0 auto !important;
                padding: 0 !important;
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                overflow: hidden !important;
                border-radius: 2px !important;
            }
            
            # /* create subject dialog*/
            div[data-testid="stDialog"] {
                background: transparent !important;
            }
            
            div[data-testid="stDialog"] h1,
            div[data-testid="stDialog"] h2,
            div[data-testid="stDialog"] p,
            div[data-testid="stDialog"] label {
                color: #2d2d2d !important;
            }


        </style>  

                """
            ,unsafe_allow_html=True)
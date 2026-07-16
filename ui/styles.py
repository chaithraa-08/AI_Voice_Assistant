import streamlit as st

def load_css():
    st.markdown("""
    <style>

    /* Hide only menu and footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    /* DO NOT hide the header */
    /* header {visibility:hidden;} */

    .main-title{
        text-align:center;
        font-size:40px;
        font-weight:bold;
    }

    .subtitle{
        text-align:center;
        color:gray;
        margin-bottom:20px;
    }

    .stButton>button{
        border-radius:10px;
    }

    </style>
    """, unsafe_allow_html=True)
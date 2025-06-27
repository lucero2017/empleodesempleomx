# utils/estilos.py

def aplicar_estilos():
    import streamlit as st
    st.markdown("""
    <style>
        body {
            background-color: #f4f6f9;
        }
        .css-18e3th9 {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
        }
        h1, h2, h3 {
            color: #003366;
        }
        .stButton>button {
            background-color: #003366;
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True)

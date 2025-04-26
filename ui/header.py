import streamlit as st

def render_header():
    st.set_page_config(page_title="Nuggets Chat App", page_icon="💬", layout="wide")
    st.markdown("""
        <h1 style='text-align: center; color: #4A90E2;'>🔮 Nugget AI Smart Search Chatbot</h1>
        <p style='text-align: center; font-size:18px;'>Ask questions and get smart responses based on your documents!</p>
    """, unsafe_allow_html=True)
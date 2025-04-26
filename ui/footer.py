import streamlit as st

def render_footer():
    st.markdown("""
        <hr style="border:1px solid #eee; margin-top:2em;"/>
        <p style='text-align: center; font-size:14px; color: grey;'>Made with Gemini + FAISS + Streamlit</p>
    """, unsafe_allow_html=True)
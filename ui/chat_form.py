import streamlit as st

def render_chat_form():
    with st.form("chat_form", clear_on_submit=True):
        user_query = st.text_input("💬 Enter your query:", "")
        submit_button = st.form_submit_button(label="Ask Nugget")
    return user_query, submit_button
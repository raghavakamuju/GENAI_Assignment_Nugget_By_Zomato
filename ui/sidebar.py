import streamlit as st

def render_sidebar(chat_history):
    st.sidebar.header("🕑 Previous Chats")
    if chat_history:
        for idx, convo in enumerate(chat_history):
            with st.sidebar.expander(f"Chat {idx+1}"):
                st.markdown(f"User: {convo['User Query']}")
                st.markdown(f"Bot: {convo['Response']}")
    else:
        st.sidebar.info("No previous chats yet!")
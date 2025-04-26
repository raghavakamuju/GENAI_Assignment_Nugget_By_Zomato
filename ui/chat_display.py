import streamlit as st

def render_chat_history(chat_history):
    if chat_history:
        st.markdown("---")
        st.markdown("## 🧠 Chat with Nugget AI")
        for convo in reversed(chat_history):
            st.markdown(f"🧑‍💻 You: **{convo['User Query']}**")
            st.markdown(f"🤖 Nugget AI: {convo['Response']}")
            st.markdown("---")
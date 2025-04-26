import streamlit as st

def gemini_response(geminimodel, extracted_texts, user_query):
    history_text = ""
    for idx, convo in enumerate(st.session_state.chat_history[-3:]):
        history_text += f"Previous Query {idx+1}: {convo['User Query']}\nPrevious Response {idx+1}: {convo['Response']}\n"
    prompt = f"""
    {history_text}
    Now the user is asking: {user_query}.
    Use the following extracted content: {extracted_texts}.
    If the extracted content is irrelevant to the query, ask the user to rephrase it.
    """
    response = geminimodel.generate_content(prompt)
    return response.parts[0].text if response.parts else "⚡ No response generated."
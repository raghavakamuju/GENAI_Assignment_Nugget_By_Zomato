import streamlit as st
import numpy as np
import faiss
import pickle
import os
import sentence_transformers
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

with open(os.path.join("knowledge_base", "text_extracted_list.pkl"), "rb") as f:
    text_extracted_list, embeddings_array = pickle.load(f)

API_KEY = os.getenv("API_KEY")  
from rag_chatbot.generative_ai_utils import configure_genai
geminimodel = configure_genai(api_key=API_KEY, model_name="gemini-2.0-flash")

dimension = embeddings_array.shape[1]
faiss_index = faiss.IndexFlatL2(dimension)
faiss_index.add(embeddings_array)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

import ui.header as header
import ui.sidebar as sidebar
import ui.chat_form as chat_form
import ui.chat_display as chat_display
import ui.footer as footer
import ui.gemini_response as gr

header.render_header()
sidebar.render_sidebar(st.session_state.chat_history)
user_query, submit_button = chat_form.render_chat_form()

if submit_button and user_query:
    model = sentence_transformers.SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode(user_query).astype('float32')
    k = 3
    distances, indices = faiss_index.search(np.array([query_embedding]), k)
    extracted_texts = [text_extracted_list[idx] for idx in indices[0]]
    bot_response = gr.gemini_response(geminimodel, extracted_texts, user_query)
    st.session_state.chat_history.append({"User Query": user_query, "Response": bot_response})

chat_display.render_chat_history(st.session_state.chat_history)
footer.render_footer()
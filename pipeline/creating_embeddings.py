import numpy as np
import pickle
from sentence_transformers import SentenceTransformer
from utils.faiss_utils import create_faiss_index

def create_embeddings(text_extracted_list, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Generates embeddings for the extracted texts and saves them to the knowledge_base."""
    model = SentenceTransformer(model_name)
    embeddings = np.array([model.encode(text) for text in text_extracted_list], dtype='float32')
    faiss_index = create_faiss_index(embeddings)
    with open("knowledge_base/text_extracted_list.pkl", "wb") as f:
        pickle.dump((text_extracted_list, embeddings), f)
    return faiss_index
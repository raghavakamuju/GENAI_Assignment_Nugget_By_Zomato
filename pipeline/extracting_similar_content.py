import numpy as np
from sentence_transformers import SentenceTransformer

def find_similar_content(user_query, faiss_index, text_extracted_list, model_name="sentence-transformers/all-MiniLM-L6-v2", k=5):
    """Finds and returns the top-k similar content for a user query."""
    model = SentenceTransformer(model_name)
    query_embedding = model.encode(user_query).astype('float32')
    distances, indices = faiss_index.search(np.array([query_embedding]), k)
    return [text_extracted_list[idx] for idx in indices[0]]
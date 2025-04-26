import faiss

def create_faiss_index(embeddings):
    """Creates a FAISS index for the provided embeddings."""
    dimension = embeddings.shape[1]
    faiss_index = faiss.IndexFlatL2(dimension)
    faiss_index.add(embeddings)
    return faiss_index
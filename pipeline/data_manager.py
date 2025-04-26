from scraper.data_collection import collect_restaurant_data
from pipeline.creating_embeddings import create_embeddings
from pipeline.extracting_similar_content import find_similar_content

def process_restaurant_data(restaurant_links, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """
    Collects data from restaurant links, generates embeddings, and saves them.
    Returns the extracted texts and the FAISS index.
    """
    text_extracted_list = collect_restaurant_data(restaurant_links)
    faiss_index = create_embeddings(text_extracted_list, model_name=model_name)
    return text_extracted_list, faiss_index

def search_similar_content(user_query, faiss_index, text_extracted_list, model_name="sentence-transformers/all-MiniLM-L6-v2", k=3):
    """
    Finds and returns the top-k similar content for the given query.
    """
    return find_similar_content(user_query, faiss_index, text_extracted_list, model_name=model_name, k=k)
from scraper.data_collection import collect_restaurant_data
from pipeline.creating_embeddings import create_embeddings

def run_preprocessing():
    restaurant_links = [
        "https://www.zomato.com/lucknow/apna-kalika-family-restaurant-gomti-nagar",
        "https://www.zomato.com/lucknow/the-terrace-2-hazratganj",
        "https://www.zomato.com/lucknow/milan-restaurant-charbagh",
        "https://www.zomato.com/lucknow/manbhavan-premium-thali-restaurant-gomti-nagar",
        "https://www.zomato.com/lucknow/the-mughals-dastarkhwan-lalbagh"
    ]
    text_extracted_list = collect_restaurant_data(restaurant_links)
    faiss_index = create_embeddings(text_extracted_list)
    print("Preprocessing complete. Embeddings saved in knowledge_base/text_extracted_list.pkl")

if __name__ == "__main__":
    run_preprocessing()
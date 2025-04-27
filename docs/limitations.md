# Limitations

This project currently has the following limitations:

1. **Limited Dataset:**
   - The serialized knowledge base (`knowledge_base/text_extracted_list.pkl`) contains data for only five restaurants:
     1. Apna Kalika Family Restaurant, Lucknow
     2. The Terrace, Lucknow
     3. Milan Restaurant, Lucknow
     4. Manbhavan Premium Thali Restaurant, Lucknow
     5. The Mughals Dastarkhwan, Lucknow

2. **Menu Item Data:**
   - The PKL file includes data on menu items for the above restaurants, which are extracted from the images present on their respective websites.
   - However, the standard preprocessing workflow in this repository does not automatically generate menu item data. The data related to menu items was manually extracted from images and added to the PKL file for training and testing purposes.

3. **Scope of Provided Information:**
   - Information for restaurants beyond the listed five is not included in the PKL file.
   - The RAG-based chatbot is limited to the data present in the knowledge base and does not have the capability to process or provide information about other restaurants or additional details beyond what is contained in the PKL.
   - Information about the restaurants in this repository are bound only to name, location, type of restaurant, menu items, contact information & operating hours.

4. **Impact on Retrieval-Augmented Generation (RAG):**
   - Since the RAG model leverages only the data from the PKL file, its responses are constrained to the content (including menu items) available for the specified five restaurants.
   - Any additional information or restaurants are outside of the system's current capabilities.

These limitations should be considered when utilizing the chatbot, as it is designed only to work with the provided dataset and may not generalize to broader or dynamically updated restaurant information.
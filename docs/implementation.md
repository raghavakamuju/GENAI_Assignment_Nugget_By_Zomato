# Implementation Details

This document provides a detailed explanation of how each component of the Nugget AI Smart Search Chatbot is implemented. It breaks down the functionality of each module, explaining the key functions and workflows used throughout the project.

---

## 1. Data Collection (Web Scraper)

### Module: `scraper/data_collection.py`

- **Purpose:**  
  This module is responsible for dynamically scraping restaurant websites. It extracts key details (restaurant name, type, location, operating hours, and contact information) by targeting specific HTML elements using CSS selectors.

- **Key Functions:**
  - **`is_allowed_by_robots(url, user_agent="*")`:**  
    Dynamically fetches the live `robots.txt` for the given URL and checks whether scraping the page is allowed according to the site's policies.
  
  - **`load_class_names(file_path="class_names.txt")`:**  
    Loads CSS class names and corresponding labels from `scraper/class_names.txt`. The file lists each selector-label pair in a comma-separated format, which allows the scraper to locate the relevant data on the page.
  
  - **`collect_restaurant_data(restaurant_links, class_names_file="class_names.txt")`:**  
    Iterates through a list of restaurant URLs, applies the dynamic `robots.txt` check, and uses BeautifulSoup to parse and extract text for each specified CSS selector. It robustly handles network errors (using try/except blocks) so that the scraping process can continue even if some URLs fail.

---

## 2. Knowledge Base Creation & Retrieval

### Data Preprocessing: `preprocess.py`

- **Purpose:**  
  This script orchestrates the complete data pipeline. It calls the scraper to collect restaurant information, generates embeddings from the scraped text, and builds a FAISS index for similarity search.

- **Workflow:**
  1. **Scraping Data:**  
     Invokes functions from `scraper/data_collection.py` to perform live data scraping.
  
  2. **Generating Embeddings:**  
     Uses a Sentence Transformer (specifically `all-MiniLM-L6-v2`) to convert raw text data into numeric embeddings.
  
  3. **Building FAISS Index:**  
     Constructs a FAISS index (using `faiss.IndexFlatL2`) over the generated embeddings which allows for efficient similarity-based lookups.
  
  4. **Serialization:**  
     Saves the final knowledge base (a tuple containing raw text data and its corresponding embedding array) into `knowledge_base/text_extracted_list.pkl`.

### Embedding & Indexing: `pipeline/creating_embeddings.py`

- **Purpose:**  
  This module focuses on converting textual data into embeddings and handling the creation/updating of the FAISS index.
  
- **Key Functions:**
  - A function to load raw texts and generate embeddings using the Sentence Transformer.
  - A function to build a FAISS index based on these embeddings.
  
### Retrieval Functionality: `pipeline/extracting_similar_content.py`

- **Purpose:**  
  Accepts a user query, converts it to an embedding, and retrieves the top-k most similar entries from the FAISS index.
  
- **Key Details:**
  - The module inputs a user query.
  - It uses the same Sentence Transformer model to generate an embedding.
  - It then performs a similarity search on the FAISS index to retrieve context, which is later used for generating a response.

---

## 3. RAG-based Chatbot & Generative AI

### Generative AI Configuration: `rag_chatbot/generative_ai_utils.py`

- **Purpose:**  
  This module sets up and configures the Google Generative AI model (Gemini 2.0 Flash). It provides the interface for generating responses based on the context retrieved from the FAISS index and the user query.
  
- **Key Functions:**
  - **`configure_genai(api_key, model_name)`**  
    Initializes and configures the generative AI model using the API key and model name.
  
  - **Response Generation Function:**  
    Combines the retrieved context (extracted restaurant data) and the user query into a prompt, calls the generative AI API, and returns a generated response.

### Integration in Main Application: `app.py`

- **Purpose:**  
  The main Streamlit application (`app.py`) is the entry point that ties together data loading, FAISS indexing, user query handling, and generative response generation.

- **Workflow:**
  1. **Initialization:**  
     - Loads environment variables (including the API key).
     - Loads the serialized knowledge base (raw texts and embeddings).
     - Builds the FAISS index from the embedding array.
  
  2. **Generative AI Setup:**  
     Configures Google’s Gemini 2.0 Flash model using functions from `rag_chatbot/generative_ai_utils.py`.
  
  3. **User Query Processing:**  
     - Captures input via the chat form (using UI components).
     - Uses Sentence Transformers to create an embedding from the user query.
     - Searches the FAISS index to retrieve the most similar restaurant data.
  
  4. **Response Generation:**  
     Passes both the retrieved context and the user query to the generative AI module to produce a contextual response.
  
  5. **User Interface Update:**  
     Updates and displays the conversation history using dedicated UI modules.

---

## 4. User Interface Implementation

### UI Components (in the `ui/` directory)

- **`ui/header.py`:**  
  Renders the header section of the application, often containing branding and a title.

- **`ui/sidebar.py`:**  
  Displays the conversation history, allowing users to review past interactions.

- **`ui/chat_form.py`:**  
  Provides the input field and submit button where users type their queries.

- **`ui/chat_display.py`:**  
  Renders the conversation (both user queries and chatbot responses) on the screen in real time.

- **`ui/footer.py`:**  
  Shows the footer with additional project details or copyright information.

- **`ui/gemini_response.py`:**  
  Acts as an intermediary between the generative AI module and the UI. It takes the output from the generative AI module and formats it for display in the chat interface.

---

## 5. Summary of Workflow

1. **Data Collection:**  
   - The system scrapes live restaurant websites, dynamically checking `robots.txt` permissions and handling errors gracefully.
  
2. **Knowledge Base Creation:**  
   - Scraped text data are transformed into embeddings and stored alongside a FAISS index for quick retrieval.
  
3. **User Interaction & Response Generation:**  
   - User queries are encoded into embeddings.
   - The FAISS index is queried for similar data.
   - The generative AI model (Google’s Gemini 2.0 Flash) processes the user query and retrieved context to generate a relevant response.
   - The UI displays the conversation history and generated response using Streamlit.

---

## Conclusion

The implementation is structured in a modular fashion, ensuring that each component (scraping, embedding creation, index building, and UI handling) can be maintained and updated independently. This modular design also facilitates future improvements, such as extending data extraction capabilities, integrating alternative generative AI models, or enhancing the user interface.

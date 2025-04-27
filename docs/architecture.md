# System Architecture

The Nugget AI Smart Search Chatbot is built to answer natural language queries about restaurant information using a Retrieval-Augmented Generation (RAG) approach combined with dynamic web scraping. This document details the design rationale, key components, and data flow within the system.

---

## 1. Overall Design & Approach

The system is divided into three main layers:

1. **Data Collection (Web Scraper):**
   - Gathers raw restaurant data dynamically from multiple websites.
   - Uses third‑party libraries such as BeautifulSoup and Requests to scrape live data.
   - Dynamically fetches the website’s `robots.txt` and checks for scraping permissions to ensure ethical data collection.
   - Implements robust error handling to recover from network or parsing issues.

2. **Knowledge Base Creation & Retrieval:**
   - Processes the scraped data by generating text embeddings using a pre-trained Sentence Transformer model.
   - Constructs an efficient FAISS index for similarity-based search.
   - Stores both the raw text data and the corresponding embedding arrays as a serialized knowledge base.

3. **RAG-based Chatbot & Generative AI:**
   - Uses Google’s Gemini 2.0 Flash model (enabled for all clients) to generate responses by combining the user query and retrieved context.
   - Maintains a conversation history to enable context-aware multi-turn interactions.
   - Deploys an intuitive Streamlit-based user interface for end-user interactions.

---

## 2. Data Collection (Web Scraper)

### Objectives
- **Data Gathering:**  
  Extract key restaurant details – such as name, type, location, operating hour, menu items & prices(if available), and contact information – by scraping live websites.
- **Dynamic `robots.txt` Check:**  
  For each target URL, the scraper dynamically fetches and parses the website’s `robots.txt` file using the live URL. This determines if scraping is permitted, ensuring compliance with the site’s policies.
- **Error Handling:**  
  Incorporates try/except blocks to handle networking errors, non-responsive pages, and parsing issues, ensuring that failures in one URL do not disrupt the overall scraping operation.

### Key Modules
- **`scraper/data_collection.py`:**
  - **`is_allowed_by_robots(url, user_agent="*")`:**  
    Dynamically retrieves the target website’s `robots.txt` file, checking whether scraping the URL is permitted.
  - **`load_class_names(file_path)`:**  
    Loads CSS selectors and target labels from [`scraper/class_names.txt`](scraper/class_names.txt) for identifying HTML elements.
  - **`collect_restaurant_data(restaurant_links, class_names_file)`:**  
    Iterates through a list of restaurant URLs, applies the dynamic `robots.txt` check, and scrapes data using BeautifulSoup.

---

## 3. Knowledge Base Creation & Retrieval

### Objectives
- **Embedding Generation:**  
  Converts the collected restaurant data into numeric embeddings using the Sentence Transformer model (e.g., `all-MiniLM-L6-v2`).
- **Indexing:**  
  Builds a FAISS index (using `faiss.IndexFlatL2`) on the embedding space to facilitate rapid similarity search.
- **Persistence:**  
  Serializes the processed data (raw texts and embeddings) into a knowledge base file located at [`knowledge_base/text_extracted_list.pkl`](knowledge_base/text_extracted_list.pkl).

### Key Modules
- **Preprocessing Script ([preprocess.py](preprocess.py)):**
  - Integrates data collection from [`scraper/data_collection.py`](scraper/data_collection.py) and passes scraped data to the embedding generator.
- **Embedding & Indexing:**
  - **`pipeline/creating_embeddings.py`:**  
    Responsible for converting raw texts into embeddings and creating the FAISS index.
- **Retrieval Module:**
  - **`pipeline/extracting_similar_content.py`:**  
    Accepts a user query, transforms it into an embedding, and retrieves the top-k similar entries from the FAISS index.

---

## 4. RAG-based Chatbot & Generative AI

### Objectives
- **Response Generation:**  
  Leverages Google’s Gemini 2.0 Flash model to generate context-aware responses by combining user queries with relevant content.
- **Conversation History:**  
  Maintains previous interactions (managed via Streamlit’s session state) to provide continuity in responses.
- **Generative AI Integration:**  
  Configures and accesses the generative AI model through functions defined in [`rag_chatbot/generative_ai_utils.py`](rag_chatbot/generative_ai_utils.py).

### Key Modules
- **`rag_chatbot/generative_ai_utils.py`:**
  - **Configuration:** Sets up the Gemini 2.0 Flash model using API credentials.
  - **Response Generation Function:** Accepts extracted context and user queries to produce final chatbot responses.
- **User Flow in `app.py`:**
  - Loads the knowledge base and sets up the FAISS index.
  - Processes user input, retrieves similar restaurant data, and utilizes the generative AI to produce responses.
  - Updates and maintains conversation history.

---

## 5. User Interface

### Objectives
- **Interactivity:**  
  Provides a responsive and intuitive chat interface for users.
- **Session Management:**  
  Displays ongoing conversation history and supports multi-turn dialogue.

### Key Modules
- **Streamlit Application ([app.py](app.py)):**
  - Orchestrates the whole system by integrating data loading, indexing, and generative AI response generation.
  - Dynamically renders UI components using modules in the [`ui/`](ui/) folder.
- **UI Components (located in `ui/`):**
  - **`ui/header.py`:** Renders the header with application branding.
  - **`ui/sidebar.py`:** Displays past conversation history.
  - **`ui/chat_form.py`:** Provides user input facilities.
  - **`ui/chat_display.py`:** Shows the chat conversation in real time.
  - **`ui/footer.py`:** Renders the footer with additional info.
  - **`ui/gemini_response.py`:** Connects the generative AI response to the UI.

---

## 6. Data Flow Summary

1. **Web Scraping:**  
   - The process starts by scraping live restaurant websites using [`scraper/data_collection.py`](scraper/data_collection.py), which dynamically checks each website’s `robots.txt` for permissions.
   - Extracted data, using selectors provided in [`scraper/class_names.txt`](scraper/class_names.txt), is compiled into text strings.

2. **Knowledge Base Creation:**  
   - The preprocessing script ([`preprocess.py`](preprocess.py)) generates embeddings from the scraped texts and builds a FAISS index.
   - The final output (raw texts and embeddings) is saved in [`knowledge_base/text_extracted_list.pkl`](knowledge_base/text_extracted_list.pkl).

3. **Query Processing & Response Generation:**  
   - User input is encoded into embeddings and compared against the FAISS index to retrieve similar content.
   - The retrieved context, alongside the conversation history, is passed to the Gemini 2.0 Flash model (via [`rag_chatbot/generative_ai_utils.py`](rag_chatbot/generative_ai_utils.py)) for response generation.
   - Responses and query history are rendered interactively using the Streamlit UI.

---

## 7. Extensibility and Future Improvements

- **Alternative Generative Models:**  
  The modular design allows for swapping Google’s Gemini model with Hugging Face or other generative AI models if needed.

- **Scalable Storage:**  
  Integrate persistent storage solutions (e.g., databases) to manage larger datasets and support continuous updates to the knowledge base.

- **UI Improvements:**  
  Refine interactive elements to enhance user experience, add responsiveness for mobile platforms, and provide adaptive UI components based on user preferences.

- **Robust Monitoring:**  
  Implement advanced error logging and system monitoring mechanisms to improve debugging and overall system stability.

- **Multiple Language Support:**  
  Extend system capabilities to handle multiple languages by detecting user language preferences and providing localized responses.

- **Adaptive Features:**  
  Incorporate mechanisms to analyze user behavior and location data to tailor responses, ensuring that the system adapts its recommendations based on regional specifics and individual user patterns.

---

This architecture outlines a scalable, maintainable system that dynamically adheres to website policies through live `robots.txt` checks, processes and indexes restaurant data, and integrates a modern generative AI model within an interactive front-end.
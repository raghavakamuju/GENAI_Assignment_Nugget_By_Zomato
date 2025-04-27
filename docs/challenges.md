# Challenges and Solutions

This document outlines the challenges encountered during the development of the Nugget AI Smart Search Chatbot and describes the solutions implemented to address them.

---

## 1. Dynamic Web Scraping

### Challenge:
- **Inconsistent Website Structures:**  
  Restaurant websites often vary in their HTML structure, making it challenging to reliably extract data.
- **Dynamic `robots.txt` Handling:**  
  Fetching and parsing the live `robots.txt` file for every URL can lead to intermittent failures due to network issues or transient errors on the remote site.

### Solutions:
- **CSS Selector Configuration:**  
  Developed a configurable system using `scraper/class_names.txt` to define CSS selectors for data extraction. This file can be updated as needed without changing the code.
- **Robust Error Handling:**  
  Wrapped HTTP requests and parsing operations in try/except blocks to gracefully handle network errors and non-responsive pages.
- **Dynamic `robots.txt` Checks:**  
  Implemented the `is_allowed_by_robots(url, user_agent="*")` function to dynamically fetch and evaluate each site's `robots.txt` before scraping, ensuring ethical data collection.

---

## 2. Knowledge Base Creation & FAISS Indexing

### Challenge:
- **Embedding Quality and Consistency:**  
  Converting raw text data into embeddings that accurately capture semantic meaning can be affected by noise in the scraped data.
- **Scaling the FAISS Index:**  
  Building an efficient and responsive FAISS index for rapid similarity search over a growing dataset.

### Solutions:
- **Pre-trained Sentence Transformer:**  
  Leveraged the `all-MiniLM-L6-v2` model from Sentence Transformers to generate robust, compact embeddings.
- **Efficient Indexing:**  
  Used `faiss.IndexFlatL2` for its simplicity and speed in similarity search, ensuring quick retrieval even as the dataset grows.

---

## 3. Integration with Generative AI

### Challenge:
- **Model Configuration and API Integration:**  
  Proper integration of Google’s Gemini 2.0 Flash model required careful configuration to work reliably with dynamic inputs.
- **Prompt Engineering:**  
  Combining retrieved context with user queries in a coherent prompt was critical for generating relevant responses.

### Solutions:
- **Modular Configuration:**  
  The `rag_chatbot/generative_ai_utils.py` module was designed to cleanly abstract the configuration and response generation for the Gemini model. This modular design allows us to easily replace or update the generative model in the future.
- **Iterative Prompt Refinement:**  
  Tested multiple prompt formats to find a balance that guides the model to produce accurate and context-aware responses, incorporating conversation history for better coherence.

---

## 4. User Interface and Session Management

### Challenge:
- **Real-Time Updates:**  
  Ensuring that the Streamlit UI updates in real time with user input and displays conversation history effectively.
- **Session State Management:**  
  Maintaining the conversation history across multiple user interactions without losing context.

### Solutions:
- **Streamlit Session State:**  
  Utilized Streamlit’s `st.session_state` to continuously store and update conversation history, ensuring that each new user query is processed in context.
- **Modular UI Design:**  
  Separated UI components (header, sidebar, chat form, chat display, and footer) into distinct modules, which improves maintainability and allows for iterative UI improvements.

---

## 5. System Integration and Testing

### Challenge:
- **End-to-End Reliability:**  
  Integrating multiple independent components (web scraper, embedding generator, FAISS index, and generative AI) posed challenges in ensuring overall system stability.
- **Error Propagation:**  
  Handling errors gracefully at each step to prevent a single failure from crashing the entire system.

### Solutions:
- **Layered Testing:**  
  Conducted unit tests for individual components (scraping, embedding, indexing, and response generation) before integrating them into the main application.
- **Graceful Degradation:**  
  Implemented error logging and fallback mechanisms to ensure that errors in one component do not cascade to the entire system, preserving the overall user experience.

---

## Conclusion

Addressing these challenges required a combination of robust error handling, modular design, and careful testing across components. The iterative improvements made throughout the development process have resulted in a stable, scalable, and user-friendly system that meets the requirements of the assignment while remaining flexible for future enhancements.
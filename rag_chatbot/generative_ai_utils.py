import google.generativeai as genai

def configure_genai(api_key, model_name):
    """Configures and returns the Generative AI model."""
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model_name)

def generate_response(model, extracted_texts, user_query, chat_history):
    """Generates a response using the Generative AI model."""
    history_text = ""
    for idx, convo in enumerate(chat_history[-3:]):
        history_text += f"Previous Query {idx+1}: {convo['User Query']}\nPrevious Response {idx+1}: {convo['Response']}\n"
    prompt = f"""
    {history_text}
    Now the user is asking: {user_query}.
    Use the following extracted content: {extracted_texts}.
    If the extracted content is irrelevant to the query, ask the user to rephrase it.
    """
    response = model.generate_content(prompt)
    return response.parts[0].text if response.parts else "⚡ No response generated."
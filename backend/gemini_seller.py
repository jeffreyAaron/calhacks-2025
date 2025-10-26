import json
import ast
import os
import google.generativeai as genai

# Initialize Gemini model (will be configured with API key)
model = None

def configure_gemini(api_key=None):
    """Configure the Gemini API with the provided key."""
    global model
    if api_key is None:
        # Try to read from API_Key.txt in parent directory
        api_key_path = os.path.join(os.path.dirname(__file__), "..", "API_Key.txt")
        if os.path.exists(api_key_path):
            with open(api_key_path, "r") as file:
                api_key = file.read().strip()
        else:
            raise ValueError("No API key provided and API_Key.txt not found")
    
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.0-flash-exp")

def prompt_gemini(item, n=5):
    """Query Gemini for top n affordable seller links for an item."""
    if model is None:
        configure_gemini()
    
    prompt = f"""
    Provide me the top {n} links for affordable {item}.
    Return the output as a single bracketed Python-style list, where each element is formatted as:
    ["WebsiteName", "URL"]

    Rules:
    - Use only one list — not multiple lines.
    - Separate entries with commas, not newlines.
    - Enclose the entire result in square brackets.
    - WebsiteName should be concise (e.g., "Pololu", "Adafruit").
    - URL must be the main home page (include https://).
    - No explanations, no extra text, just the list.
    """

    response = model.generate_content(prompt)
    return response.text.strip()

def get_seller_info(items):
    """Get seller information for a list of items."""
    results = []
    
    for item in items:
        item_name = item.get("name")
        if not item_name:
            continue
            
        response_text = prompt_gemini(item_name, n=5)
        
        # Convert string → Python list
        try:
            data = json.loads(response_text)
        except json.JSONDecodeError:
            try:
                data = ast.literal_eval(response_text)
            except:
                data = []
        
        # Format as list of dicts
        sellers = [{"company": company, "link": link} for company, link in data]
        
        results.append({
            "name": item_name,
            "quantity": item.get("quantity"),
            "sellers": sellers
        })
    
    return results

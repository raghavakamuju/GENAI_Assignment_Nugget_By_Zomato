import os
import requests
from bs4 import BeautifulSoup

def load_class_names(file_path="class_names.txt"):
    """Loads a list of (CSS class name, label) tuples from a text file.
    Each line in the file should be in the format: class_name,label
    Lines starting with '#' or empty lines are skipped.
    """
    class_names_list = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                parts = line.split(",", 1)
                if len(parts) == 2:
                    class_names_list.append((parts[0].strip(), parts[1].strip()))
    return class_names_list

def collect_restaurant_data(restaurant_links, class_names_file="class_names.txt"):
    """Collects data from restaurant links using dynamically loaded CSS class names.
       If the external file is missing or empty, a default list is used.
    """
    # Load dynamic class names list from file
    class_names_list = load_class_names(class_names_file)
    
    # Fallback to defaults if no data is loaded
    if not class_names_list:
        class_names_list = [
            ("sc-7kepeu-0 sc-iSDuPN fwzNdh", "Restaurant Name"),
            ("sc-eXNvrr cMFgfA", "Restaurant Type"),
            ("sc-clNaTc ckqoPM", "Location"),
            ("sc-kasBVs dfwCXs", "Operating Hours"),
            ("sc-bFADNz leEVAg", "Contact Information"),
        ]
    
    text_extracted_list = []
    headers = {"User-Agent": "Mozilla/5.0"}
    for link in restaurant_links:
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = ""
        for class_name, label in class_names_list:
            elements = soup.find_all(class_=class_name)
            text += f"{label}: " + " ".join([element.get_text(strip=True) for element in elements]) + "\n"
        text_extracted_list.append(text)
    return text_extracted_list
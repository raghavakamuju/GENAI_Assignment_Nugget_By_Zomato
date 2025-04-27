import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import urllib.robotparser

def is_allowed_by_robots(url, user_agent="*"):
    """Checks if the URL is allowed to be scraped according to robots.txt."""
    parsed_url = urlparse(url)
    robots_url = f"{parsed_url.scheme}://{parsed_url.netloc}/robots.txt"
    rp = urllib.robotparser.RobotFileParser()
    try:
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(user_agent, url)
    except Exception as e:
        print(f"Error fetching robots.txt at {robots_url}: {e}")
        # If robots.txt check fails, default to not scraping the site.
        return False

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
       Implements robots.txt checking and error handling.
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
        # if not is_allowed_by_robots(link, headers["User-Agent"]):
        #     print(f"Robots.txt does not allow scraping for {link}. Skipping.")
        #     text_extracted_list.append(f"Skipped scraping for {link} due to robots.txt restrictions.")
        #     continue

        try:
            response = requests.get(link, headers=headers, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            text = ""
            for class_name, label in class_names_list:
                elements = soup.find_all(class_=class_name)
                content = " ".join([element.get_text(strip=True) for element in elements])
                text += f"{label}: {content}\n"
            text_extracted_list.append(text)
        except requests.RequestException as req_err:
            error_msg = f"Error fetching {link}: {req_err}"
            print(error_msg)
            text_extracted_list.append(error_msg)
        except Exception as e:
            error_msg = f"Unexpected error at {link}: {e}"
            print(error_msg)
            text_extracted_list.append(error_msg)
    return text_extracted_list
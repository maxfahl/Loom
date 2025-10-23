import requests

def fetch_data(url):
    """Fetches JSON data from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def process_data(url):
    data = fetch_data(url)
    if data:
        return {"processed": True, "original_data": data}
    return {"processed": False}

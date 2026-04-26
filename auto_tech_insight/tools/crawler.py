from bs4 import BeautifulSoup
import requests


def fetch_url_text(url: str, timeout: int = 10) -> str:
    """Fetch a web page and return plain text."""
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return ""

    soup = BeautifulSoup(response.text, "html.parser")
    return " ".join(soup.stripped_strings)[:3000]

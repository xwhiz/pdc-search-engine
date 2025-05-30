from urllib.parse import urlparse
from typing import Dict
import os
from .constants import DATA_PATH

from .get_search_results import get_search_results
from .extract_content import extract_content
from .save_extracted_data import save_extracted_data


def scrape_and_save_content_from_search_results(keyword: str):
    try:
        search_results = get_search_results(keyword)
    except FileNotFoundError:
        print(f"Search results not found for {keyword}")
        return

    if os.path.exists(f"{DATA_PATH}/{'-'.join(keyword.split())}/extracted_data.json"):
        print(f"Extracted data already exists for {keyword}")
        return

    save_from_links([result["link"] for result in search_results], keyword)


def save_from_links(links: list, keyword: str):
    extracted_data: Dict[str, Dict] = dict()
    for url in links:
        domain = urlparse(url).netloc
        content = extract_content(url)
        extracted_data[domain] = content

    save_extracted_data(extracted_data, keyword)

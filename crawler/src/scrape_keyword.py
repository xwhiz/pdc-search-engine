from urllib.parse import urlparse
from typing import Dict
import os
from .constants import DATA_PATH

from .save_search_results import save_search_results
from .get_search_results import get_search_results
from .extract_content import extract_content
from .save_extracted_data import save_extracted_data


def scrape_keyword(driver, keyword: str):
    save_search_results(driver, keyword)

    try:
        search_results = get_search_results(keyword)
    except FileNotFoundError:
        save_search_results(driver, keyword)
        search_results = get_search_results(keyword)

    # if data is already extracted, skip it
    if os.path.exists(f"{DATA_PATH}/{'-'.join(keyword.split())}/extracted_data.json"):
        return

    extracted_data: Dict[str, Dict] = dict()
    for url in map(lambda x: x["link"], search_results):
        domain = urlparse(url).netloc
        content = extract_content(driver, url)
        extracted_data[domain] = content

    save_extracted_data(extracted_data, keyword)

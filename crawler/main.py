from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os

from src.get_search_results import get_search_results
from src.constants import DATA_PATH
from src.save_search_results import save_search_results
from src.extract_content import extract_content
from src.save_extracted_data import save_extracted_data


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    options.page_load_strategy = "eager"
    # options.add_argument("headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def main():
    keywords = open(f"{DATA_PATH}/keywords.txt")
    driver = get_driver()

    keyword = next(keywords).strip()
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

    driver.quit()


if __name__ == "__main__":
    main()

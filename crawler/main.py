from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading as th

from src.scrape_and_save_content_from_search_results import (
    scrape_and_save_content_from_search_results,
)
from src.search_and_save_results import search_and_save_results
from src.constants import DATA_PATH, THREAD_COUNT


def main():
    keywords = open(f"{DATA_PATH}/keywords.txt")

    drivers = [get_driver(headless=False) for _ in range(THREAD_COUNT)]
    scrape_multithread(keywords, drivers, search_and_save_results)
    for driver in drivers:
        driver.quit()

    # drivers = [get_driver(headless=True, eager=True) for _ in range(THREAD_COUNT)]
    # scrape_multithread(keywords, drivers, scrape_and_save_content_from_search_results)
    # for driver in drivers:
    #     driver.quit()


def get_driver(headless=False, eager=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    if eager:
        options.page_load_strategy = "eager"

    if headless:
        options.add_argument("--headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def scrape_multithread(keywords: str, drivers: list[webdriver.Chrome], fn):
    """Expects fn to takes driver and keyword as arguments."""

    threads = []
    current_driver = 0
    for keyword in list(keywords)[:10]:
        t = th.Thread(
            target=fn,
            args=(drivers[current_driver], keyword),
        )
        threads.append(t)
        t.start()
        current_driver = (current_driver + 1) % len(drivers)

        if len(threads) == len(drivers):
            for t in threads:
                t.join()
            threads = []


if __name__ == "__main__":
    main()

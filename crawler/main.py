from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading as th
from concurrent.futures import ThreadPoolExecutor, wait, ALL_COMPLETED

from src.scrape_and_save_content_from_search_results import (
    scrape_and_save_content_from_search_results,
)
from src.search_and_save_results import search_and_save_results
from src.constants import DATA_PATH, THREAD_COUNT


def main():
    with open(f"{DATA_PATH}/keywords.txt") as keywords:
        drivers = [get_driver(headless=False) for _ in range(THREAD_COUNT)]
        scrape_multithread(keywords, drivers, search_and_save_results)
        for driver in drivers:
            driver.quit()

    with open(f"{DATA_PATH}/keywords.txt") as keywords:
        scrape_multithread(keywords, None, scrape_and_save_content_from_search_results)


def get_driver(headless=False, eager=False):
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    if eager:
        options.page_load_strategy = "eager"

    if headless:
        options.add_argument("--headless")

    try:
        return webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
    except Exception as e:
        print(e)
        print("Trying again...")
        return get_driver(headless, eager)


def scrape_multithread(keywords, drivers, fn):
    keywords = keywords.readlines()

    threads = []
    for keyword in tqdm(keywords):
        if drivers is not None:
            threads.append(th.Thread(target=fn, args=(drivers[0], keyword.strip())))
        else:
            threads.append(th.Thread(target=fn, args=(keyword.strip(),)))

        if len(threads) == THREAD_COUNT:
            for thread in threads:
                thread.start()

            for thread in threads:
                thread.join()

            threads = []


if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading as th
from concurrent.futures import ThreadPoolExecutor

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
        drivers = [get_driver(headless=False, eager=True) for _ in range(THREAD_COUNT)]
        print("Drivers created.")
        scrape_multithread(
            keywords, drivers, scrape_and_save_content_from_search_results
        )
        for driver in drivers:
            driver.quit()


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


def scrape_multithread(keywords, drivers: list[webdriver.Chrome], fn):
    """Expects fn to takes driver and keyword as arguments."""

    current_driver = 0
    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        for keyword in keywords:
            executor.submit(fn, drivers[current_driver], keyword.strip())
            current_driver = (current_driver + 1) % len(drivers)

    # t = th.Thread()

    # threads = []
    # current_driver = 0
    # for keyword in keywords:
    #     t = th.Thread(
    #         target=fn,
    #         args=(drivers[current_driver], keyword.strip()),
    #     )
    #     threads.append(t)
    #     t.start()
    #     current_driver = (current_driver + 1) % len(drivers)

    #     if len(threads) == len(drivers):
    #         for t in threads:
    #             t.join()
    #         threads = []


if __name__ == "__main__":
    main()

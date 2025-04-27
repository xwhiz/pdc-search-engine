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
    # with open(f"{DATA_PATH}/keywords.txt") as keywords:
    #     #     drivers = [get_driver(headless=False) for _ in range(THREAD_COUNT)]
    #     scrape_multithread(keywords, search_and_save_results)
    # for driver in drivers:
    #     driver.quit()

    with open(f"{DATA_PATH}/keywords.txt") as keywords:
        # drivers = [get_driver(headless=False, eager=False) for _ in range(THREAD_COUNT)]
        # print("Drivers created.")
        scrape_multithread(keywords, scrape_and_save_content_from_search_results)
        # for driver in drivers:
        #     driver.quit()


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


def scrape_multithread(keywords, fn):
    # current_driver = 0
    # driver_map = {
    #     i: drivers[i] for i in range(len(drivers))
    # }  # Map driver index to driver

    keywords = keywords.readlines()

    with ThreadPoolExecutor(max_workers=THREAD_COUNT) as executor:
        futures = {}
        for keyword in keywords:
            # driver_idx = current_driver
            future = executor.submit(fn, keyword.strip())
            # futures[future] = driver_idx
            # current_driver = (current_driver + 1) % len(driver_map)

        # Wait with timeout
        done, not_done = wait(
            futures.keys(), timeout=5 * 60, return_when=ALL_COMPLETED
        )  # 5 min timeout

        for future in not_done:
            # driver_idx = futures[future]
            # stuck_driver = driver_map[driver_idx]
            # try:
            #     stuck_driver.quit()  # Close old stuck driver
            # except Exception:
            #     pass
            # driver_map[driver_idx] = get_driver(headless=False)  # Restart new driver
            future.cancel()  # Cancel stuck task

            # submit all the keywords of this driver again
            # for i, keyword in enumerate(keywords):
            #     if i % len(driver_map) == driver_idx:
            #         future = executor.submit(
            #             fn, driver_map[driver_idx], keyword.strip()
            #         )
            #         futures[future] = driver_idx


if __name__ == "__main__":
    main()

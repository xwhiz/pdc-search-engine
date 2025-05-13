from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import threading as th
import os
from functools import partial

from src.scrape_and_save_content_from_search_results import (
    scrape_and_save_content_from_search_results,
    save_from_links,
)
from src.search_and_save_results import search_and_save_results
from src.constants import DATA_PATH, THREAD_COUNT


def main():
    # with open(f"{DATA_PATH}/keywords.txt") as keywords:
    #     drivers = [get_driver(headless=False) for _ in range(THREAD_COUNT)]
    #     scrape_multithread(keywords, drivers, search_and_save_results)
    #     for driver in drivers:
    #         driver.quit()

    # with open(f"{DATA_PATH}/keywords.txt") as keywords:
    #     scrape_multithread(keywords, None, scrape_and_save_content_from_search_results)

    all_links = []
    with open(f"{DATA_PATH}/top-1000-websites.txt") as links:
        for keyword in links.readlines():
            all_links.append("https://" + keyword.strip())

    with open(f"{DATA_PATH}/top-10000-websites.txt") as links:
        for keyword in links.readlines():
            all_links.append("https://" + keyword.strip())

    keywords = []
    for link in all_links:
        keywords.append(link.split("//")[1].split("/")[0])

    all_links = [[link] for link in all_links]

    threads = []
    for keyword, links in zip(keywords, all_links):
        thread = th.Thread(target=save_from_links, args=(links, keyword))
        threads.append(thread)
        thread.start()

        print(f"[Threads working]: {len(threads)}")

        if len(threads) == THREAD_COUNT:
            for thread in threads:
                thread.join()

            threads = []


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


def delete_extracted_data(keywords: list):
    for keyword in keywords:
        file = f"{DATA_PATH}/{'-'.join(keyword.split())}/extracted_data.json"
        # delete file if it exists
        if os.path.exists(file):
            os.remove(file)


def scrape_multithread(keywords, drivers, fn):
    if "list" in str(type(keywords)):
        pass
    else:
        keywords = keywords.readlines()

    threads = []
    driver_index = 0
    for keyword in keywords:
        if drivers is not None:
            thread = th.Thread(target=fn, args=(drivers[driver_index], keyword.strip()))
            driver_index = (driver_index + 1) % len(drivers)
            threads.append(thread)
        else:
            thread = th.Thread(target=fn, args=(keyword.strip(),))
            threads.append(thread)
            print(f"[Threads working]: {len(threads)}")

        thread.start()

        if len(threads) == THREAD_COUNT:
            for thread in threads:
                thread.join()

            threads = []


if __name__ == "__main__":
    main()

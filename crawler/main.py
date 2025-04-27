from typing import Dict
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import os
import threading as th

from src.scrape_keyword import scrape_keyword
from src.constants import DATA_PATH


def get_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--disable-dev-shm-usage")
    # options.page_load_strategy = "eager"
    # options.add_argument("headless")
    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )


def main():
    keywords = open(f"{DATA_PATH}/keywords.txt")
    drivers = [get_driver() for _ in range(2)]

    threads = []

    current_driver = 0

    for keyword in list(keywords)[:10]:
        t = th.Thread(target=scrape_keyword, args=(drivers[current_driver], keyword))
        threads.append(t)
        t.start()
        current_driver = (current_driver + 1) % len(drivers)

        if len(threads) == len(drivers):
            for t in threads:
                t.join()
            threads = []

    # for t in threads:
    #     t.join()

    for driver in drivers:
        driver.quit()


if __name__ == "__main__":
    main()

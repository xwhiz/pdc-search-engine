from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import os
import json

from src.get_search_results import get_search_results


def main():
    options = webdriver.ChromeOptions()
    # options.add_argument("headless")
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()), options=options
    )
    keywords = open("../data/keywords.txt")

    # 1. have keyword
    # 2. check if search results has already been scraped or not
    # 3. if not, then scrape the search results
    # 4. if yes, then skip
    # 5. save the search results

    keyword = next(keywords).strip()
    search_results = get_search_results(driver, keyword)

    # # I wanna go on each link and scrape the meta data
    # for link in map(lambda x: x["link"], search_results):
    #     driver.get(link)
    #     soup = BeautifulSoup(driver.page_source, "html.parser")
    #     head = soup.find("head")

    #     for tag in head.select("meta"):
    #         print(tag)

    #     break

    driver.quit()


if __name__ == "__main__":
    main()

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from src.get_search_results import get_search_results
from src.constants import DATA_PATH
from src.save_search_results import save_search_results


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

    # I wanna go on each link and scrape the meta data
    for link in map(lambda x: x["link"], search_results):
        driver.get(link)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        head = soup.find("head")
        body = soup.find("body")

        title = head.select_one("title").text
        description = head.select_one("meta[name='description']").get("content")
        keywords = head.select_one("meta[name='keywords']")
        if keywords is not None:
            keywords = keywords.get("content")
        else:
            keywords = ""

        headings_tags = body.select("h1, h2, h3, h4, h5, h6")
        headings_content = list(set(map(lambda x: x.text, headings_tags)))

        # first two paragraphs
        paragraphs = body.select("h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p")[:2]
        paragraphs_content = list(map(lambda x: x.text, paragraphs))

        # self_domain = parse_link(link)[0]
        all_links = body.select("a")

        for wl in all_links:
            if wl.get("href") is None:
                continue

            wl_href = wl.get("href")
            if not wl_href.startswith("http"):
                continue

            print(urlparse(wl_href))
            # wl_domain = parse_link(wl_href)[0]

            # print(self_domain, wl_domain)

        break

    driver.quit()


if __name__ == "__main__":
    main()

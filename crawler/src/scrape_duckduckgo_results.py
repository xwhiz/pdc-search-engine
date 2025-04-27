from bs4 import BeautifulSoup
from typing import List, Dict


def scrape_duckduckgo_results(driver, query: str) -> List[Dict[str, str]]:
    """Scrapes DuckDuckGo search results for a given query.

    Args:
        query (str): The search query.

    Returns:
        list: A list of dictionaries containing the search results.
    """

    try:
        driver.get(f"http://duckduckgo.com/?q={query}")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        articles = soup.select("ol li[data-layout='organic'] article")
        data: List[Dict[str, str]] = []

        for article in articles:
            data.append(
                {
                    "heading": article.select_one("h2").text,
                    "link": article.select_one(
                        "[data-testid='result-extras-url-link']"
                    ).get("href"),
                    "description": article.select_one("[data-result='snippet']").text,
                }
            )

        return data
    except Exception as e:
        print(e)
        return []

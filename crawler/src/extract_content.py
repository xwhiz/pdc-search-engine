from typing import Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def extract_content(driver, url: str) -> Dict[str, Any]:
    """Extracts content from a given URL using Selenium and BeautifulSoup.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL to extract content from.

    Returns:
        dict: A dictionary containing the extracted content.
    """
    driver.get(url)
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

    paragraphs = body.select("h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p")[:4]
    paragraphs_content = list(map(lambda x: x.text, paragraphs))

    recommendations = _extract_recommendations(url, body)

    return {
        "url": url,
        "domain": urlparse(url).netloc,
        "title": title,
        "description": description,
        "keywords": keywords,
        "headings": headings_content,
        "paragraphs": paragraphs_content,
        "recommendations": recommendations,
    }


def _extract_recommendations(url: str, body) -> List[str]:
    url_domain = urlparse(url).netloc
    recommendations = set()
    for link in body.select("a"):
        if link is None:
            continue

        if link.get("href") is None:
            continue

        link_url = link.get("href")
        if not link_url.startswith("http"):
            continue

        link_domain = urlparse(link_url).netloc
        if link_domain == url_domain:
            continue

        recommendations.add(link_domain)

    return list(recommendations)

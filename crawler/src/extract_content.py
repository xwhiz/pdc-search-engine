from typing import Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests


def extract_content(driver, url: str) -> Dict[str, Any]:
    """Extracts content from a given URL using Selenium and BeautifulSoup.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL to extract content from.

    Returns:
        dict: A dictionary containing the extracted content.
    """
    try:
        # driver.get(url)
        content = requests.get(url)
        soup = BeautifulSoup(content.text, "html.parser")
        print(soup.select("title"))
    except Exception as e:
        print("Exc", url, e)
        return {}

    head = soup.find("head")
    body = soup.find("body")

    title = head.select_one("title")
    if title is not None:
        title = title.text
    else:
        title = ""

    description = head.select_one("meta[name='description']")
    if description is not None:
        description = description.get("content")
    else:
        description = ""

    keywords = head.select_one("meta[name='keywords']")
    if keywords is not None:
        keywords = keywords.get("content")
    else:
        keywords = ""

    headings_tags = body.select("h1, h2, h3, h4, h5, h6")
    headings_content = list(set(map(lambda x: x.text.strip(), headings_tags)))

    paragraphs = body.select("h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p")[:4]
    paragraphs_content = list(map(lambda x: x.text.strip(), paragraphs))

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

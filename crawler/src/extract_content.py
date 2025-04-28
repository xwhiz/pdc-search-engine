from typing import Dict, Any, List
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests


def extract_content(url: str) -> Dict[str, Any]:
    """Extracts content from a given URL using Selenium and BeautifulSoup.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL to extract content from.

    Returns:
        dict: A dictionary containing the extracted content.
    """
    try:
        content = requests.get(url, timeout=8)
        soup = BeautifulSoup(content.text, "html.parser")
    except Exception as e:
        print("Exc", url, e)
        return {}

    head = soup.find("head")
    body = soup.find("body")

    if head is None and body is None:
        return {}

    output = {
        "url": url,
        "domain": urlparse(url).netloc,
    }
    if head is not None:
        title = head.select_one("title")
        if title is not None:
            title = title.text
        else:
            title = ""
        output["title"] = title
        description = head.select_one("meta[name='description']")
        if description is not None:
            output["description"] = description.get("content")
        else:
            output["description"] = ""

        keywords = head.select_one("meta[name='keywords']")
        if keywords is not None:
            output["keywords"] = keywords.get("content")
        else:
            output["keywords"] = ""

    if body is not None:
        headings_tags = body.select("h1, h2, h3, h4, h5, h6")
        output["headings"] = list(set(map(lambda x: x.text.strip(), headings_tags)))

        paragraphs = body.select("h1 + p, h2 + p, h3 + p, h4 + p, h5 + p, h6 + p")[:4]
        output["paragraph"] = list(map(lambda x: x.text.strip(), paragraphs))

        output["recommendations"] = _extract_recommendations(url, body)

    return output


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

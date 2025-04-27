import os
import json

from .constants import DATA_PATH
from .scrape_duckduckgo_results import scrape_duckduckgo_results


def search_and_save_results(driver, keyword: str):
    path = f"{DATA_PATH}/{'-'.join(keyword.split())}"
    if os.path.exists(path):
        return

    os.makedirs(path)
    print(f"Created directory: {path}")
    search_results = scrape_duckduckgo_results(driver, keyword)

    with open(f"{path}/search_results.json", "w") as f:
        json.dump(search_results, f)
        print(
            f"Saved {len(search_results)} search results to {path}/search_results.json"
        )

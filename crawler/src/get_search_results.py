from typing import List, Dict
import os
import json

from .scrape_duckduckgo_results import scrape_duckduckgo_results


def get_search_results(driver, keyword: str) -> List[Dict[str, str]]:
    path = f"../data/{'-'.join(keyword.split())}"
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Created directory: {path}")
        search_results = scrape_duckduckgo_results(driver, keyword)

        with open(f"{path}/search_results.json", "w") as f:
            json.dump(search_results, f)
            print(f"Saved search results to {path}/search_results.json")
    else:
        with open(f"{path}/search_results.json", "r") as f:
            search_results = json.load(f)
            print(f"Loaded search results from {path}/search_results.json")

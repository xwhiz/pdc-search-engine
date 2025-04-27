import os
import json

from .constants import DATA_PATH


def get_search_results(keyword: str) -> list:
    """Returns the search results for a given keyword.

    - **Requires the search results to be saved in the data directory.**

    Args:
        keyword (str): The keyword to search for.

    Returns:
        list: A list of dictionaries containing the search results.
    """
    path = f"{DATA_PATH}/{'-'.join(keyword.split())}/search_results.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r") as f:
        return json.load(f)

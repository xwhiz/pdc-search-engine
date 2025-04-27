import os
import json

from .constants import DATA_PATH


def get_search_results(keyword: str) -> list:
    path = f"{DATA_PATH}/{'-'.join(keyword.split())}/search_results.json"
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")

    with open(path, "r") as f:
        return json.load(f)

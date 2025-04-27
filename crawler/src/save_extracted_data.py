import os
import json

from .constants import DATA_PATH


def save_extracted_data(data: dict, keyword: str):
    path = f"{DATA_PATH}/{'-'.join(keyword.split())}"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/extracted_data.json", "w") as f:
        json.dump(data, f)
        print(f"Saved extracted data to {path}")

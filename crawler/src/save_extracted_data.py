import json

from .constants import DATA_PATH


def save_extracted_data(data: dict, keyword: str):
    path = f"{DATA_PATH}/{'-'.join(keyword.split())}/extracted_data.json"
    with open(path, "w") as f:
        json.dump(data, f)
        print(f"Saved extracted data to {path}")

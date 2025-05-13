import requests
import os

from src.constants import DATA_PATH


def main():
    try:
        url = os.environ["URL"]
    except KeyError:
        url = "http://localhost:8983"

    with open(f"{DATA_PATH}/all_data.json", "r") as f:
        data = f.read()

    solr_url = f"{url}/solr/main_core/update?commit=true"
    empty_solr(solr_url)

    response = requests.post(
        solr_url, data=data, headers={"Content-Type": "application/json"}
    )

    print("Write updated data", response.status_code, response.text)


def empty_solr(url):
    headers = {"Content-Type": "application/json"}
    delete_query = {"delete": {"query": "*:*"}}

    response = requests.post(url, headers=headers, json=delete_query)
    print("Empty solr", response.status_code, response.text)


if __name__ == "__main__":
    main()

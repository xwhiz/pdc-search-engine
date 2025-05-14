import os
import json
from collections import defaultdict
from dotenv import load_dotenv

from src.constants import DATA_PATH

load_dotenv()


def main():
    directories = [
        f"{DATA_PATH}/{dr}"
        for dr in os.listdir(DATA_PATH)
        if os.path.isdir(f"{DATA_PATH}/{dr}")
    ]
    print(len(os.listdir("./data")))
    print("DATA_PATH:", DATA_PATH)
    all_pages = []

    for directory in directories:
        try:
            file = open(f"{directory}/extracted_data.json", "r")
        except FileNotFoundError:
            continue

        pages: dict = json.loads(file.read())

        for page in pages.values():
            # skip empty records
            if len(page) == 0:
                continue

            # skip records with no title
            if "title" not in page:
                continue

            title = page["title"].strip()

            if title == "":
                continue

            negative_cases = [
                "access denied",
                "sorry",
                "something went wrong",
                "403",
                "502",
                "robot or human",
                "no index",
                "just a moment",
                "not acceptable",
                "request has been blocked",
                "checking your browser",
                "service unavailabel",
                "attention required",
                "access to this page has been denied",
                "404",
                "error",
            ]

            if any([v in title.lower() for v in negative_cases]):
                continue

            all_pages.append(page)

        file.close()

    page_ranks = compute_pagerank(all_pages)

    for i in range(len(all_pages)):
        domain = all_pages[i]["domain"]
        all_pages[i]["page_rank"] = page_ranks[domain]

    with open(f"{DATA_PATH}/all_data.json", "w") as f:
        json.dump(all_pages, f)
        print("Data written successfully to file")


def compute_pagerank(pages, damping=0.85, max_iterations=100_000, tol=1.0e-6):
    # Extract all unique domains
    domains = {page["domain"] for page in pages}
    N = len(domains)
    domain_list = list(domains)

    # Initialize PageRank scores
    pr = {domain: 0 for domain in domain_list}

    # build the link graph (domain -> list of outbound domains in dataset)
    out_links = defaultdict(set)
    in_links = defaultdict(set)

    for page in pages:
        src = page["domain"]
        for rec in page.get("recommendations", []):
            if rec in domains:
                out_links[src].add(rec)
                in_links[rec].add(src)

    # power iteration
    for iteration in range(max_iterations):
        new_pr = {}
        for domain in domain_list:
            inbound_sum = 0
            for linker in in_links[domain]:
                outbound_count = len(out_links[linker])
                if outbound_count > 0:
                    inbound_sum += pr[linker] / outbound_count
            new_pr[domain] = (1 - damping) / N + damping * inbound_sum

        # Check for convergence
        delta = sum(abs(new_pr[d] - pr[d]) for d in domain_list)
        pr = new_pr
        if delta < tol:
            break

    return pr


if __name__ == "__main__":
    main()

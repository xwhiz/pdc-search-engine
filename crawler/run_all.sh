#!/bin/bash

set -e

source .venv/bin/activate

echo "Running prepare data"
uv run prepare_data.py

echo "Running upload data"
uv run upload_to_solr.py
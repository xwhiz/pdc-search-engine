#!/bin/bash
set -e

# Wait for Solr to be available
echo "Waiting for Solr at ${URL} to be ready..."
until curl -s "${URL}/solr/#/main_core/core-overview" >/dev/null; do
  echo "Solr is not ready, waiting 5 seconds..."
  sleep 5
done

source .venv/bin/activate

echo "Solr is up. Running prepare_data.py..."
python prepare_data.py

echo "Running upload_to_solr.py..."
python upload_to_solr.py

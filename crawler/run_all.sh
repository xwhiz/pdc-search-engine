#!/bin/bash

set -e

echo "Running prepare data"
python prepare_data.py

echo "Running upload data"
python upload_to_solr.py
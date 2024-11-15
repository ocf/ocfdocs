#!/bin/bash
source /ocfdocs/venv/bin/activate

while true; do
    python3 ./sync.py
    mkdocs build
    sleep 3600  # Every hour     
done
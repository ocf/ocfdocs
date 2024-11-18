#!/bin/bash
source /ocfdocs/venv/bin/activate

while true; do
    python3 ./sync.py
    mkdocs build
    sleep 1800  # Every 30 minutes     
done
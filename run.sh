#!/bin/bash


python3 sync.py # sync changes
mkdocs build

cd site
python3 -m http.server
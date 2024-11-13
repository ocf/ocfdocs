#!/bin/sh
while true; do
    python3 ./sync.py
    sleep 3600  # Every hour
done
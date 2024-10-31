#!/bin/bash

# Create docs directory and move base template 
mkdir docs

cp ./base/* ./docs

# Create .env file for secrets
# YOU NEED TO MANUALLY ADD YOUR API
touch .env
echo "API_KEY=" > .env


# Activate python venv
python3 -m venv venv

source ./venv/bin/activate

pip install -r requirement.txt



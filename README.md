This is the mkdocs application for OCF Documentation.

## Development
As of now (before containarization), you need to activate a virtual environment and install the dependencies:

```bash
python3 -m virtualenv venv
source venv/bin/activate
pip3 install -r requirements.txt
```

You also need to generate your API key for Outline. Go to Outing -> Settings and generate you key. Then create .env file and append:

```bash
API_KEY=[your API Key] 
```

Running the application
./run.sh



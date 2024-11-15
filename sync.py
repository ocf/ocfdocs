import re
import requests
import time
import os
from dotenv import load_dotenv
import zipfile
import shutil
import json

class OutlineAPI:
    def __init__(self, api_token):
        self.base_url = "https://docs.ocf.berkeley.edu/api"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }


    def get_collection_documents(self, collection_id):
        """
        Fetch Zip file of a collection from Outline and return the download URL.
        """

        # Request the collection export and initialize the file operation
        url = f"{self.base_url}/collections.export"
        payload = {
            "id": collection_id,
            "format": "outline-markdown"
        }

        response = requests.post(url, json=payload, headers=self.headers)


        try:
            operation_id = response.json().get("data").get("fileOperation").get('id')

        except AttributeError as e:
            raise ValueError(f"Error fetch content [{response}]. Your API key might be invalid or the collection might not exist.")

        # Check the file operation and await completion
        operation_url = f"{self.base_url}/fileOperations.info"
        operation_payload = {
            "id": operation_id
        }

        while True:
            operation_request = requests.post(operation_url, json=operation_payload, headers=self.headers).json()
            state = operation_request.get("data").get("state")
            if state == "complete":
                break
            if state == "failed":
                raise Exception("File operation failed.")
            else:
                time.sleep(1)

        # Fetch the downloadable collection url from file operation
        operation_response = requests.post(f"{self.base_url}/fileOperations.redirect", json=operation_payload, headers=self.headers)
        return operation_response.url


    def download_collection(self, collection_url):
        """
        Download a collection from Outline and save it docs folder.
        """
        # Get zip file
        response = requests.get(collection_url)
        with open("temp.zip", "wb") as f:
            f.write(response.content)

        # Unzip
        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall("./temp")
        
        # Move all contents from temp to docs
        for item in os.listdir("./temp"):
            try:
                shutil.move(os.path.join("./temp", item), "./docs")
            except:
                shutil.rmtree(os.path.join("./docs", item))
                shutil.move(os.path.join("./temp", item), "./docs")

        # Outline API downloads the index page of each section outside the section folder
        # As a result, Mkdocs would build the index page outside the section, which is not desired
        # This code moves the index pages into the section folder
        # However, this would break the internal links to the moved index pages...
        # Is there is a better approach?
        for root, dirs, files in os.walk("./docs"):
            for file in files:
                file_name = os.path.splitext(file)[0]
                subdir_path = os.path.join(root, file_name)
                if os.path.isdir(subdir_path):
                    source_file = os.path.join(root, file)
                    shutil.move(source_file, os.path.join(subdir_path, "index.md"))

        # Remove temp files and directory
        shutil.rmtree("./temp")
        os.remove("temp.zip")



    
def main():
    load_dotenv()
    api_token = os.getenv("API_KEY")
    outline_api = OutlineAPI(api_token)

    # Reinitialize the docs folder
    shutil.rmtree("./docs")
    os.mkdir("docs")
    for item in os.listdir("./base"):
        s = os.path.join("./base", item)
        d = os.path.join("./docs", item)
        if os.path.isdir(s):
            shutil.copytree(s, d, dirs_exist_ok=True)
        else:
            shutil.copy(s, d)
        
    # Fetch from outline
    with open("config.json") as f:
        collections = json.load(f)
    ids = collections["collections"]

    for collection in ids:
        response = outline_api.get_collection_documents(collection)
        outline_api.download_collection(response)
    
    print("Sync complete.")
    

if __name__ == "__main__":
    main()


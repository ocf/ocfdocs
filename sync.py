import re
import requests
import time
import os
from dotenv import load_dotenv
import zipfile
import shutil

class OutlineAPI:
    def __init__(self, api_token):
        self.base_url = "https://docs.ocf.berkeley.edu/api"
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_token}"
        }

    def list_file_operations(self): 
        url = "https://docs.ocf.berkeley.edu/api/fileOperations.list"

        payload = {
            "limit": 25,
            "sort": "updatedAt",
            "direction": "DESC",
            "type": "export"
        }

        response = requests.get(url, json=payload, headers=self.headers)
        return response.json()

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
        Download a collection from Outline and save it in docs folder
        """
        # Get zip file
        response = requests.get(collection_url)
        with open("temp.zip", "wb") as f:
            f.write(response.content)

        # Unzip
        with zipfile.ZipFile("temp.zip", "r") as zip_ref:
            zip_ref.extractall("./temp")

        # Rename files and directories to replace spaces with hyphens
        # for root, dirs, files in os.walk("./temp", topdown=False):
        #     for name in files + dirs:
        #         new_name = name.replace(" ", "-")
        #         os.rename(os.path.join(root, name), os.path.join(root, new_name))
        # Removed, since it results in incompatible internal links after Mkdocs build
        
        # Move all contents from temp to docs
        for item in os.listdir("./temp"):
            try:
                shutil.move(os.path.join("./temp", item), "./docs")
            except:
                shutil.rmtree(os.path.join("./docs", item))
                shutil.move(os.path.join("./temp", item), "./docs")

        # Remove temp files and directory
        shutil.rmtree("./temp")
        os.remove("temp.zip")


    def save_as_md(self, text, filename):
        """
        Save a block of text as a Markdown (.md) file.
    
        :param text: The text to save as markdown.
        :param filename: The name of the file to save (without extension).
        """
        # Ensure the file ends with .md extension
        if not filename.endswith(".md"):
            filename += ".md"
            filename.replace(" ", "-")
    
        try:
            # Open file in write mode
            with open(filename, "w") as file:
                file.write(text)
            print(f"File saved as {filename}")

        except Exception as e:
            print(f"An error occurred: {e}")

    
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
    # Should be improved
    user_docs = "user-facing-docs-2akcai9GbX"
    staff_docs = "staff-documentation-rMKefp3gWm"

    # Should be improved
    response = outline_api.get_collection_documents(staff_docs)
    outline_api.download_collection(response)
    
    # Should be improved
    response = outline_api.get_collection_documents(user_docs)
    outline_api.download_collection(response)





if __name__ == "__main__":
    main()


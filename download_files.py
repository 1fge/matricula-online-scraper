import os
import sys
import logging
import requests
import traceback

from ast import literal_eval
from bs4 import BeautifulSoup
from headers import csrf_request_headers

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)


class Downloader:
    def __init__(self, record_URL, images_dir):
        self.session = requests.Session()
        self.record_URL = record_URL
        self.images_dir = images_dir
        self.image_URLs_list = None
        self.csrf_token = None

    ''
    @classmethod
    def log_error_and_exit(cls, error_message):
        logging.error(error_message)
        sys.exit()

    def prepare_images_dir(self):
        if not os.path.exists(self.images_dir):
            os.mkdir(self.images_dir)
        logging.info(f"Saving Images to {os.path.abspath(self.images_dir)}")

    def fetch_record_page(self):
        try:
            response = self.session.get(self.record_URL, headers=csrf_request_headers())
            if response.status_code == 200:
                self.get_csrf_token()
                self.parse_image_URLs(response.text)
            else:
                self.log_error_and_exit(f"{response.status_code} Status Code Fetching CSRF Token, Exiting")
        except Exception:
            self.log_error_and_exit(f"Unexpected Error Fetching Record Page, Exiting\n{traceback.format_exc()}")

    def get_csrf_token(self):
        csrf_token = self.session.cookies.get_dict().get("shared_csrftoken")

        if csrf_token is not None:
            logging.info("Fetched CSRF")
            self.csrf_token = csrf_token
        else:
            self.log_error_and_exit("CSRF Token Not Received, Exiting")

    def parse_image_URLs(self, record_reponse_text):
        if '"files":' not in record_reponse_text:
            self.log_error_and_exit("Error Parsing Image URLs, Exiting")

        start_files_list = record_reponse_text.split('"files":')[1]
        full_files_list = start_files_list.split('"],')[0].strip() + '"]'

        self.image_URLs_list = literal_eval(full_files_list)
        logging.info(f"Fetched List of {len(self.image_URLs_list)} Images")


if __name__ == "__main__":
    download = Downloader("https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0001", "./images")
    download.prepare_images_dir()
    download.fetch_record_page()

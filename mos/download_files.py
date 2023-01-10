#!/usr/bin/env python3

import logging
import os
import requests
import sys
import time
import traceback
import uuid

from ast import literal_eval
from bs4 import BeautifulSoup as bs

try:
    from mos.encryption_routine import encryption_routine
    from mos.headers import csrf_request_headers, download_image_headers
except ModuleNotFoundError:
    from encryption_routine import encryption_routine
    from headers import csrf_request_headers, download_image_headers


class Downloader:
    def __init__(self, record_URL, file_range, base_images_dir):
        self.session = requests.Session()
        self.record_URL = record_URL
        self.file_range = file_range
        self.base_images_dir = base_images_dir

        self.archive_directory_name = None
        self.image_URLs_and_labels = None
        self.csrf_token = None
        self.CRAWL_SPEED = 2  # 2 second delay between each archive request

    @classmethod
    def log_error_and_exit(cls, error_message):
        logging.error(error_message)
        sys.exit()

    def create_archive_directory(self):
        archive_directory_path = os.path.join(
            self.base_images_dir, self.archive_directory_name
        )
        archive_directory_path = os.path.normpath(archive_directory_path)
        os.makedirs(archive_directory_path, exist_ok=True)

    def fetch_record_page(self):
        try:
            response = self.session.get(self.record_URL, headers=csrf_request_headers())
            if response.status_code == 200:
                self.get_csrf_token()
                self.parse_image_URLs_and_labels(response.text)
                self.parse_archive_name(response.text)
                self.create_archive_directory()
            else:
                self.log_error_and_exit(
                    f"{response.status_code} Status Code Fetching CSRF Token, Exiting"
                )
        except Exception:
            self.log_error_and_exit(
                f"Unexpected Error Fetching Record Page, Exiting\n{traceback.format_exc()}"
            )

    def get_csrf_token(self):
        csrf_token = self.session.cookies.get_dict().get("shared_csrftoken")

        if csrf_token is not None:
            logging.info("Fetched CSRF")
            self.csrf_token = csrf_token
        else:
            self.log_error_and_exit("CSRF Token Not Received, Exiting")

    def parse_image_URLs_and_labels(self, record_response_text):
        if '"files":' not in record_response_text or "labels" not in record_response_text:
            self.log_error_and_exit("Error Parsing Image URLs, Exiting")

        start_files_list = record_response_text.split('"files":')[1]
        full_files_list = literal_eval(start_files_list.split('"],')[0].strip() + '"]')

        start_labels_list = record_response_text.split('"labels":')[1]
        full_labels_list = literal_eval(
            start_labels_list.split('"],')[0].strip() + '"]'
        )

        self.image_URLs_and_labels = tuple(zip(full_files_list, full_labels_list))

        # if a range is provided and the range is less than the number of scraped files, use it
        if self.file_range is not None and self.file_range < len(
            self.image_URLs_and_labels
        ):
            self.image_URLs_and_labels = self.image_URLs_and_labels[0 : self.file_range]

        logging.info(
            f"Fetched List of {len(self.image_URLs_and_labels)} Images From '{self.record_URL}'"
        )

    def parse_archive_name(self, record_response_text):
        try:
            soup = bs(record_response_text, "html.parser")
            archive_category = (
                soup.find("table", {"class": "table table-register-data"})
                .find("a")
                .text.strip()
            )
            archive_category = "".join(
                [char for char in archive_category if char.isalnum()]
            )  # removing characters that could cause errors when writing creating dir
            archive_id = (
                record_response_text.split("Archival identifier<td>")[1]
                .split("\n")[0]
                .strip()
            )
            archive_id = "".join([char for char in archive_id if char.isalnum()])
            self.archive_directory_name = archive_category + "_" + archive_id
        except Exception as e:
            logging.error(
                "Error Parsing Archive Category and ID, Creating Random Directory Name"
            )
            self.archive_directory_name = str(uuid.uuid4())[
                0:18
            ]  # first 18 chars of a random UUID

    def save_image(self, image_content, image_label, file_number):
        logging.info(
            f"Downloaded File {file_number} of {len(self.image_URLs_and_labels)}"
        )
        file_path = os.path.join(
            self.base_images_dir, self.archive_directory_name, f"{image_label}.jpg"
        )

        with open(file_path, "wb") as f:
            f.write(image_content)

    def download_files(self):
        for index, (image_path, image_label) in enumerate(self.image_URLs_and_labels):
            request_attempts = 0
            url = encryption_routine.createValidURL(image_path, self.csrf_token)
            file_number = index + 1

            while request_attempts < 3:
                try:
                    response = self.session.get(url, headers=download_image_headers())
                    if response.status_code == 200:
                        self.save_image(response.content, image_label, file_number)
                    else:
                        logging.info(
                            f"Skipping File {file_number} ({response.status_code} Response)"
                        )
                    time.sleep(self.CRAWL_SPEED)
                    break
                except requests.exceptions.ConnectionError:
                    if request_attempts < 3:
                        request_attempts += 1
                        logging.info(
                            f"Retrying File {file_number}, Attempt ({request_attempts})"
                        )
                    else:
                        logging.info(
                            f"Skipping File {file_number}, {request_attempts} failed attempts"
                        )
                except Exception:
                    logging.info(
                        f"Skipping File {file_number}\n ({traceback.format_exc()})"
                    )
                    break


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    download = Downloader(
        "https://data.matricula-online.eu/en/deutschland/akmb/militaerkirchenbuecher/0002/?pg=1",
        None,
        "./images",
    )
    download.fetch_record_page()
    download.download_files()

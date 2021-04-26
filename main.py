import argparse
import logging
import os
import sys

from download_files import Downloader

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_parsed_args():
    download_parser = argparse.ArgumentParser(description="Download scanned images from matricula-online")
    download_parser.add_argument("-o", "--output-directory", help="The directory to store the folder of downloaded images", required=True)

    input_group = download_parser.add_mutually_exclusive_group(required=True)
    input_group.add_argument("-u", "--url", help="URL to download the images from")
    input_group.add_argument("-t", "--text-file", help="Path to file containing a list of scanned image URLs")

    return download_parser.parse_args()

def verify_archive_list_exists(urls_file_path):
    if not os.path.exists(urls_file_path):
        logging.error(f"{urls_file_path} Not Found, Exiting")
        sys.exit()

def download_archive(url, output_directory):
    download = Downloader(url, output_directory)
    download.fetch_record_page()
    download.download_files()

def download_archives_from_list(urls_file_path, ouptut_directory):
    with open(urls_file_path) as f:
        urls = f.read().splitlines()

    for url in urls:
        download_archive(url, output_directory)

if __name__ == "__main__":
    args = get_parsed_args()
    output_directory = args.output_directory

    if args.url is not None:
        download_archive(args.url, output_directory)
    else:
        verify_archive_list_exists(args.text_file)
        download_archives_from_list(args.text_file, output_directory)
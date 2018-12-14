#!/usr/bin/env python -OO
# -*- coding: utf-8 -*-
import logging
import os
import sys
import requests
import time

current_working_directory = os.path.dirname(os.path.abspath(__file__))
archive_folder = os.path.join(current_working_directory, "j-archive")
GAME_URL = 'http://j-archive.com/showgame.php'
SECONDS_BETWEEN_REQUESTS = 3
ERROR_MSG = "ERROR: No game"

def main():
    create_archive_dir()
    logging.info("Downloading game files")
    download_pages()

def create_archive_dir():
    if not os.path.isdir(archive_folder):
        logging.info("Making {}".format(archive_folder))
        os.mkdir(archive_folder)

def download_pages():
    page = 0
    more_pages = True
    while more_pages:
        page += 1
        more_pages = download_and_save_page(page)


def download_and_save_page(page):
    destination_file_path = os.path.join(archive_folder, "{}.html".format(page))
    if not os.path.exists(destination_file_path):
        html = download_page(page)
        if ERROR_MSG in html:
            # Now we stop
            logging.info("Finished downloading!")
            return False
        elif html:
            with open(destination_file_path, 'w') as f:
                f.write(html)
            time.sleep(SECONDS_BETWEEN_REQUESTS)  # Remember to be kind to the server
    else:
        logging.info("Already downloaded {}".format(destination_file_path))
    return True


def download_page(page):
    """Grabs a game page"""
    try:
        response = requests.get(GAME_URL, params={'game_id': page})
        if response.ok:
            logging.info("Downloading {}".format(response.url))
            return response.text
        else:
            logging.info("Invalid URL: {}".format(response.url))
    except:
        logging.info("Failed to open {}".format(response.url))


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()

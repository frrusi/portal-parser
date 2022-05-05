import os

import requests


class SecondaryUtils:
    def __init__(self):
        pass

    @staticmethod
    def check_internet_by_url(url):
        try:
            requests.get(url)
            return True
        except requests.ConnectionError:
            return False

    @staticmethod
    def get_image(url):
        response = requests.get(url)
        with open(r"data\user_avatar.png", "wb") as file:
            file.write(response.content)

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

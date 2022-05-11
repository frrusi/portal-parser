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

    def get_image(self, url):
        response = requests.get(url)
        with open(rf"data\user_avatar.{self.get_file_extension(url)}", "wb") as file:
            file.write(response.content)

    @staticmethod
    def create_dir(dir_path: str):
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)

    @staticmethod
    def get_file_extension(file):
        return file[file.rfind('.') + 1:]

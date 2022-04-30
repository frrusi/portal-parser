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

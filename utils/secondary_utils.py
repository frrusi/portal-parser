import requests


def check_internet_by_url(url):
    try:
        requests.get(url)
        return True
    except requests.ConnectionError:
        return False

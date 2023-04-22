import requests
from bs4 import BeautifulSoup


def get_request(url: str, encoding: str):
    html = requests.get(url)
    html.encoding = encoding
    html_text = html.text
    soup = BeautifulSoup(html_text, 'lxml')
    return soup

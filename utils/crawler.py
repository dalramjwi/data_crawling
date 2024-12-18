import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    response = requests.get(url)
    response.encoding = 'utf-8'
    if response.status_code != 200:
        raise ValueError(f"요청 실패: {url}, 상태 코드: {response.status_code}")
    return BeautifulSoup(response.text, "html.parser")

def extract_data(soup, parser_function):
    return parser_function(soup)

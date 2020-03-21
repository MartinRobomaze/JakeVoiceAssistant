import re

import requests
from bs4 import BeautifulSoup


class NewsScraper:
    def __init__(self, url):
        self._url = url

    def get_latest_news(self):
        response = requests.get(self._url)
        soup = BeautifulSoup(response.text, 'lxml')
        headlines = soup.find_all(attrs={"itemprop": "headline"})

        headlines_no_html = []
        for headline in headlines:
            headlines_no_html.append(re.sub('<[^<]+?>', '', str(headline)))

        return headlines_no_html[0:3]

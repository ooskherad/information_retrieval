import requests
from bs4 import BeautifulSoup


class Crawl:
    def __init__(self, url):
        self.base_url = url

    def crawl(self, start_url=None):
        contents = []
        url = start_url if start_url else self.base_url
        for i in range(1, 40):
            url += f'{i}'
            links = self.get_and_select(url, ['section.news-list-items> article> div> h4 > a'])
            for link in links:
                content_url = self.base_url + link.attrs.get('href')
                content = self.get_and_select(content_url, ['.content > p'])
                if not content:
                    content = self.get_and_select(content_url, ['#news > p'])
                contents.append({'url': content_url, 'text': content})
            url = url.removesuffix(f'{i}')
        return contents

    @staticmethod
    def get_and_select(url, selectors: list):
        data = []
        request = requests.get(url)
        soup = BeautifulSoup(request.text, 'html.parser')
        for selector in selectors:
            data.extend(soup.select(selector))

        return data if data else None


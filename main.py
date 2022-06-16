from data_gathering import DataGathering
from database import sqlite
from tokenizer import tokenize


class Crawl(DataGathering):
    def __init__(self, url):
        super(Crawl, self).__init__()
        self.base_url = url

    async def crawl(self, start_url=None):
        url = start_url if start_url else self.base_url
        for i in range(1, 40):
            url += f'{i}'
            links = await self.select_crawl_data(url, 'section.news-list-items> article> div> h4 > a')
            for link in links:
                content_url = self.base_url + link.attrs.get('href')
                content = await self.select_crawl_data(content_url, '.content > p')
                if not content:
                    content = await self.select_crawl_data(content_url, '#news > p')
                self.save_data(content_url, content)
            url = url.removesuffix(f'{i}')

    def save_data(self, url, content):
        if sqlite.url_exists(url):
            return
        doc_id = sqlite.save_url(url)
        if content is not None:
            contents = ''
            for text in content:
                contents = contents + text.text + ' '
            for term in tokenize.execute(contents):
                sqlite.save_term((term['term'], doc_id, term['tf']))


if __name__ == '__main__':
    c = Crawl('https://raisi.ir/')
    c.run(c.crawl, start_url='https://raisi.ir/service/news/')

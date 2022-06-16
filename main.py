from cosine_similarity_score import CosineScore
from data_gathering import DataGathering
from database import sqlite
from tokenizer import tokenize
import streamlit as st
import pandas as pd


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


def make_clickable(link):
    return f'<a target="_blank" href="{link}">{link}</a>'


if __name__ == '__main__':
    # c = Crawl('https://raisi.ir/')
    # c.run(c.crawl, start_url='https://raisi.ir/service/news/')
    # configuration
    st.set_page_config(page_title="cosine similarity", layout='wide')
    st.header('Cosine Similarity Score')
    input_data = st.text_input(label='', placeholder='search somethings')
    query = "select link from documents where id = ?"
    if input_data:
        cs = CosineScore()
        result = cs.search(input_data)
        result = {sqlite.select(f"select link from documents where id = {k}")[0]['link']: v for k, v in
                  sorted(result.items(), key=lambda item: item[1], reverse=True)}
        print(result)
        result = pd.DataFrame(list(result.items()), columns=['link', 'Value'])
        result['link'] = result['link'].apply(make_clickable)
        result = result.to_html(escape=False)
        st.write(result, unsafe_allow_html=True)

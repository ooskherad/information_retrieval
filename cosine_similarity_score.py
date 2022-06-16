from database import sqlite
from tokenizer import tokenize
import math


class CosineScore:
    def __init__(self):
        self.corpus_size = self.get_corpus_size()

    def search(self, query):
        scores = {}
        tq = tokenize.execute(query)
        for term in tq:
            posting_list = self.get_posting_list(term['term'])
            if posting_list:
                df = len(posting_list)
                query_wight = self.tf_idf(term, df)
                print('\n****\n', term, '-> ', query_wight, '\n')
                for item in posting_list:
                    document_wight = self.tf_idf(item, df)
                    doc_score = 0 if not scores.get(item['doc_id']) else scores.get(item['doc_id'])
                    print(scores.get(item['doc_id']), '-> ', document_wight, ' : ',
                          doc_score + query_wight * document_wight, '\n')
                    scores.update({item['doc_id']: doc_score + query_wight * document_wight})

        return scores

    @classmethod
    def get_posting_list(cls, term: str):
        query = f"select * from terms where term='{term}'"
        data = sqlite.select(query)
        return data

    def tf_idf(self, item, document_frequency):
        if item['tf'] == 0:
            tf = 0
        else:
            tf = 1 + math.log(item['tf'])
        idf = math.log(self.corpus_size / (document_frequency + 1))
        score = tf * idf
        return score

    @classmethod
    def get_corpus_size(cls):
        query = 'select count(*) as cnt from documents'
        return sqlite.select(query)[0]['cnt']


if __name__ == '__main__':
    c = CosineScore()
    x = c.search('شهادت')
    query = "select link from documents where id = ?"
    result = {sqlite.select(f"select link from documents where id = {k}")[0]['link']: v for k, v in sorted(x.items(), key=lambda item: item[1], reverse=True)}
    import pandas as pd

    # result = pd.DataFrame(result)
    print(result)

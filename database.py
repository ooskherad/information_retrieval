import sqlite3


class Connection:
    @classmethod
    def get_connection(cls):
        return sqlite3.connect('data.db')

    @classmethod
    def select(cls, query):
        con = cls.get_connection()
        con.row_factory = sqlite3.Row
        cursor = con.cursor().execute(query)
        list_accumulator = []
        for item in cursor.fetchall():
            list_accumulator.append({k: item[k] for k in item.keys()})
        return list_accumulator

    def first(self, query):
        result = self.select(query)
        return result[0] if result else None

    def get_doc_by_id(self, identifier):
        query = f"select * from documents where id = {identifier}"
        return self.first(query)

    def save_url(self, url: str):
        query = 'insert into documents(link) values (?)'
        return self.execute(query, (url,))

    def save_term(self, params: tuple):
        query = 'insert into terms(term, doc_id, tf) values (?, ?, ?)'
        return self.execute(query, params)

    def url_exists(self, url):
        query = f"select id from documents where link = '{url}'"
        return self.first(query) is not None

    @classmethod
    def execute(cls, query, param):
        con = cls.get_connection()
        cursor = con.cursor()
        cursor.execute(query, param)
        con.commit()
        return cursor.lastrowid


sqlite = Connection()

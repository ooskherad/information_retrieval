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

    @classmethod
    def execute(cls, query, param):
        con = cls.get_connection()
        cursor = con.cursor()
        cursor.execute(query, param)
        con.commit()
        return cursor.lastrowid


sqlite = Connection()

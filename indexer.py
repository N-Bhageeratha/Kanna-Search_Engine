import sqlite3
import re
from collections import defaultdict

def create_tables(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY, url TEXT, content TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS inverted_index (term TEXT, doc_id INTEGER)''')
    conn.commit()

def index_documents(conn, documents):
    c = conn.cursor()
    for doc in documents:
        c.execute('INSERT INTO documents (url, content) VALUES (?, ?)', (doc['url'], doc['text']))
        doc_id = c.lastrowid
        terms = set(re.findall(r'\w+', doc['text'].lower()))
        for term in terms:
            c.execute('INSERT INTO inverted_index (term, doc_id) VALUES (?, ?)', (term, doc_id))
    conn.commit()

if __name__ == "__main__":
    conn = sqlite3.connect('search.db')
    create_tables(conn)
    # Example: index_documents(conn, [{'url': 'http://example.com', 'text': 'Example text'}])
    conn.close()

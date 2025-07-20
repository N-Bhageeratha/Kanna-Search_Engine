import sqlite3
import math
from collections import Counter

def boolean_search(conn, query):
    terms = query.lower().split()
    c = conn.cursor()
    doc_sets = []
    for term in terms:
        c.execute('SELECT doc_id FROM inverted_index WHERE term=?', (term,))
        doc_sets.append(set(row[0] for row in c.fetchall()))
    if not doc_sets:
        return []
    result_ids = set.intersection(*doc_sets)
    c.execute('SELECT id, url FROM documents WHERE id IN (%s)' % ','.join('?'*len(result_ids)), tuple(result_ids))
    return c.fetchall()

def tfidf_search(conn, query):
    terms = query.lower().split()
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM documents')
    N = c.fetchone()[0]
    scores = Counter()
    for term in terms:
        c.execute('SELECT doc_id FROM inverted_index WHERE term=?', (term,))
        doc_ids = [row[0] for row in c.fetchall()]
        df = len(set(doc_ids))
        if df == 0:
            continue
        idf = math.log(N / (1 + df))
        for doc_id in doc_ids:
            c.execute('SELECT content FROM documents WHERE id=?', (doc_id,))
            text = c.fetchone()[0]
            tf = text.lower().split().count(term)
            scores[doc_id] += tf * idf
    ranked = scores.most_common()
    results = []
    for doc_id, score in ranked:
        c.execute('SELECT url FROM documents WHERE id=?', (doc_id,))
        url = c.fetchone()[0]
        results.append((url, score))
    return results

if __name__ == "__main__":
    conn = sqlite3.connect('search.db')
    q = input("Enter search query: ")
    print("Boolean Search Results:")
    print(boolean_search(conn, q))
    print("TF-IDF Search Results:")
    print(tfidf_search(conn, q))
    conn.close()

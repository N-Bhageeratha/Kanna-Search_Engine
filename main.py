from crawler import crawl
from indexer import create_tables, index_documents
import sqlite3
import os

def main():
    seeds = input("Enter seed URLs (comma or space separated): ")
    url_list = [u.strip() for u in seeds.replace(',', ' ').split() if u.strip()]
    for i, url in enumerate(url_list):
        if not url.startswith(('http://', 'https://')):
            url_list[i] = 'https://' + url
    print("Crawling...")
    pages = crawl(url_list)
    print(f"Crawled {len(pages)} pages. Indexing...")
    conn = sqlite3.connect('search.db')
    create_tables(conn)
    index_documents(conn, pages)
    conn.close()
    print("Indexing complete. Run search.py to query.")

if __name__ == "__main__":
    main()

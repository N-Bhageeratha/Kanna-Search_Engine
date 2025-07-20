import requests
from bs4 import BeautifulSoup

def crawl(urls, max_pages=10):
    if isinstance(urls, str):
        urls = [urls]
    all_pages = []
    for url in urls:
        visited = set()
        to_visit = [url]
        pages = []
        while to_visit and len(pages) < max_pages:
            current = to_visit.pop(0)
            if current in visited:
                continue
            try:
                resp = requests.get(current, timeout=5)
                soup = BeautifulSoup(resp.text, 'html.parser')
                text = soup.get_text()
                pages.append({'url': current, 'text': text})
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if href.startswith('http') and href not in visited:
                        to_visit.append(href)
            except Exception as e:
                print(f"Failed to crawl {current}: {e}")
            visited.add(current)
        all_pages.extend(pages)
    return all_pages

if __name__ == "__main__":
    seeds = input("Enter seed URLs (comma or space separated): ")
    url_list = [u.strip() for u in seeds.replace(',', ' ').split() if u.strip()]
    for i, url in enumerate(url_list):
        if not url.startswith(('http://', 'https://')):
            url_list[i] = 'https://' + url
    crawled = crawl(url_list)
    for page in crawled:
        print(page['url'])

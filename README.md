
![Kanna Search Engine Screenshot](assets/screenshot.png)

# Kanna Search Engine

A Google-like search engine built with Python. It crawls, indexes, and searches multiple websites using a simple web interface.

---

## Features
- 🚀 Crawl and index multiple websites at once
- 🗄️ Store and search content using SQLite
- 🔍 Boolean and TF-IDF search ranking
- 🌐 Google-style web interface (Flask + HTML/CSS)

---

## Requirements
- Python 3.7+
- `pip install -r requirements.txt`

---

## Installation
1. Clone or download this repository.
2. Open a terminal in the project folder.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

---

## Usage
### 1. Crawl and Index Websites
Run the crawler and indexer:
```
& ".venv/Scripts/python.exe" main.py
```
When prompted, enter one or more URLs (comma or space separated), e.g.:
```
example.com, wikipedia.org, python.org
```
The crawler will fetch and index pages from all provided sites.

### 2. Start the Web Search Interface
Run:
```
& ".venv/Scripts/python.exe" app.py
```
Then open [http://127.0.0.1:5000/](http://127.0.0.1:5000/) in your browser. Enter a search query to see results from your indexed sites.

---

## Project Structure
| File/Folder         | Purpose                                 |
|---------------------|-----------------------------------------|
| `main.py`           | Entry point for crawling and indexing    |
| `crawler.py`        | Web crawler for extracting content       |
| `indexer.py`        | Builds and stores the inverted index     |
| `search.py`         | Boolean and TF-IDF search logic          |
| `app.py`            | Flask web server for the search UI       |
| `templates/`        | HTML templates for the web interface     |
| `requirements.txt`  | Python dependencies                      |

---

## Customization
- Edit `main.py` or `crawler.py` to change crawl depth or filtering.
- Edit `templates/index.html` and `templates/results.html` to change the UI.

---

## Notes
- ⚠️ Crawling is limited by the number of pages per site (default: 10 per site, can be changed in `crawler.py`).
- 🚫 Some sites may block crawlers or limit access.
- 📚 This project is for educational/demo use and not intended for large-scale or commercial deployment.

---

## License
MIT License

---

> _Made with Python, Flask, and a love for search!_

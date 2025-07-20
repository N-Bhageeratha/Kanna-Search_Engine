

from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from search import boolean_search, tfidf_search
import re

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Change this in production

ADMIN_USER = 'admin'
ADMIN_PASS = 'admin123'  # Change this in production

def get_db():
    conn = sqlite3.connect('search.db')
    conn.row_factory = sqlite3.Row
    return conn

def is_math_expression(query):
    # Only allow numbers, operators, parentheses, decimal points, and spaces
    return bool(re.fullmatch(r'[\d\s\+\-\*/\(\)\.]+', query))

def safe_eval(expr):
    # Only allow math expressions, no builtins or names
    try:
        return eval(expr, {"__builtins__": None}, {})
    except Exception:
        return None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    results = []
    calc_result = None
    calc_error = None
    if query:
        stripped_query = query.replace(' ', '')
        # Fuzzy match for calculator-related keywords
        calc_keywords = ['calculator', 'calculater', 'calc', 'calclator', 'calulator', 'calcutor', 'caluclator', 'calclater', 'cal', 'math', 'maths', 'mathematics']
        from difflib import get_close_matches
        show_calc_ui = False
        # If the query is a math expression or looks like a math attempt
        if is_math_expression(stripped_query):
            calc_result = safe_eval(stripped_query)
            show_calc_ui = True
            if calc_result is None:
                calc_error = 'Invalid expression'
        elif any(op in stripped_query for op in '+-*/'):
            calc_error = 'Invalid expression'
            show_calc_ui = True
        # If the query is a calculator-related word (even with typo)
        elif get_close_matches(query.lower(), calc_keywords, n=1, cutoff=0.7):
            show_calc_ui = True
        conn = get_db()
        tfidf_results = tfidf_search(conn, query)
        results = [{'url': url, 'score': score} for url, score in tfidf_results]
        conn.close()
    else:
        show_calc_ui = False
    return render_template('results.html', query=query, results=results, calc_result=calc_result, calc_error=calc_error, show_calc_ui=show_calc_ui)

# Admin login
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            error = 'Invalid credentials.'
    return render_template('login.html', error=error)

# Admin dashboard
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    conn = get_db()
    docs = conn.execute('SELECT id, url FROM documents').fetchall()
    conn.close()
    return render_template('admin.html', docs=docs)

# Admin logout
@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

# Admin delete document
@app.route('/admin/delete', methods=['POST'])
def admin_delete():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    doc_id = request.form['id']
    conn = get_db()
    conn.execute('DELETE FROM documents WHERE id=?', (doc_id,))
    conn.execute('DELETE FROM inverted_index WHERE doc_id=?', (doc_id,))
    conn.commit()
    conn.close()
    return redirect(url_for('admin_dashboard'))

# Admin crawl new URLs
@app.route('/admin/crawl', methods=['POST'])
def admin_crawl():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    urls = request.form['urls']
    url_list = [u.strip() for u in urls.replace(',', ' ').split() if u.strip()]
    for i, url in enumerate(url_list):
        if not url.startswith(('http://', 'https://')):
            url_list[i] = 'https://' + url
    from crawler import crawl
    from indexer import index_documents
    pages = crawl(url_list)
    conn = get_db()
    index_documents(conn, pages)
    conn.close()
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, jsonify, render_template, request, abort
import json
from query import preliminary_search

app = Flask(__name__)
with open("inverted_index_pos.json", "r") as f:
    INDEX = json.load(f)
with open("forward_index.json", "r", encoding="utf-8") as f:
    DOCS = json.load(f)
DOCS_BY_ID = {str(d["id"]): d for d in DOCS}

@app.get("/doc/<doc_id>")
def doc_page(doc_id):
    doc = DOCS_BY_ID.get(str(doc_id))
    if not doc:
        abort(404)
    return render_template("doc.jinja", doc=doc)

@app.get("/")
def home():
    return render_template("index.jinja", query="", results=[])

@app.get("/search")
def search():
    q = request.args.get("q", "")
    method = request.args.get("method", "tfidf")
    ranked = preliminary_search(q, method)
    results = []
    for doc_id, score in ranked:
        doc = DOCS_BY_ID.get(str(doc_id))
        if not doc:
            continue
        results.append({
            "id": str(doc_id),
            "score": score,
            "title": doc["title"],
            "text": doc["text"],
        })
    return render_template("index.jinja", query=q, results=results)

if __name__ == '__main__':
  app.run(host='0.0.0.0', debug=True)
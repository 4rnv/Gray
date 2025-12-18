from flask import Flask, jsonify, render_template, request, abort
from sklearn.metrics.pairwise import cosine_similarity
import json
import pandas as pd
from query import preliminary_search

app = Flask(__name__)
with open("inverted_index_pos.json", "r") as f:
    INDEX = json.load(f)

with open("wikipedia_clean.json", "r", encoding="utf-8") as f:
    DOCS = json.load(f)

FORWARD_INDEX = {str(d["id"]): d for d in DOCS}

DOC_TOPICS = pd.read_csv( "doc_topic_matrix.csv", index_col="document_id" )
DOC_TOPICS.drop(columns=['dominant_topic'], inplace=True)

def similar_docs(doc_id, top_k=5):
    if doc_id not in DOC_TOPICS.index:
        return []
    target_vec = DOC_TOPICS.loc[[doc_id]].values
    sims = cosine_similarity(target_vec, DOC_TOPICS.values)[0]
    sim_scores = list(zip(DOC_TOPICS.index, sims))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    results = []
    for sim_doc_id, score in sim_scores[1:top_k+1]:
        doc = FORWARD_INDEX.get(str(sim_doc_id))
        if not doc:
            continue
        results.append({
            "id": sim_doc_id,
            "title": doc["title"],
            "score": float(score)
        })
    return results

@app.get("/doc/<doc_id>")
def doc_page(doc_id):
    doc = FORWARD_INDEX.get(str(doc_id))
    if not doc:
        abort(404)
    similar = similar_docs(int(doc_id))
    return render_template("doc.jinja", doc=doc, similar=similar)

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
        doc = FORWARD_INDEX.get(str(doc_id))
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
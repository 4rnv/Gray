from cosine import similarity
from tfidf import tf, idf

def ranking(results : list, index : dict, query_terms : list, method: str):
    all_docs = set()
    docs_wordcounts = {}
    for term in index:
        for posting in index[term]:
            all_docs.add(posting[0])
            doc_id = posting[0]
            term_count = len(posting[1])
            docs_wordcounts[doc_id] = docs_wordcounts.get(doc_id, 0) + term_count
    n_docs = len(all_docs)
    print("N Docs: ", n_docs)
    doc_scores = []
    for doc_id in results:
        score = 0.0
        if method.lower().strip()=='tf-idf' or method.lower().strip()=='tfidf':
            for term in query_terms:
                if term in index:
                    idf_score = idf(term, index, n_docs)
                    score += tf(term, doc_id, index, docs_wordcounts[doc_id]) * idf_score # A better way to do this rather than just adding the scores of query terms, averaging maybe
        elif method.lower().strip()=='cosine':
            score = similarity(doc_id, query_terms, index, n_docs, docs_wordcounts[doc_id])
        doc_scores.append((doc_id, score))
    doc_scores.sort(key=lambda x: x[1], reverse=True)
    print("\nRanked Results:")
    for doc_id, score in doc_scores:
        print(f"Document {doc_id}: Score = {score:.4f}")
    return doc_scores

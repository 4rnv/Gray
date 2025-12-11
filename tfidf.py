import math

def ranking(results : list, index : dict, query_terms : list):
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
        score = 0
        for term in query_terms:
            if term in index:
                idf_score = idf(term, index, n_docs)
                score += tf(term, doc_id, index, docs_wordcounts) * idf_score
        doc_scores.append((doc_id, score))
    doc_scores.sort(key=lambda x: x[1], reverse=True)
    print("\nRanked Results:")
    for doc_id, score in doc_scores:
        print(f"Document {doc_id}: Score = {score:.4f}")
    return doc_scores

def tf(term : str, doc_id : int, index : dict, docs_wordcounts : dict):
    for posting in index[term]:
        if posting[0] == doc_id:
            return len(posting[1]) / docs_wordcounts[doc_id]
    return 0

def idf(term : str, index : dict, n_docs : int):
    if term not in index:
        return 0
    n_docs_with_term = len(index[term])
    idf_score = math.log10( n_docs / (1 + n_docs_with_term))
    return idf_score if idf_score > 0 else 0

def tf_idf(term : str, doc_id : int, index : dict, n_docs : int):
    return tf(term, doc_id, index, docs_wordcounts={}) * idf(term, index, n_docs)
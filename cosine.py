import math
from tfidf import tf_idf

def similarity(doc_id : int, query_terms : list, index : dict, n_docs : int, docs_wordcount : int):
    query_vector = {}
    doc_vector = {}
    doc_term_freqs = {}
    for term in query_terms:
        query_vector[term] = 1
        if term in index:
            term_freq = 0
            for posting in index[term]:
                if posting[0] == doc_id:
                    term_freq = len(posting[1])
                    doc_term_freqs[term] = term_freq
                    break
            #doc_vector[term] = doc_term_freqs.get(term, 0) * tf_idf(term, doc_id, index, n_docs, docs_wordcount)
            doc_vector[term] = tf_idf(term, doc_id, index, n_docs, docs_wordcount)
        else:
            doc_vector[term] = 0
    print(doc_id, "DTF", doc_term_freqs)
    print(doc_id, "DV", doc_vector)
    dot_product = sum(query_vector.get(term, 0) * doc_vector.get(term, 0) for term in query_vector)

    query_magnitude = math.sqrt(sum(v**2 for v in query_vector.values()))
    doc_magnitude = math.sqrt(sum(v**2 for v in doc_vector.values()))
    if query_magnitude == 0 or doc_magnitude == 0:
        return 0
    return dot_product / (query_magnitude * doc_magnitude)
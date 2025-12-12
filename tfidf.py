import math

def tf(term : str, doc_id : int, index : dict, docs_wordcount : int):
    for posting in index[term]:
        if posting[0] == doc_id:
            return len(posting[1]) / docs_wordcount
    return 0

def idf(term : str, index : dict, n_docs : int):
    if term not in index:
        return 0
    n_docs_with_term = len(index[term])
    idf_score = math.log10( n_docs / (1 + n_docs_with_term))
    return idf_score if idf_score > 0 else 0

def tf_idf(term : str, doc_id : int, index : dict, n_docs : int, docs_wordcount : int):
    return tf(term, doc_id, index, docs_wordcount=docs_wordcount) * idf(term, index, n_docs)
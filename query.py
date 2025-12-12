import json
import re
import time
import sys
from tfidf import ranking

def getQuery(query_input : str):
    if not query_input or query_input.strip()=="":
        query = input("Enter query: ").lower().strip()
    else:
        query = query_input
    if not query:
        return None, False
    pattern = r'^[\'\"].*[\'\"]$'
    is_phrase_query = bool(re.match(pattern, query))
    if is_phrase_query:
        query = query[1:-1].strip()
    query_list = query.split()
    if len(query_list)>1:
        return query_list, is_phrase_query
    if len(query_list)==1:
        return query_list[0], False
    return None, False

if __name__=='__main__':
    with open('inverted_index_pos.json', 'r') as f:
        index : dict = json.load(f)
    if len(sys.argv) > 1:
        query_input = sys.argv[1]
    else:
        query_input = ""
    result_docs = []
    query_parsed, is_phrase_query = getQuery(query_input)
    if type(query_parsed)==str:
        try:
            result_docs = [posting[0] for posting in index[query_parsed]]
        except:
            result_docs = []
    elif type(query_parsed)==list and not is_phrase_query:
        docs = set()
        for query in query_parsed:
            try:
                term_docs = [posting[0] for posting in index[query]]
                print(f"query: {query} {len(term_docs)}", term_docs)
                docs |= set(term_docs)
            except:
                pass
        result_docs=list(docs)
    elif type(query_parsed)==list and is_phrase_query:
        docs = set()
        docs_set = []
        for query in query_parsed:
            try:
                if query not in index:
                    print(f"No results for {query}")
                    break
                term_docs = set(posting[0] for posting in index[query])
                print(f"query: {query} {len(term_docs)}", term_docs)
                docs_set.append(term_docs)
                common_values = set.intersection(*docs_set)
                docs = set(common_values)
            except:
                pass
        result_docs=list(docs)
        result_docs_copy = result_docs
        result_docs = []
        for doc in result_docs_copy:
            positions_lists = []
            for term_idx, term in enumerate(query_parsed):
                for posting in index[term]:
                    if posting[0] == doc:
                        positions_lists.append(posting[1])
                        break
            adjusted_positions = []
            for i, positions in enumerate(positions_lists):
                adjusted = [pos - i for pos in positions]
                adjusted_positions.append(set(adjusted))
            common_positions = set.intersection(*adjusted_positions)
            if common_positions:
                result_docs.append(doc)

        print(docs_set)
    if len(result_docs)==0:
        print(f"No results for {query_parsed}")
    else:
        print(f"Length: {len(result_docs)}", result_docs)
    if type(query_parsed)==str:
        query_terms = [query_parsed]
    elif type(query_parsed)==list:
        query_terms = query_parsed
    start = time.time()
    ranks = ranking(result_docs, index, query_terms)
    end = time.time()
    print("Ranking time : ", end - start)
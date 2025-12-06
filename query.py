import json
import re

def getQuery():
    query = input("Enter query: ").lower().strip()
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

with open('inverted_index_pos.json', 'r') as f:
    index = json.load(f)

query_parsed, is_phrase_query = getQuery()
if type(query_parsed)==str:
    try:
        docs = [posting[0] for posting in index[query_parsed]]
    except:
        docs = []
elif type(query_parsed)==list and not is_phrase_query:
    docs = set()
    for query in query_parsed:
        try:
            term_docs = [posting[0] for posting in index[query]]
            print(f"query: {query} {len(term_docs)}", term_docs)
            docs |= set(term_docs)
        except:
            pass
    docs=list(docs)
elif type(query_parsed)==list and is_phrase_query:
    docs = set()
    docs2 = []
    for query in query_parsed:
        try:
            term_docs = set(posting[0] for posting in index[query])
            print(f"query: {query} {len(term_docs)}", term_docs)
            docs2.append(term_docs)
            common_values = set.intersection(*docs2)
            docs |= set(common_values)
        except:
            pass
    docs=list(docs)
print(docs2)
if len(docs)==0:
    print(f"No results for {query_parsed}")
else:
    print(f"Length: {len(docs)}", docs)
import json

def getQuery():
    query = input("Enter query: ").lower().strip()
    query_list = query.split()
    if len(query_list)>1:
        return query_list
    if len(query_list)==1:
        return query_list[0]

with open('inverted_index_pos.json', 'r') as f:
    index = json.load(f)

query_parsed = getQuery()
if type(query_parsed)==str:
    try:
        docs= [posting[0] for posting in index[query_parsed]]
    except:
        docs = []
elif type(query_parsed)==list:
    docs=set()
    for query in query_parsed:
        try:
            term_docs= [posting[0] for posting in index[query]]
            docs |= set(term_docs)
        except:
            pass
    docs=list(docs)

if len(docs)==0:
    print(f"No results for {query_parsed}")
else:
    print(docs)
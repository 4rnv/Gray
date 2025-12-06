import json
import re
from collections import defaultdict

with open("wikipedia_tokenized.json", mode="r", encoding="utf-8") as f:
    forward_index = json.load(f)
inverted_index = {}

inverted = defaultdict(lambda: defaultdict(list))
for document in forward_index:
    doc_id = document["id"]
    for pos, token in enumerate(document["tokens"]):
        inverted[token][doc_id].append(pos)

inverted_index = {
    term: [[doc_id, positions] for doc_id, positions in docs.items()]
    for term, docs in inverted.items()
}
with open("inverted_index_pos.json", mode="w", encoding="utf-8") as f:
    json.dump(inverted_index, f, ensure_ascii=False, indent=2)
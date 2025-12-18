import json
import re

with open("wikipediajsonrandom.json", mode="r", encoding="utf-8") as f:
    raw = json.load(f)
stop_words = ["i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you", "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself", "she", "her", "hers", "herself", "it", "its", "itself", "they", "them", "their", "theirs", "themselves", "what", "which", "who", "whom", "this", "that", "these", "those", "am", "is", "are", "was", "were", "be", "been", "being", "have", "has", "had", "having", "do", "does", "did", "doing", "a", "an", "the", "and", "but", "if", "or", "because", "as", "until", "while", "of", "at", "by", "for", "with", "about", "against", "between", "into", "through", "during", "before", "after", "above", "below", "to", "from", "up", "down", "in", "out", "on", "off", "over", "under", "again", "further", "then", "once", "here", "there", "when", "where", "why", "how", "all", "any", "both", "each", "few", "more", "most", "other", "some", "such", "only", "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "just", "don", "should", "now"]

markup_tags = ["bgcolor", "rowspan", "colspan", "category", "font-size", "align", "style", "width", "class", "dfffdf", "colspan", "bgcolor", "color", "wikitable", "e0e0e0", "row", "col", "959ffd", "00fe95", "valign", "font", "size", "efcfff", "cfcfff", "dfdfdf", "ffffbf"]

tokenized_data = []
forward_index = []
counter = 0
for i in raw:
    title = str(i["title"]).lower()
    text = str(i["text"]).lower()
    combined_text = f"{title} {text}"
    tokens = re.findall(r'\b[a-z]+\b', combined_text)
    tokens = [token for token in tokens if token not in stop_words and token not in markup_tags]
    #stemmed_tokens = [stemmer.stem(token) for token in tokens]
    stemmed_tokens = tokens
    counter += 1
    tokenized_data.append({
        "id" : counter,
        "title": title,
        "tokens": stemmed_tokens
    })
    forward_index.append({"id": counter, "title": i["title"], "text": i["text"]})

with open("wikipedia_clean.json", mode="w", encoding="utf-8") as f:
    json.dump(raw, f)

with open("forward_index.json", "w", encoding="utf-8") as f:
    json.dump(forward_index, f, ensure_ascii=False)

with open("wikipedia_tokenized.json", mode="w", encoding="utf-8") as f:
    json.dump(tokenized_data, f, ensure_ascii=False, indent=2)
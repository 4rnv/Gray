import json
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer

with open('wikipedia_tokenized.json', 'r', encoding='utf-8') as f:
    docs : dict = json.load(f)

docs_as_strings = [" ".join(doc['tokens']) for doc in docs]

vectorizer = CountVectorizer()
dtm = vectorizer.fit_transform(docs_as_strings)
lda_model=LatentDirichletAllocation(n_components=20,learning_method='online',random_state=83,max_iter=4)
lda_top=lda_model.fit_transform(dtm)

def print_top_words(model, feature_names, n_top_words=20):
    for topic_idx, topic in enumerate(model.components_):
        message = f"Topic #{topic_idx+1}: "
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)

tf_feature_names = vectorizer.get_feature_names_out()
print_top_words(lda_model, tf_feature_names)

doc_ids = [doc['id'] for doc in docs]
doc_topic_df = pd.DataFrame(lda_top, columns=[f"Topic_{i}" for i in range(1,21)], index=doc_ids)

doc_topic_df.index.name = 'document_id'
print(doc_topic_df.iloc[0]) 

doc_topic_df['dominant_topic'] = doc_topic_df.idxmax(axis=1)
doc_topic_df.to_csv('doc_topic_matrix.csv', index=True)
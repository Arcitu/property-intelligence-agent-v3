# app/vector_store.py
# Lightweight local "vector store" using TF-IDF for semantic-ish search across planning documents.
import os, pickle
from sklearn.feature_extraction.text import TfidfVectorizer

STORE_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'vector_store')
VECT_PICKLE = os.path.join(STORE_DIR, 'vectorizer.pkl')
DOCS_PICKLE = os.path.join(STORE_DIR, 'docs.pkl')

os.makedirs(STORE_DIR, exist_ok=True)

def build_index(docs: dict):
    """docs: dict of {doc_name: text}
    Stores vectorizer and doc list to disk."""
    texts = [t for t in docs.values()]
    names = [n for n in docs.keys()]
    if not texts:
        return False
    vect = TfidfVectorizer(stop_words='english', max_features=2000)
    X = vect.fit_transform(texts)
    with open(VECT_PICKLE, 'wb') as f:
        pickle.dump({'vectorizer': vect, 'X': X}, f)
    with open(DOCS_PICKLE, 'wb') as f:
        pickle.dump({'names': names, 'texts': texts}, f)
    return True

def semantic_search(query: str, top_k=3):
    """Return top_k doc names and snippets matching the query."""
    if not os.path.exists(VECT_PICKLE) or not os.path.exists(DOCS_PICKLE):
        return []
    with open(VECT_PICKLE, 'rb') as f:
        data = pickle.load(f)
    vect = data['vectorizer']; X = data['X']
    with open(DOCS_PICKLE, 'rb') as f:
        docs = pickle.load(f)
    qv = vect.transform([query])
    import numpy as np
    scores = (X @ qv.T).toarray().ravel()
    idx = scores.argsort()[::-1][:top_k]
    results = []
    for i in idx:
        results.append({'doc': docs['names'][i], 'score': float(scores[i]), 'snippet': docs['texts'][i][:800]})
    return results

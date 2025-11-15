# app/docs_loader.py
import os
from pathlib import Path
try:
    from PyPDF2 import PdfReader
except:
    PdfReader = None
from .vector_store import build_index, semantic_search

PDF_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'palo_alto_pdfs')

def _extract_text(pdf_path):
    if PdfReader is None:
        return ''
    try:
        reader = PdfReader(pdf_path)
        texts = []
        for p in reader.pages:
            texts.append(p.extract_text() or '')
        return '\n'.join(texts)
    except Exception as e:
        print('PDF read error', e)
        return ''

def index_documents():
    docs = {}
    if os.path.exists(PDF_DIR):
        for fname in Path(PDF_DIR).glob('*.pdf'):
            docs[fname.name] = _extract_text(str(fname))
    if docs:
        build_index(docs)
    return docs

# index at import time (lightweight)
INDEX = index_documents()

def search_docs(query):
    # First run a simple substring search
    q = query.lower()
    hits = []
    for name, text in INDEX.items():
        if not text:
            continue
        if q in text.lower():
            snippet = text.lower().split(q,1)[0][-300:] + q + text.lower().split(q,1)[1][:300]
            hits.append({'doc': name, 'snippet': snippet[:1000]})
    # If no substring hits, run semantic search via vector store
    if not hits:
        hits = semantic_search(query, top_k=3)
    # if still no hits, return top doc list
    if not hits:
        hits = [{'doc': name, 'snippet': (text[:500] if text else '')} for name, text in INDEX.items()]
    return hits

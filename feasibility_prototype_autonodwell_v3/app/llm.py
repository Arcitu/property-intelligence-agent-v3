# app/llm.py
import os, json, hashlib
OPENAI_KEY = os.getenv('OPENAI_API_KEY')  # <-- place your OpenAI key in environment to enable real LLM calls
CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', 'cache')
os.makedirs(CACHE_DIR, exist_ok=True)

def _cache_get(key):
    p = os.path.join(CACHE_DIR, key + '.json')
    if os.path.exists(p):
        with open(p, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def _cache_set(key, val):
    p = os.path.join(CACHE_DIR, key + '.json')
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(val, f, indent=2)

def _make_cache_key(*args):
    s = json.dumps(args, sort_keys=True, default=str)
    return hashlib.sha1(s.encode('utf-8')).hexdigest()

def summarize_feasibility(parcel, det, doc_hits):
    key = _make_cache_key(parcel.get('apn',''), det.get('feasibility',''), [d.get('doc') for d in doc_hits])
    cached = _cache_get(key)
    if cached:
        return cached.get('summary')
    # If OPENAI_API_KEY is set, you can implement a real call here. For demo we return a concise stub.
    if OPENAI_KEY:
        out = "[LLM] (OPENAI_API_KEY set) - summary placeholder. Replace with real call in production."
    else:
        out = (f"Parcel {parcel.get('address','(unknown)')} (zoning {parcel.get('zoning','unknown')}) - "
               f"Deterministic feasibility: {det.get('feasibility')}. Allowed units (estimate): {det.get('allowed_units_estimate')}. "
               "Documents consulted: " + ", ".join([d.get('doc') for d in doc_hits]) + ".")
    _cache_set(key, {'summary': out})
    return out

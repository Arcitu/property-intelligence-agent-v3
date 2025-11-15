Autonodwell Prototype v3
------------------------
This package includes:
 - ArcGIS connector + seeded county services
 - Field mapping normalization across county schemas
 - Local lightweight vector store (TF-IDF) for semantic search of planning PDFs
 - PDF report generator endpoint (/report_pdf)
 - LLM integration point: set OPENAI_API_KEY environment variable to enable real LLM calls in app/llm.py

Quickstart (Windows):
1. Extract ZIP to C:\Some\Path\autonodwell_v3
2. cd to the folder in CMD
3. python -m venv venv
4. venv\Scripts\activate
5. pip install -r requirements.txt
6. (optional) place planning PDFs in data/palo_alto_pdfs/
7. start_demo.bat to launch backend + UI OR run manually:
   python -m uvicorn app.main:app --reload --port 8000
   streamlit run ui/streamlit_app.py --server.port 8501

Where to add OpenAI key:
 - In Windows CMD: set OPENAI_API_KEY=sk-...
 - Or add to your system environment variables for persistence.

Notes:
 - The TF-IDF vector store is a simple local substitute for semantic search. For production, replace with Pinecone or Weaviate.
 - County service endpoints are seeded but may need validation per-county. Use scripts/find_arcgis_service.py to discover.

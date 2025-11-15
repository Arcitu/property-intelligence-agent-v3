from fastapi import FastAPI, Response
from pydantic import BaseModel
from .geocode import geocode_address
from .county_mapper import find_service_for_county
from .arcgis_query import query_feature_by_point
from .field_mapping import map_attributes_to_canonical
from .zoning_rules import analyze_parcel
from .docs_loader import search_docs, index_documents
from .llm import summarize_feasibility
from .report_generator import generate_pdf_report

app = FastAPI(title='Autonodwell Feasibility API (v3)')

class AddressQuery(BaseModel):
    address: str

@app.get('/health')
def health():
    return {'status':'ok'}

@app.post('/analyze_address')
def analyze_address(payload: AddressQuery):
    address = payload.address
    geo = geocode_address(address)
    if not geo:
        return {'error':'Failed to geocode address', 'address': address}
    county = None
    display = geo.get('display_name','').lower()
    for part in display.split(','):
        if 'county' in part:
            county = part.replace('county','').strip().title()
            break
    if not county:
        county = 'San Mateo'
    svc = find_service_for_county(county)
    parcel = None
    if svc and 'feature_service_url' in svc:
        attrs = query_feature_by_point(svc['feature_service_url'], geo['lon'], geo['lat'], out_fields=svc.get('out_fields','*'))
        if attrs:
            parcel = map_attributes_to_canonical(attrs)
            if not parcel.get('address'):
                parcel['address'] = address
    if not parcel:
        parcel = {'apn':'UNKNOWN','address':address,'zoning':'UNKNOWN','lot_width':0,'lot_depth':0}
    det = analyze_parcel(parcel)
    index_documents()
    doc_hits = search_docs(address)
    summary = summarize_feasibility(parcel, det, doc_hits)
    report = {
        'query_address': address,
        'geocode': geo,
        'county': county,
        'service_used': svc if svc else None,
        'parcel': parcel,
        'deterministic': det,
        'document_matches': doc_hits,
        'llm_summary': summary
    }
    return report

@app.post('/report_pdf')
def report_pdf(payload: AddressQuery):
    report = analyze_address(payload)
    if 'error' in report:
        return report
    pdf_bytes = generate_pdf_report(report)
    return Response(content=pdf_bytes, media_type='application/pdf')

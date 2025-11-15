# app/report_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from datetime import datetime

def generate_pdf_report(report: dict) -> bytes:
    """Return PDF bytes for the given report dict."""
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont('Helvetica-Bold', 16)
    c.drawString(72, y, 'Autonodwell Feasibility Report')
    y -= 30
    c.setFont('Helvetica', 10)
    c.drawString(72, y, f"Address: {report.get('query_address','')}")
    y -= 14
    g = report.get('geocode', {})
    c.drawString(72, y, f"Geocode: {g.get('lat','')} , {g.get('lon','')}   County: {report.get('county','')}")
    y -= 20
    # Parcel
    p = report.get('parcel', {})
    c.setFont('Helvetica-Bold', 12); c.drawString(72, y, 'Parcel Summary'); y -= 16
    c.setFont('Helvetica', 10)
    for k in ['apn','address','zoning','lot_width','lot_depth','last_assessed_value']:
        c.drawString(80, y, f"{k}: {p.get(k,'')}"); y -= 12
    y -= 8
    # Deterministic
    d = report.get('deterministic', {})
    c.setFont('Helvetica-Bold', 12); c.drawString(72, y, 'Deterministic Checks'); y -= 16
    c.setFont('Helvetica', 10)
    for kk,vv in d.items():
        c.drawString(80, y, f"{kk}: {vv}"); y -= 12
        if y < 80:
            c.showPage(); y = height - 50
    y -= 6
    # LLM summary
    c.setFont('Helvetica-Bold', 12); c.drawString(72, y, 'Summary & Recommendations'); y -= 16
    c.setFont('Helvetica', 10)
    summary = report.get('llm_summary', '')
    from reportlab.lib.utils import simpleSplit
    lines = simpleSplit(summary, 'Helvetica', 10, width-150)
    for line in lines:
        c.drawString(80, y, line); y -= 12
        if y < 80:
            c.showPage(); y = height - 50
    # footer
    c.setFont('Helvetica-Oblique', 8)
    c.drawString(72, 40, f"Generated: {datetime.utcnow().isoformat()} UTC")
    c.save()
    buf.seek(0)
    return buf.getvalue()

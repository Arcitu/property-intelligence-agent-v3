import requests, time
NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
def geocode_address(address):
    params = {"q": address, "format": "json", "addressdetails": 1, "limit": 1}
    try:
        resp = requests.get(NOMINATIM_URL, params=params, headers={"User-Agent":"AutonodwellDemo/1.0"}, timeout=10)
        if resp.status_code == 200 and resp.json():
            d = resp.json()[0]
            return {"lat": float(d["lat"]), "lon": float(d["lon"]), "display_name": d.get("display_name",""), "raw": d}
    except Exception as e:
        print("Geocode error", e)
    time.sleep(1)
    return None

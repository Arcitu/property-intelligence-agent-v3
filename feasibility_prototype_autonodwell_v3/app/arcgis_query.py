import requests

def query_feature_by_point(feature_service_url, lon, lat, out_fields="*"):
    base = feature_service_url.rstrip("/") + "/query"
    params = {
        "geometry": f"{lon},{lat}",
        "geometryType": "esriGeometryPoint",
        "inSR": "4326",
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": out_fields,
        "f": "pjson",
        "returnGeometry": "false"
    }
    try:
        resp = requests.get(base, params=params, timeout=15)
        resp.raise_for_status()
        j = resp.json()
    except Exception as e:
        print(f"ArcGIS query error: {e}")
        return None
    features = j.get("features", [])
    if not features:
        return None
    return features[0].get("attributes", {})

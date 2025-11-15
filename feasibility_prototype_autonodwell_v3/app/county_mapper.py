import json, os
BASE = os.path.join(os.path.dirname(__file__), '..', 'data', 'county_services.json')

def load_services():
    if not os.path.exists(BASE):
        return {}
    with open(BASE, 'r', encoding='utf-8') as f:
        return json.load(f)

def find_service_for_county(county_name):
    services = load_services()
    return services.get(county_name)

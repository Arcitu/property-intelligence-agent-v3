# scripts/find_arcgis_service.py
import sys, requests
def search_arcgis(query, max_items=5):
    params = {'q': query + ' parcels', 'num': max_items, 'f':'json'}
    resp = requests.get('https://www.arcgis.com/sharing/rest/search', params=params, timeout=15)
    resp.raise_for_status()
    j = resp.json()
    results = []
    for itm in j.get('results', []):
        results.append({'title': itm.get('title'), 'url': itm.get('url'), 'id': itm.get('id'), 'type': itm.get('type')})
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python scripts/find_arcgis_service.py "County Name"')
        sys.exit(1)
    county = sys.argv[1]
    items = search_arcgis(county)
    for i in items:
        print(i)

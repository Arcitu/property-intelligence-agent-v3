def analyze_parcel(parcel):
    zone = parcel.get('zoning', 'R1')
    zoning_rules = {
        'R1': {'max_units_per_lot': 1, 'front': 20, 'side': 5, 'rear': 15, 'max_height_ft': 30},
        'R2': {'max_units_per_lot': 2, 'front': 20, 'side': 5, 'rear': 15, 'max_height_ft': 35},
    }
    rules = zoning_rules.get(zone, zoning_rules['R1'])
    lot_width = float(parcel.get('lot_width', 0) or 0)
    lot_depth = float(parcel.get('lot_depth', 0) or 0)
    setbacks_ok = (lot_depth - (rules['front'] + rules['rear']) > 0) and (lot_width - (2 * rules['side']) > 0)
    allowed_units = rules['max_units_per_lot']
    feasibility = 'PASS' if setbacks_ok else 'FAIL'
    reasons = []
    if not setbacks_ok:
        reasons.append('Setbacks not met for typical configuration.')
    return {'zoning_rules': rules, 'setbacks_ok': setbacks_ok, 'allowed_units_estimate': allowed_units, 'feasibility': feasibility, 'reasons': reasons}

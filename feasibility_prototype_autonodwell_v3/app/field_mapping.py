# app/field_mapping.py
# Provides mapping utilities to normalize attributes from different county schemas
from typing import Dict

# define canonical keys we want in our system
CANONICAL_KEYS = ['apn', 'address', 'zoning', 'lot_width', 'lot_depth', 'last_assessed_value']

# common attribute name variants seen across counties/vendors
MAPPING_HINTS = {
    'apn': ['APN','APN_NUM','PARCEL_ID','ParcelID','parcel_id','apn'],
    'address': ['ADDRESS','ADDRESS_FULL','SITUS','SITE_ADDR','address'],
    'zoning': ['ZONE','ZONING','ZONEDIST','zoning'],
    'lot_width': ['LOT_WIDTH','LOT_WIDTH_FEET','LotWidth','lot_width'],
    'lot_depth': ['LOT_DEPTH','LOT_DEPTH_FEET','LotDepth','lot_depth'],
    'last_assessed_value': ['ASSESSED_VALUE','LAND_VALUE','AV_TOTAL','assessedvalue','last_assessed_value']
}

def map_attributes_to_canonical(attrs: Dict) -> Dict:
    """Take raw attributes (dict) and return a normalized dict with canonical keys."""
    out = {}
    for key in CANONICAL_KEYS:
        out[key] = None
        hints = MAPPING_HINTS.get(key, [])
        for h in hints:
            if h in attrs and attrs[h] not in (None, ''):
                out[key] = attrs[h]
                break
        # also check lowercase variants
        if out[key] in (None, ''):
            for k,v in attrs.items():
                if k.lower() in [hh.lower() for hh in hints]:
                    out[key] = v
                    break
    # post-process numeric conversions
    try:
        if out.get('lot_width') is not None:
            out['lot_width'] = float(out['lot_width'])
    except:
        out['lot_width'] = 0.0
    try:
        if out.get('lot_depth') is not None:
            out['lot_depth'] = float(out['lot_depth'])
    except:
        out['lot_depth'] = 0.0
    return out

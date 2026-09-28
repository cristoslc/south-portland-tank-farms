#!/usr/bin/env python3
"""Canonical tank-farm structure loader (shared by all analysis/map scripts).

Inclusion rule (corrected after the Sept 28 arrow audit):
  A mapped OSM structure belongs to the tank-farm fence-line geometry iff
    - it is a storage tank (man_made=storage_tank), OR
    - it is an industrial parcel that CONTAINS at least one mapped storage tank, OR
    - it is tagged industrial=oil, OR
    - it is named for a licensed oil operator (Gulf/Portland Pipe Line).
  Excluded: piers/wharves, buoy yards, shipyards, and bare landuse=industrial
  parcels with NO mapped tanks and no oil tag (Custom House Wharf, Widgery
  Wharf, Buoy Yards, Yard South shipyard, an unnamed pier, and two empty
  industrial parcels). Parcels containing even one mapped tank are kept —
  the tank proves petroleum infrastructure on the parcel. Lone tanks are
  included as tanks. These were incorrectly shaded in earlier map versions.
"""
import json, math, os

FARMS = {
    "global": (43.634665, -70.275381),
    "citgo": (43.637390, -70.267687),
    "buckeye": (43.636551, -70.285118),
    "gulf_sunoco": (43.650445, -70.238583),
    "sprague": (43.637217, -70.286403),
    "pplc": (43.629026, -70.271068),
}
ASSIGN_R = 1200.0  # m from farm anchor

def hav(a, b, c, d):
    R = 6371000.0
    p1, p2 = math.radians(a), math.radians(c)
    x = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))

def ring_contains(ring, lat, lon):
    inside = False; j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i]; xj, yj = ring[j]
        if ((yi > lat) != (yj > lat)) and (lon < (xj-xi)*(lat-yi)/(yj-yi)+xi):
            inside = not inside
        j = i
    return inside

def load(repo_root):
    """Returns (assigned, excluded). assigned: list of dicts with
    id/tags/ring/farm/kind/contains_tanks. excluded: same + 'reason'."""
    osm = json.load(open(os.path.join(repo_root, 'data', 'overpass_tanks.json')))
    raw = []
    for e in osm.get('elements', []):
        g = e.get('geometry')
        if not g:
            continue
        t = e.get('tags', {}) or {}
        ring = [[p['lon'], p['lat']] for p in g]
        clat = sum(p[1] for p in ring)/len(ring)
        clon = sum(p[0] for p in ring)/len(ring)
        fid, d = min(((k, hav(clat, clon, v[0], v[1])) for k, v in FARMS.items()), key=lambda x: x[1])
        if d > ASSIGN_R:
            continue  # too far from any farm anchor to matter
        raw.append({
            'id': e['id'], 'tags': t, 'ring': ring, 'farm': fid,
            'kind': 'tank' if t.get('man_made') == 'storage_tank' else 'parcel',
            'clat': clat, 'clon': clon,
        })
    tanks = [s for s in raw if s['kind'] == 'tank']
    assigned, excluded = [], []
    for s in raw:
        t = s['tags']
        if s['kind'] == 'tank':
            s['contains_tanks'] = 1
            s['keep'] = True
        else:
            n_inside = sum(1 for tk in tanks if ring_contains(s['ring'], tk['clat'], tk['clon']))
            s['contains_tanks'] = n_inside
            oil_tag = t.get('industrial') == 'oil'
            op_name = (t.get('name') or '')
            op_named = ('Gulf Oil' in op_name) or ('Portland Pipe Line' in op_name)
            s['keep'] = bool(n_inside >= 1 or oil_tag or op_named)
        if s['keep']:
            assigned.append(s)
        else:
            if t.get('man_made') == 'pier':
                s['reason'] = 'pier/wharf (no tanks)'
            elif t.get('name') == 'Yard South':
                s['reason'] = 'shipyard (no tanks)'
            elif t.get('name') == 'Buoy Yard':
                s['reason'] = 'buoy yard (no tanks)'
            elif t.get('name') == 'Cape Gas Turbine':
                s['reason'] = 'power-plant parcel (not petroleum storage)'
            else:
                s['reason'] = 'industrial parcel with no mapped tanks or oil tag'
            excluded.append(s)
    return assigned, excluded

if __name__ == '__main__':
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    assigned, excluded = load(root)
    from collections import Counter
    per_farm = Counter(s['farm'] for s in assigned)
    print("assigned structures per farm:", dict(per_farm), "| total", len(assigned))
    print("excluded:")
    for s in excluded:
        print(f"   {s['id']:>10} {s['tags'].get('name') or '(unnamed)':<24} -> {s['reason']}")
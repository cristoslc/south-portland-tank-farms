#!/usr/bin/env python3
"""GIS distance: from each receptor to the nearest tank farm STRUCTURE (OSM
industrial parcel boundary or individual storage tank polygon), per tank farm."""
import json, math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'outputs')

# ---------- geometry helpers ----------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1; dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

def local_xy(lat, lon, lat0, lon0):
    """Approximate planar coords (meters) around reference point."""
    kx = 111320.0 * math.cos(math.radians(lat0))
    ky = 110540.0
    return (lon - lon0) * kx, (lat - lat0) * ky

def pt_to_segment_dist(px, py, ax, ay, bx, by):
    dx, dy = bx-ax, by-ay
    L2 = dx*dx + dy*dy
    if L2 == 0:
        return math.hypot(px-ax, py-ay)
    t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy) / L2))
    return math.hypot(px-(ax+t*dx), py-(ay+t*dy))

def pt_to_ring_dist(lat, lon, ring, lat0, lon0):
    """ring: list of [lon, lat] (overpass geom). Returns meters."""
    px, py = (lon-lon0)*111320.0*math.cos(math.radians(lat0)), (lat-lat0)*110540.0
    best = float('inf')
    # treat as closed ring
    pts = ring + [ring[0]]
    for i in range(len(pts)-1):
        ax, ay = (pts[i][0]-lon0)*111320.0*math.cos(math.radians(lat0)), (pts[i][1]-lat0)*110540.0
        bx, by = (pts[i+1][0]-lon0)*111320.0*math.cos(math.radians(lat0)), (pts[i+1][1]-lat0)*110540.0
        d = pt_to_segment_dist(px, py, ax, ay, bx, by)
        if d < best:
            best = d
    return best

def ring_contains(ring, lat, lon):
    """Ray casting; ring = [[lon,lat],...]; True if point inside."""
    inside = False
    n = len(ring)
    j = n - 1
    for i in range(n):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def ring_centroid(ring):
    xs = [p[0] for p in ring]; ys = [p[1] for p in ring]
    return sum(ys)/len(ys), sum(xs)/len(xs)

# ---------- load OSM structures ----------
d = json.load(open(os.path.join(DATA, 'overpass_tanks.json')))
structures = []
for e in d['elements']:
    t = e.get('tags', {}) or {}
    geom = e.get('geometry')
    if not geom:
        continue
    ring = [[g['lon'], g['lat']] for g in geom]
    kind = 'tank' if t.get('man_made') == 'storage_tank' else 'parcel'
    name = t.get('name') or t.get('operator') or ''
    structures.append({'kind': kind, 'name': name, 'ring': ring})

print(f"OSM structures loaded: {len(structures)} "
      f"({sum(1 for s in structures if s['kind']=='tank')} tanks, "
      f"{sum(1 for s in structures if s['kind']=='parcel')} parcels)")

# ---------- tank farm anchors ----------
TANKS = {
    "Global":      (43.634665, -70.275381),
    "CITGO":       (43.637390, -70.267687),
    "Buckeye":     (43.636551, -70.285118),
    "GulfSunoco":  (43.650445, -70.238583),
    "Sprague":     (43.637217, -70.286403),
    "PPLC":        (43.629026, -70.271068),
}

# Assign each OSM structure to nearest tank farm by centroid distance.
# Include only structures within 1200 m of an anchor to avoid absorbing unrelated industry.
ASSIGN_RADIUS = 1200.0
farm_structs = {k: [] for k in TANKS}
for s in structures:
    clat, clon = ring_centroid(s['ring'])
    best_k, best_d = None, float('inf')
    for k, (tlat, tlon) in TANKS.items():
        dd = haversine(clat, clon, tlat, tlon)
        if dd < best_d:
            best_k, best_d = k, dd
    if best_d <= ASSIGN_RADIUS:
        s['assigned'] = best_k
        s['dist_from_anchor'] = best_d
        farm_structs[best_k].append(s)

for k in TANKS:
    tanks_n = sum(1 for s in farm_structs[k] if s['kind'] == 'tank')
    parcels_n = sum(1 for s in farm_structs[k] if s['kind'] == 'parcel')
    print(f"{k:<11} {tanks_n} tanks, {parcels_n} parcel polygons")

# ---------- receptors ----------
cache = json.load(open(os.path.join(DATA, 'geocode_cache.json')))
def best_latlon(query):
    r = cache.get(query)
    if r and r['results']:
        return r['results'][0]['lat'], r['results'][0]['lon']
    return None

# manual fixes for geocode misses (lat, lon)
MANUAL = {
    "107 Mussey St Apt C, South Portland , ME 04106": (43.640725, -70.244397),
    "209 Western Ave Units B1 &amp; B2 &amp; F, South Portland, ME 04106": (43.637455, -70.321580),
    "2401 Broadway, Building 2, South Portland, ME 04106": (43.633867, -70.256817),
}

def farm_distance(lat, lon, farm):
    """Min distance (m) from point to farm's assigned structures."""
    best = float('inf')
    for s in farm_structs[farm]:
        ring = s['ring']
        if ring_contains(ring, lat, lon):
            return 0.0
        d = pt_to_ring_dist(lat, lon, ring, lat, lon)
        best = min(best, d)
    return best

# ---------- receptors: schools + seniors + childcare ----------
import sys
SCHOOLS = {
    "Dora L. Small Elementary": ("school", "87 Thompson Street South Portland ME"),
    "Frank I. Brown Elementary": ("school", "37 Highland Avenue South Portland ME"),
    "Skillin Elementary": ("school", "180 Wescott Road South Portland ME"),
    "Dyer Elementary": ("school", "52 Alfred Street South Portland ME"),
    "Kaler Elementary (summer camp 2026)": ("school", "165 South Kelsey Street South Portland ME"),
    "South Portland Middle School": ("school", "120 Wescott Road South Portland ME"),
    "South Portland High School": ("school", "637 Highland Avenue South Portland ME"),
}
SENIORS = {
    "Betsy Ross House (SPHA)": ("senior", "99 Preble Street Extension South Portland ME"),
    "Ridgeland Estates (SPHA)": ("senior", "109 Ridgeland Avenue South Portland ME"),
    "Thornton Heights Commons (SPHA)": ("senior", "611 Main Street South Portland ME"),
    "Linton Street Facility": ("senior", "66 Linton Street South Portland ME"),
    "Albany Street (AL)": ("senior", "49 Albany Street Extension South Portland ME"),
    "Gordon Green": ("senior", "23 Third Street South Portland ME"),
    "Sawyer Street House": ("senior", "388 Sawyer Street South Portland ME"),
    "One Willow Manor": ("senior", "97 School Street South Portland ME"),
    "Colony Lane": ("senior", "19 Colony Lane South Portland ME"),
    "Pride House": ("senior", "549 Westbrook Street South Portland ME"),
    "Wescott": ("senior", "194 Wescott Road South Portland ME"),
    "Wilson Street": ("senior", "15 Wilson Street South Portland ME"),
}
CHILDCARE = json.load(open(os.path.join(DATA, 'ccc_union.json')))

def resolve(addr):
    ll = best_latlon(addr)
    if ll: return ll
    if addr in MANUAL: return MANUAL[addr]
    return None

def fmt_mi(m):
    return f"{m/1609.344:.2f}"

MILE = 1609.344
rows = []

for label, (cat, addr) in {**SCHOOLS, **SENIORS}.items():
    ll = resolve(addr)
    if not ll:
        print("MISS", label, addr); continue
    lat, lon = ll
    dists = {k: farm_distance(lat, lon, k) for k in TANKS}
    rows.append((label, cat, dists))

for p in CHILDCARE:
    ll = resolve(p['address'])
    if not ll:
        continue  # other-town or unresolvable; noted separately
    lat, lon = ll
    dists = {k: farm_distance(lat, lon, k) for k in TANKS}
    rows.append((p['name'], 'childcare-' + (p['type'] or '').lower(), dists))

print()
print(f"{'receptor':<50}{'cat':<20}" + "".join(f"{k:>11}" for k in TANKS))
within = {k: [] for k in TANKS}
for label, cat, dists in rows:
    marks = ""
    for k in TANKS:
        m = dists[k]
        c = f"{fmt_mi(m):>9}Y" if m <= MILE else f"{fmt_mi(m):>10}"
        marks += f"{c:>11}"
        if m <= MILE:
            within[k].append((label, cat))
    print(f"{label[:49]:<50}{cat[:19]:<20}{marks}")

print()
print("=== per-farm counts (fence-line / structure distance) ===")
for k in TANKS:
    sch = [l for l, c in within[k] if c.startswith('school')]
    chc = [l for l, c in within[k] if c.startswith('childcare-center')]
    chf = [l for l, c in within[k] if c.startswith('childcare-family')]
    chn = [l for l, c in within[k] if c.startswith('childcare-nursery')]
    sen = [l for l, c in within[k] if c.startswith('senior')]
    print(f"\n{k}: schools={len(sch)}, childcare centers={len(chc)}, family homes={len(chf)}, nurseries={len(chn)}, senior={len(sen)}")
    for l in sorted(sen): print("   senior -", l)

# union
print("\n=== UNION across farms (receptors within 1 mile of ANY farm) ===")
seen = {}
for label, cat, dists in rows:
    dmin = min(dists.values())
    if dmin <= MILE:
        seen.setdefault(cat, []).append((label, dmin))
for cat, items in sorted(seen.items()):
    print(f"{cat}: {len(items)}")
    for label, dmin in sorted(items, key=lambda x: x[1]):
        print(f"   {dmin/1609.344:5.2f} mi  {label}")
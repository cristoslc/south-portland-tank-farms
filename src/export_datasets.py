#!/usr/bin/env python3
"""Export tidy CSV datasets: receptor master file + per-farm fence-line distances."""
import json, csv, math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(HERE, 'data')
OUT = os.path.join(HERE, 'outputs')
os.chdir(DATA)

# ---- geometry (same as polygon_analysis.py) ----
def haversine(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = p2 - p1; dl = math.radians(lon2 - lon1)
    a = math.sin(dp/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(dl/2)**2
    return 2*R*math.asin(math.sqrt(a))

def ring_contains(ring, lat, lon):
    inside = False
    j = len(ring) - 1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]
        xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi):
            inside = not inside
        j = i
    return inside

def pt_to_ring_dist(lat, lon, ring):
    def to_xy(p):
        return (p[0]-lon)*111320.0*math.cos(math.radians(lat)), (p[1]-lat)*110540.0
    px, py = 0.0, 0.0  # point at origin
    best = float('inf')
    pts = ring + [ring[0]]
    for i in range(len(pts)-1):
        ax, ay = to_xy(pts[i]); bx, by = to_xy(pts[i+1])
        dx, dy = bx-ax, by-ay
        L2 = dx*dx + dy*dy
        if L2 == 0:
            d = math.hypot(px-ax, py-ay)
        else:
            t = max(0.0, min(1.0, ((px-ax)*dx + (py-ay)*dy)/L2))
            d = math.hypot(px-(ax+t*dx), py-(ay+t*dy))
        if d < best:
            best = d
    return best

def ring_centroid(ring):
    return sum(p[1] for p in ring)/len(ring), sum(p[0] for p in ring)/len(ring)

# ---- OSM structures ----
osm = json.load(open('overpass_tanks.json'))
structures = []
for e in osm['elements']:
    t = e.get('tags', {}) or {}
    geom = e.get('geometry')
    if not geom:
        continue
    ring = [[g['lon'], g['lat']] for g in geom]
    kind = 'tank' if t.get('man_made') == 'storage_tank' else 'parcel'
    structures.append({'kind': kind, 'name': t.get('name') or t.get('operator') or '', 'ring': ring})

TANKS = {
    "Global":     (43.634665, -70.275381, "Global Companies LLC", "1 Clark Road"),
    "CITGO":      (43.637390, -70.267687, "CITGO Petroleum Corp.", "102 Mechanic St"),
    "Buckeye":    (43.636551, -70.285118, "South Portland Terminal LLC (Buckeye)", "170 Lincoln St"),
    "GulfSunoco": (43.650445, -70.238583, "Gulf Oil / Sunoco Midstream", "175 Front St"),
    "Sprague":    (43.637217, -70.286403, "Sprague Operating Resources", "59 Main Street"),
    "PPLC":       (43.629026, -70.271068, "Portland Pipe Line Corp.", "30 Hill Street"),
}
ASSIGN_R = 1200.0
farm_structs = {k: [] for k in TANKS}
for s in structures:
    clat, clon = ring_centroid(s['ring'])
    bk, bd = None, float('inf')
    for k, (tlat, tlon, _, _) in TANKS.items():
        dd = haversine(clat, clon, tlat, tlon)
        if dd < bd:
            bk, bd = k, dd
    if bd <= ASSIGN_R:
        farm_structs[bk].append(s)

def farm_distance(lat, lon, farm):
    best = float('inf')
    for s in farm_structs[farm]:
        if ring_contains(s['ring'], lat, lon):
            return 0.0
        d = pt_to_ring_dist(lat, lon, s['ring'])
        best = min(best, d)
    return best

# ---- receptors ----
cache = json.load(open('geocode_cache.json'))
def ll(q):
    r = cache.get(q)
    return (r['results'][0]['lat'], r['results'][0]['lon']) if r and r['results'] else None

MANUAL = {
    "107 Mussey St Apt C, South Portland , ME 04106": (43.640725, -70.244397),
    "209 Western Ave Units B1 &amp; B2 &amp; F, South Portland, ME 04106": (43.637455, -70.321580),
    "2401 Broadway, Building 2, South Portland, ME 04106": (43.633867, -70.256817),
}

SCHOOLS = [
    ("Dora L. Small Elementary", "public school", "87 Thompson Street South Portland ME"),
    ("Frank I. Brown Elementary", "public school", "37 Highland Avenue South Portland ME"),
    ("Skillin Elementary", "public school", "180 Wescott Road South Portland ME"),
    ("Dyer Elementary", "public school", "52 Alfred Street South Portland ME"),
    ("Kaler Elementary (closed as school; summer camp use 2026)", "public school", "165 South Kelsey Street South Portland ME"),
    ("South Portland Middle School", "public school", "120 Wescott Road South Portland ME"),
    ("South Portland High School", "public school", "637 Highland Avenue South Portland ME"),
]
SENIORS = [
    ("Betsy Ross House (SPHA, 123 units, 62+)", "senior housing", "99 Preble Street Extension South Portland ME"),
    ("Ridgeland Estates (SPHA)", "senior housing", "109 Ridgeland Avenue South Portland ME"),
    ("Thornton Heights Commons (SPHA, elderly preference)", "senior housing", "611 Main Street South Portland ME"),
    ("Linton Street Facility (assisted living, RCC610)", "senior housing", "66 Linton Street South Portland ME"),
    ("Albany Street (assisted living, RCC1301)", "senior housing", "49 Albany Street Extension South Portland ME"),
    ("Gordon Green (assisted living)", "senior housing", "23 Third Street South Portland ME"),
    ("Sawyer Street House (assisted living)", "senior housing", "388 Sawyer Street South Portland ME"),
    ("One Willow Manor (residential care)", "senior housing", "97 School Street South Portland ME"),
    ("Colony Lane (assisted living, RCC213)", "senior housing", "19 Colony Lane South Portland ME"),
    ("Pride House (assisted living)", "senior housing", "549 Westbrook Street South Portland ME"),
    ("Wescott (residential care)", "senior housing", "194 Wescott Road South Portland ME"),
    ("Wilson Street (assisted living)", "senior housing", "15 Wilson Street South Portland ME"),
]

rows = []
def add(name, cat, addr):
    p = ll(addr) or MANUAL.get(addr)
    if not p:
        return False
    lat, lon = p
    row = {"receptor": name, "category": cat, "address": addr, "lat": lat, "lon": lon}
    for k in TANKS:
        row[f"dist_mi_{k}"] = round(farm_distance(lat, lon, k)/1609.344, 3)
    row["nearest_farm"] = min(TANKS, key=lambda k: row[f"dist_mi_{k}"])
    row["min_dist_mi"] = row[f"dist_mi_{row['nearest_farm']}"]
    row["within_1mi_of_any"] = "Y" if row["min_dist_mi"] <= 1.0 else "N"
    rows.append(row)
    return True

for name, cat, addr in SCHOOLS: add(name, cat, addr)
for name, cat, addr in SENIORS: add(name, cat, addr)
for p in json.load(open('ccc_union.json')):
    add(p['name'], f"childcare-{(p['type'] or '').lower()}", p['address'])

with open(os.path.join(OUT, 'receptor_fenceline_distances.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(rows)

n_inside = sum(1 for r in rows if r["within_1mi_of_any"] == "Y")
print(f"exported {len(rows)} receptors; {n_inside} within 1 mile of any farm fence line")
print("file: outputs/receptor_fenceline_distances.csv")
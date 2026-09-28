#!/usr/bin/env python3
"""Audit OSM structures: identify non-tank-farm parcels caught in the net,
orphan tank clusters, and whether they affected receptor counts."""
import json, math, csv, os

HERE = os.getcwd(); DATA = os.path.join(HERE, 'data'); OUT = os.path.join(HERE, 'outputs')
FARMS = {"global":(43.634665,-70.275381),"citgo":(43.637390,-70.267687),
         "buckeye":(43.636551,-70.285118),"gulf_sunoco":(43.650445,-70.238583),
         "sprague":(43.637217,-70.286403),"pplc":(43.629026,-70.271068)}
def hav(a,b,c,d):
    R=6371000.0
    p1,p2=math.radians(a),math.radians(c)
    x=math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))

osm = json.load(open(os.path.join(DATA,'overpass_tanks.json')))
tanks, parcels = [], []
for e in osm['elements']:
    g = e.get('geometry')
    if not g: continue
    t = e.get('tags', {}) or {}
    ring = [[p['lon'], p['lat']] for p in g]
    clat = sum(p[1] for p in ring)/len(ring); clon = sum(p[0] for p in ring)/len(ring)
    fid, d = min(((k, hav(clat,clon,v[0],v[1])) for k,v in FARMS.items()), key=lambda x: x[1])
    item = {'id': e['id'], 'tags': t, 'clat': clat, 'clon': clon,
            'assigned': fid if d <= 1200 else None, 'd_anchor': d,
            'kind': 'tank' if t.get('man_made')=='storage_tank' else 'parcel',
            'ring': ring}
    (tanks if item['kind']=='tank' else parcels).append(item)

print(f"tanks: {len(tanks)}, parcels: {len(parcels)}\n")
print("=== ALL PARCELS: classification ===")
for p in sorted(parcels, key=lambda x: (x['assigned'] or 'zzz', x['d_anchor'])):
    t = p['tags']
    name = t.get('name') or t.get('operator') or '(unnamed)'
    kind_detail = t.get('industrial') or t.get('man_made') or '-'
    has_tanks = any(hav(tk['clat'],tk['clon'],p['clat'],p['clon']) < 200 for tk in tanks)
    status = "OIL-TANK-FARM" if (t.get('industrial')=='oil' or has_tanks) else "NON-TANK-FARM"
    print(f"  {p['id']:>10} {p['kind']:<7} '{name:<30}' ind={kind_detail:<9} tanks_nearby={str(has_tanks):<5} "
          f"asg={p['assigned'] or '-':<11} {p['d_anchor']:>5.0f}m  [{status}]")

print("\n=== ORPHAN TANKS (no parcel within 60 m) ===")
for tk in tanks:
    dmin = min((hav(tk['clat'],tk['clon'],p['clat'],p['clon']) for p in parcels), default=9e9)
    if dmin > 60:
        print(f"  {tk['id']:>10} at ({tk['clat']:.4f},{tk['clon']:.4f}) nearest parcel {dmin:.0f}m "
              f"asg={tk['assigned'] or '-'} tags={ {k:v for k,v in tk['tags'].items() if k in ('name','operator','content','industrial')} }")

print("\n=== TANKS BY CLUSTER (which tanks belong to no-named parcels?) ===")
clusters = {}
for tk in tanks:
    key = tk['assigned']
    clusters.setdefault(key, []).append(tk)
for k, v in sorted(clusters.items(), key=lambda x: str(x[0])):
    print(f"  {k or 'UNASSIGNED'}: {len(v)} tanks")

# ---- which structures drove the 42 receptor hits? ----
def pt_to_ring_dist(lat, lon, ring):
    def xy(p):
        return ((p[0]-lon)*111320.0*math.cos(math.radians(lat)), (p[1]-lat)*110540.0)
    px_, py_ = 0.0, 0.0
    best = float('inf')
    pts = ring + [ring[0]]
    for i in range(len(pts)-1):
        ax_, ay_ = xy(pts[i]); bx_, by_ = xy(pts[i+1])
        dx_, dy_ = bx_-ax_, by_-ay_
        L2 = dx_*dx_+dy_*dy_
        d = math.hypot(px_-ax_, py_-ay_) if L2 == 0 else (
            math.hypot(px_-(ax_+(t_:=max(0,min(1,((-px_*dx_)+( -py_*dy_)*-1 if False else (px_-ax_)*dx_+(py_-ay_)*dy_)/L2)))*dx_), py_-(ay_+t_*dy_)))
        best = min(best, d)
    return best
def ring_contains(ring, lat, lon):
    inside = False
    j = len(ring)-1
    for i in range(len(ring)):
        xi, yi = ring[i][0], ring[i][1]; xj, yj = ring[j][0], ring[j][1]
        if ((yi > lat) != (yj > lat)) and (lon < (xj-xi)*(lat-yi)/(yj-yi)+xi):
            inside = not inside
        j = i
    return inside

recs = [r for r in csv.DictReader(open(os.path.join(OUT,'receptor_fenceline_distances.csv')))
        if r['within_1mi_of_any'] == 'Y']
# For each receptor-farm inside-1mi pair, find argmin structure
parc_by_farm = {}
for p in parcels:
    if p['assigned']:
        parc_by_farm.setdefault(p['assigned'], []).append(p)
tank_by_farm = {}
for tk in tanks:
    if tk['assigned']:
        tank_by_farm.setdefault(tk['assigned'], []).append(tk)

print("\n=== RECEPTOR MIN-DISTANCE STRUCTURE AUDIT (the 42 counted sites) ===")
suspect_hits = []
for r in recs:
    # replicate polygon_analysis: per-farm min over structures assigned to that farm
    best_struct = None
    for farm_col, farm in [("dist_mi_Global","global"),("dist_mi_CITGO","citgo"),("dist_mi_Buckeye","buckeye"),
                           ("dist_mi_GulfSunoco","gulf_sunoco"),("dist_mi_Sprague","sprague"),("dist_mi_PPLC","pplc")]:
        mi = float(r[farm_col])
        if mi > 1.0: continue
        # find the structure of that farm with the matching min distance
        target_m = mi*1609.344
        cands = []
        for s in parc_by_farm.get(farm, []) + tank_by_farm.get(farm, []):
            if ring_contains(s['ring'], float(r['lat']), float(r['lon'])):
                cands.append((0.0, s))
            else:
                cands.append((pt_to_ring_dist(float(r['lat']), float(r['lon']), s['ring']), s))
        if cands:
            dm, s = min(cands, key=lambda x: x[0])
            t = s['tags']
            name = t.get('name') or t.get('operator') or '(unnamed)'
            kind_detail = t.get('industrial') or t.get('man_made') or '-'
            is_nonfarm = s['kind']=='parcel' and not (t.get('industrial')=='oil' or any(hav(tk2['clat'],tk2['clon'],s['clat'],s['clon'])<200 for tk2 in tanks))
            marker = "  <-- SUSPECT (non-tank-farm parcel)" if is_nonfarm else ""
            if is_nonfarm:
                suspect_hits.append((r['receptor'], farm, s['id'], name, kind_detail))
            if abs(dm - target_m) < 40 or is_nonfarm:  # only print close matches
                pass
    # print receptor's own overall argmin
for sh in suspect_hits:
    print("  SUSPECT:", sh)
print(f"\ntotal receptor-farm hits relying on non-tank-farm parcels: {len(suspect_hits)} (receptors may repeat)")
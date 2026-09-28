#!/usr/bin/env python3
"""Interactive map (self-contained HTML w/ Leaflet CDN): tank farms, receptors,
monitoring stations, 1-mile rings. Styled to PSP brand."""
import csv, json, math, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs")

FARMS = [
    {"id":"global","name":"Global Companies LLC","addr":"1 Clark Road","lat":43.634665,"lon":-70.275381,
     "voc":21.9,"lic":"A-432-71-S-R/M","renew":"Dec 2023 (10-yr) → ~2033"},
    {"id":"citgo","name":"CITGO Petroleum Corp.","addr":"102 Mechanic St","lat":43.637390,"lon":-70.267687,
     "voc":117.3,"lic":"A-460-70-H-R","renew":"Nov 2025 (5-yr) → ~2030"},
    {"id":"buckeye","name":"Buckeye / South Portland Terminal","addr":"170 Lincoln St","lat":43.636551,"lon":-70.285118,
     "voc":135.4,"lic":"A-282-70-G-R","renew":"2015 license, evergreen"},
    {"id":"gulf_sunoco","name":"Gulf / Sunoco Midstream","addr":"175 Front St","lat":43.650445,"lon":-70.238583,
     "voc":49.9,"lic":"A-390-71-P-R/M","renew":"Feb 2023 (10-yr) → ~2033"},
    {"id":"sprague","name":"Sprague Operating Resources","addr":"59 Main St","lat":43.637217,"lon":-70.286403,
     "voc":49.9,"lic":"A-179-71-P-R/M","renew":"Mar 2018 (10-yr) → ~2028"},
    {"id":"pplc","name":"Portland Pipe Line Corp.","addr":"30 Hill Street","lat":43.629026,"lon":-70.271068,
     "voc":220.0,"lic":"A-197-70-H-R","renew":"Feb 2025 (5-yr) → ~2030; marine renewal pending"},
]
MON = [("POG","Portland – Ocean Gateway",43.6561,-70.2409),
       ("PWC","Portland – West Commercial",43.6598,-70.2563),
       ("SPCC","South Portland – Cash Corner",43.6292,-70.2955),
       ("SPFS","South Portland – Front Street",43.6518,-70.2402),
       ("SPMS","South Portland – Mechanic St",43.6386,-70.2666),
       ("SPPS","South Portland – Pearl Street",43.6389,-70.2555),
       ("SPRB","South Portland – Red Bank",43.6166,-70.3245)]

def hav(a,b,c,d):
    R=6371000.0
    p1,p2=math.radians(a),math.radians(c)
    x=math.sin((p2-p1)/2)**2+math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))

structs = json.load(open(os.path.join(DATA, "overpass_tanks.json")))
polys = []
for e in structs.get("elements", []):
    g = e.get("geometry")
    if not g: continue
    ring = [[pt["lon"], pt["lat"]] for pt in g]
    clat = sum(p[1] for p in ring)/len(ring); clon = sum(p[0] for p in ring)/len(ring)
    best = min(FARMS, key=lambda f: hav(clat, clon, f["lat"], f["lon"]))
    if hav(clat, clon, best["lat"], best["lon"]) <= 1200:
        tags = e.get("tags", {}) or {}
        polys.append({"ring": ring, "kind": "tank" if tags.get("man_made")=="storage_tank" else "parcel", "farm": best["id"]})

def cat_group(c):
    if c == "public school": return ("school","#1b4332")
    if c == "senior housing": return ("senior","#7b2cbf")
    return ("childcare","#d62828")

recs = list(csv.DictReader(open(os.path.join(HERE, "outputs", "receptor_fenceline_distances.csv"))))
rec_js = []
for r in recs:
    if r["within_1mi_of_any"] != "Y": continue
    grp, color = cat_group(r["category"])
    rec_js.append({"name": r["receptor"], "cat": grp, "color": color,
                   "lat": float(r["lat"]), "lon": float(r["lon"]),
                   "min": r["min_dist_mi"], "near": r["nearest_farm"]})

farm_js = [{"id": f["id"], "name": f["name"], "addr": f["addr"], "lat": f["lat"], "lon": f["lon"],
            "voc": f["voc"], "lic": f["lic"], "renew": f["renew"]} for f in FARMS]
mon_js = [{"code": c, "name": n, "lat": la, "lon": lo} for c, n, la, lo in MON]

html = """<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>South Portland Tank Farms &amp; Sensitive Receptors — Protect South Portland</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<style>
:root{--forest:#1b4332;--pine:#2d6a4f;--leaf:#52b788;--pale:#d8f3dc;--amber:#f77f00;--red:#d62828;--text:#1a1a2e;--muted:#555}
*{box-sizing:border-box} body{margin:0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;color:var(--text)}
header{background:var(--forest);color:#fff;padding:14px 20px;display:flex;align-items:baseline;gap:14px;flex-wrap:wrap}
header h1{font-size:1.25rem;margin:0;font-weight:800;letter-spacing:-.02em}
header span{font-size:.85rem;opacity:.85}
#map{height:calc(100vh - 58px);min-height:420px}
.panel{position:absolute;top:80px;right:14px;z-index:1000;background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:12px 14px;max-width:250px;box-shadow:0 2px 8px rgba(0,0,0,.15);font-size:.82rem}
.panel h2{margin:0 0 8px;font-size:.95rem;color:var(--forest)}
.panel .leg{display:flex;align-items:center;gap:8px;margin:5px 0}
.panel .dot{width:12px;height:12px;border-radius:50%;flex:none}
.panel .sq{width:11px;height:11px;flex:none;transform:rotate(45deg)}
.panel .ring{width:14px;height:14px;border:2px dashed var(--amber);border-radius:50%;flex:none}
.panel .star{color:var(--amber);font-size:1.1rem;flex:none;line-height:1}
.panel .facts{margin-top:10px;padding-top:8px;border-top:1px solid #e0e0e0;font-size:.78rem;color:var(--muted);line-height:1.5}
.leaflet-popup-content{font-size:.85rem;line-height:1.4}
.leaflet-popup-content b{color:var(--forest)}
.farm-label{background:var(--forest);color:#fff;padding:2px 7px;border-radius:4px;font-weight:700;font-size:.72rem;white-space:nowrap;border:none;box-shadow:0 1px 4px rgba(0,0,0,.4)}
</style></head><body>
<header><h1>South Portland Tank Farms &amp; Sensitive Receptors</h1><span>Fence-line distances · 1-mile radius · DEP VOC monitors</span></header>
<div id="map"></div>
<div class="panel">
  <h2>Legend</h2>
  <div class="leg"><span class="sq" style="background:var(--forest)"></span>Tank (OSM)</div>
  <div class="leg"><span class="sq" style="background:var(--leaf)"></span>Parcel (OSM)</div>
  <div class="leg"><span class="ring"></span>1-mile radius</div>
  <div class="leg"><span class="dot" style="background:var(--forest)"></span>School (7)</div>
  <div class="leg"><span class="dot" style="background:var(--red)"></span>Child care (25)</div>
  <div class="leg"><span class="dot" style="background:#7b2cbf"></span>Senior housing (9)</div>
  <div class="leg"><span class="star">★</span>Tank farm (6)</div>
  <div class="leg"><span class="dot" style="background:var(--pine);border-radius:2px;transform:rotate(45deg)"></span>DEP VOC monitor (7)</div>
  <div class="facts"><b>42 sites</b> within 1 mile of a fence line. Kaler Elem <b>0.04 mi</b> from Pipe Line parcel; Betsy Ross House adjacent to Gulf/Sunoco. Licensed VOC: <b>~597 tpy</b>.<br><br><span style="font-size:.68rem;color:var(--muted)">Straight-line distances to OSM-mapped fence lines; not walking distances. Sources: DEP licenses, OCFS 9/2026, NCES, SPHA, OSM. Data: github.com/cristoslc/south-portland-tank-farms</span></div>
</div>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script>
const FARMS = __FARMS__;
const RECS = __RECS__;
const MON = __MON__;
const POLYS = __POLYS__;
const map = L.map('map').setView([43.635, -70.275], 13);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; OpenStreetMap contributors'}).addTo(map);
const icons = {school:L.divIcon({className:'',html:'<div style="width:14px;height:14px;background:#1b4332;transform:rotate(45deg);border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[14,14],iconAnchor:[7,7]}),
 childcare:L.divIcon({className:'',html:'<div style="width:12px;height:12px;background:#d62828;transform:rotate(45deg);border:1.5px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[12,12],iconAnchor:[6,6]}),
 senior:L.divIcon({className:'',html:'<div style="width:13px;height:13px;background:#7b2cbf;border:1.5px solid #fff;border-radius:2px;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[13,13],iconAnchor:[6,6]})};
POLYS.forEach(p=>{L.polygon(p.ring.map(c=>[c[1],c[0]]),{color:'#1b4332',weight:0.7,fillColor:p.kind==='tank'?'#1b4332':'#2d6a4f',fillOpacity:0.5})
  .bindPopup(`<b>${p.kind==='tank'?'Storage tank':'Industrial parcel'}</b><br>Farm: ${p.farm}`).addTo(map);});
FARMS.forEach(f=>{L.circle([f.lat,f.lon],{radius:1609.344,color:'#f77f00',weight:1.4,dashArray:'6 5',fill:false}).addTo(map);
  L.marker([f.lat,f.lon]).bindPopup(`<b>${f.name}</b><br>${f.addr}<br>License ${f.lic} · VOC cap ${f.voc} tpy<br>Renewal: ${f.renew}`).addTo(map);
  L.marker([f.lat,f.lon],{icon:L.divIcon({className:'',html:`<div class="farm-label">${f.name.split(' ')[0]}</div>`,iconAnchor:[0,0]})}).addTo(map);});
RECS.forEach(r=>{L.marker([r.lat,r.lon],{icon:icons[r.cat]}).bindPopup(`<b>${r.name}</b><br>${r.cat==='school'?'Public school':r.cat==='senior'?'Senior housing':'Child care'}<br><b>${r.min} mi</b> to ${r.near} fence line`).addTo(map);});
MON.forEach(m=>{L.marker([m.lat,m.lon],{icon:L.divIcon({className:'',html:'<div style="width:12px;height:12px;background:#2d6a4f;border:2px solid #fff;box-shadow:0 1px 3px rgba(0,0,0,.4)"></div>',iconSize:[12,12],iconAnchor:[6,6]})}).bindPopup(`<b>${m.code}</b> — ${m.name}<br><i>DEP VOC monitoring station</i>`).addTo(map);});
</script></body></html>"""

html = html.replace("__FARMS__", json.dumps(farm_js))
html = html.replace("__RECS__", json.dumps(rec_js))
html = html.replace("__MON__", json.dumps(mon_js))
html = html.replace("__POLYS__", json.dumps(polys))
open(os.path.join(OUT, "map_interactive.html"), "w").write(html)
print(f"interactive map: {len(rec_js)} receptors, {len(polys)} structures, {len(FARMS)} farms -> outputs/map_interactive.html")
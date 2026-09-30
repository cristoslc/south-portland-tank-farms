#!/usr/bin/env python3
"""Build the microsite's map.html: inject receptor polygons + buffer data into
the data-driven template, writing to the microsite folder."""
import csv, json, math, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs")
MICROSITE = os.path.expanduser("~/projects/psp/microsite")

sys.path.insert(0, os.path.join(HERE, "src"))
from farm_structures import load as fs_load

# receptors (within 1 mile only)
recs = list(csv.DictReader(open(os.path.join(OUT, "receptor_fenceline_distances.csv"))))
def grp(c):
    if c == "public school": return "school"
    if c == "senior housing": return "senior"
    return "childcare"
FARM_LABEL = {"global":"Global","citgo":"CITGO","buckeye":"Buckeye",
              "gulf_sunoco":"Gulf/Sunoco","sprague":"Sprague","pplc":"Pipe Line"}
rec_js = []
for r in recs:
    if r["within_1mi_of_any"] != "Y":
        continue
    rec_js.append({
        "name": r["receptor"], "cat": grp(r["category"]),
        "lat": float(r["lat"]), "lon": float(r["lon"]),
        "min": r["min_dist_mi"], "near": FARM_LABEL.get(r["nearest_farm"], r["nearest_farm"]),
    })

# structures
assigned, _ = fs_load(HERE)
polys = [{"ring": s["ring"], "kind": s["kind"], "farm": FARM_LABEL.get(s["farm"], s["farm"])}
         for s in assigned]

# buffer rings (lat,lon ordered for Leaflet)
bgj = json.load(open(os.path.join(OUT, "gis", "tank_farm_1mile_buffer.geojson")))
bg = bgj["features"][0]["geometry"]
if bg["type"] == "Polygon":
    rings = [bg["coordinates"][0]]
else:
    rings = [mp[0] for mp in bg["coordinates"]]
buffer_rings = [[[c[1], c[0]] for c in ring] for ring in rings]

html = open(os.path.join(HERE, "src", "microsite_map_t.html"), encoding="utf-8").read()
html = html.replace("__RECEPTORS__", json.dumps(rec_js))
html = html.replace("__POLYGONS__", json.dumps(polys))
html = html.replace("__BUFFER__", json.dumps(buffer_rings))

out_path = os.path.join(MICROSITE, "map.html")
open(out_path, "w", encoding="utf-8").write(html)
print(f"wrote {out_path} ({len(html):,} bytes): {len(rec_js)} receptors, {len(polys)} polygons")
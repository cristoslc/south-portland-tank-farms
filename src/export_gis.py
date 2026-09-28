#!/usr/bin/env python3
"""Export GIS-ready datasets: point layers (wide + long), facility/permit table,
per-farm counts, and tank fence-line structures as GeoJSON.

Reads:  outputs/receptor_fenceline_distances.csv (master dataset)
        data/overpass_tanks.json                (OSM structures)
Writes: outputs/gis/*
"""
import csv, json, math, os, re, unicodedata

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs", "gis")
os.makedirs(OUT, exist_ok=True)

# Farm metadata: anchors (same coords used in polygon_analysis.py) + permit facts
# sourced from each facility's DEP air license order (see report References).
FARMS = [
    {"farm_id": "global", "operator": "Global Companies LLC",
     "address": "1 Clark Road, South Portland, ME 04106",
     "latitude": 43.634665, "longitude": -70.275381,
     "license": "A-432-71-S-R/M", "license_renewed": "2023-12-05",
     "license_term_years": 10, "voc_limit_tpy": 21.9, "hap_limit_tpy": 9.9,
     "license_expires_approx": "2033-12-05"},
    {"farm_id": "citgo", "operator": "CITGO Petroleum Corp.",
     "address": "102 Mechanic Street, South Portland, ME 04106",
     "latitude": 43.637390, "longitude": -70.267687,
     "license": "A-460-70-H-R", "license_renewed": "2025-11-05",
     "license_term_years": 5, "voc_limit_tpy": 117.3, "hap_limit_tpy": 5.0,
     "license_expires_approx": "2030-11-05"},
    {"farm_id": "buckeye", "operator": "South Portland Terminal LLC (Buckeye Terminals)",
     "address": "170 Lincoln Street, South Portland, ME 04106",
     "latitude": 43.636551, "longitude": -70.285118,
     "license": "A-282-70-G-R / A-282-70-H-A", "license_renewed": "2015-11/12",
     "license_term_years": 5, "voc_limit_tpy": 135.4, "hap_limit_tpy": 14.1,
     "license_expires_approx": "nominally ~2020; evergreen pending renewal"},
    {"farm_id": "gulf_sunoco", "operator": "Gulf Oil LP / Sunoco Midstream LLC",
     "address": "175 Front Street, South Portland, ME 04106",
     "latitude": 43.650445, "longitude": -70.238583,
     "license": "A-390-71-P-R/M", "license_renewed": "2023-02-22",
     "license_term_years": 10, "voc_limit_tpy": 49.9, "hap_limit_tpy": 24.9,
     "license_expires_approx": "2033-02-22"},
    {"farm_id": "sprague", "operator": "Sprague Operating Resources LLC",
     "address": "59 Main Street, South Portland, ME 04106",
     "latitude": 43.637217, "longitude": -70.286403,
     "license": "A-179-71-P-R/M (SM)", "license_renewed": "2018-03",
     "license_term_years": 10, "voc_limit_tpy": 49.9, "hap_limit_tpy": 24.9,
     "license_expires_approx": "2028-03"},
    {"farm_id": "pplc", "operator": "Portland Pipe Line Corp.",
     "address": "30 Hill Street, South Portland, ME 04106",
     "latitude": 43.629026, "longitude": -70.271068,
     "license": "A-197-70-H-R", "license_renewed": "2025-02-24",
     "license_term_years": 5, "voc_limit_tpy": 220.0, "hap_limit_tpy": 24.9,
     "license_expires_approx": "2030-02-24"},
]
FARM_BY_ID = {f["farm_id"]: f for f in FARMS}
# master CSV column suffix -> farm_id
FARM_KEYS = {"Global": "global", "CITGO": "citgo", "Buckeye": "buckeye",
             "GulfSunoco": "gulf_sunoco", "Sprague": "sprague", "PPLC": "pplc"}

CAT_MAP = {
    "public school": "school",
    "senior housing": "senior_housing",
    "childcare-center": "childcare_center",
    "childcare-nursery": "childcare_nursery",
    "childcare-family": "childcare_family",
    "childcare-license": "childcare_license_exempt",
}

def slugify(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    s = re.sub(r"[^a-zA-Z0-9]+", "_", s).strip("_").lower()
    return s[:60] or "site"

import re  # noqa: E402

import re  # noqa: E402

def wkt_point(lat, lon):
    return f"POINT ({lon:.6f} {lat:.6f})"

rows = list(csv.DictReader(open(os.path.join(HERE, "outputs",
                                               "receptor_fenceline_distances.csv"))))
farm_cols = list(FARM_KEYS.items())

# ---------- 1. receptors_points.csv (wide; one row per receptor) ----------
used_ids = {}
wide_rows = []
for r in rows:
    rid = slugify(r["receptor"])
    if rid in used_ids:
        used_ids[rid] += 1
        rid = f"{rid}_{used_ids[rid]}"
    else:
        used_ids[rid] = 1
    lat, lon = float(r["lat"]), float(r["lon"])
    out = {
        "receptor_id": rid, "receptor_name": r["receptor"],
        "category": CAT_MAP.get(r["category"], r["category"]),
        "category_original": r["category"], "address": r["address"],
        "latitude": lat, "longitude": lon, "wkt": wkt_point(lat, lon),
    }
    for suffix, fid in farm_cols:
        mi = float(r[f"dist_mi_{suffix}"])
        out[f"dist_mi_{fid}"] = mi
        out[f"dist_m_{fid}"] = round(mi * 1609.344, 1)
    out["nearest_farm"] = FARM_KEYS.get(r["nearest_farm"], r["nearest_farm"])
    out["min_dist_mi"] = r["min_dist_mi"]
    out["min_dist_m"] = round(float(r["min_dist_mi"]) * 1609.344, 1)
    out["within_1mi_of_any"] = r["within_1mi_of_any"]
    out["suspect_geocode"] = "Y" if float(r["min_dist_mi"]) > 20 else "N"
    wide_rows.append(out)

wide_cols = list(wide_rows[0].keys())
with open(os.path.join(OUT, "receptors_points.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=wide_cols)
    w.writeheader()
    w.writerows(wide_rows)

# ---------- 2. receptor_farm_distances_long.csv (tidy/long) ----------
long_rows = []
for r, wr in zip(rows, wide_rows):
    for suffix, fid in farm_cols:
        mi = float(r[f"dist_mi_{suffix}"])
        long_rows.append({
            "receptor_id": wr["receptor_id"], "receptor_name": r["receptor"],
            "category": wr["category"], "farm_id": fid,
            "operator": FARM_BY_ID[fid]["operator"],
            "distance_mi": mi, "distance_m": round(mi * 1609.344, 1),
            "within_1mi": "Y" if mi <= 1.0 else "N",
        })
with open(os.path.join(OUT, "receptor_farm_distances_long.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(long_rows[0].keys()))
    w.writeheader()
    w.writerows(long_rows)

# ---------- 3. tank_farm_facilities.csv ----------
with open(os.path.join(OUT, "tank_farm_facilities.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(FARMS[0].keys()) + ["wkt"])
    w.writeheader()
    for farm in FARMS:
        row = dict(farm)
        row["latitude"] = f"{farm['latitude']:.6f}"
        row["longitude"] = f"{farm['longitude']:.6f}"
        row["wkt"] = wkt_point(farm["latitude"], farm["longitude"])
        w.writerow(row)

# ---------- 4. receptor_counts_by_farm.csv ----------
counts = []
for farm in FARMS:
    fid = farm["farm_id"]
    inside = [r for r in long_rows if r["farm_id"] == fid and r["within_1mi"] == "Y"]
    c = {"farm_id": fid, "operator": farm["operator"]}
    for cat in ["school", "childcare_center", "childcare_nursery",
                "childcare_family", "childcare_license_exempt", "senior_housing"]:
        c[cat] = sum(1 for r in inside if r["category"] == cat)
    c["total_within_1mi"] = len(inside)
    counts.append(c)
with open(os.path.join(OUT, "receptor_counts_by_farm.csv"), "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(counts[0].keys()))
    w.writeheader()
    w.writerows(counts)

# ---------- 5. tank_farm_structures.geojson (corrected rule) ----------
import sys
sys.path.insert(0, os.path.join(HERE, "src"))
from farm_structures import load as fs_load, ring_contains as fs_contains
_assigned, _excluded = fs_load(HERE)
features = []
for s in _assigned:
    features.append({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [s["ring"]]},
        "properties": {
            "osm_way_id": s["id"],
            "structure_type": "storage_tank" if s["kind"] == "tank" else "industrial_parcel",
            "name": (s["tags"].get("name") or s["tags"].get("operator") or ""),
            "farm_id": s["farm"],
            "used_in_analysis": "Y",
            "contains_tanks": s.get("contains_tanks", 0),
        },
    })
for s in _excluded:
    features.append({
        "type": "Feature",
        "geometry": {"type": "Polygon", "coordinates": [s["ring"]]},
        "properties": {
            "osm_way_id": s["id"],
            "structure_type": "storage_tank" if s["kind"] == "tank" else "industrial_parcel",
            "name": (s["tags"].get("name") or s["tags"].get("operator") or ""),
            "farm_id": "",
            "used_in_analysis": "N",
            "exclusion_reason": s.get("reason", ""),
        },
    })
gj = {"type": "FeatureCollection",
      "name": "south_portland_tank_farm_structures",
      "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
      "features": features}
json.dump(gj, open(os.path.join(OUT, "tank_farm_structures.geojson"), "w"), indent=1)

print(f"wrote {len(wide_rows)} receptor points, {len(long_rows)} long rows, "
      f"{len(features)} structures ({sum(1 for x in features if x['properties']['used_in_analysis']=='Y')} assigned to farms)")
print("files in", OUT)
for fn in sorted(os.listdir(OUT)):
    print("  -", fn)
#!/usr/bin/env python3
"""Compute the 1-mile buffer around the union of all tank-farm structures
(the true 'within 1 mile of a fence line' zone) and export as GeoJSON."""
import json, math, os
from shapely.geometry import Polygon, mapping, shape
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs", "gis")
os.makedirs(OUT, exist_ok=True)

FARMS = {
    "global": (43.634665, -70.275381),
    "citgo": (43.637390, -70.267687),
    "buckeye": (43.636551, -70.285118),
    "gulf_sunoco": (43.650445, -70.238583),
    "sprague": (43.637217, -70.286403),
    "pplc": (43.629026, -70.271068),
}
LAT0, LON0 = 43.6335, -70.278
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0
MILE = 1609.344
ASSIGN_R = 1200.0

def to_m(lon, lat):
    return ((lon - LON0) * KX, (lat - LAT0) * KY)
def to_ll(x, y):
    return (LON0 + x / KX, LAT0 + y / KY)

def hav(a, b, c, d):
    R = 6371000.0
    p1, p2 = math.radians(a), math.radians(c)
    x = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))

osm = json.load(open(os.path.join(DATA, "overpass_tanks.json")))
polys = []
for e in osm.get("elements", []):
    g = e.get("geometry")
    if not g: continue
    ring = [[p["lon"], p["lat"]] for p in g]
    clat = sum(p[1] for p in ring)/len(ring); clon = sum(p[0] for p in ring)/len(ring)
    fid, d = min(((k, hav(clat, clon, v[0], v[1])) for k, v in FARMS.items()), key=lambda t: t[1])
    if d <= ASSIGN_R:
        # to meters, closed ring
        ring_m = [to_ll(*to_m(p[0], p[1])) for p in ring]  # keep ll for now
        ring_m = [(to_m(lo, la)) for lo, la in ring]
        try:
            poly = Polygon(ring_m)
            if poly.is_valid and poly.area > 0:
                polys.append(poly)
        except Exception:
            pass
print(f"{len(polys)} polygons")
union = unary_union(polys)
buffered = union.buffer(MILE, resolution=32)
print(f"buffer area: {buffered.area/1e6:.2f} km^2")

def shp_to_lonlat_geom(geom):
    """convert shapely geom in local meters back to lon/lat geojson geometry"""
    def rec(coords):
        if isinstance(coords[0], (int, float)):
            x, y = coords
            lo, la = to_ll(x, y)
            return [round(lo, 6), round(la, 6)]
        return [rec(c) for c in coords]
    return {"type": geom.geom_type, "coordinates": rec(geom.exterior.coords) if geom.geom_type == "Polygon" else [rec(g.exterior.coords) for g in geom.geoms]}

gj = {
    "type": "FeatureCollection",
    "name": "tank_farm_1mile_fenceline_buffer",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "Tank farms — 1-mile fence-line buffer",
            "definition": "Union of all 125 OSM-mapped tank/parcel polygons assigned to the six South Portland tank farms, buffered by 1 statute mile (1609.344 m). A receptor is 'within 1 mile' iff its point falls inside this zone.",
            "source": "OpenStreetMap structures + analysis in this repo",
        },
        "geometry": json.loads(json.dumps(mapping(buffered), default=lambda o: list(o.coords))) if False else None,
    }],
}
# build geometry manually (handles Polygon and MultiPolygon)
if buffered.geom_type == "Polygon":
    rings = [[list(c) for c in buffered.exterior.coords]]
    extra = [[list(c) for c in i.exterior.coords] for i in buffered.interiors] if buffered.interiors else []
    geom = {"type": "Polygon", "coordinates": [rings[0]]}
else:
    polys_g = []
    for gpart in buffered.geoms:
        rings = [[list(c) for c in gpart.exterior.coords]]
        polys_g.append(rings)
    geom = {"type": "MultiPolygon", "coordinates": polys_g}
# convert meter coords back to lon/lat
def conv_ring(ring):
    return [[round(v, 6) for v in to_ll(x, y)] for x, y in ring]
if geom["type"] == "Polygon":
    geom["coordinates"] = [conv_ring(geom["coordinates"][0])]
else:
    geom["coordinates"] = [[conv_ring(r[0])] for r in geom["coordinates"]]
gj["features"][0]["geometry"] = geom
json.dump(gj, open(os.path.join(OUT, "tank_farm_1mile_buffer.geojson"), "w"))
print("saved outputs/gis/tank_farm_1mile_buffer.geojson")
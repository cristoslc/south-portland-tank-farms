#!/usr/bin/env python3
"""Compute the fence-line buffer around the union of all corrected tank-farm
structures (the true 'within N miles of a fence line' zone) and export as GeoJSON.

Buffer geometry itself lives in src/buffer_geometry.py (structure-corrected
union per the Sept 28 2026 Structure Audit Addendum, same local-meter
projection the original build used).
"""
import json, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(HERE, "outputs", "gis")
os.makedirs(OUT, exist_ok=True)

import sys
sys.path.insert(0, os.path.join(HERE, "src"))
from buffer_geometry import buffer_geometry

union, n_polys = None, None
from buffer_geometry import structures_union
union, n_polys = structures_union(HERE)
geom = buffer_geometry(1.0)
print(f"{n_polys} polygons; buffer area: {union.buffer(1609.344, resolution=32).area/1e6:.2f} km^2")

gj = {
    "type": "FeatureCollection",
    "name": "tank_farm_1mile_fenceline_buffer",
    "crs": {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}},
    "features": [{
        "type": "Feature",
        "properties": {
            "name": "Tank farms — 1-mile fence-line buffer",
            "definition": f"Union of all {n_polys} corrected OSM-mapped tank/parcel polygons assigned to the six South Portland tank farms (storage tanks, parcels containing tanks, and operator-named oil parcels; see Structure Audit Addendum), buffered by 1 statute mile (1609.344 m). A receptor is 'within 1 mile' iff its point falls inside this zone.",
            "source": "OpenStreetMap structures + analysis in this repo",
        },
        "geometry": geom,
    }],
}
json.dump(gj, open(os.path.join(OUT, "tank_farm_1mile_buffer.geojson"), "w"))
print("saved outputs/gis/tank_farm_1mile_buffer.geojson")
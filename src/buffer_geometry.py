#!/usr/bin/env python3
"""Fence-line buffer geometry, shared by the buffer exporter and the maps.

Builds the union of all corrected tank-farm fence-line structures
(src/farm_structures.py, corrected Sept 28 2026 audit rule) in a local-meter
projection and buffers it to any radius. Uses the same projection anchors,
mile constant, and shapely resolution as the original 1-mile buffer build,
so the recomputed radius buffers are the same logic reprojected to the
slider's distance — never a scaling of the 1-mile polygon.
"""
import json, math, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(HERE, "src"))
from farm_structures import load as fs_load

# projection anchors (identical to the original build_buffer.py)
LON0, LAT0 = -70.278, 43.6335
KX = 111320.0 * math.cos(math.radians(LAT0))
KY = 110540.0
MILE = 1609.344

def to_m(lon, lat):
    return ((lon - LON0) * KX, (lat - LAT0) * KY)
def to_ll(x, y):
    return (LON0 + x / KX, LAT0 + y / KY)

def _shapely():
    import shapely.geometry, shapely.ops
    return shapely.geometry, shapely.ops

_UNION_CACHE = {}

def structures_union(repo_root=None):
    """Shapely union (local meters) of the corrected fence-line structures."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    here = repo_root or HERE
    if here in _UNION_CACHE:
        return _UNION_CACHE[here]
    assigned, _excluded = fs_load(here)
    polys = []
    for s in assigned:
        try:
            p = Polygon([to_m(lo, la) for lo, la in s["ring"]])
            if p.is_valid and p.area > 0:
                polys.append(p)
        except Exception:
            pass
    union = unary_union(polys)
    _UNION_CACHE[here] = (union, len(polys))
    return _UNION_CACHE[here]

def buffer_geometry(radius_miles, resolution=32, repo_root=None):
    """GeoJSON geometry (lon/lat, Polygon or MultiPolygon) of the union of all
    corrected fence-line structures buffered by `radius_miles` statute miles."""
    union, _n = structures_union(repo_root)
    buffered = union.buffer(radius_miles * MILE, resolution=resolution)

    def rec(coords):
        if isinstance(coords[0], (int, float)):
            x, y = coords
            lo, la = to_ll(x, y)
            return [round(lo, 6), round(la, 6)]
        return [rec(c) for c in coords]

    if buffered.geom_type == "Polygon":
        parts = [buffered]
    else:
        parts = list(buffered.geoms)
    ring_sets = []
    for part in parts:
        rings = [[rec(c) for c in part.exterior.coords]]
        for ir in part.interiors:
            rings.append([rec(c) for c in ir.coords])
        ring_sets.append(rings)
    if len(ring_sets) == 1:
        return {"type": "Polygon", "coordinates": ring_sets[0]}
    return {"type": "MultiPolygon", "coordinates": ring_sets}

def leaflet_rings(geom):
    """GeoJSON geometry dict (Polygon/MultiPolygon, holes supported) -> flat list
    of exterior+interior [lat, lon] rings for Leaflet. Leaflet fills a polygon's
    rings with even-odd, so listing holes after their outer ring subtracts them
     correctly, and the published buffer style stays one polygon layer."""
    if geom["type"] == "Polygon":
        ring_sets = [geom["coordinates"]]
    else:
        ring_sets = geom["coordinates"]
    out = []
    for rings in ring_sets:
        for ring in rings:
            out.append([[c[1], c[0]] for c in ring])
    return out

if __name__ == "__main__":
    union, n = structures_union()
    print(f"{n} corrected structures in union")
    geom = buffer_geometry(1.0)
    print(f"1-mile buffer geometry: {geom['type']}")
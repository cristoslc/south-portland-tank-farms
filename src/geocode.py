#!/usr/bin/env python3
"""Geocode tank farm / sensitive-receptor addresses via Nominatim, cache results."""
import json, os, sys, time, urllib.request, urllib.parse

CACHE_FILE = os.path.join(os.path.dirname(__file__), "geocode_cache.json")
HEADERS = {"User-Agent": "PSP-research-tank-farm-study/1.0 (civic research, Portland ME)"}

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE) as f:
            return json.load(f)
    return {}

def geocode(query, label=None):
    cache = load_cache()
    key = query.strip()
    if key in cache:
        return cache[key]
    url = "https://nominatim.openstreetmap.org/search?" + urllib.parse.urlencode(
        {"q": query, "format": "json", "limit": 3, "countrycodes": "us"})
    req = urllib.request.Request(url, headers=HEADERS)
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read())
            break
        except Exception as e:
            print(f"  attempt {attempt+1} failed: {e}", file=sys.stderr)
            time.sleep(3)
    else:
        raise RuntimeError(f"geocode failed for {query}")
    result = {"query": query, "label": label,
              "results": [{"lat": float(r["lat"]), "lon": float(r["lon"]),
                           "display_name": r["display_name"], "type": r["type"],
                           "class": r["class"]} for r in data[:3]]}
    cache = load_cache()
    cache[key] = result
    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f, indent=2)
    time.sleep(1.2)  # Nominatim rate limit: 1 req/sec
    return result

if __name__ == "__main__":
    for q in sys.argv[1:]:
        res = geocode(q)
        print(f"== {q}")
        for r in res["results"]:
            print(f"   {r['lat']:.6f}, {r['lon']:.6f}  {r['display_name'][:90]}")
        if not res["results"]:
            print("   NO RESULTS")
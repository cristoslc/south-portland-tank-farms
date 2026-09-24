#!/usr/bin/env python3
"""Run OCFS childcare search from each tank farm, union results, dedupe."""
import json, subprocess, os, re, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ccc_parse import parse
from ccc_search import search_around
import asyncio

TANKS = {
    "Global":      (43.634665, -70.275381, "1 Clark Road, South Portland, ME"),
    "CITGO":       (43.637390, -70.267687, "102 Mechanic Street, South Portland, ME"),
    "Buckeye":     (43.636551, -70.285118, "170 Lincoln Street, South Portland, ME"),
    "GulfSunoco":  (43.650445, -70.238583, "175 Front Street, South Portland, ME"),
    "Sprague":     (43.637217, -70.286403, "59 Main Street, South Portland, ME"),
    "PPLC":        (43.629026, -70.271068, "30 Hill Street, South Portland, ME"),
}

async def main():
    all_providers = {}
    for name, (lat, lon, addr) in TANKS.items():
        out_html = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", f"ccc_{name}.html")
        if not os.path.exists(out_html):
            await search_around(lat, lon, addr, out_html)
        provs = parse(out_html)
        uniq = {}
        for p in provs:
            key = (p["name"], p["address"])
            uniq[key] = p
        print(f"{name:<11} {len(uniq)} unique providers")
        for k, v in uniq.items():
            all_providers.setdefault(k, v)
    import os
os.makedirs(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"), exist_ok=True)
out_json = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "ccc_union.json")
json.dump(list(all_providers.values()), open(out_json, "w"), indent=1)
    print(f"UNION: {len(all_providers)} unique providers -> data/ccc_union.json")

if __name__ == "__main__":
    asyncio.run(main())
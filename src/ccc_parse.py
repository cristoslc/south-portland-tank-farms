#!/usr/bin/env python3
"""Parse childcarechoices.me results into JSON list of providers."""
import re, sys, json

def parse(html_path):
    html = open(html_path).read()
    # Drop scripts to reduce noise
    html = re.sub(r'<script.*?</script>', '', html, flags=re.S)
    blocks = re.split(r'Licensing Details/Reports', html)
    out = []
    for b in blocks[1:]:
        t = re.sub(r'<[^>]+>', '\n', b)
        t = re.sub(r'\r', '', t)
        lines = [l.strip() for l in t.splitlines() if l.strip()]
        # find address line like: 68 Jordan Ave, South Portland, ME 04106
        addr_idx = None
        for i, l in enumerate(lines):
            if re.match(r'^\d+ .*, .*, ME \d{5}$', l):
                addr_idx = i
                break
        if addr_idx is None:
            continue
        address = lines[addr_idx]
        # name: nearest preceding non-empty line(s)
        name = lines[addr_idx-1] if addr_idx > 0 else ''
        ptype = None
        for l in lines:
            m = re.match(r'Provider Type:\s*(\w+)', l)
            if m:
                ptype = m.group(1)
                break
        star = None
        m = re.search(r'Star Rating:\s*\n?\s*(\d)', b)
        if m:
            star = m.group(1)
        out.append({"name": name, "address": address, "type": ptype, "star": star})
    return out

if __name__ == "__main__":
    providers = parse(sys.argv[1])
    seen = set()
    uniq = []
    for p in providers:
        key = (p["name"], p["address"])
        if key not in seen:
            seen.add(key)
            uniq.append(p)
    json.dump(uniq, open(sys.argv[2], "w"), indent=1)
    print(f"{len(uniq)} unique providers -> {sys.argv[2]}")
    for p in uniq[:10]:
        print(f"  {p['type']:<8} {p['name'][:40]:<42} {p['address']}")
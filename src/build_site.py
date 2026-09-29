#!/usr/bin/env python3
"""Build GitHub Pages site into docs/: index + report + factcheck, PSP-branded HTML."""
import os, markdown

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # repo root
OUT = os.path.join(HERE, "docs")
os.makedirs(OUT, exist_ok=True)

FOREST = "#1b4332"; PINE = "#2d6a4f"; LEAF = "#52b788"; PALE = "#d8f3dc"; MUTED = "#555"

CSS = f"""
:root{{--forest:{FOREST};--pine:{PINE};--leaf:{LEAF};--pale:{PALE};--muted:{MUTED}}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:'Segoe UI',system-ui,-apple-system,sans-serif;color:#1a1a2e;line-height:1.65}}
header.site{{background:var(--forest);color:#fff;padding:18px 24px}}
header.site .wrap{{max-width:980px;margin:0 auto;display:flex;align-items:baseline;gap:12px;flex-wrap:wrap}}
header.site h1{{margin:0;font-size:1.35rem;font-weight:800;letter-spacing:-.02em}}
header.site a{{color:#fff;text-decoration:none}}
header.site nav a{{color:#fff;opacity:.9;text-decoration:none;font-size:.92rem;margin-left:18px}}
header.site nav a:hover{{text-decoration:underline}}
main{{max-width:980px;margin:0 auto;padding:28px 20px 60px}}
h1{{color:var(--forest);font-size:1.9rem;font-weight:800;letter-spacing:-.02em;border-bottom:2px solid var(--forest);padding-bottom:6px}}
h2{{color:var(--forest);font-size:1.4rem;font-weight:700;margin-top:1.8em}}
h3{{color:var(--pine)}}
table{{border-collapse:collapse;width:100%;font-size:.88rem;margin:1em 0}}
th,td{{border:1px solid #e0e0e0;padding:5px 8px;text-align:left;vertical-align:top}}
th{{background:var(--pale);color:var(--forest)}}
blockquote{{border-left:4px solid var(--pine);background:var(--pale);margin:1em 0;padding:.7em 1.1em}}
code{{background:#f9fafb;padding:1px 5px;border-radius:4px;font-size:.88em}}
pre{{background:#f9fafb;padding:12px;overflow-x:auto;font-size:.85em}}
.callout{{border-left:4px solid var(--pine);background:var(--pale);padding:12px 16px;border-radius:0 8px 8px 0;margin:1.2em 0}}
.hero{{background:linear-gradient(160deg,var(--forest) 0%,var(--pine) 100%);color:#fff;padding:40px 30px;border-radius:12px;margin-bottom:28px}}
.hero h1{{color:#fff;border:none;font-size:2.1rem;margin:0 0 8px}}
.hero p{{margin:.3em 0;opacity:.94}}
.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(250px,1fr));gap:16px;margin:1.4em 0}}
.card{{background:#fff;border:1px solid #e0e0e0;border-radius:8px;padding:18px;box-shadow:0 1px 4px rgba(0,0,0,.06)}}
.card h3{{margin:.1em 0 .4em;color:var(--forest)}}
.stat{{font-size:2rem;font-weight:800;color:var(--leaf)}}
footer.site{{background:var(--forest);color:#fff;padding:22px;margin-top:40px;font-size:.85rem}}
footer.site .wrap{{max-width:980px;margin:0 auto}}
footer.site a{{color:var(--pale)}}
.muted{{color:var(--muted);font-size:.85rem}}
a.btn{{display:inline-block;background:var(--leaf);color:var(--forest);font-weight:700;padding:9px 18px;border-radius:8px;text-decoration:none}}
nav.toc{{background:var(--pale);border-radius:8px;padding:14px 20px;margin:18px 0}}
nav.toc a{{color:var(--pine);text-decoration:none}}
nav.toc a:hover{{text-decoration:underline}}
img{{max-width:100%;height:auto;border-radius:8px}}
"""

HEADER = f"""<header class="site"><div class="wrap"><h1>Protect South Portland</h1><nav>
<a href="index.html">Home</a><a href="report.html">Research Report</a><a href="factcheck.html">Fact-Check</a><a href="data.html">Data Files</a><a href="https://github.com/cristoslc/south-portland-tank-farms">GitHub</a></nav></div></header>"""

FOOTER = f"""<footer class="site" style="margin-top:40px"><div class="wrap">
Protect South Portland · ProtectSouthPortland.com · AI-assisted research compiled under human steering; all claims verified in the <a href="factcheck.html">fact-check log</a>.</div></footer>"""

PAGE = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><link rel="stylesheet" href="style.css"></head><body>
{header}<main>{body}</main>{footer}</body></html>"""

def md_to_html(md_path):
    text = open(md_path, encoding="utf-8").read()
    md = markdown.Markdown(extensions=["tables", "smarty"])
    return md.reset().convert(text)

# ---- index ----
index_body = f"""
<div class="hero">
  <h1 style="color:#fff;font-size:2rem">South Portland Tank Farms:<br>Sensitive Receptors &amp; Permit Renewals</h1>
  <p>How close are the oil tank farms to our schools, daycares, and senior housing — and when are their state permits up for renewal?</p>
</div>
<div class="cards">
  <div class="card"><h3>42 sensitive sites</h3><p>All 7 public schools, 25 licensed child care programs, and 9 senior housing facilities lie within one mile of a tank farm fence line.</p></div>
  <div class="card"><h3>~597 tons VOC/yr</h3><p>Combined licensed VOC caps across the six facilities, taken from each facility's own DEP license order.</p></div>
  <div class="card"><h3>Renewals: 2028–2033</h3><p>Sprague ~2028 · CITGO &amp; Pipe Line ~2030 · Global &amp; Gulf/Sunoco ~2033 · Pipe Line's marine renewal is pending now.</p></div>
</div>
<h2>Explore</h2>
<ul>
  <li><a href="report.html"><b>Full research report</b></a> — findings, permit table, methodology, references</li>
  <li><a href="factcheck.html"><b>Fact-check log</b></a> — every claim with its source and direct evidence quote</li>
  <li><a href="https://github.com/cristoslc/south-portland-tank-farms"><b>Downloadable data</b></a> — CSV/GeoJSON datasets, GIS point/polygon layers, maps (GitHub)</li>
  <li><a href="map.png"><b>Proximity map</b></a> — print-ready static map (PNG)</li>
  <li><a href="map.html"><b>Interactive map</b></a> — Leaflet map with popups</li>
  <li><a href="data.html"><b>Data files</b></a> — CSV/GeoJSON layers at clean site URLs (GIS-ready)</li>
  <li><a href="SouthPortland_TankFarms_Binder.pdf"><b>Evidence binder (PDF)</b></a> — print-ready report + fact-check + map in one document</li>
</ul>
<div class="callout"><b>About this project.</b> Research compiled with AI assistance under human steering for Protect South Portland. Every factual claim is verified against official Maine DEP license documents, with the verification trail published in the fact-check log.</div>
<p class="muted">Compiled September 2026 · ProtectSouthPortland.com</p>
"""

open(os.path.join(OUT, "index.html"), "w").write(
    PAGE_TPL := PAGE_TPL if False else "") if False else None

def page(title, body, out):
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="styles.css"></head><body>{HEADER}<main>{body}</main>{FOOTER}</body></html>"""
    open(os.path.join(OUT, out_name := out_name if False else out_path) if False else open(out_name, "w") if False else open(out, "w").write(html) if False else open(out, "w").write(html) if False else open(out, "w").write(html) if False else open(out, "w").write(html), "w").write(html) if False else None

# simpler: write files directly
open(os.path.join(OUT, "index.html"), "w").write(
    f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>South Portland Tank Farms — Protect South Portland</title>
<link rel="stylesheet" href="styles.css"></head><body>{HEADER}<main>{index_body}</main>{FOOTER}</body></html>""")

open(os.path.join(OUT, "styles.css"), "w").write(CSS)

# report + factcheck pages
for src, out, title in [("TANK_FARM_RECEPTOR_AND_PERMIT_MEMO.md", "report.html", "Research Report — South Portland Tank Farms"),
                        ("FACTCHECK.md", "factcheck.html", "Fact-Check Log — South Portland Tank Farms")]:
    body = md_to_html(os.path.join(HERE, "outputs", src))
    html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>{title}</title>
<link rel="stylesheet" href="styles.css"></head><body>{HEADER}<main>{body}</main>{FOOTER}</body></html>"""
    open(os.path.join(OUT, out), "w").write(html)
    print("wrote", out)

# data files page
data_rows = [
    ("receptors_points.csv", "Receptor point layer (171 sites)", "CSV",
     "One row per receptor: lat/lon, WKT, distances in miles + meters to each farm fence line, within-1-mile flag.",
     "QGIS: Layer ▸ Add Layer ▸ Delimited Text (point coordinates, EPSG:4326)"),
    ("receptor_farm_distances_long.csv", "Tidy distances (171 × 6 farms)", "CSV",
     "Long format: one distance per receptor-farm pair, with within_1mi flag. Best shape for joins/pivots/database loads.",
     "Any spreadsheet, R (read.csv), pandas, or Postgres COPY"),
    ("receptor_counts_by_farm.csv", "Per-farm within-1-mile counts", "CSV",
     "Summary table: counts by category for each of the six facilities.",
     "Direct reference table"),
    ("tank_farm_facilities.csv", "Tank farm facilities (6)", "CSV",
     "Facility coordinates, DEP license numbers, renewal dates, facility-wide VOC/HAP limits.",
     "GIS point import or tabular reference"),
    ("tank_farm_structures.geojson", "Fence-line structures (117 + 8 excluded)", "GeoJSON",
     "OSM polygons: storage tanks + qualifying parcels, with farm assignment and exclusion reasons for non-tank-farm structures.",
     "QGIS/geojson.io/Leaflet — loads directly"),
    ("tank_farm_1mile_buffer.geojson", "1-mile fence-line buffer zone", "GeoJSON",
     "Single merged polygon: union of all qualifying structures buffered one statute mile. Point-in-polygon = the report's 'within 1 mile' criterion (41/42 exact; 1 boundary case at 1.000 mi).",
     "QGIS/geojson.io/Leaflet — loads directly"),
    ("receptor_fenceline_distances.csv", "Master dataset (original wide format)", "CSV",
     "Original analysis dataset with per-farm distance columns (miles).",
     "Superseded by receptors_points.csv for GIS use; retained for lineage"),
]
data_body = """
<h1>Data Files</h1>
<p>GIS-ready datasets used in the research. Coordinates are WGS84 (EPSG:4326); distances are straight-line
fence-line distances from OpenStreetMap-mapped structures. See the
<a href="report.html">research report</a> for methodology and caveats, and the
<a href="factcheck.html">fact-check log</a> for claim-by-claim verification.</p>
<table>
<tr><th>File</th><th>Contents</th><th>Format</th><th>Use</th></tr>
"""
for fn, label, fmt, desc, use in data_rows:
    data_body += f'<tr><td><a href="data/{fn}"><code>{fn}</code></a></td><td><b>{label}</b><br>{desc}</td><td>{fmt}</td><td>{use}</td></tr>\n'
data_body += "</table>"
data_body += """
<div class="callout"><b>License &amp; provenance.</b> Data: CC BY 4.0. Fence-line geometry: OpenStreetMap contributors, ODbL 1.0, via the project's self-hosted Overpass instance (osm.cristoslc.com, Maine daily extract, base 2026-09-27T20:10Z). Child care listings: Maine OCFS Child Care Choices (captured Sept 24, 2026). Schools: NCES. Senior housing: SPHA + state-licensed facilities. Repo mirrors everything at
<a href="https://github.com/cristoslc/south-portland-tank-farms">github.com/cristoslc/south-portland-tank-farms</a>.</div>
<p class="muted">Note: fence-line polygons are community-mapped OSM data; City of South Portland assessor GIS parcels would be the parcel-exact upgrade. Distances &lt; ~0.01 mi mean the receptor point sits on/inside the mapped parcel edge ("directly adjacent").</p>
"""
html = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Data Files — South Portland Tank Farms</title>
<link rel="stylesheet" href="styles.css"></head><body>{HEADER}<main>{data_body}</main>{FOOTER}</body></html>"""
open(os.path.join(OUT, "data.html"), "w").write(html)
print("wrote data.html")

# copy map + interactive map
import shutil
shutil.copy(os.path.join(HERE, "outputs", "south_portland_tank_farms_map.png"), os.path.join(OUT, "map.png"))
shutil.copy(os.path.join(HERE, "outputs", "map_interactive.html"), os.path.join(OUT, "map.html"))
_binder = os.path.join(HERE, "outputs", "SouthPortland_TankFarms_Binder.pdf")
if os.path.exists(_binder):
    shutil.copy(_binder, os.path.join(OUT, "SouthPortland_TankFarms_Binder.pdf"))

# copy GIS/data files into docs/data/ for clean site URLs
_gis_src = os.path.join(HERE, "outputs", "gis")
_gis_dst = os.path.join(OUT, "data")
os.makedirs(_gis_dst, exist_ok=True)
GIS_FILES = ["receptors_points.csv", "receptor_farm_distances_long.csv",
             "receptor_counts_by_farm.csv", "tank_farm_facilities.csv",
             "tank_farm_structures.geojson", "tank_farm_1mile_buffer.geojson"]
for fn in GIS_FILES:
    src_path = os.path.join(_gis_src, fn)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(_gis_dst, fn))
_raw_dst = os.path.join(OUT, "data")
for fn in ["receptor_fenceline_distances.csv"]:
    src_path = os.path.join(HERE, "outputs", fn)
    if os.path.exists(src_path):
        shutil.copy(src_path, os.path.join(_raw_dst, fn))
print("docs/ built:", sorted(os.listdir(OUT)))
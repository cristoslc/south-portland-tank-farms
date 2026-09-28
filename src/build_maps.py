#!/usr/bin/env python3
"""Build PSP-branded maps of tank farms + sensitive receptors + DEP monitoring stations.

Outputs:
  outputs/south_portland_tank_farms_map.png   (print/static, Letter landscape)
  outputs/map_interactive.html                (self-contained Leaflet map)
"""
import csv, json, math, os, io, time, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs")
os.makedirs(OUT, exist_ok=True)

# ---------- brand palette (VISUAL_IDENTITY.md) ----------
FOREST = "#1b4332"; PINE = "#2d6a4f"; LEAF = "#52b788"; PALE = "#d8f3dc"
AMBER = "#f77f00"; RED = "#d62828"; CREAM = "#fefefe"; MUTED = "#555555"

FARMS = [
    ("global", "Global Companies LLC", "1 Clark Road", 43.634665, -70.275381),
    ("citgo", "CITGO Petroleum Corp.", "102 Mechanic St", 43.637390, -70.267687),
    ("buckeye", "Buckeye / S. Portland Terminal", "170 Lincoln St", 43.636551, -70.285118),
    ("gulf_sunoco", "Gulf / Sunoco Midstream", "175 Front St", 43.650445, -70.238583),
    ("sprague", "Sprague Operating Resources", "59 Main St", 43.637217, -70.286403),
    ("pplc", "Portland Pipe Line Corp.", "30 Hill Street", 43.629026, -70.271068),
]
MONITORING = [  # DEP VOC project stations (approximate locations, from DEP Read Me)
    ("POG", "Portland - Ocean Gateway", 43.6561, -70.2409),
    ("PWC", "Portland - West Commercial St", 43.6598, -70.2563),
    ("SPCC", "S. Portland - Cash Corner", 43.6292, -70.2955),
    ("SPFS", "S. Portland - Front Street", 43.6518, -70.2402),
    ("SPMS", "S. Portland - Mechanic Street", 43.6386, -70.2666),
    ("SPPS", "S. Portland - Pearl Street", 43.6389, -70.2555),
    ("SPRB", "S. Portland - Red Bank", 43.6166, -70.3245),
]

# ---------- load data ----------
import unicodedata, re
structures = json.load(open(os.path.join(DATA, "overpass_tanks.json")))
def hav(lat1, lon1, lat2, lon2):
    R = 6371000.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    a = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(lon2-lon1)/2)**2
    return 2*R*math.asin(math.sqrt(a))
features = []
for e in structures.get("elements", []):
    geom = e.get("geometry")
    if not geom: continue
    ring = [[g["lon"], g["lat"]] for g in geom]
    if ring[0] != ring[-1]: ring = ring + [ring[0]]
    clat = sum(p[1] for p in ring[:-1])/(len(ring)-1)
    clon = sum(p[0] for p in ring[:-1])/(len(ring)-1)
    best = min(FARMS, key=lambda f: hav(clat, clon, f[3], f[4]))
    d = hav(clat, clon, best[3], best[4])
    if d <= 1200:
        tags = e.get("tags", {}) or {}
        features.append({"ring": ring, "kind": "tank" if tags.get("man_made")=="storage_tank" else "parcel", "farm": best[0]})
print(f"{len(features)} structures assigned")

recs = list(csv.DictReader(open(os.path.join(OUT, "receptor_fenceline_distances.csv"))))
def cat_group(c):
    if c == "public school": return "school"
    if c == "senior housing": return "senior"
    return "childcare"

# ---------- OSM basemap tiles ----------
def deg2num(lat, lon, z):
    n = 2**z
    x = int((lon + 180.0)/360.0 * n)
    y = int((1.0 - math.log(math.tan(math.radians(lat)) + 1/math.cos(math.radians(lat)))/math.pi)/2.0 * n)
    return x, y
def num2deg(x, y, z):
    n = 2.0**z
    lon = x/n*360.0 - 180.0
    lat = math.degrees(math.atan(math.sinh(math.pi*(1 - 2*y/n))))
    return lat, lon
def lonlat_to_px(lat, lon, z, x0, y0, tile_px=256):
    n = 2.0**z
    xt = (lon + 180.0)/360.0 * n
    yt = (1.0 - math.log(math.tan(math.radians(lat)) + 1/math.cos(math.radians(lat)))/math.pi)/2
    return (xt*n*tile_px - x0*tile_px, yt*n*tile_px - y0*tile_px)

Z = 13
lat0, lon0 = 43.635, -70.275
x0, y0 = deg2num(lat0, lon0, Z)
NT = 4  # 4x4 tiles = 1024x1024
tiles = {}
for dx in range(-2, 2):
    for dy in range(-1, 3):
        x, y = x0+dx, y0+dy
        url = f"https://tile.openstreetmap.org/{Z}/{x}/{y}.png"
        req = urllib.request.Request(url, headers={"User-Agent": "PSP-research-map/1.0 (civic data viz; contact via github)"})
        tiles[(x, y)] = urllib.request.urlopen(req, timeout=30).read()
        time.sleep(0.3)
print(f"fetched {len(tiles)} OSM tiles")

# ---------- static map ----------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon as MplPoly
from PIL import Image

tile_px = 256
W, H = tile_px*4, tile_px*4
canvas = Image.new("RGB", (W, H), CREAM)
for (x, y), data in tiles.items():
    im = Image.open(io.BytesIO(data)).convert("RGB")
    canvas.paste(im, ((x-x0)*tile_px, (y-y0)*tile_px))
w_px, h_px = canvas.size

def px(lat, lon):
    p = lonlat_to_px(lat, lon, Z, x0, y0)
    return p[0], h_px - p[1]  # flip y for matplotlib

plt.rcParams["font.family"] = "DejaVu Sans"
fig = plt.figure(figsize=(11, 8.5), dpi=150)
ax = fig.add_axes([0.02, 0.04, 0.62, 0.92])
ax.imshow(canvas, extent=(0, W, 0, H), interpolation="bilinear")
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# fence polygons
for f in features:
    pts = [px(ll[1], ll[0]) for ll in f["ring"]]
    ax.add_patch(MplPoly(pts, closed=True, facecolor="#1b4332" if f["kind"]=="tank" else "#2d6a4f", alpha=0.55, edgecolor="#1b4332", linewidth=0.6, zorder=3))

# 1-mile rings (from each farm anchor)
MILE_M = 1609.344
for fid, name, addr, flat, flon in FARMS:
    px_f = lonlat_to_px(flat, flon, Z, x0, y0)
    cx = px_f[0]
    cy = h_px - px_f[1]
    # radius in pixels: distance from anchor to a point 1 mile due north
    nlat = flat + MILE_M/111320.0
    nx, ny = lonlat_to_px(nlat, flon, Z, x0, y0)
    rpx = abs((h_px - ny) - cy)
    ax.add_patch(Circle((cx, cy), rpx, fill=False, edgecolor="#f77f00", linewidth=1.1, linestyle=(0, (5, 4)), alpha=0.85, zorder=4))

# receptors
receptors = list(csv.DictReader(open(os.path.join(HERE, "outputs", "receptor_fenceline_distances.csv"))))
style = {"school": ("#1b4332", "s", 60), "childcare": ("#d62828", "^", 42), "senior": ("#7b2cbf", "D", 46)}
import matplotlib.collections as mc
for r in receptors:
    if r["within_1mi_of_any"] != "Y":
        continue
    lat, lon = float(r["lat"]), float(r["lon"])
    g = cat_group(r["category"])
    c, m, s = style[g]
    p = lonlat_to_px(lat, lon, Z, x0, y0)
    ax.scatter([p[0]], [h_px - p[1]], c=c, marker=m, s=s, edgecolors="white", linewidths=0.7, zorder=6)

# facility stars + labels
label_offsets = {"global": (8, -14), "citgo": (8, 8), "buckeye": (-10, -22), "gulf_sunoco": (8, 10), "sprague": (10, -18), "pplc": (8, 12)}
for fid, name, addr, flat, flon in FARMS:
    p = lonlat_to_px(flat, flon, Z, x0, y0)
    ax.scatter([p[0]], [h_px - p[1]], c="#f77f00", marker="*", s=320, edgecolors="#1a1a2e", linewidths=0.8, zorder=8)
    dx, dy = label_offsets[fid]
    ax.annotate(f"{name}\n{addr}", (p[0], h_px - p[1]), textcoords="offset points", xytext=(dx, dy),
                fontsize=7.2, fontweight="bold", color="#1a1a2e",
                bbox=dict(boxstyle="round,pad=0.25", fc="white", ec="#1b4332", lw=0.8, alpha=0.92), zorder=7)

# monitoring stations (triangles w/ code labels)
for code, label, mlat, mlon in MONITORING:
    p = lonlat_to_px(mlat, mlon, Z, x0, y0)
    ax.scatter([p[0]], [h_px - p[1]], c="#2d6a4f", marker="v", s=90, edgecolors="white", linewidths=1.0, zorder=6)
    ax.annotate(code, (p[0], h_px - p[1]), textcoords="offset points", xytext=(4, -12), fontsize=6.5, color="#2d6a4f", fontweight="bold", zorder=7)

ax.set_xticks([]); ax.set_yticks([])

# legend panel
lx = 0.66
fig.text(lx, 0.93, "South Portland Tank Farms &", fontsize=17, fontweight="bold", color="#1b4332")
fig.text(lx, 0.875, "Sensitive Receptors", fontsize=17, fontweight="bold", color="#1b4332")
fig.text(lx, 0.835, "Fence-line distances (OSM parcels/tanks) · 1-mile radius rings", fontsize=8.5, color=MUTED)
items = [
    ("#1b4332", "s", "Public school (7)"),
    ("#d62828", "^", "Child care (25)"),
    ("#7b2cbf", "D", "Senior housing (9)"),
    ("#f77f00", "*", "Tank farm (6 facilities)"),
    ("#f77f00", "ring", "1-mile radius"),
    ("#2d6a4f", "v", "DEP VOC monitor"),
]
y = 0.80
for c, m, label in items:
    ax_l = fig.add_axes([lx, y-0.008, 0.05, 0.02])
    ax_l.axis("off")
    ax_l.set_xlim(0, 1); ax_l.set_ylim(0, 1)
    if m == "ring":
        ax_l.add_patch(Circle((0.5, 0.5), 0.38, fill=False, edgecolor=c, linewidth=1.4, linestyle=(0, (5, 4))))
    else:
        ax_l.scatter([0.5], [0.5], c=c, marker=m, s=110 if m!="*" else 200, edgecolors="white" if m=="v" else "none", linewidths=0.6)
    fig.text(lx+0.06, y-0.002, label, fontsize=9.5, va="center", color="#1a1a2e")
    y -= 0.032
# stat band
stats = [
    "42 sensitive sites within 1 mile of a fence line",
    "All 7 public schools · 25 child care programs · 9 senior facilities",
    "Kaler Elem: 0.04 mi from Portland Pipe Line parcel",
    "Betsy Ross House: adjacent to Gulf/Sunoco parcel",
    "Licensed VOC caps: ~597 tpy (six facilities, DEP orders)",
]
yy = 0.60
fig.text(lx, yy, "KEY FACTS", fontsize=10, fontweight="bold", color="#1b4332")
yy -= 0.045
for s in stats:
    fig.text(lx, yy, "• " + s, fontsize=9, color="#1a1a2e")
    yy -= 0.042
# renewal mini-table
fig.text(lx, yy, "PERMIT RENEWAL WINDOW", fontsize=10, fontweight="bold", color="#1b4332")
yy -= 0.045
for t_ in ["Sprague   ~2028", "CITGO     ~2030", "Pipe Line ~2030 (marine renewal pending)", "Buckeye   evergreen (2015 license)", "Global    ~2033", "Gulf/Sunoco ~2033"]:
    fig.text(lx, yy, t_, fontsize=8.6, color="#1a1a2e", family="monospace")
    yy -= 0.038
fig.text(lx, 0.06, "Sources: Maine DEP air license orders; OCFS Child Care Choices (9/24/2026); NCES; SPHA; OpenStreetMap (ODbL).", fontsize=7, color=MUTED)
fig.text(lx, 0.032, "Straight-line fence-line distances (OSM parcels). DEP monitor sites approximate. Data: github.com/cristoslc/south-portland-tank-farms", fontsize=7, color=MUTED)
fig.text(lx, 0.005, "Protect South Portland · Sept 2026", fontsize=7.5, color="#1b4332", fontweight="bold")
fig.savefig(os.path.join(OUT, "south_portland_tank_farms_map.png"), dpi=150, facecolor="white")
plt.close(fig)
print("static map saved")
#!/usr/bin/env python3
"""Static map: South Portland tank farms + sensitive receptors + DEP monitors.
PSP-branded, print-ready. Legibility-first: short facility labels with leader
lines, larger canvas, decluttered sidebar."""
import csv, json, math, os, io, time, urllib.request

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(HERE, "data")
OUT = os.path.join(HERE, "outputs")

FOREST = "#1b4332"; PINE = "#2d6a4f"; LEAF = "#52b788"; PALE = "#d8f3dc"
AMBER = "#f77f00"; RED = "#d62828"; CREAM = "#fefefe"; MUTED = "#555555"; TEXT = "#1a1a2e"

FARMS = [
    ("global",     "Global",      "1 Clark Rd",     43.634665, -70.275381),
    ("citgo",      "CITGO",       "102 Mechanic St",43.637390, -70.267687),
    ("buckeye",    "Buckeye/SPT", "170 Lincoln St", 43.636551, -70.285118),
    ("gulf_sunoco","Gulf/Sunoco", "175 Front St",   43.650445, -70.238583),
    ("sprague",    "Sprague",     "59 Main St",     43.637217, -70.286403),
    ("pplc",       "Pipe Line",   "30 Hill St",     43.629026, -70.271068),
]
MON = [("POG",43.6561,-70.2409),("PWC",43.6598,-70.2563),("SPCC",43.6292,-70.2955),
       ("SPFS",43.6518,-70.2402),("SPMS",43.6386,-70.2666),("SPPS",43.6389,-70.2555),
       ("SPRB",43.6166,-70.3245)]
# hand-tuned label placement: (dx, dy) points, ha alignment
LABEL_POS = {
    "global":     (14,  14, "left"),
    "citgo":      (14,  10, "left"),
    "buckeye":    (-14, 16, "right"),
    "gulf_sunoco":(14,  8, "left"),
    "sprague":    (-14, -6, "right"),
    "pplc":       (14,  -6, "left"),
}

def hav(a, b, c, d):
    R = 6371000.0
    p1, p2 = math.radians(a), math.radians(c)
    x = math.sin((p2-p1)/2)**2 + math.cos(p1)*math.cos(p2)*math.sin(math.radians(d-b)/2)**2
    return 2*R*math.asin(math.sqrt(x))

# structures
import sys
sys.path.insert(0, os.path.join(HERE, "src"))
from farm_structures import load as fs_load
VOC_TPY_IDS = {"global": 21.9, "citgo": 117.3, "buckeye": 135.4, "gulf_sunoco": 49.9,
               "sprague": 49.9, "pplc": 220.0}
features = [{"ring": s["ring"], "kind": s["kind"], "farm": s["farm"],
             "voc": VOC_TPY_IDS[s["farm"]]} for s in fs_load(HERE)[0]]
print(f"{len(features)} structures")

# ---- tiles: zoom 14, 6x5 ----
def deg2num(lat, lon, z):
    n = 2**z
    return (int((lon+180)/360*n), int((1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n))
def num2deg(x, y, z):
    n = 2.0**z
    return math.degrees(math.atan(math.sinh(math.pi*(1-2*y/n)))), x/n*360-180
Z = 14
COLS, ROWS = 6, 5
TP = 256
lat_c, lon_c = 43.6335, -70.278   # center of tank-farm cluster
# fractional tile coords of the DESIRED CENTER, then back off half the grid
# (deg2num returns the tile CONTAINING a point -> top-left; using it as the
# grid origin shifts the view half a frame southeast. This was the bug.)
n = 2.0 ** Z
fx = (lon_c + 180.0) / 360.0 * n
fy = (1 - math.log(math.tan(math.radians(lat_c)) + 1 / math.cos(math.radians(lat_c))) / math.pi) / 2 * n
x0 = round(fx - COLS / 2)
y0 = round(fy - ROWS / 2)
import PIL.Image as Image
canvas = Image.new("RGB", (COLS*TP, ROWS*TP), CREAM)
n_fetched = 0
for dx in range(COLS):
    for dy in range(ROWS):
        x, y = x0+dx, y0+dy
        url = f"https://tile.openstreetmap.org/{Z}/{x}/{y}.png"
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, headers={"User-Agent":"PSP-map/1.0 (civic; github.com/cristoslc/south-portland-tank-farms)"})
                data = urllib.request.urlopen(req, timeout=30).read()
                canvas.paste(Image.open(io.BytesIO(data)).convert("RGB"), (dx*TP, dy*TP))
                n_fetched += 1
                break
            except Exception:
                time.sleep(2)
        time.sleep(0.35)
print(f"{n_fetched} tiles")


def lonlat_px_abs(lat, lon):
    n = 2.0**Z
    xt = (lon+180)/360*n*TP - x0*TP
    yt = (1-math.log(math.tan(math.radians(lat))+1/math.cos(math.radians(lat)))/math.pi)/2*n*TP - y0*TP
    return xt, yt

# --- fade the basemap, full strength inside the 1-mile fence-line buffer ---
from PIL import ImageEnhance
FADED = 0.30          # opacity of basemap outside the buffer (0..1)
FULL = 0.98           # opacity inside the buffer
faded = Image.blend(Image.new("RGB", canvas.size, (255,255,255)), canvas, FADED)
full  = Image.blend(Image.new("RGB", canvas.size, (255,255,255)), canvas, FULL)
# buffer mask at pixel resolution (soft edge ~4px for a smooth transition)
import json as _json
_bgj = _json.load(open(os.path.join(HERE, "outputs", "gis", "tank_farm_1mile_buffer.geojson")))
_bg = _bgj["features"][0]["geometry"]
def _ring_px(ring):
    return [lonlat_px_abs(la, lo) for lo, la in ring]   # canvas coords (y down)
if _bg["type"] == "Polygon":
    _rings = [_bg["coordinates"][0]]
else:
    _rings = [mp[0] for mp in _bg["coordinates"]]
_mask = Image.new("L", canvas.size, 255)   # start fully faded (mask=0 => faded)
from PIL import ImageDraw, ImageFilter
_dr = ImageDraw.Draw(_mask)
_dr.rectangle([0, 0, canvas.size[0], canvas.size[1]], fill=0)   # canvas coords, y down
for _r in _rings:
    _pts = [(x, y) for x, y in _ring_px(_r)]
    if len(_pts) >= 3:
        _dr.polygon(_pts, fill=255)
_mask = _mask.filter(ImageFilter.GaussianBlur(3))
canvas = Image.composite(full, faded, _mask)
W, H = canvas.size

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon as MplPoly, Circle, FancyArrowPatch
plt.rcParams["font.family"] = "DejaVu Sans"

def px(lat, lon):
    xt, yt = lonlat_px_abs(lat, lon)
    return xt, H - yt

fig = plt.figure(figsize=(13.2, 9.6), dpi=150)
ax = fig.add_axes([0.015, 0.02, 0.615, 0.96])
ax.imshow(canvas, extent=(0, W, 0, H), interpolation="bilinear")
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# fence polygons — red shading proportional to the farm's permitted VOC
for f in features:
    pts = [px(ll[1], ll[0]) for ll in f["ring"]]
    a = 0.15 + 0.45*min(1, f["voc"]/220.0)
    ax.add_patch(MplPoly(pts, closed=True, facecolor=RED,
                         alpha=a, edgecolor="white", linewidth=0.7, zorder=3))

# 1-mile fence-line buffer (union zone) — matches the counted geometry
from matplotlib.patches import PathPatch
from matplotlib.path import Path as MplPath
import shapely.geometry as sg
gj = json.load(open(os.path.join(DATA, "..", "outputs", "gis", "tank_farm_1mile_buffer.geojson")))
gj = json.load(open(os.path.join(HERE, "outputs", "gis", "tank_farm_1mile_buffer.geojson")))
geom = gj["features"][0]["geometry"]
def ring_to_px(ring):
    return [px(la, lo) for lo, la in ring]
if geom["type"] == "Polygon":
    rings = [ring_to_px(geom["coordinates"][0])]
    verts = rings[0]; codes = [MplPath.MOVETO] + [MplPath.LINETO]*(len(verts := verts)-2) + [MplPath.CLOSEPOLY]
else:
    allverts = []; allcodes = []
    for mp in geom["coordinates"]:
        rv = ring_to_px(mp[0])
        allverts += rv
        allcodes += [MplPath.MOVETO] + [MplPath.LINETO]*(len(rv)-2) + [MplPath.CLOSEPOLY]
    verts = allverts; codes = allcodes
path = MplPath(verts, codes)
ax.add_patch(PathPatch(path, fill=False, edgecolor=AMBER, linewidth=1.6, linestyle=(0,(6,4)), alpha=0.9, zorder=4))

# receptors
receptors = list(csv.DictReader(open(os.path.join(HERE, "outputs", "receptor_fenceline_distances.csv"))))
style = {"school": (FOREST, "s", 78), "childcare": (RED, "^", 58), "senior": ("#7b2cbf", "D", 62)}
def grp(c):
    if c == "public school": return "school"
    if c == "senior housing": return "senior"
    return "childcare"
for r in receptors:
    if r["within_1mi_of_any"] != "Y": continue
    c, m, s = style[grp(r["category"])]
    p = px(float(r["lat"]), float(r["lon"]))
    ax.scatter([p[0]], [p[1]], c=c, marker=m, s=s, edgecolors="white", linewidths=0.8, zorder=6)

# facility markers + short labels with leader arrows
VOC_TPY = {"global": 21.9, "citgo": 117.3, "buckeye": 135.4, "gulf_sunoco": 49.9,
           "sprague": 49.9, "pplc": 220.0}  # from each DEP license order
MPP = 156543.03392 * math.cos(math.radians(lat_c)) / 2**Z   # meters per canvas px
for fid, name, addr, flat, flon in FARMS:
    p = px(flat, flon)
    ax.scatter([p[0]], [p[1]], c=AMBER, marker="*", s=420, edgecolors=TEXT, linewidths=0.9, zorder=8)
    dx, dy, ha = LABEL_POS[fid]
    ax.annotate(f"{name}\n{addr} \u00b7 {VOC_TPY[fid]:.0f} tpy", (p[0], p[1]), textcoords="offset points",
                xytext=(dx, dy), ha=ha, va="center", fontsize=9.2, fontweight="bold",
                color="white", zorder=9,
                bbox=dict(boxstyle="round,pad=0.32", fc=FOREST, ec="white", lw=1.0, alpha=0.95),
                arrowprops=dict(arrowstyle="-", color=FOREST, lw=1.1, shrinkA=2, shrinkB=6))

# monitoring stations
for code, mlat, mlon in [(m[0], m[2], m[3]) for m in
        [("POG",0,43.6561,-70.2409),("PWC",0,43.6598,-70.2563),("SPCC",0,43.6292,-70.2955),
         ("SPFS",0,43.6518,-70.2402),("SPMS",0,43.6386,-70.2666),("SPPS",0,43.6389,-70.2555),
         ("SPRB",0,43.6166,-70.3245)][::1]]:
    pass
MON = [("POG",43.6561,-70.2409),("PWC",43.6598,-70.2563),("SPCC",43.6292,-70.2955),
       ("SPFS",43.6518,-70.2402),("SPMS",43.6386,-70.2666),("SPPS",43.6389,-70.2555),
       ("SPRB",43.6166,-70.3245)]
for code, mlat, mlon in MON:
    p = px(mlat, mlon)
    ax.scatter([p[0]], [p[1]], c=PINE, marker="v", s=120, edgecolors="white", linewidths=1.2, zorder=7)
    ax.annotate(code, (p[0], p[1]), textcoords="offset points", xytext=(5, -13),
                fontsize=7.6, fontweight="bold", color=PINE, zorder=7,
                bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.8))

# scale bar (0.5 mi) bottom-left
sb_lat = 43.6190; sb_lon0 = -70.323
p0 = px(sb_lat, sb_lon0); p1 = px(sb_lat, sb_lon0 + 0.5/(69.0*math.cos(math.radians(sb_lat))))
ax.plot([p0[0], p1[0]], [p1[1], p1[1]], color=TEXT, lw=2.5, zorder=10)
for xx in (p0[0], p1[0]):
    ax.plot([xx, xx], [p1[1]-5, p1[1]+5], color=TEXT, lw=2.0, zorder=10)
ax.text((p0[0]+p1[0])/2, p1[1]+10, "0.5 mile", ha="center", fontsize=8.5, color=TEXT, zorder=10,
        bbox=dict(boxstyle="round,pad=0.15", fc="white", ec="none", alpha=0.85))

# ---------- sidebar ----------
lx = 0.655
fig.text(lx, 0.945, "South Portland Tank Farms", fontsize=19, fontweight="bold", color=FOREST)
fig.text(lx, 0.912, "Sensitive Receptors Within One Mile", fontsize=13.5, color=PINE)
fig.text(lx, 0.905, "", fontsize=1)

items = [(FOREST,"s","Public school (7)"), (RED,"^","Child care (25)"),
         ("#7b2cbf","D","Senior housing (9)"), (AMBER,"*","Tank farm (6)"),
         (RED,"grad","Petroleum shading \u221d VOC (22\u2192220 t/yr)"),
         (AMBER,"ring","1-mile fence-line buffer"), (PINE,"v","DEP VOC monitor")]
y = 0.895
for c, m, label in items:
    axl = fig.add_axes([lx, y-0.012, 0.045, 0.024]); axl.axis("off"); axl.set_xlim(0,1); axl.set_ylim(0,1)
    if m == "ring":
        axl.add_patch(Circle((0.5,0.5), 0.42, fill=False, edgecolor=c, linewidth=1.6, linestyle=(0,(5,3))))
    elif m == "grad":
        for ai in (0.22, 0.42, 0.62):
            axl.add_patch(Circle((0.3 + (ai-0.22)*1.35, 0.5), 0.30, facecolor=RED, alpha=ai, edgecolor="none"))
        axl.set_xlim(0, 1); axl.set_ylim(0, 1)
    else:
        axl.scatter([0.5],[0.5], c=c, marker=m, s=150 if m=="*" else 120, edgecolors="white" if m=="v" else "none", linewidths=0.7)
    fig.text(lx+0.055, y, label, fontsize=11, va="center", color=TEXT)
    y -= 0.043

y -= 0.02
fig.text(lx, y, "FACILITIES", fontsize=11, fontweight="bold", color=FOREST); y -= 0.038
fac_lines = ["Global — 1 Clark Rd", "CITGO — 102 Mechanic St", "Buckeye/SPT — 170 Lincoln St",
             "Gulf/Sunoco — 175 Front St", "Sprague — 59 Main St", "Pipe Line — 30 Hill St"]
for s in fac_lines:
    fig.text(lx, y, s, fontsize=9.6, color=TEXT, family="DejaVu Sans")
    y -= 0.031

y -= 0.015
fig.text(lx, y, "KEY FACTS", fontsize=11, fontweight="bold", color=FOREST); y -= 0.04
for s in ["42 sensitive sites within 1 mile of a fence line:",
          "   all 7 public schools · 25 child care · 9 senior housing",
          "Kaler Elementary: 0.04 mi from Pipe Line parcel",
          "Betsy Ross House: adjacent to Gulf/Sunoco parcel",
          "Growing Learners childcare: on Sprague fence line",
          "Licensed VOC caps: ~594 tons/yr total (parcel shading shows each)"]:
    fig.text(lx, y, s, fontsize=9.6, color=TEXT); y -= 0.036


fig.text(lx, 0.065, "V▼  DEP VOC monitors: POG Ocean Gateway · PWC W Commercial ·", fontsize=8.2, color=MUTED)
fig.text(lx, 0.045, "SPCC Cash Corner · SPFS Front St · SPMS Mechanic St ·", fontsize=8.2, color=MUTED)
fig.text(lx, 0.025, "SPPS Pearl St · SPRB Red Bank (sites approximate)", fontsize=8.2, color=MUTED)
fig.text(0.015, 0.008, "Sources: Maine DEP air license orders · OCFS Child Care Choices (9/24/2026) · NCES · SPHA · OpenStreetMap (ODbL). Straight-line fence-line distances, not walking routes. | Protect South Portland · Sept 2026 · data: github.com/cristoslc/south-portland-tank-farms", fontsize=7.2, color=MUTED)
fig.savefig(os.path.join(OUT, "south_portland_tank_farms_map.png"), dpi=150, facecolor="white")
plt.close(fig)
print("static map saved")
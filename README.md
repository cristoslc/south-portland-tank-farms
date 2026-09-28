# South Portland Tank Farms — Sensitive Receptors & Permit Renewals

Research for Protect South Portland quantifying how many public schools, licensed
child care programs, and senior housing facilities sit within one mile of any of
South Portland's six oil tank farms, and tracking each facility's Maine DEP air
license renewal timeline.

## Outputs (start here)

| File | What it is |
|---|---|
| `outputs/TANK_FARM_RECEPTOR_AND_PERMIT_MEMO.md` | **Main report.** Executive summary (FK Grade ~6.4), permit table with official VOC/HAP limits, fence-line counts, address cross-check, human-operator methodology, caveats, regulatory context, references. |
| `outputs/FACTCHECK.md` | Claim-by-claim verification log: section → claim → source → direct evidence quote. Includes §FC-6 documenting every claim removed when the PSP advocacy packet was dropped as a source. |
| `outputs/receptor_fenceline_distances.csv` | **Master dataset.** 171 receptors (7 public schools, 12 senior facilities, 152 child care programs) with lat/lon, distance in miles to each farm's fence line, nearest farm, and within-1-mile flag. |
| `outputs/SouthPortland_TankFarms_Binder.pdf` | 15-page shareable PDF binder: cover + report + fact-check. |
| `outputs/polygon_results.txt` | Full console output of the fence-line analysis (per-farm counts, union lists). |

## Headline findings (as of 2026-09-24)

- **All 7 public schools**, **25 licensed child care programs**, and **9 senior
  housing facilities** lie within 1 mile of at least one tank farm fence line —
  42 sensitive sites total. Address-to-address (conservative) method: 5 / 14 / 6.
- Kaler Elementary is **0.04 mi (~200 ft)** from Portland Pipe Line's Hill St
  parcel; Betsy Ross House sits **directly adjacent** to the Gulf/Sunoco parcel;
  Growing Learners @ Harding St **touches** Sprague's fence line.
- Licensed facility-wide VOC caps at last issuance total **~597 tpy**
  (21.9 Global + 117.3 CITGO + 135.4 Buckeye + 49.9 Gulf + 49.9 Sprague + 220 PPLC).
- Permit renewal windows: **Sprague ~2028** · **CITGO ~2030** · **PPLC air ~2030
  (ch.600 marine renewal already pending, accepted Aug 2025)** · **Buckeye
  nominally expired ~2020, on evergreen** · **Global ~2033** · **Gulf/Sunoco ~2033**.

## Directory layout

```
├── README.md
├── outputs/        Deliverables (report, fact-check, dataset, binder)
├── src/            Reproducible scripts (see "Reproducing" below)
├── data/           Fetched data: OCFS captures, geocode cache, OSM structures
├── sources/        Official DEP license orders + DEP legislative report
└── archive/        Superseded scripts, scratch files, intermediate renders
```

### sources/ — the official record

| File | Contents |
|---|---|
| `A0197HR.pdf` | PPLC Part 70 renewal A-197-70-H-R (Feb 24, 2025) — VOC 220.0 tpy, HAP 9.9/24.9, 11.0 Bgal/yr crude throughput |
| `A0460HR.pdf` | CITGO Part 70 renewal A-460-70-H-R (Nov 5, 2025) — VOC 117.3→104.4 tpy, HAP 5.0 |
| `A0432SRM.pdf` | Global renewal A-432-71-S-R/M (Dec 5, 2023) — VOC 21.9 tpy |
| `A0432PM.pdf` | Global Amendment #2 (Feb 17, 2021) |
| `A0390PRM.pdf` | Gulf renewal A-390-71-P-R/M (Feb 22, 2023) — VOC 49.9, HAP 24.9 |
| `A0390RT.pdf` | Sunoco Midstream multi-program license transfer (2024) |
| `A0179PRM.pdf` | Sprague renewal A-179-71-P-R/M (Mar 2018; scanned) — VOC 49.9, HAP 24.9 |
| `A0179RM.pdf` | Sprague Amendment #2 (Jun 29, 2021) |
| `A0282GR.pdf` | Buckeye/SPT Part 70 renewal A-282-70-G-R (Nov–Dec 2015; scanned) — VOC 135.4, HAP 14.1 |
| `A0282HA.pdf` | Buckeye/SPT Amendment #1 (Nov 1, 2016) |
| `A0282_fenceline.pdf`, `A0282_2026Q1.pdf` | Buckeye ch.171 fenceline reports Q1 2025 & Q1 2026 (still citing the 2015 licenses) |
| `MEDEP_tank_report_2021.pdf` | DEP legislative report, "Measurement and Control of Emissions from Aboveground Petroleum Storage Tanks" (Jan 2021) |
| `A0202LR.pdf` *(archive/)* | Buckeye **Bangor** license — pulled to rule out a false match; not a SoPo source |

## Reproducing the analysis (human-operator path)

The full browser-and-spreadsheet procedure — no coding required — is §5.3 of the
report (search NCES/OCFS/SPHA, geocode, pull OSM fence lines via overpass-turbo.eu,
measure in QGIS, then permit research in DEP's license archive). Automated
equivalents live in `src/`:

```bash
python3 src/geocode.py "87 Thompson Street South Portland ME"   # cached geocoder
export LD_LIBRARY_PATH=~/chrome-libs/usr/lib/x86_64-linux-gnu    # Chromium libs (see below)
python3 src/ccc_union.py          # OCFS search x6 tank farms -> data/ccc_union.json
python3 src/polygon_analysis.py   # fence-line distances -> outputs/polygon_results.txt
python3 src/export_datasets.py    # -> outputs/receptor_fenceline_distances.csv
python3 src/build_binder.py       # -> outputs/SouthPortland_TankFarms_Binder.pdf
```

**Chromium note (OCFS search only):** Playwright's bundled Chromium needs system
libraries absent on this machine. They were provisioned by extracting Debian .debs
(`~/debs` + libcups/avahi from ftp.debian.org) into `~/chrome-libs` and setting
`LD_LIBRARY_PATH` as above. `src/ccc_search.py <lat> <lon> "<address>" <out.html>`
drives the OCFS page (injects lat/lon into hidden form fields, checks all four
provider types, submits).

## Data provenance

- Public schools: NCES CCD directory, South Portland district 2312330 (2025-26)
- Child care (centers + family homes): Maine OCFS "Child Care Choices" search
  (search.childcarechoices.me), 6 searches 2026-09-24, union = 166 programs;
  raw captures in `data/ccc_*.html`
- Senior housing: SPHA (spha.net) + state-licensed AL/RCF homes
- Fence lines: OpenStreetMap via self-hosted Overpass (osm.cristoslc.com, Maine daily extract), base 2026-09-27 (`data/overpass_tanks.json`)
- Geocodes: Nominatim, cached in `data/geocode_cache.json`

## Verification & known limits

- Every factual claim in the memo is logged in `outputs/FACTCHECK.md` with its
  source and a direct quote. The Protect South Portland advocacy packet is
  intentionally **not** used as a source (see FACTCHECK §FC-6).
- Fence-line geometry is community-mapped OSM; city assessor GIS parcels would be
  the parcel-exact gold standard. Distances are straight-line, not walking.
- Distances < ~0.01 mi mean the receptor geocode sits on/inside the mapped parcel
  edge ("directly adjacent").
- Buckeye's renewal-application status is the memo's one inference (2015 order +
  evergreen rule + no newer public document + fenceline reports through Q1 2026);
  confirm via DEP Bureau of Air Quality (207-287-7688) or a FOAA request.
- Sprague and Buckeye license figures were read via OCR from scanned orders.
# South Portland Tank Farms — Public Data

Supporting dataset for Protect South Portland's research on oil tank farm
proximity to sensitive receptors (public schools, licensed child care programs,
senior housing) and Maine DEP air-license renewal timelines.

The report and fact-check log are published here in full; the DEP license-order PDFs are public record at maine.gov/dep/ftp/AIR/licenses/ and are cited (not re-hosted) in the References section.

## What's here

| File | Contents |
|---|---|
| `outputs/TANK_FARM_RECEPTOR_AND_PERMIT_MEMO.md` | **Full research report** — executive summary, permit table with official VOC/HAP limits from each DEP license order, fence-line and address-based counts, human-operator methodology, caveats, and a numbered references section with DEP archive URLs. |
| `outputs/FACTCHECK.md` | **Claim-by-claim fact-check log** — for every claim: report section → claim → source → direct evidence quoted from the source document. Includes the removal trail for advocacy-packet-sourced claims (§FC-6). |
| `data/receptor_fenceline_distances.csv` | **Master dataset** — 171 receptors (7 public schools, 12 senior facilities, 152 child care programs) with lat/lon, distance in miles to each of 6 tank-farm fence lines (OpenStreetMap parcels/tanks), nearest farm, and within-1-mile flag. |
| `data/ccc_union.json` | 166 unique licensed child care programs from Maine OCFS "Child Care Choices" search (name, address, type, star rating). Includes family child care homes. |
| `data/overpass_tanks.json` | OpenStreetMap structures: 113 storage-tank polygons + 37 industrial parcel polygons, bbox 43.62–43.66 / −70.31 to −70.22. |
| `data/geocode_cache.json` | Nominatim geocodes for all receptor + facility addresses. |
| `outputs/polygon_results.txt` | Full distance-matrix and per-farm count output. |
| `src/` | Reproducible scripts (geocoding, OCFS search union, polygon distance analysis, dataset export). |
| `README.md` | Methodology summary, data provenance, known limitations. |

## Headline findings

- All 7 public schools, 25 licensed child care programs, and 9 senior housing
  facilities fall within 1 mile of at least one tank farm fence line —
  42 sensitive sites total.
- Kaler Elementary: 0.04 mi from Portland Pipe Line's parcel. Betsy Ross House
  (SPHA senior housing): directly adjacent to Gulf/Sunoco's parcel.
- Facility-wide VOC license caps total ~597 tpy across the six facilities.
- Permit renewals: PPLC ch.600 marine renewal pending (accepted Aug 2025);
  Sprague ~2028; CITGO ~2030; Global/Gulf/Sunoco ~2033; Buckeye nominally
  expired ~2020, operating under Maine's evergreen rule.

## Reproducing

```bash
python3 src/geocode.py "87 Thompson Street South Portland ME"
python3 src/polygon_analysis.py
python3 src/export_datasets.py
```

Full human-operator procedure (no coding required): §5.3 of the project report
(private). Automated scripts read from `data/` and write to `outputs/`.

## Method & caveats

- **Distances are straight-line** (fence-line method: receptor point to nearest
  OSM industrial parcel / storage-tank polygon edge; address-to-address as
  conservative cross-check). Not walking distances.
- **Fence-line geometry is community-mapped OSM**; City of South Portland
  assessor GIS parcels would be the parcel-exact gold standard.
- Distances < ~0.01 mi mean the receptor geocode sits on/inside the mapped
  parcel edge ("directly adjacent").
- OCFS search includes programs with expired/conditional licenses (its own
  disclosure); captured 2026-09-24. Listings change over time.
- Permit data from Maine DEP license orders (maine.gov/dep/ftp/AIR/licenses/),
  verified claim-by-claim with direct evidence quotes in the private fact-check
  log. Sprague (2018) and Buckeye (2015) orders are scanned; figures read via OCR.
- Buckeye renewal status is the analysis' one inference (2015 order + evergreen
  rule + no newer public document + fenceline reports through Q1 2026); confirm
  via DEP Bureau of Air Quality (207-287-7688) or a FOAA request.

## License & attribution

Data: CC BY 4.0. Scripts: MIT.
Sources: Maine DEP license orders (public record); OCFS Child Care Choices
(state licensing data); NCES (federal); OpenStreetMap (ODbL 1.0).
AI-assisted compilation under human steering (see private report's disclosure).

---
*Questions or corrections: Protect South Portland — protectsouthportland.com*
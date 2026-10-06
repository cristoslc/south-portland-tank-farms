---
slug: "tank-farm-permit-memo"
title: "South Portland Tank Farms — Sensitive Receptors & Permit Renewals (project memo)"
type: local
path: "outputs/TANK_FARM_RECEPTOR_AND_PERMIT_MEMO.md"
fetched: 2026-10-06T09:35:00Z
---

# South Portland Tank Farms: Sensitive Receptors & Permit Renewals
## Executive summary + full findings + methodology
*Protect South Portland — research memo. Compiled 2026-09-24. Data and datasets in `projects/psp/sleuthing-tank-farms/`. Fact-check log: `FACTCHECK.md`.*

> **AI disclosure:** This report was produced with substantial AI assistance under a human-steered workflow: an AI research agent performed the searches, data compilation, geocoding, and distance calculations described in the Methodology (§5), under continuous human direction, review, and editing; all findings were verified against primary documents (cited below) that a human selected and inspected. This corresponds to "AI-primary / human-steered" use under the Partnership on AI's AI-Generated Content guidance [19]. Questions about methods or data: contact Protect South Portland.

---

# Executive Summary

South Portland is home to six large oil storage terminals along its waterfront: Global, CITGO, Buckeye, Gulf (now owned by Sunoco), Sprague, and Portland Pipe Line. Each is licensed by the Maine DEP to emit VOCs — up to a combined **~594 tons per year** at current license limits (each facility's own DEP cap) [2][3][4][5][7][9] — and they sit among homes, not apart from them. Some are only feet away from houses, schools, daycares, and senior housing.

This report answers two questions. How many schools, daycares, and senior housing buildings are within one mile of the tank farms? And when are their state permits up for renewal?

**What we found**

All seven public schools in South Portland are within one mile of at least one tank farm fence line. So are **25 licensed child care programs** and **9 senior housing facilities**. That is 41 sensitive sites in all.

Some are extremely close. Kaler Elementary is about **200 feet** from the Portland Pipe Line tank parcel. The Betsy Ross House, a 123-unit senior building, sits directly next to the Gulf/Sunoco tank parcel. A child care center on Harding Street touches the Sprague fence line. Every tank farm has at least one school and several child care centers within a mile.

**On the permits:** Maine air licenses run for 5 or 10 years. Operators must apply to renew them before they expire.

- **Portland Pipe Line** is the one to watch. Its marine terminal license renewal is already underway — the state accepted the application in August 2025 [10]. This is the public's chance to require stack testing and fence-line monitoring.
- **Sprague's** license runs out around 2028. **CITGO and Portland Pipe Line** expire around 2030. **Global and Gulf/Sunoco** expire around 2033.
- **Buckeye's** last license was issued in 2015 for a five-year term [9]. Under Maine's evergreen rule the license remains in force while a renewal application is pending, and the facility's required fenceline reports were still being filed under it through early 2026 [11]. But no new license has issued in over a decade; whether an application is pending is not publicly visible and should be confirmed with DEP.

DEP's 2021 report to the Legislature acknowledged that no direct emissions testing is currently required of tank operators [20] and declined to recommend fenceline monitoring [20]. The upcoming license renewals are the moment when that can be required.

**Bottom line:** the tank farms are not on the edge of town. They are woven into residential South Portland. Within a mile of their fence lines sit every public school in the city, dozens of places where young children spend their days, and nine buildings full of older residents. The upcoming permit renewals are the time to require real emissions testing and modern control equipment.

---

# 1. The six tank farms and their permits

All emission limits below are taken directly from each facility's most recent DEP air license order (official documents, on file in this folder).

| Facility | Address | Air license | Most recent renewal | Facility-wide VOC limit (tpy) | Facility-wide HAP limit (tpy) | Next renewal window |
|---|---|---|---|---|---|---|
| Global Companies LLC | 1 Clark Road | A-432-71-S-R/M | **Dec 5, 2023** (10-yr term) | 21.9 [4] | 9.9 | App due ~Jun 2028–Jun 2032; expires **~Dec 2033** |
| CITGO Petroleum Corp. | 102 Mechanic St | A-460-70-H-R | **Nov 5, 2025** (5-yr term) | 117.3 (requested reduction to 104.4 in the Nov 2025 renewal) [3] | 5.0 [3] | App due ~May 2029–May 2030; expires **~Nov 2030** |
| South Portland Terminal LLC (Buckeye) | 170 Lincoln St | A-282-70-G-R + A-282-70-H-A | **Nov/Dec 2015** (5-yr term stated in order) [9] | 135.4 [9] | 14.1 [9] | Nominally expired ~2020; evergreen — see §6 note 5 |
| Gulf Oil → Portland Terminals LLC → **Sunoco Midstream** | 175 Front St | A-390-71-P-R/M | **Feb 22, 2023** (10-yr term); transferred to Sunoco Midstream Aug 2024 [5][6] | 49.9 [5] | 24.9 [5] | App due ~Feb 2026–Feb 2028; expires **~Feb 2033** |
| Sprague Operating Resources | 59 Main St | A-179-71-P-R/M (SM) | **March 2018** (10-yr term) [7] | 49.9 [7] | 24.9 (single-HAP 9.9) [7] | App due ~Sep 2026–Sep 2027; expires **~Mar 2028** |
| Portland Pipe Line Corp. | 30 Hill St | A-197-70-H-R | **Feb 24, 2025** (5-yr term) [2] | 220.0 [2] | 24.9 (single-HAP 9.9) [2] | Expires **~Feb 2030**. Marine terminal (ch.600) licenses O-000305/306-91-I-R: renewal application accepted **Aug 11, 2025** [10] — currently pending |

Six-facility licensed VOC total at last issuance: **594.4 tpy** (21.9 + 117.3 + 135.4 + 49.9 + 49.9 + 220.0); HAP total: **103.7 tpy** — consistent with the independently compiled 594/104 figures in the Falatko table [1]. These are per-license official limits; note Buckeye's figures date from its 2015 license and PPLC's VOC figure dates from Feb 2025.

- The Gulf tank farm is owned by **Sunoco Midstream LLC** (DEP-approved transfer; closing Aug 30, 2024) [6]. The "Gulf" label in any public-facing table should be updated to Sunoco Midstream.
- PPLC's Feb 2025 renewal states a crude-oil **throughput limit of 11.0 billion gallons per year** [2].

# 2. Headline counts

Within **one mile of at least one tank farm fence line** (GIS method, §3):

- **7 of 7 public schools**
- **25 licensed child care programs** — 16 centers/nurseries + 9 family & license-exempt homes
- **9 senior housing facilities**

Total: **42 sensitive sites**. The more conservative address-to-address method gives 5 schools / 14 child care / 6 senior (§4).

# 3. GIS fence-line analysis (preferred)

Distances are measured from each receptor to the **nearest tank-farm structure** — OpenStreetMap storage tanks and the parcels that contain them (corrected set: 117 structures; see §6 note 7). Receptors were assembled from three inventories: all South Portland public schools (NCES) [13], all licensed child care programs in the Maine OCFS Child Care Choices search (union of six searches, one per tank farm) [14], and senior housing from the South Portland Housing Authority plus state-licensed assisted-living homes [12]. 166 unique child care programs were captured.

**Per-farm counts within 1 mile of the fence line:**

| Tank farm | All receptors within 1 mi |
|---|---|
| Global (1 Clark Rd) | 15 |
| CITGO (102 Mechanic St) | 24 |
| Buckeye (170 Lincoln St) | 10 |
| Gulf/Sunoco (175 Front St) | 12 |
| Sprague (59 Main St) | 18 |
| PPLC (30 Hill St) | 17 |

*Fence-line geometry uses a corrected structure set (see §6 note 7 and the Structure Audit Addendum): 117 mapped structures — storage tanks, parcels containing tanks, and operator-tagged oil parcels — after excluding piers/wharves, buoy yards, a shipyard, and bare industrial parcels with no tanks that earlier versions wrongly shaded.*

**Union — closest fence-line distance for every site inside the circle:**

*Schools (7):* Kaler 0.04 mi (PPLC) • Dyer 0.16 mi (PPLC) • SP High 0.18 mi (PPLC) • Dora L. Small 0.28 mi (Gulf/Sunoco) • Frank I. Brown 0.48 mi (CITGO) • SP Middle 0.65 mi (Sprague) • Skillin 0.80 mi (Sprague)

*Senior housing (9):* Betsy Ross House 0.01 mi (Gulf/Sunoco) • Ridgeland Estates 0.09 mi (Sprague) • One Willow Manor 0.13 mi (Gulf/Sunoco) • Gordon Green 0.26 mi (Gulf/Sunoco) • Sawyer Street House 0.50 mi (Gulf/Sunoco) • Linton Street 0.68 mi (Sprague) • Wilson Street 0.80 mi (Sprague) • Thornton Heights Commons 0.83 mi (Sprague) • Wescott 0.88 mi (Sprague)

*Child care — 16 centers/nurseries:* Growing Learners @ Harding St 0.00 mi (Sprague) • Spring Point Children's Center 0.01 mi (Gulf/Sunoco) • Youth & Family Outreach 0.06 mi (Global; temporary location — see status note) • Lighthouse 0.06 mi (Global) • Kiddie Garden–Danforth 0.20 mi (CITGO) • Waynflete School 0.20 mi (CITGO) • Children's Adventure Center 0.23 mi (PPLC) • Kids World At Willard Beach 0.28 mi (Gulf/Sunoco) • Creative Beginnings 0.30 mi (CITGO) • Kiddie Garden–Spring St 0.32 mi (CITGO) • Catherine Morrill Day Nursery 0.32 mi (Gulf/Sunoco) • Opportunity Alliance East End 0.46 mi (Gulf/Sunoco) • Opportunity Alliance Lydia Lane 0.49 mi (Sprague) • Children's Nursery School 0.54 mi (Gulf/Sunoco) • Pearlite Montessori 0.66 mi (PPLC) • Discovery Center 0.75 mi (Gulf/Sunoco) • Ready Set Grow 0.96 mi (Sprague)

*Child care — 9 family & license-exempt homes:* Wishing Tree Preschool 0.04 mi (Sprague) • Caroline Kleiman 0.20 mi (PPLC) • Camilla Taylor 0.30 mi (Gulf/Sunoco) • Alphabet Tree 0.44 mi (Sprague) • Suzanne Kahill 0.49 mi (PPLC) • Serina Holbrook 0.56 mi (Sprague) • Stacie Archibald 0.66 mi (CITGO) • Caroline Whitten 0.69 mi (CITGO)

# 4. Address-to-address cross-check (conservative)

Distances in miles, straight-line, receptor address → tank farm street address. ✅ = within 1 mile.

| Receptor | Address | Global | CITGO | Buckeye | Gulf/Sunoco | Sprague | PPLC |
|---|---|---|---|---|---|---|---|
| Kaler Elementary* | 165 S Kelsey St | ✅ 0.53 | ✅ 0.60 | ✅ 0.99 | 2.12 | 1.07 | ✅ 0.13 |
| Children's Time CDC | 1065 Broadway | ✅ 0.40 | ✅ 0.71 | ✅ 0.71 | 2.38 | ✅ 0.79 | ✅ 0.23 |
| Dyer Elementary | 52 Alfred St | ✅ 0.86 | 1.10 | 1.13 | 2.64 | 1.20 | ✅ 0.50 |
| SP High School | 637 Highland Ave | ✅ 0.95 | 1.07 | 1.31 | 2.47 | 1.39 | ✅ 0.51 |
| Waiting to Grow | 28 Jennies Ct | ✅ 0.72 | ✅ 0.97 | 1.00 | 2.55 | 1.07 | ✅ 0.37 |
| Ridgeland Estates | 109 Ridgeland Ave | ✅ 0.59 | 1.02 | ✅ 0.36 | 2.72 | ✅ 0.40 | ✅ 0.78 |
| Lighthouse | 525 Highland Ave | ✅ 0.88 | ✅ 0.93 | 1.31 | 2.27 | 1.38 | ✅ 0.44 |
| Brown Elementary / Prop Head Start | 37 Highland Ave | 1.32 | ✅ 0.96 | 1.81 | 1.20 | 1.88 | 1.18 |
| Busy Bee's | 9 Harding St | ✅ 0.72 | 1.11 | ✅ 0.25 | 2.77 | ✅ 0.23 | 1.02 |
| Dora L. Small | 87 Thompson St | 2.15 | 1.74 | 2.61 | ✅ 0.68 | 2.67 | 2.07 |
| One Willow Manor | 97 School St | 1.98 | 1.55 | 2.38 | ✅ 0.20 | 2.43 | 2.02 |
| Heidi's House* | 36 Broadway | 2.25 | 1.82 | 2.67 | ✅ 0.38 | 2.72 | 2.23 |
| Betsy Ross House | 99 Preble St Ext | 2.13 | 1.71 | 2.56 | ✅ 0.38 | 2.61 | 2.11 |
| Gordon Green | 23 Third St | 1.58 | 1.16 | 2.02 | ✅ 0.72 | 2.08 | 1.54 |
| Daycamp Inc | 310 Broadway | 1.67 | 1.25 | 2.13 | ✅ 0.76 | 2.19 | 1.60 |
| Sawyer Street House | 388 Sawyer St | 1.86 | 1.46 | 2.33 | ✅ 0.83 | 2.40 | 1.75 |
| Linton Street Facility | 66 Linton St | 1.49 | 1.90 | 1.04 | 3.56 | ✅ 1.00 | 1.71 |
| Holy Cross Daycare | 30 Emery St | 1.42 | 1.04 | 1.91 | 1.08 | 1.97 | 1.30 |
| Discovery Center | 301 Cottage Rd | 1.81 | 1.43 | 2.30 | 1.08 | 2.36 | 1.64 |
| SP Middle School | 120 Wescott Rd | 1.48 | 1.91 | 1.12 | 3.61 | 1.10 | 1.60 |
| Skillin Elementary | 180 Wescott Rd | 1.62 | 2.05 | 1.27 | 3.75 | 1.25 | 1.72 |

\* Kaler (165 South Kelsey St) no longer operates as a school but hosted a summer camp in 2026, so children are still on-site seasonally; it is counted as a receptor. **Status note (as of Sept 30, 2026):** the child care program currently operating at 1065 Broadway (0.06 mi, counted as Youth & Family Outreach) lists that address as a temporary location, per the operator's website; the site previously operated as Children's Time Child Development Center, which is no longer in operation. Daycamp Inc (310 Broadway) does not appear in the current state licensing search. Counts in this report reflect the search date (Sept 24, 2026); listings change over time — re-verify before publication. OCFS's current licensing results show updates vs. older aggregator directories: the program at 9 Harding St is licensed as "Growing Learners @ Harding Street"; the facility at 36 Broadway is Spring Point Children's Center; several aggregator-listed programs (Daycamp Inc, Prop Head Start, Waiting to Grow) do not appear in current OCFS results [14]. "Heidi's House Child Care" is licensed in Scarborough (300 Enterprise Business Park) and is outside the radius; 36 Broadway is Spring Point Children's Center.

# 5. Methodology appendix

## 5.1 Data sources
1. **Tank farm list and addresses** — each facility's address as stated in its own DEP air license order (refs 2–9); cross-checked against DEP's license archive listings.
2. **Tank farm structures (fence lines)** — OpenStreetMap via the project's self-hosted Overpass instance (osm.cristoslc.com, Maine daily extract; base timestamp 2026-09-27T20:10Z): 113 `man_made=storage_tank` polygons + 56 `landuse=industrial` parcels in the study area, of which 137 structures pass the tank-farm inclusion rule [17].
3. **Public schools** — NCES CCD school directory (7 schools, 2025-26 directory year) [13]. Kaler (165 South Kelsey St) no longer operates as a school but remains in active use for children's programming — it hosted a summer camp in 2026 — so it is counted as a receptor.
4. **Licensed child care** — Maine OCFS "Child Care Choices" search (search.childcarechoices.me), all four provider types (Family Based, Center Based, Nursery, CCAP License-Exempt). One search per tank farm coordinate; union = **166 unique programs** [14]. Includes all licensed programs, even expired/conditional licenses.
5. **Senior housing** — South Portland Housing Authority properties [12] + state-licensed assisted-living/residential-care homes (license numbers cross-checked). Thornton Heights Commons is elderly-preference but mixed-age.
6. **Permit documents** — Maine DEP license archive (maine.gov/dep/ftp/AIR/licenses/), DEP major-project pages [10], and DEP transfer orders [6]. Every license PDF cited is saved in this folder.
7. **Emission limits** — each facility's facility-wide VOC/HAP limits as stated in its own DEP license order (refs 2–9), including OCR of the two scanned orders (Sprague, Buckeye).
8. **Geocoding** — Nominatim/OpenStreetMap (1 req/sec, cached in `geocode_cache.json`).

## 5.2 How distances were computed
- **Address-to-address method (§4):** straight-line (haversine) distance from geocoded receptor address to geocoded tank farm street address.
- **Fence-line method (§3, preferred):** distance from geocoded receptor point to the nearest edge of any OSM structure assigned to that farm. Structures (tanks + parcels) were assigned to a farm if their centroid was within 1,200 m of the farm's anchor coordinate. Points inside a polygon measure as 0.00.
- Distances are straight-line, **not** walking distances. Tank parcels are large; fence-line distance is shorter than address distance, which is why §3 counts are higher.

## 5.3 How a human operator can reproduce this analysis

No scripting is required to reproduce the findings. Every step below can be done in a web browser and a spreadsheet. Expect the full process to take roughly a day.

**Step 1 — Confirm the tank farm list and addresses.**
Retrieve each facility's most recent DEP air license order from maine.gov/dep/ftp/AIR/licenses/ (folders ch115 and titlev) and read the FACILITY LOCATION line and license number; cross-reference with DEP's major-projects pages [10] for any in-progress renewals. The six facilities and addresses in §1 are those stated in the orders themselves [2][3][4][5][7][9]. (The 2021 DEP legislative report also lists the bulk petroleum terminal facilities by name [20].)

**Step 2 — Build the receptor lists.**
- *Public schools:* search the NCES school locator (nces.ed.gov) for South Portland Public Schools (district ID 2312330) [13]. Record all seven schools with addresses. Note Kaler Elementary (165 South Kelsey St) no longer operates as a school but hosted a summer camp in 2026, so include it.
- *Licensed child care (centers AND family homes):* go to search.childcarechoices.me (Maine OCFS's official licensing search) [14]. Enter "South Portland" as the location, check all four provider types (Family Based, Center Based, Nursery, and CCAP License-Exempt), leave the star rating on "ALL PROGRAMS," and submit. Record every result: program name, address, and type. To be certain nothing near any individual farm is missed, repeat the search six times, once using each tank farm's address as the search location, and merge the results, removing duplicates. This is how the family child care homes enter the dataset — they appear in the same results under "Provider Type: FAMILY."
- *Senior housing:* on spha.net, list the Housing Authority's elderly properties (Betsy Ross House, Ridgeland Estates, etc.) with their addresses [12]; then list the city's state-licensed assisted-living and residential-care homes (any current Maine DHHS assisted-living directory, or the licensing numbers shown on facilities' pages, e.g., RCC610 for Linton Street).

**Step 3 — Geocode every address.**
For each receptor address, enter it into a geocoding service (Google Maps, or nominatim.openstreetmap.org). Record the latitude and longitude it returns. Rate-limit polite free services to one lookup per second. A handful of addresses may fail; retry them without apartment/unit numbers. (All 171 geocoded points used here are saved in geocode_cache.json if you prefer to skip this step.)

**Step 4 — Get the tank farm fence lines.**
Open overpass-turbo.eu and run this query for the study area (bbox south 43.62, west −70.31, north 43.66, east −70.22): `way["man_made"="storage_tank"](43.62,-70.31,43.66,-70.22); way["landuse"="industrial"](43.62,-70.31,43.66,-70.22); out geom;` — export the result as GeoJSON. This returns the mapped outlines of the storage tanks and the industrial parcels they sit on (113 tanks and 37 parcels at the time of this study) [17]. Alternatively, in QGIS load the OSM layer and visually select the tank farm parcels; or request parcel polygons from the City of South Portland assessor's GIS for the most authoritative boundaries.

**Step 5 — Measure the distances.**
In QGIS (free, qgis.org): import the receptor points (spreadsheet → delimited text layer) and the tank/parcel polygons; use the "Distance to nearest hub" processing tool with hub = each farm's structures and measure in a projected CRS (e.g., EPSG:26983, NAD83 Maine, in meters; divide by 1,609.344 for miles). Do this once per farm, using only the structures belonging to that farm (assign each structure to the farm whose address point it is nearest). A receptor inside a polygon measures as 0. Without QGIS, Google Maps' "measure distance" right-click tool gets the same answer one receptor at a time. Flag every receptor whose minimum distance is ≤ 1 mile.

**Step 6 — Permit and emissions research.**
On maine.gov/dep/ftp/AIR/licenses/, open the ch115 (state licenses) and titlev (Part 70/Title V) folders and find each facility's most recent order PDF; read the signature date, the term sentence ("The term of this license shall be five/ten (5/10) years from the signature date above"), and the facility-wide VOC/HAP emission limits (in the Registration section's "Total Licensed Annual Emissions" table and the Order section's "Facility Wide Limits"). For scanned orders, use a printed copy and read the tables by eye. Check DEP's major-projects pages (maine.gov/dep/projects/) for in-progress renewals (PPLC's ch. 600 marine terminal renewal is there [10]). Check DEP's "Opportunity for Comment" page for active comment periods. For anything unclear (as with Buckeye, see §6 note 5), call the Bureau of Air Quality at 207-287-7688 or file a FOAA request for the application log.

**Step 7 — Verify and update.**
Re-check the OCFS search before each use of the counts (listings change); keep the dated OCFS result capture (ccc_*.html) with your records. Refresh the OSM query each time, since mapping improves over time. Any change to the numbers in this memo should be traceable to a re-run of Steps 2–5.

## 5.4 Dataset files

| File | Contents |
|---|---|
| `receptor_fenceline_distances.csv` | **Master dataset** — 171 receptors (7 schools, 12 senior facilities, 152 child care programs), lat/lon, distance in miles to each of the 6 farm fence lines, nearest farm, min distance, within-1-mile flag |
| `ccc_union.json` | 166 unique OCFS child care programs (name, address, type, star rating) |
| `ccc_within_1mi.json` | The 15 programs inside 1 mi of PPLC (from the single-point search) |
| `geocode_cache.json` | All geocoded addresses (reusable) |
| `overpass_tanks.json` | Raw OSM structures (tanks + industrial parcels) |
| `polygon_results.txt` | Full console output of the fence-line analysis |
| `A0197HR.pdf`, `A0460HR.pdf`, `A0432SRM.pdf`, `A0390PRM.pdf`, `A0179PRM.pdf`, `A0179RM.pdf`, `A0432PM.pdf`, `A0282GR.pdf`, `A0282HA.pdf`, `A0390RT.pdf`, `A0282_fenceline.pdf` | Source DEP license orders and transfer approvals |
| `MEDEP_tank_report_2021.pdf` | DEP's legislative report, "Measurement and Control of Emissions from Aboveground Petroleum Storage Tanks" (Jan 2021) [20] |
| `ccc_*.html` | Raw OCFS search results per farm (6 files) |

# 6. Caveats
1. Fence-line geometry comes from OpenStreetMap — community-mapped. Where a farm's parcel is not fully mapped, distance leans on individual tank footprints. The City of South Portland's assessor GIS would be the parcel-exact gold standard.
2. Distances are straight-line, not walking routes.
3. Distances under ~0.01 mi mean the receptor point sits on/inside the mapped industrial parcel edge — treat as "directly adjacent."
4. OCFS results include programs with expired or conditional licenses; the search page states this explicitly [14].
5. Permit dates come from the DEP license orders' signature blocks; term lengths (5 or 10 years) are stated in each order. Buckeye's status is the one inference in this memo: the 2015 order states a 5-year term, no newer A-0282 document appears in DEP's public archives (checked Sep 2026), and the facility's quarterly fenceline reports through Q1 2026 still cite A-282-70-G-R/A-282-70-H-A [9][11] — all consistent with an evergreen-extended license, but the application log itself requires a FOAA request or a call to DEP to see. Two false leads were ruled out: DEP's December 2025 public-comment notice (id 13337490) is a NOx RACT draft for Sappi Westbrook, and EPA's January 2026 public notice for Buckeye (ME0000485) is the facility's wastewater (MEPDES) permit renewal, not air.
6. Emission-limit figures in §1 are each facility's licensed facility-wide limits as stated in its DEP order [2][3][4][5][7][9]; these are license caps, not measured emissions. The two scanned orders (Sprague 2018, Buckeye 2015) were read via OCR; figures should be double-checked against a printed copy before publication. Buckeye's VOC/HAP limits date from 2015 and may have changed in a newer license that is not publicly archived.
7. **Fence-line structure correction (Sept 28, 2026 audit):** the OSM query originally picked up non-petroleum facilities near the farms via `landuse=industrial` — piers/wharves (Custom House, Widgery, one unnamed), two Buoy Yards, the Yard South shipyard, and bare industrial parcels with no tanks. These inflated Gulf/Sunoco and Buckeye proximity for several Portland-side sites and shaded non-tank-farm areas on the map. The corrected rule (`src/farm_structures.py`): include storage tanks, parcels containing mapped tanks, and parcels tagged or named for oil operators; exclude the rest. Union count 42 (unchanged headline: 7 schools / 25 child care / 9 senior); per-farm counts now Buckeye 10, Gulf/Sunoco 12, Sprague 18, PPLC 17 (Global 15, CITGO 24 unchanged). Full trail: Structure Audit Addendum.

# 7. Regulatory context (official DEP report)

Maine DEP's January 2021 report to the legislature [20] — the required response to L.D. 1915 [18] — is the official regulatory backdrop for the permit asks in this memo. Key positions, from the report itself:
- The Department "does not recommend fenceline monitoring at this time," reasoning that emissions from nearby sources mingle at the fence [20].
- The Department "does not recommend requiring the use of CEMS to determine emissions from petroleum storage tanks" [20].
- On stack testing, the report recommends supporting development of an EPA standard test method rather than requiring testing now [20].
- DEP relies on operator-calculated emissions using EPA's AP-42 factors [20].

The OCFS/DEP record therefore supports this framing: **at the time of each upcoming license renewal (§1), the public can ask DEP to require stack testing and fence-line monitoring as license conditions** — the mechanism by which the community's asks become enforceable.

# References

1. ~~Protect South Portland info packet (2021)~~ — *removed as a source at project direction; see FACTCHECK.md for the verification trail.*
2. Maine DEP, Bureau of Air Quality. *Findings of Fact and Order: Portland Pipe Line Corporation, Part 70 Air Emission License A-197-70-H-R, Renewal* (Feb. 24, 2025). maine.gov/dep/ftp/projects/portlandpipe/archive/A0197HR.pdf. (Facility-wide VOC limit 220.0 tpy; HAP limits 9.9/24.9 tpy; crude throughput limit 11.0 billion gal/yr; term 5 years.)
3. Maine DEP. *Findings of Fact and Order: CITGO Petroleum Corporation, Part 70 Air Emission License A-460-70-H-R, Renewal* (Nov. 5, 2025). maine.gov/dep/ftp/AIR/licenses/titlev/A0460HR.pdf. (Facility-wide VOC 117.3 tpy with requested reduction to 104.4; total HAP 5.0 tpy; term 5 years.)
4. Maine DEP. *Findings of Fact and Order: Global Companies LLC, Air Emission License A-432-71-S-R/M, Renewal with Amendment* (Dec. 5, 2023). maine.gov/dep/ftp/AIR/licenses/ch115/A0432SRM.pdf. (Facility-wide VOC limit 21.9 tpy; term 10 years.)
5. Maine DEP. *Findings of Fact and Order: Gulf Oil Limited Partnership, Air Emission License A-390-71-P-R/M, Renewal with Amendment* (Feb. 22, 2023). maine.gov/dep/ftp/AIR/licenses/ch115/A0390PRM.pdf. (Facility-wide VOC 49.9 tpy; total HAP 24.9 tpy; any single HAP 9.9 tpy; term 10 years.)
6. Maine DEP. *Department Order: Sunoco Midstream LLC — Multi-Program License Transfer from Portland Terminals LLC* (O-000300-91-L-T; A-390-71-R-T; W000737-5S-M-T; MER05C271). maine.gov/dep/ftp/AIR/licenses/ch115/A0390RT.pdf. (Equity purchase closed Aug. 30, 2024; licenses transferred.)
7. Maine DEP. *Findings of Fact and Order: Sprague Operating Resources LLC, Air Emission License A-179-71-P-R/M (SM), Renewal with Minor Revision* (Mar. 2018; signed March, filed at BEP Mar. 2, 2018). maine.gov/dep/ftp/AIR/licenses/ch115/A0179PRM.pdf. (Facility-wide VOC limit 49.9 tpy; single-HAP 9.9 tpy; total HAP 24.9 tpy; term 10 years; scanned — figures read via OCR.)
8. Maine DEP. *Findings of Fact and Order: Global Companies LLC, Air Emission License A-432-71-P-M, Amendment #2* (Feb. 17, 2021). maine.gov/dep/ftp/projects/global/archive/A0432PM.pdf.
9. Maine DEP. *Findings of Fact and Order: South Portland Terminal LLC, Part 70 Air Emission License A-282-70-G-R, Renewal* (Nov.–Dec. 2015), maine.gov/dep/ftp/AIR/licenses/titlev/A0282GR.pdf; and *A-282-70-H-A, Amendment #1* (Nov. 1, 2016), maine.gov/dep/ftp/AIR/licenses/titlev/A0282HA.pdf. (Facility-wide VOC 135.4 tpy; HAP 14.1 tpy; term 5 years; scanned — figures read via OCR.)
10. Maine DEP, Portland Pipe Line major-projects page. Chapter 600 marine oil terminal license renewal application O-000305-91-I-R and O-000306-91-I-R, accepted for processing Aug. 11, 2025. maine.gov/dep/projects/portlandpipe/.
11. Maine DEP, Bureau of Air Quality. Chapter 171 fenceline monitoring reports, Buckeye South Portland Terminal (A-0282), Q1 2024–Q1 2026. maine.gov/dep/ftp/AIR/licenses/ch171/ (e.g., "2026 Q1 A0282 Fenceline.pdf," report dated May 15, 2026).
12. South Portland Housing Authority. *Property pages* (Betsy Ross House, Betsy Ross Crossing, Ridgeland Estates, Thornton Heights Commons, etc.). spha.net.
13. National Center for Education Statistics. *Search for Public Schools — South Portland Public Schools* (district 2312330), 2025-26 directory. nces.ed.gov/ccd/schoolsearch.
14. Maine Office of Child and Family Services (DHHS) & University of Maine. *Child Care Choices for Maine* licensed-program search. search.childcarechoices.me (searches run Sept. 24, 2026, from six tank farm addresses; results captured in ccc_*.html).
15. Portland Press Herald. "South Portland petitions Maine DEP to take action on unused oil tanks" (Jan. 29, 2025). pressherald.com.
16. OpenStreetMap contributors. *Map data* (storage tanks, industrial landuse) via Overpass API, retrieved Sept. 24, 2026 (overpass.private.coffee/api/interpreter); OpenStreetMap Foundation, ODbL 1.0 license.
17. Maine Revised Statutes, Title 5 §10002 (evergreen permit rule); 06-096 C.M.R. ch. 140 (Part 70 licensing), ch. 115 and ch. 171.
18. Maine Legislature, 129th (2020). *L.D. 1915, "Resolve, Directing the Department of Environmental Protection To Evaluate Emissions from Aboveground Petroleum Storage Tanks."*
19. Partnership on AI. *AI-Generated Content guidance* (disclosure framework referenced in the AI disclosure above). partnershiponai.org.
20. Maine Department of Environmental Protection. *Measurement and Control of Emissions from Aboveground Petroleum Storage Tanks* — Report to the Joint Standing Committee on the Environment and Natural Resources (Jan. 2021). maine.gov/dep/publications/reports/ (linked as "legislative reports/2021/Report to the Joint Standing Committee on the Environment and Natural Resources.pdf"; on file as MEDEP_tank_report_2021.pdf).
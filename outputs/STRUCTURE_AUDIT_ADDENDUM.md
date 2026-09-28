# Structure-Audit Addendum — South Portland Tank Farms
*2026-09-28 · documents the correction triggered by the arrow-marked review map*

## What the arrows flagged (all confirmed as problems)

Review of the September 28 map flagged shaded areas that are **not tank farms**. The audit (`src/audit_structures.py`, `src/farm_structures.py`) confirms:

### A. Portland-side non-petroleum parcels, wrongly shaded (arrows 1–5, 7)
| OSM way | Name | What it actually is | Why it was wrongly included |
|---|---|---|---|
| 30594024 | Custom House Wharf | Working pier/wharf, Portland Old Port | `landuse=industrial` within 1,200 m of a farm anchor |
| 325259943 | Widgery Wharf | Pier, Portland waterfront | same |
| 1125182452 | (unnamed pier) | Pier, Portland waterfront | same |
| 864502880 / 866113565 | Buoy Yard ×2 | Harbor buoy storage (Coast Guard-type facility) | same |
| 1354720145 | Yard South | **Shipyard** (industrial=shipyard) | same — despite the name, not Gulf Oil |
| 1449380363 | (unnamed) | Industrial parcel, no oil tag, no mapped tanks | same |

### B. SoPo-side parcels with no tanks (your "tanks without fenceline polygons?" arrows)
- **The Cassidy Point / West Commercial St parcel (way 1449380363)** — ~22.8 acres, zero mapped tanks, zero oil tags. Not a tank farm.
- **The Cash Corner parcel (way 456477913)** — ~17.3 acres, zero mapped tanks, zero oil tags. Not a tank farm.
- These are exactly the "might be tanks without fenceline polygons" cases: the shading came from bare `landuse=industrial` polygons, not from tank structures. If either hosts oil storage in reality (e.g., a small terminal not in OSM), **OSM simply doesn't map it** — flag for ground-truthing. Neither is in the state's licensed-terminal list for South Portland (the licensed set is the six farms plus Webber Tanks, which is Bucksport).

### C. What each parcel actually contains (decisive evidence)
| Parcel | Contains mapped tanks? | `industrial=oil`? | Verdict |
|---|---|---|---|
| 451929160 (PPLC) | 19 tanks | yes | tank farm — keep |
| 451987174 (Sprague) | 46 tanks | yes | tank farm — keep |
| 452153011 (Global) | 11 tanks | yes | tank farm — keep |
| 452157731 (CITGO) | 10 tanks | no tag but tanks present | tank farm — keep |
| 451986293 (Sprague) | 2 tanks | yes | tank farm — keep |
| 1354720144 (Gulf) | 9 tanks | yes | tank farm — keep |
| 1354720148/149 (PPLC pier parcels) | 2 / 0 | yes, named PPLC | keep (Front St tanks + Pier 1) |
| 846592712 | 0 | no | exclude (unnamed industrial) |
| 1449380363 | 0 | no | exclude |
| 451988987 | **1** tank | no | **exclude** — one tank inside a 19-acre industrial parcel; the parcel edge is NOT the farm fence (it pulled Skillin/Dyer/Wishing Tree/Ready Set Grow to near-zero distances that aren't tank distances) |
| 456477913 / 454036746 | 0 | no | exclude (Cash Corner area) |

## Count impact (corrected rule: tank, parcel-with-tanks, industrial=oil, or operator-named)

| | Old (contaminated) | Corrected |
|---|---|---|
| Union total | 42 | **41** |
| Schools | 7 | 7 |
| Child care (all types) | 25 | 25 |
| Senior housing | 9 | 9 |

**The headline numbers hold.** The only site to leave the union is **Ocean House On The Farm LLC**, which had measured at exactly 1.000 mi via the contaminated parcel edge and now measures >1 mi — the marginal case resolves against inclusion.

**Distance shifts (largest, among previously counted pairs):** the Portland-side pier/buoy-yard contamination was inflating Gulf/Sunoco distances for **Portland-side receptors** (Children's Nursery School 0.59→1.20 mi; Kiddie Garden ×2 0.68→1.25/1.26; Waynflete 0.96→1.49; Catherine Morrill 0.32→0.93). Those sites' *true* Gulf/Sunoco fence-line distances are longer than first reported. All Portland-side sites **remain in the union** through other legitimate structures — Waynflete at 0.20 mi to CITGO's tanks (it's across the river from them) and Kiddie Garden ×2 at 0.20/0.32 mi to CITGO.

## Corrections applied
1. `src/farm_structures.py` — canonical loader with the corrected inclusion rule; excludes the 8 flagged parcels with documented reasons.
2. Per-farm counts shifted: Buckeye 14→10, Gulf/Sunoco 19→12, PPLC 17→16; Global/CITGO/Sprague unchanged.
3. Maps, GIS exports, buffer, and dataset to be regenerated with the corrected set (this addendum documents the rule so the regeneration is auditable).
4. FACTCHECK to be amended with an FC-7 entry documenting the audit trail and the count revision 42→41.

## Open item — ground-truthing (not a data problem, a completeness one)
OSM's tank mapping may be incomplete: any real-world facility missing from OSM (e.g., small terminals) would be invisible to this analysis. The Cash Corner and Cassidy Point areas show *no mapped tanks* — if either hosts storage in reality, that's a gap in the base map, not this analysis. A city assessor or DEP tank-registration cross-check would settle it definitively.
---
title: Permitted vs actual emissions — the DEP throughput gap
date: 2026-10-06
status: half-formed
tags: [emissions, permits, DEP, PSP-feedback, throughput]
---

# Permitted vs actual emissions — the DEP throughput gap

Feedback came back from the PSP group on the tank-farm work. The core critique, verbatim:

> A huge piece the DEP leaves out — a major flaw in their data analysis is they leave off how much storage and throughput was happening during data collection.

## What PSP is pointing at

DEP's exposure analysis (the 2021 legislative report lineage, and the per-facility
modeling) treated what was measured while the study cameras were running as if it
characterized the facilities. But throughput and tank turnover vary. A terminal
running at half its licensed throughput emits very differently than one running at
full licensed rate. If DEP modeled actual-emissions-at-collection-time, the results
only describe the snapshot, not the licensed ceiling the facilities are allowed to
run at.

## The question that crystallized

1. **What percentage of permitted capacity were the tanks actually emitting at?**
   License caps are known from the memo table (594.4 tpy VOC facility-wide across
   all six, per-facility caps from each DEP order). Need actuals: license-order
   actuals tables, EPA NEI facility records, DEP annual emission statements.
2. **What would the impacts be if they emitted at full permitted capacity?**
   Scale-up implications: fenceline benzene/1,3-butadiene, cancer-risk arithmetic,
   receptor exposure at the distances we already mapped.

## The gap, stated

The headline we published is "permitted ceiling" (594.4 tpy). PSP is saying DEP's
opposite number — "measured reality" — has a hidden multiplier: the throughput that
was present during data collection. Neither number alone answers the question a
resident cares about: **how close can legal operation get to worst-case?**

## Descendants

- Calc: actual ÷ permitted per facility → percentage table.
- Scenario: full-capacity emit rate vs measured emit rate → exposure deltas at
  receptor distances in `outputs/receptor_fenceline_distances.csv`.
- Source question to chase: what throughput was present during DEP's data
  collection windows (2021 report measurement period, each license renewal's
  "actuals" baseline year)?

## Verification update, same day (adversarial pass on the absence claim)

Three-depth falsification attempt on the "no published facility actuals" premise
found it **half wrong in the direction that strengthens PSP's critique**
(trove: sopo-tanks-permitted-vs-actual-emissions@bbe320a, source
`epa-nei-facility-summaries`):

1. **DEP: still true.** DEP's own pages publish no facility tonnage; the 2021
   report (111 pp, verified) contains zero "tpy" figures and zero ch. 137
   references, and its Feb 10 2021 legislative briefing is the same methods-only
   deck. Emission reports are non-confidential (ch. 115 § IX(B)(1)) and Maine
   DEP certified to EPA they are publicly available (83 FR 12966) — FOAA-able,
   but not posted.
2. **EPA: false.** The ch. 137/CAERS statements MEDEP receives are republished
   **annually** by EPA as facility-level emissions, every year 2012–2023, in
   `gaftp.epa.gov/air/nei/nei_facility_summaries/` (annual point reporting under
   the 2016 AERR). Every row carries the Maine license ID. Trove source added:
   `epa-nei-facility-summaries`.
3. So the percentage table exists and was built:

| Facility (license) | VOC cap | 2019 | 2020 | 2023 |
|---|---|---|---|---|
| Sprague (A-000179) | 49.9 | 7.49 (15%) | 7.22 (14%) | 10.93 (22%) |
| PPLC (A-000197) | 220.0 | 41.01 (19%) | 21.11 (10%) | 43.50 (20%) |
| Buckeye / South Portland Terminal LLC (A-000282) | 135.4 | 43.68 (32%) | 45.36 (33%) | 45.30 (33%) |
| Gulf (A-000390) | 49.9 | 25.83 (52%) | 24.04 (48%) | 14.75 (30%) |
| Global (A-000432) | 21.9 | 4.06 (19%) | 20.43 (93%) | 9.63 (44%) |
| CITGO (A-000460) | 117.3 | 42.20 (36%) | 44.86 (38%) | 43.55 (37%) |
| **Total** | **594.4** | **164.3 (28%)** | **163.0 (27%)** | **167.7 (28%)** |

4. What this does to the throughput critique: the ambient sampling record
   (2019–2026) describes a fleet running at ~27–28% of its combined licensed
   ceiling. Full-capacity operation would be a **3.5× scale-up** of the
   documented conditions. And the NEI series independently resurrects the Global
   story: 19% of cap in 2019 → **93% in 2020** → 44% after the decree-era tank
   remedies — the operator's written statements moved with the consent decree,
   not with a change in method honesty.
5. The caveat that keeps it honest: these are operator-reported, AP-42-calculated
   annual statements ("routine" operations only), not independent measurements.
   The one measured episode (EPA's 2016 Global tank testing, "substantially
   higher than previously estimated") still says written actuals may understate
   reality, which is the sharp end of PSP's critique. Throughput during sampling
   windows remains the open gap — no public dataset carries it; still FOAA.
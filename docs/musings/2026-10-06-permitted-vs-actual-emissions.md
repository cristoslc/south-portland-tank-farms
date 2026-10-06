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
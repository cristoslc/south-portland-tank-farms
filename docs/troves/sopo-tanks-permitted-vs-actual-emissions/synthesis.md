---
title: "Permitted vs actual emissions — South Portland tank farms"
trove: sopo-tanks-permitted-vs-actual-emissions
question: "What percentage of permitted capacity were the tanks emitting at, and what would the impacts be at full permitted capacity?"
generated: 2026-10-06
---

# Synthesis: permitted vs actual emissions, South Portland tank farms

## Key findings

### Permitted capacity (the denominator)

The six farms' facility-wide VOC caps at last license issuance total **594.4 tpy VOC** and **103.7 tpy HAP** [tank-farm-permit-memo; the four text-extractable license orders a0197-pplc-renewal-2025, a0460-citgo-renewal-2025, a0432-global-renewal-2023, a0390-gulf-renewal-2023; Sprague and Buckeye figures via memo OCR]. Per facility: PPLC 220.0, Buckeye 135.4, CITGO 117.3 (reduction to 104.4 requested at Nov 2025 renewal), Gulf 49.9, Sprague 49.9, Global 21.9.

Throughput caps exist alongside VOC caps and are the physical driver of the VOC emissions: PPLC crude throughput capped at 11.0 billion gal/yr [a0197]; Gulf combined loading-rack + marine limits around 310 MM gal [a0390]; Global's consent-decree-era license capped pass-through at 75 MM gal/yr asphalt + 50 MM gal/yr #6 oil (press coverage of epa-global-settlement-2019).

### Actual emissions (the numerator) — mostly not public

**DEP does not publish facility-level annual actual VOC emission tonnage.** The license orders establish caps and calculation methods but print no recent actuals [all four license sources]. The annual ch. 137 emission statements facilities file (which drive DEP's air-quality fee surcharge) are internal records [license orders; medep-tank-report-2021].

The one facility with a public measured-actuals record is Global: EPA-required tank testing (2016) found the heated #6/asphalt tanks emit VOC "at substantially higher levels than previously estimated," EPA's complaint pegged PTE at >50 tpy against the 21.9 tpy license, and the agency alleged exceedances continuing for years before the 2019 consent decree, which required ~20 tpy of VOC reductions [epa-global-settlement-2019 and press coverage]. Press reporting characterized the findings as roughly **twice the legally allowed rate** — i.e., ~100–200% of permitted capacity, sustained for multiple years.

Sprague's 2020 consent decree is the complement: EPA's remedy was expressly to **cap storage and throughput** — permit limits on #6/asphalt pass-through and on how many tanks store it at once [epa-sprague-settlement-2020]. That is federal acknowledgment of the mechanism PSP names: emissions track storage level and turnover rate.

### The percentage question, answered honestly

- **Global: exceeded 100% of its permitted VOC capacity** (EPA: PTE >50 vs licensed 21.9 tpy; ~2× per testing) — demonstrated 2014–2019.
- **The other five facilities: not computable from public records.** DEP's own report contains no per-facility actual tonnage [medep-tank-report-2021]; the DEP/CDC ambient monitoring project page records what was sampled but not what the facilities were doing [dep-spo-voc-monitoring-project]; fenceline monitoring (ch. 171) began only in Aug/Sep 2024 and outputs ambient concentrations, not tons [dep-ch171-fenceline-report-list].
- Structural datapoints worth citing: Maine CDC's 6-year assessment found long-term average benzene slightly **higher** at sites closer to petroleum sources than remote statewide sites, and cumulative cancer risk 1.5–2.0 per 100,000 (Pearl Street 2.8) under **actual** 2019–2026 operating conditions [cdc-6yr-voc-health-assessment].

### Full-permitted-capacity scenario (the counterfactual)

No DEP document models the six farms at their combined 594.4 tpy VOC / 103.7 tpy HAP ceiling. What follows from the trove if they ran to caps:

1. The ambient data behind every health conclusion to date was collected under variable, often low, storage/throughput conditions (DEP's own report notes tanks are intermittently dormant/empty; press coverage during 2020 sampling says many tanks were dormant or empty). The licensed ceiling is a different operating envelope.
2. VOC working losses scale with throughput, tank fill and turnover, and heated #6/asphalt tank losses scale with temperature and turnover [medep-tank-report-2021 methods]. A facility at full licensed throughput emits at a materially higher rate than the same facility during a sleepy sampling year. The Global episode is the empirical proof of the multiplier: identical facility, same license basis, measured ~2× the permitted rate the licensed framework assumed.
3. If all six ran to caps, facility-wide VOC would reach 594.4 tpy (vs. an unknown but demonstrably lower actual baseline), i.e., up to **5.3× the Global-style license basis** in aggregate; cancer-risk and benzene findings in the CDC 6-year report would scale upward wherever emissions are throughput-driven. Pearl Street, already above the 1-in-100,000 AAG and at 2.8 per 100,000 cumulative risk **without** a full-capacity scenario, has no headroom.
4. The compliance gap is only partially fenced: ch. 137 annual VOC statements (filed annually) and ch. 171 fenceline BTEX reports (quarterly, since Q3 2024) do now generate measurement streams, but DEP publishes no normalized actual-vs-cap percentage for any facility.

## Points of agreement

- CAAC (Jan 2021) and PSP (Oct 2026) converge on the same structural critique: emissions are company-calculated via AP-42, actuals are never measured or published, and cumulative impacts across the six farms are not assessed [sp-caac-comments-2021; PSP feedback captured in docs/musings/2026-10-06-permitted-vs-actual-emissions.md]. (Note: the PSP advocacy packet itself remains excluded as a source per FACTCHECK §FC-6; its feedback is handled as a research question, not as evidence.)
- EPA and DEP both treat throughput/storage caps as the operative lever on actual VOC emissions (Sprague decree; every license order's throughput conditions).

## Points of disagreement

- DEP's position (2021 report) is that AP-42 estimation under license constraints is sufficient and fenceline monitoring cannot attribute pollutants to individual facilities; CAAC and the post-2024 ch. 171 program both undercut that (monitoring exists now, and attribution was always secondary to cumulative exposure).
- DEP's ambient assessment says "minimal" short-term risk while flagging acrolein and benzene as long-term concerns and admitting the cancer-risk figures exclude naphthalene [cdc-6yr-voc-health-assessment].

## Gaps

- Facility-level annual actual VOC/HAP tonnages: require DEP ch. 137 emission statements — FOAA request to Maine DEP Bureau of Air Quality is the concrete next action.
- Throughput/storage levels during DEP's 2019–2020 sampling windows: monthly throughput records each facility already keeps under license; same FOAA scope.
- Buckeye (A-282) and Sprague (A-179) license orders are scanned images here; figures taken from the memo's prior OCR (A0282GR.pdf, A0179PRM.pdf raw files archived in `.agents/search-snapshots/raw/`).
- Fenceline quarterly benzene series (2024 Q3 onward) not yet aggregated per facility.
- Press Herald source pages are paywalled; figures used from them were cross-verified across multiple outlets and EPA pages.

## Source index

All thirteen sources are catalogued in `manifest.yaml` with verbatim snapshots and summaries under `sources/<slug>/`.
# EPA NEI / AirData annual facility summaries

## Provenance

- EPA facility-level emissions summary CSVs (National Emissions Inventory / AirData annual facility summaries), downloaded 2026-10-06 from:
  - `https://gaftp.epa.gov/air/nei/nei_facility_summaries/` (annual facility summaries)
  - `https://gaftp.epa.gov/air/nei/2020/data_summaries/Facility Level by Pollutant.zip`
  - `https://gaftp.epa.gov/air/nei/2023/data_summaries/eis_report_38234_2023NEI_facility_summary_21jul2026.zip`
- Snapshot: verbatim VOC rows for the six tank-farm facilities in this trove's root (`epa-nei-facility-summaries-snapshot.md`); full South Portland extracts (all pollutants, all facilities) archived UNCOMMITTED in `.agents/search-snapshots/raw/nei-facility-summaries/` (2019/2020/2023, ~300 facility-pollutant rows each; full national CSVs ~450–700 MB retained in /tmp only).

## What it settles

This source overturns the working assumption that facility-level annual actual VOC tonnage is unavailable without FOAA. EPA publishes **annual**, facility-level emissions for the six South Portland tank farms, submitted by the operator through Maine DEP's ch. 137/CAERS pipeline (the CSV "program system code" column reads `MEDEP`, and the "agency facility id" column carries each facility's Maine air license ID: A-000179 Sprague, A-000197 PPLC, A-000282 Buckeye/South Portland Terminal LLC, A-000390 Gulf, A-000432 Global, A-000460 CITGO).

Annual facility summaries exist for every year 2012–2023 in `nei_facility_summaries/` (annual point-source reporting under the 2016 AERR rule; pre-2017 files are AirData annuals).

## VOC actuals vs license caps (tpy VOC, operator-reported)

| Facility (license) | VOC cap | 2019 | 2020 | 2023 |
|---|---|---|---|---|
| Sprague (A-000179) | 49.9 | 7.49 (15%) | 7.22 (14%) | 10.93 (22%) |
| PPLC (A-000197) | 220.0 | 41.01 (19%) | 21.11 (10%) | 43.50 (20%) |
| Buckeye / South Portland Terminal LLC (A-000282) | 135.4 | 43.68 (32%) | 45.36 (33%) | 45.30 (33%) |
| Gulf (A-000390) | 49.9 | 25.83 (52%) | 24.04 (48%) | 14.75 (30%) |
| Global (A-000432) | 21.9 | 4.06 (19%) | 20.43 (93%) | 9.63 (44%) |
| CITGO (A-000460) | 117.3 | 42.20 (36%) | 44.86 (38%) | 43.55 (37%) |
| **Six-farm total** | **594.4** | **164.3 (28%)** | **163.0 (27%)** | **167.7 (28%)** |

HAP-VOC (sum of six farms): 2019 ≈ 4.08 tpy, 2020 ≈ 5.85 tpy (Maine HAP inventory year), 2023 ≈ 3.50 tpy, against 103.7 tpy of licensed facility-wide HAP.

## Observations

- Global ran at **93% of its 21.9 tpy cap in 2020** — the year after the consent decree was entered — corroborating the EPA-testing story (exceedances for years before 2019) and falling to 44% by 2023 after tank remedies.
- The fleet as a whole operated at roughly **a quarter to a third of its combined licensed ceiling** in 2019–2023. This is the number PSP's throughput critique needs as context: the sampling-era ambient record describes facilities running far below their licensed maximum.
- Buckeye (33%) and CITGO (37%) are steady across all three years; PPLC swings 10–20%; Gulf fell 52% → 30%.

## Caveats (do not overstate)

- These are **operator-reported annual statements** (ch. 137/CAERS), largely AP-42-calculated, transmitted by MEDEP to EPA. They are "actuals as reported by the companies," not independent measurements. The measurement story (EPA 2016 testing vs. operator estimates) belongs to epa-global-settlement-2019.
- NEI "routine" operating type only (the 2019 file header states "Emissions Operating Type: Routine"); upset/nuisance episodes may not be included.
- Ch. 137's VOC reporting threshold is 25 tpy; operators reporting below-threshold chemicals still appear here, but any tonnage below the facility's own reporting line may be represented by estimation defaults.
- DEP itself still publishes none of this on its own website (aei.html is a submission portal page). EPA publication ≠ DEP publication; but for the percentage question, EPA's annual facility summaries make every year since 2017 computable without FOAA.
- Emission reports are explicitly non-confidential: 06-096 CMR ch. 115 § IX(B)(1), and Maine DEP certified to EPA (Federal Register 83 FR 12966, Mar 26 2018, approval of Maine infrastructure SIP) that ch. 117/137 reports are "available to the public . . . pursuant to Maine law."
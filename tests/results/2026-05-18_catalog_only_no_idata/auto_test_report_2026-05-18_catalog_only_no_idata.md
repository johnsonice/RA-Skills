# RA Skills Auto-Test Report - 2026-05-18

Scope: `imf-ra` and `imf-ra-catalog` only. iData metadata, retrieval, and output-generation cases were skipped because iData pull functionality is unavailable in this environment.

## Summary

Pre-test status: Pass

| Result | Count |
|---|---:|
| Pass | 28 |
| Fail | 0 |
| Needs follow-up | 1 |
| Skipped out of scope | 24 |
| Total defined cases | 53 |

## Run Notes

- Branch: `bella_0515_test_with_Yaml`
- Commit: `a75d255`
- Runner: Codex
- Date: `2026-05-18`
- Case source: `tests/auto_test_cases.yaml`
- Detailed result file: `tests/results/2026-05-18_catalog_only_no_idata/auto_test_results_2026-05-18_catalog_only_no_idata.yaml`

## Pre-Test Checks

| Check | Result | Evidence |
|---|---|---|
| Reference reachability | Pass | `bash .claude/skills/imf-ra/scripts/check_references.sh` returned `OK: all skills found, all references resolve.` |
| Referenced-file consistency | Pass | `python3 tests/check_referenced_files.py` returned `OK: checked 271 file reference(s) across 19 active file(s).` |
| Required files | Pass | YAML required-file validation found all referenced paths present. |

## Helper Contracts

| ID | Result | Evidence |
|---|---|---|
| CONTRACT-01 | Pass | Skill reference checker returned OK. |
| CONTRACT-02 | Pass | `latest-weo` returned `IMF.RES.WEO:WEO_LIVE`. |
| CONTRACT-03 | Pass | Real GDP growth search returned WEO Live `NGDP_RPCH` as top candidate. |
| CONTRACT-04 | Pass | Vintage-only WEO listing returned `VINTAGE` resources and excluded plain WEO Live. |
| CONTRACT-05 | Pass | `G110` expanded to Advanced Economies member countries including `USA`. |
| CONTRACT-06 | Pass | Active referenced-file scanner verified all extracted file references exist. |

## Failures

No failures in the focused `imf-ra` / `imf-ra-catalog` run.

## Needs Follow-Up

| ID | Reason |
|---|---|
| E2E-01 | Discovery can be evaluated, but handoff to `imf-ra-data` and long CSV download require an iData-capable environment. |

## Skipped Out Of Scope

Skipped because the user requested no iData/data-pull execution:

`SMOKE-01`, `SMOKE-04`, `DATA-01`, `DATA-02`, `DATA-03`, `DATA-04`, `DATA-05`, `DATA-06`, `DATA-07`, `DATA-08`, `DATA-09`, `DATA-10`, `GROUP-01`, `GROUP-03`, `DATA-11`, `DATA-12`, `DATA-13`, `DATA-14`, `DATA-15`, `DATA-16`, `DATA-17`, `DATA-18`, `DATA-19`, `DATA-20`.

## Coverage Notes

- Routing smoke: Passed scoped orientation, catalog-discovery, and WEO-vs-CPI comparison routing.
- Shared conventions: Passed WEO group reference use, EMDE/G200 handling, low-income coverage clarification, and groupcode-vs-country-selector policy.
- Catalog discovery: Passed WEO Live defaults, real GDP growth `NGDP_RPCH`, nominal GDP USD `NGDPD`, current-account ambiguity, FSI expansion beyond WEO, WDI-specific lookup, Bloomberg-specific lookup, WTO-specific lookup, and vintage policy.
- Helper contracts: Passed all deterministic helper checks.
- Data workflow: Skipped all iData metadata/fetch/output cases.
- End to end: Discovery side evaluated; download side needs follow-up with iData available.

## Evidence Highlights

- `catalog_search.py search "real GDP growth"` returned `IMF.RES.WEO:WEO_LIVE`, `INDICATOR`, `NGDP_RPCH` as the top candidate.
- `catalog_search.py search "nominal GDP USD"` returned `IMF.RES.WEO:WEO_LIVE`, `INDICATOR`, `NGDPD` as the top candidate.
- `catalog_search.py search "current account balance" --all-databases` returned WEO, GDS, BOP, SPE, and percent-of-GDP variants.
- `catalog_search.py search "financial soundness regulatory capital risk weighted assets" --all-databases` returned FSI capital-adequacy candidates including `FSI688_CFSI_PT`.
- WDI, Bloomberg, and WTO requests were checked against their source-specific indicator files.

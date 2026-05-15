# RA Skills Auto-Test Report - 2026-05-15

## Summary

Scope: `imf-ra` and `imf-ra-catalog` only. iData/data-pull execution was skipped.

| Result | Count |
|---|---:|
| Pass | 18 |
| Fail | 0 |
| Needs follow-up | 1 |
| Skipped out of scope | 19 |
| Total defined cases | 38 |

## Run Notes

- Branch: `bella_0515_test_with_Yaml`
- Commit: `93448c4`
- Runner: Codex
- Date: `2026-05-15`
- Case source: `tests/auto_test_cases.yaml`
- Detailed result file: `tests/results/2026-05-15_bella_0515_test_with_Yaml/auto_test_results_2026-05-15_bella_0515_test_with_Yaml.yaml`
- Reference check: `OK: all skills found, all references resolve.`

## Failures

No failures in the scoped `imf-ra` / `imf-ra-catalog` run.

## Needs Follow-Up

| ID | Reason |
|---|---|
| E2E-01 | Catalog discovery can be evaluated, but the case also requires handoff to data workflow and long CSV download. That part needs an iData-capable environment. |

## Skipped Out Of Scope

Skipped because the user requested no data-pull/iData execution:

`SMOKE-01`, `SMOKE-04`, `DATA-01`, `DATA-02`, `DATA-03`, `DATA-04`, `DATA-05`, `DATA-06`, `DATA-07`, `DATA-08`, `DATA-09`, `DATA-10`, `GROUP-01`, `GROUP-03`, `DATA-11`, `DATA-12`, `DATA-13`, `DATA-14`, `DATA-15`.

## Coverage Notes

- Routing smoke: Passed scoped orientation, catalog-discovery, and comparison routing cases.
- Shared conventions: Passed WEO group reference use, EMDE/G200 handling, low-income coverage clarification, and groupcode-vs-country-selector policy.
- Catalog discovery: Passed WEO Live defaults, real GDP growth `NGDP_RPCH`, nominal GDP USD `NGDPD`, current-account ambiguity, FSI expansion beyond WEO, WDI-specific lookup, Bloomberg-specific lookup, and vintage policy.
- Data workflow: Not executed except where catalog guardrails overlap; all iData/fetch cases were skipped.
- End to end: Discovery side evaluated; download side requires follow-up with iData available.

## Evidence Highlights

- `bash .claude/skills/imf-ra/scripts/check_references.sh` returned `OK: all skills found, all references resolve.`
- `catalog_search.py search "real GDP growth"` returned `IMF.RES.WEO:WEO_LIVE`, `INDICATOR`, `NGDP_RPCH` as the top candidate.
- `catalog_search.py search "nominal GDP USD"` returned `IMF.RES.WEO:WEO_LIVE`, `INDICATOR`, `NGDPD` as the top candidate.
- WEO group references map Advanced Economies to `G110` and EMDEs to `G200`, and state that group codes should not be used directly as iData country selectors.
- WDI and Bloomberg explicit requests were checked against their source-specific indicator files rather than only the general IMF variable list.

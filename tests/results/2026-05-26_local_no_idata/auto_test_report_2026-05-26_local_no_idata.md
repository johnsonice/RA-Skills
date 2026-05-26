# RA Skills Auto-Test Report - 2026-05-26

## Summary

Pre-test status: Pass

| Result | Count |
|---|---:|
| Pass | 11 |
| Fail | 0 |
| Needs follow-up | 34 |
| Total | 45 |

Local scope: command contracts and machine-check commands were executed. iData pull/data commands were skipped because iData is unavailable on this machine. Prompt-level final response checks were not marked pass without separate fresh-session transcripts.

## Pre-Test Checks

| Check | Result | Evidence |
|---|---|---|
| `bash .claude/skills/imf-ra/scripts/check_references.sh` | Pass | OK: all skills found, all references resolve. |
| `python3 tests/check_referenced_files.py` | Pass | OK: checked 276 file reference(s) across 23 active file(s). |

## Failures

| ID | Failed Check(s) | Evidence |
|---|---|---|
| None | - | - |

## Needs Follow-Up

| ID | Reason |
|---|---|
| SMOKE-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| SMOKE-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CONV-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CONV-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CONV-03 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-03 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-04 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-05 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-06 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| HPIPE-07 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CAT-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CAT-04 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CAT-05 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CAT-06 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-03 | iData-dependent command skipped because iData is unavailable locally. Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-07 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-09 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-10 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| GROUP-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| GROUP-04 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| PIPE-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| PIPE-03 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| VINTAGE-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| VINTAGE-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| VINTAGE-04 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| CAT-11 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-15 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-19 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| DATA-22 | iData-dependent command skipped because iData is unavailable locally. Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| E2E-01 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |
| E2E-02 | Prompt-level final response checks require a separate agent transcript; not marked pass from command evidence alone. |

## Coverage Notes

- core_behavior_pipeline: pass 0, fail 0, needs follow-up 5
- weo_group_helper_behavior: pass 0, fail 0, needs follow-up 7
- catalog_helper_behavior: pass 0, fail 0, needs follow-up 14
- data_workflow_guardrails: pass 0, fail 0, needs follow-up 8
- command_contracts: pass 11, fail 0, needs follow-up 0

## Run Notes

- Branch: bella_0521_catalog_patch
- Commit: faee2f6
- Runner: Codex local command runner
- Case source: `tests/auto_test_cases.yaml`
- Detailed result file: `tests/results/2026-05-26_local_no_idata/auto_test_results_2026-05-26_local_no_idata.yaml`

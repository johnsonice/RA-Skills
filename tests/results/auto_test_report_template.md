# RA Skills Auto-Test Report - YYYY-MM-DD

## Summary

Pre-test status: Pass / Fail / Not run

| Result | Count |
|---|---:|
| Pass | 0 |
| Fail | 0 |
| Needs follow-up | 0 |
| Total | 0 |

## Pre-Test Checks

| Check | Result | Evidence |
|---|---|---|
| Reference reachability | Pass | `bash .claude/skills/imf-ra/scripts/check_references.sh` returned OK. |
| Referenced-file consistency | Pass | `python3 tests/check_referenced_files.py` returned `OK: checked ... file reference(s)`. |

If either pre-test check fails, stop and ask the user how to revise the
missing target or inconsistent path/name before running behavioral cases.

## Failures

| ID | Failed Assertion(s) | Evidence |
|---|---|---|
| DATA-10 | `ask_explicit_confirmation_before_broad_all_pull` | Agent attempted a broad pull without confirmation. |

## Needs Follow-Up

| ID | Reason |
|---|---|
| DATA-04 | Metadata API unavailable in the test environment. |

## Coverage Notes

- Routing smoke:
- Shared conventions:
- Catalog discovery:
- Data workflow:
- Helper contracts:
- End to end:

## Run Notes

- Branch:
- Commit:
- Runner:
- Case source: `tests/auto_test_cases.yaml`
- Detailed result file: `tests/results/auto_test_results_YYYY-MM-DD.yaml`

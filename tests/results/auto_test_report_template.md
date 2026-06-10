# RA Skills Auto-Test Report - YYYY-MM-DD

## Summary

| Result | Count |
|---|---:|
| Pass | 0 |
| Fail | 0 |
| Needs follow-up | 0 |
| Total | 0 |

## Failures

| ID | Failed Assertion(s) | Evidence |
|---|---|---|
| DATA-10 | `ask_explicit_confirmation_before_broad_all_pull` | Agent attempted a broad pull without confirmation. |

## Machine Check Failures

| ID | Failed Check | Evidence |
|---|---|---|
| HPIPE-03 | `final_response_must_not_include: handoff-ready` | Agent treated an ambiguous WDI lookup as ready for handoff. |

## Needs Follow-Up

| ID | Reason |
|---|---|
| DATA-04 | Metadata API unavailable in the test environment. |

## Coverage Notes

- Core behavior pipeline:
- Catalog helper behavior:
- WEO group helper behavior:
- Data workflow guardrails:
- Command contracts:

## Run Notes

- Branch:
- Commit:
- Runner:
- Case source: `tests/auto_test_cases.yaml`
- Detailed result file: `tests/results/auto_test_results_YYYY-MM-DD.yaml`

# Recovery and reporting contract

Use this contract after a failure. An attempt includes the first execution;
three attempts means one initial execution and at most two retries. Count per
operation (fixed request and inputs), not per whole conversation. A materially
changed user request is a new operation; restarting a helper does not reset the
budget for the same operation. This budget covers RA helper/agent retries, not
unobservable retries inside the external SDK.

## Retry ownership

| Operation | Owner and limit | After failure |
|---|---|---|
| Haver fetch | `fetch_haver.py` already makes at most 3 attempts | Do not rerun the unchanged helper automatically. |
| Chunked iData fetch | `fetch_idata.py` already makes at most 3 attempts per chunk | Preserve successful chunks and disclose incomplete coverage; do not rerun the entire panel automatically. |
| Single-request iData or metadata without helper retries | Agent may make at most 3 total attempts for an evidenced transient failure, waiting 5 then 15 seconds | Stop when the budget is exhausted; do not add another outer retry loop. |
| SDK installation | One installer invocation | Retry only after correcting an identified cause; never loop installation. |
| Generated chart/analysis script | At most 3 executions for the same failure, with a concrete fix before each retry | Stop and explain the blocker on the third failure or earlier if no fix is available. |
| Haver catalog lookup | One query, batched across the selected databases | Inspect results; ask for a distinguishing clue if insufficient. Do not rephrase and rerun the same lookup. |

Agent-owned retries are for timeouts or evidenced temporary service failures,
not invalid identifiers, missing packages/files, or unchanged permission errors.
A 403 alone is not evidence of a transient failure: inspect access/private-data
setup before deciding whether a corrected request is possible. Honor explicit
rate-limit timing; do not busy-loop. Existing helpers may retry internally;
count those attempts and do not add agent retries after their final failure.

Fix deterministic errors before running again. Never reduce geography, dates,
frequency, or indicators silently to make a request succeed. A new search after
the user changes the scope or supplies a distinguishing clue is allowed; a
cosmetic rephrase does not establish a new operation.

## Reporting is a separate decision

`imf-ra-error-report` owns consent and the report destination. A failed attempt
does not itself authorize a report. Use its classification table after triage:

- For a fixable setup/input problem, explain the specific next step; do not
  offer a report for normal clarification.
- For an unexpected helper defect, corrupt output, or exhausted recovery that
  still blocks/degrades the requested result, offer a report once.
- For an unsatisfactory answer, do not force 3 or 5 more turns. Offer once when
  the user identifies a persistent unresolved problem after a revision, or the
  agent has no useful next correction. An explicit report request is consent
  immediately after a user-visible failure.

Do not repeat the offer after refusal unless the user requests it or a distinct
failure occurs. Retain the independent maximum of 5 reports per conversation.
Record observed attempt/retry counts; use Unknown for SDK-internal counts that
were not exposed. Do not fabricate a numeric dissatisfaction threshold.

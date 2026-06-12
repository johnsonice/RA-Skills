---
name: imf-ra-error-report
description: Use when a user wants to report a user-visible RA-Skills failure, including a system or execution error, failed helper/SDK/data fetch, missing output file, crash or timeout, or an unsatisfactory answer after repeated attempts. Creates a structured local JSON error report for the development team only after user consent.
---

# IMF RA Error Report

Use this skill to prepare a local, consent-based JSON report for a user-visible RA-Skills failure.

This is a side skill for support and product feedback. It does not add telemetry, remote upload, GitHub issue creation, dashboards, background logging, Python wrappers, or report lifecycle tracking.

## Scope

Use this skill for exactly two report scenarios:

1. `system_error` - a concrete execution failure blocks or degrades the RA workflow.
2. `unsatisfactory_answer` - the system does not crash, but the user still cannot get a useful result after repeated attempts.

Manual user report requests count as consent. If the user says "report this issue", "send an error report", "log this for the development team", "I am not satisfied, please report it", or similar after a visible failure, create the report without asking for consent again.

Do not use this skill for normal RA-Skills clarification behavior, such as asking for a missing time range, output format, ambiguous catalog candidate, WEO vs SPR/PRGT framework, or unsupported chart implementation status. If the user insists that one of these was problematic, allow a manual `unsatisfactory_answer` report.

## Consent Rule

Never write a report silently.

After a qualifying failure, offer to prepare a local report and wait for consent before creating the JSON file. Accepted consent includes "yes", "please report it", "send it", "create the report", or "log it".

If the user declines, acknowledge briefly and do not create a file.

Ask at most two concise follow-up questions before creating the report. Ask only for missing information that materially improves the report, such as:

- What were you trying to accomplish?
- What result did you expect instead?
- Can I include the command/output summary from this session?

Do not block report creation if the user does not know the answer.

## Report Limit

Create at most 5 reports per conversation session.

If the user attempts to create a sixth report, do not create a file. Say:

```text
The maximum number of error reports for this session has been reached. Please start a new conversation.
```

## Report Location

Write reports to:

```text
tests/user_error_report/
```

Filename pattern:

```text
MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary.json
```

Example filenames in that folder:

```text
06-05-2026-14-32-10-missing-haver-db.json
06-05-2026-15-10-41-unsatisfactory-weo-lookup.json
```

This repo-local folder is the single report destination for this skill. Do not write reports to the user's Desktop folder unless the user explicitly asks for a different location.

## Trigger Rules

### Scenario 1: System Or Execution Error

Use this when a concrete execution failure blocks or degrades the workflow.

Offer a report when one of these occurs:

- A helper command fails unexpectedly.
- iData, Haver, SDK, API, or data fetch fails after retry or self-correction policy.
- A Python import, dependency, permission, sandbox, or path error blocks the workflow.
- A required local resource is missing and setup guidance does not resolve it.
- A command times out repeatedly.
- The agent or tool run crashes, stops, or is interrupted unexpectedly.
- The agent says it created an output file, but the file is missing.
- Output is empty, corrupt, saved to the wrong location, or in the wrong format.

Suggested offer:

```text
It looks like this hit a system or execution error. Would you like me to prepare a local report for the development team so they can investigate?
```

### Scenario 2: Unsatisfactory Answer After Repeated Attempts

Use this when the system does not crash, but the user still cannot get a useful result after repeated attempts.

Offer a report when one of these occurs:

- The user asks the same or very similar query repeatedly and still does not get a useful answer.
- The user says the answer is wrong, unsatisfactory, not ideal, or not what they need after 5 attempts or revisions.
- The agent has tried several self-corrections on the same topic without progress after 3 attempts.
- The agent keeps asking the same clarification question and does not move the task forward.

Suggested offer:

```text
It seems like we still have not gotten you a useful answer after several tries.  Would you like me to prepare a local report so the development team can improve this workflow?
```

## Classification Taxonomy

Use this taxonomy to decide when to offer a report, when to retry or guide the user first, and when to wait until recovery attempts are exhausted.

| Category | Should offer report? | Severity | How to handle |
|---|---|---|---|
| `user_error` | No | Low | User input is invalid or incomplete. Explain and ask for corrected input. |
| `config_fixable` | No | Low | Environment issue the user can fix directly, such as an obviously missing package, checkout, or local resource like `haver.db`. Give setup guidance. |
| `config_unfixable` | Yes, after recovery fails | Medium | Environment issue that needs development review, such as missing expected local resources or unclear setup contract. |
| `transient_retry` | No | Low | Temporary network, tool, or API issue while fewer than three retries have been attempted. Retry or self-correct first. |
| `transient_exhausted` | Yes | High | Temporary issue persists after three retries or self-correction attempts. |
| `data_format` | Yes | High | Data schema, API contract, parser, or field mismatch. |
| `logic_bug` | Yes | High | Agent or helper code logic error, such as `IndexError`, `AttributeError`, impossible branch, or invalid assumption. |
| `subprocess_failure` | Yes | High | Required helper script crashes or returns blocking nonzero status. |
| `database_corruption` | Yes | High | Reference data appears corrupt, missing required columns, or internally inconsistent. |
| `rate_limit` | No | Low | API or session usage limit. Explain limitation and possible retry timing. |
| `file_io_error` | Usually no | Medium | File permission, disk, sandbox, or path issue. Give guidance first; report only if expected output remains blocked after correction attempts. |
| `custom_script_first_attempt` | No | Low | First, second, or third failure in an ad hoc script written during the session. Debug and retry first. |
| `custom_script_exhausted` | Yes | High | Three custom-script attempts fail and the RA workflow remains blocked. |
| `unsatisfactory_answer` | Yes | Medium | User remains unsatisfied after three repeated attempts or the agent cannot make progress. |
| `unknown` | Yes, after brief triage | Medium | Failure is unclassifiable but user-visible and blocks or degrades the task. |

Offer a report immediately for:

```text
logic_bug
database_corruption
subprocess_failure
data_format
transient_exhausted
custom_script_exhausted
```

Offer a report only after retry, self-correction, or user guidance has failed for:

```text
config_unfixable
file_io_error
unknown
```

Do not offer a report by default for:

```text
user_error
config_fixable
transient_retry
rate_limit
custom_script_first_attempt
```

In no-report cases, explain the issue, retry when appropriate, or give the user a concrete next step. If the user explicitly asks to report anyway after a visible failure, allow a manual `unsatisfactory_answer` report.

## Severity And Area

Severity:

- `high` - Blocks the RA workflow, produces likely wrong official identifiers/data, or crashes/fails repeatedly.
- `medium` - Produces confusing, incomplete, or unsatisfactory behavior that requires repeated user correction.
- `low` - Minor output, wording, formatting, or report-quality issue that does not block the task.

Choose one or two areas:

```text
catalog
data
country-groups
charts
Haver
iData
docs
environment
output-file
agent-behavior
other
```

## Evidence Rules

Describe the visible symptom, not internal policy labels.

Use:

```text
Agent appeared to guess or skipped validation and returned an unsupported code.
```

Avoid:

```text
Agent violated helper-first policy.
```

Use available conversation and command context. Include `Unknown` for missing values rather than inventing details.

Capture for all reports:

- Local username, if available.
- Original user request or concise task summary.
- Scenario, category, severity, and area.
- Commands attempted, files involved, and relevant error snippets.
- Whether the failure repeated.
- Retry or self-correction status.
- Duplicate fingerprint based on scenario, category, area, and short title.
- Expected behavior, if stated.
- Likely cause or current hypothesis.
- Suggested development action.
- Proposed regression test, if obvious.

For `system_error`, include deeper debugging evidence:

- Up to three command, helper, or code attempts.
- Command, working directory, exit code, timestamp, raw stdout, and raw stderr for each attempt when available.
- Full raw failing command/tool output when available.
- Files involved or expected output paths.
- Environment context such as OS type, Python version, repo path, and username.

For `unsatisfactory_answer`, include lighter product-feedback evidence:

- Original user request.
- Repeated-attempt count.
- Short summaries of the failed answers or approaches.
- User's stated dissatisfaction, correction, or expected answer.
- The likely stuck point, such as wrong database, wrong code, unclear geography, unsupported output format, or repeated clarification loop.
- Do not include a full raw conversation transcript by default.

## JSON Report Template

Each report is a single JSON file. Preserve raw stdout, stderr, or tool output for `system_error` reports when available because this is an internal support workflow.

```json
{
  "report_id": "MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "username": "Unknown",
  "report_number": 1,
  "status": "new",
  "fingerprint": "scenario|category|area|short-title",
  "scenario": "system_error | unsatisfactory_answer",
  "category": "user_error | config_fixable | config_unfixable | transient_retry | transient_exhausted | data_format | logic_bug | subprocess_failure | database_corruption | rate_limit | file_io_error | custom_script_first_attempt | custom_script_exhausted | unsatisfactory_answer | unknown",
  "severity": "high | medium | low",
  "area": ["catalog | data | country-groups | charts | Haver | iData | docs | environment | output-file | agent-behavior | other"],
  "original_request": "<original prompt or concise summary>",
  "failure_summary": "<one-paragraph description of what went wrong>",
  "expected_behavior": "<what the user expected, or Unknown>",
  "observed_behavior": "<what actually happened>",
  "evidence": {
    "command_attempts": [
      {
        "attempt": 1,
        "command": "<command or Unknown>",
        "cwd": "<working directory or Unknown>",
        "exit_code": "Unknown",
        "stdout_raw": "<raw stdout for system errors or Unknown>",
        "stderr_raw": "<raw stderr for system errors or Unknown>",
        "timestamp": "YYYY-MM-DDTHH:MM:SSZ"
      }
    ],
    "raw_output": "<full raw failing command/tool output for system errors or Unknown>",
    "answer_attempt_summaries": ["<short summary for unsatisfactory-answer reports or Unknown>"],
    "user_dissatisfaction": "<user correction, rejection, or expected answer for unsatisfactory-answer reports or Unknown>",
    "files_involved": ["<path or Unknown>"],
    "attempt_count": "Unknown",
    "retry_count": "Unknown",
    "retry_limit": "3 for system/code errors; 5 for unsatisfactory-answer reports",
    "retry_status": "not_applicable | not_retried | retry_succeeded | retries_exhausted | Unknown"
  },
  "reproduction_notes": {
    "reproducibility": "reproducible | intermittent | unknown | not_reproducible_session_crashed",
    "steps": ["<step or Unknown>"]
  },
  "environment": {
    "python_version": "Unknown",
    "os_type": "Unknown",
    "repo_path": "Unknown"
  },
  "likely_cause": "Unknown",
  "suggested_development_action": "Unknown",
  "proposed_regression_test": "Not proposed"
}
```

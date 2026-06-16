# IMF RA Error Reporting Skill Plan - V1/V2 Merged

**Date:** 2026-06-05
**Status:** Planning artifact, not yet implemented
**Proposed skill name:** `imf-ra-error-report`
**Final v1 approach:** Skill-only, consent-based JSON report workflow

## Executive Summary

Add one lightweight error-reporting skill to the IMF RA skill family. The experience should resemble a crash-report prompt in desktop applications: when a user-visible RA-Skills failure occurs, the agent may ask whether the user wants to report it to the development team. A report is created only after user consent.

The basic framework is V2: product-oriented, friendly, local, and small. The useful V1 pieces retained here are the formal classification taxonomy, explicit report/no-report rules, retry thresholds, rate limiting, and structured report output.

## Design Principles

1. **Consent first.** Never create or submit a report silently.
2. **User-visible failures only.** Report the symptom the user experienced, not hidden internal policy concerns.
3. **Local first.** Write one JSON report file locally; no remote upload, dashboard, email, GitHub issue creation, or background telemetry in v1.
4. **Side skill, not core infrastructure.** Implement v1 through `SKILL.md` only. Do not add Python logging modules, try/catch wrappers, dashboards, or automated submission.
5. **Evidence depth depends on scenario.** For system errors, capture raw command/tool output. For unsatisfactory answers, summarize attempts and the user's stated dissatisfaction.
6. **Internal-tool context.** This is an internal support workflow. Include the local username when available so the team can follow up for interviews or debugging context.
7. **Actionable for developers.** The core skill knowledge is deciding when to trigger the report offer. The saved JSON should then include area, severity, likely cause, reproduction notes, and a proposed regression test when possible.
8. **Friendly colleague tone.** The agent should offer reporting calmly and helpfully, as a teammate improving the skillset, not as an alarming crash dialog.

## Product Definition

The new skill helps users report two classes of RA-Skills failure.

### Scenario 1: System Or Execution Error

Use this when a concrete execution failure blocks or degrades the workflow.

Examples:

- A helper command fails unexpectedly.
- iData or Haver fetch fails after retry/self-correction policy.
- A Python import, SDK, dependency, permission, or path error blocks the workflow.
- A required local resource is missing, such as `haver.db`.
- A command times out repeatedly.
- The agent or tool run crashes, stops, or is interrupted unexpectedly.
- The agent says it created an output file, but the file is missing.
- Output is empty, corrupt, saved to the wrong location, or in the wrong format.

Suggested offer:

```text
It looks like this hit a system or execution error. I can prepare a local report for the development team with the raw command output so they can investigate. Would you like me to do that?
```

### Scenario 2: Unsatisfactory Answer After Repeated Attempts

Use this when the system does not crash, but the user still cannot get a useful result after repeated attempts.

Examples:

- The user asks the same or very similar query multiple times.
- The agent tries several self-corrections but still cannot find the right approach.
- The agent cannot identify the right database, dimension, code, geography, output format, or handoff.
- The agent repeatedly gives vague, incomplete, or unhelpful answers.
- The agent keeps asking the same clarification question and does not move the task forward.
- The user says the result is wrong, still not ideal, not what they need, or asks the agent to try again repeatedly.

Suggested offer:

```text
It seems like we still have not gotten you a useful answer after several tries. I can prepare a local report so the team can improve this workflow. Would you like me to do that?
```

### Manual User Trigger

The user may explicitly ask to report at any time after a visible failure.

Examples:

```text
Report this issue.
Send an error report.
Log this for the development team.
I am not satisfied, please report it.
Create an RA-Skills error report.
```

Manual report requests count as consent. Treat them as Scenario 2 unless the user describes a concrete system or execution failure, in which case use Scenario 1.


## Proposed Skill Location

Add a fifth sibling skill:

```text
.claude/skills/
├── imf-ra/
├── imf-ra-catalog/
├── imf-ra-data/
├── imf-ra-charts/
└── imf-ra-error-report/
    └── SKILL.md
```

Update the umbrella skill map in `.claude/skills/imf-ra/SKILL.md`:

```text
imf-ra-error-report | Use when the user wants to report a system/execution failure or an unsatisfactory RA-Skills answer after repeated attempts.
```

Proposed frontmatter:

```yaml
---
name: imf-ra-error-report
description: Use when a user wants to report a user-visible RA-Skills failure, including a system or execution error, failed helper/SDK/data fetch, missing output file, crash or timeout, or an unsatisfactory answer after repeated attempts. Creates a structured local JSON error report for the development team only after user consent.
---
```

## Target Report Folder

Report folder:

```text
tests/user_error_report/
```

Filename pattern:

```text
MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary.json
```

Examples:

```text
tests/user_error_report/06-05-2026-14-32-10-missing-haver-db.json
tests/user_error_report/06-05-2026-15-10-41-unsatisfactory-weo-lookup.json
```

Use this repo-local folder as the single report destination. Do not add a database, cloud sink, GitHub issue creation, dashboard, or report lifecycle workflow in v1.

## Consent And Follow-Up Rules

### Consent Rule

Never write a report silently.

The skill may offer a report after Scenario 1 or Scenario 2, but it must wait for user consent before creating the JSON file.

Accepted consent examples:

```text
yes
please report it
send it
create the report
log it
```

Decline examples:

```text
no
not now
do not report
skip
```

If the user declines, acknowledge briefly and do not create a file.

Manual report requests count as consent. If the user says "report this issue" or similar, create the JSON report without asking for consent again.

### Rate Limit Rule

Create at most five reports per conversation session.

If the user attempts to create a sixth report, do not silently drop it. Say:

```text
The maximum number of error reports for this session has been reached. Please start a new session if you need to report additional issues.
```

Do not create a sixth JSON file.

### Follow-Up Question Rule

Ask at most two concise follow-up questions before creating the report.

Ask only for missing information that materially improves the report. Do not block report creation if the user does not know the answer.

Useful questions:

```text
What were you trying to accomplish?
What result did you expect instead?
Can I include the command/output summary from this session?
```

If context is already available, use it and avoid asking.

## What To Capture

Use available conversation and command context where possible:

- Local username, if available.
- Original user request or concise task summary.
- Scenario: system/execution error or unsatisfactory answer after repeated attempts.
- Area: catalog, data, country-groups, charts, Haver, iData, docs, environment, output-file, agent-behavior, or other.
- Severity: High, Medium, or Low.
- Error category from the formal taxonomy below.
- Commands attempted.
- Raw stdout/stderr or raw tool output for system/execution errors.
- Short answer-attempt summaries for unsatisfactory-answer reports.
- Relevant error snippets.
- Files involved.
- Whether failure repeated.
- Retry/self-correction status.
- Duplicate fingerprint based on scenario, category, area, and short title.
- Expected behavior, if stated.
- Likely cause or current hypothesis.
- Suggested development action.
- Proposed regression test, if obvious.

If something is unknown, write `Unknown`.

## Evidence Depth By Scenario

### Scenario 1: System Or Execution Error

Capture deeper debugging evidence:

- Up to three command/helper/code attempts.
- Command, working directory, exit code, timestamp, raw stdout, and raw stderr for each attempt when available.
- Full raw output from the failing command/tool run when available.
- Files involved or expected output paths.
- Environment context such as OS type, Python version, repo path, and username.
- Retry count and whether retries were exhausted.

### Scenario 2: Unsatisfactory Answer After Repeated Attempts

Capture lighter product-feedback evidence:

- Original user request.
- Repeated-attempt count.
- Short summaries of the failed answers or approaches.
- User's stated dissatisfaction, correction, or expected answer.
- The likely stuck point, such as wrong database, wrong code, unclear geography, unsupported output format, or repeated clarification loop.
- Do not include a full raw conversation transcript by default.

## Framing Rule

Describe the visible symptom rather than internal policy labels.

Example framing:

Use:

```text
Agent appeared to guess or skipped validation and returned an unsupported code.
```

Avoid:

```text
Agent violated helper-first policy.
```

## Severity Guidance

```text
High: Blocks the RA workflow, produces likely wrong official identifiers/data, or crashes/fails repeatedly.
Medium: Produces confusing, incomplete, or unsatisfactory behavior that requires repeated user correction.
Low: Minor output, wording, formatting, or report-quality issue that does not block the task.
```

## Area Guidance

Choose one or two areas:

```text
catalog: database/code/dimension discovery issues
data: iData/Haver fetch workflow issues
country-groups: WEO group membership, expansion, framework ambiguity
charts: chart handoff or chart-ready data issues
Haver: Haver lookup/fetch/resource issues
iData: iData SDK/API/private-data issues
docs: skill docs/reference instructions are missing or misleading
environment: dependency, permission, missing local file, setup issue
output-file: expected artifact missing, corrupt, wrong format, wrong path
agent-behavior: repeated unsatisfactory answers, loops, poor clarification
other: none of the above
```

## Formal Classification Taxonomy

The taxonomy is the core knowledge of the skill. It tells the agent when to offer a report, when to retry or guide the user instead, and when to wait until recovery attempts are exhausted. This taxonomy lives in `SKILL.md` as agent reasoning guidance, not as a Python classifier.

| Category | Should offer report? | Severity | How to handle |
|---|---|---|---|
| `user_error` | No | Low | User input is invalid or incomplete. Explain and ask for corrected input. |
| `config_fixable` | No | Low | Environment issue the user can fix directly, such as an obviously missing package, checkout, or local resource like `haver.db`. Give setup guidance. |
| `config_unfixable` | Yes, after recovery fails | Medium | Environment issue that needs development review, such as missing expected local resources or unclear setup contract. |
| `transient_retry` | No | Low | Temporary network/tool/API issue while fewer than three retries have been attempted. Retry or self-correct first. |
| `transient_exhausted` | Yes | High | Temporary issue persists after three retries or self-correction attempts. |
| `data_format` | Yes | High | Data schema, API contract, parser, or field mismatch. |
| `logic_bug` | Yes | High | Agent/helper code logic error, such as `IndexError`, `AttributeError`, impossible branch, or invalid assumption. |
| `subprocess_failure` | Yes | High | Required helper script crashes or returns blocking nonzero status. |
| `database_corruption` | Yes | High | Reference data appears corrupt, missing required columns, or internally inconsistent. |
| `rate_limit` | No | Low | API/session usage limit. Explain limitation and possible retry timing. |
| `file_io_error` | Usually no | Medium | File permission, disk, sandbox, or path issue. Give guidance first; report only if expected output remains blocked after correction attempts. |
| `custom_script_first_attempt` | No | Low | First, second, or third failure in an ad hoc script written during the session. Debug and retry first. |
| `custom_script_exhausted` | Yes | High | Three custom-script attempts fail and the RA workflow remains blocked. |
| `unsatisfactory_answer` | Yes | Medium | User remains unsatisfied after three repeated attempts or the agent cannot make progress. |
| `unknown` | Yes, after brief triage | Medium | Failure is unclassifiable but user-visible and blocks or degrades the task. |

## Explicit Report And No-Report Rules

Offer a report immediately when the category is:

```text
logic_bug
database_corruption
subprocess_failure
data_format
transient_exhausted
custom_script_exhausted
```

Offer a report only after retry, self-correction, or user guidance has failed when the category is:

```text
config_unfixable
file_io_error
unknown
```

Offer a report for `unsatisfactory_answer` when the user has repeated the same or similar request three times, rejected the answer after three revisions, or the agent is stuck asking the same clarification without progress after three attempts.

Do not offer a report by default when the category is:

```text
user_error
config_fixable
transient_retry
rate_limit
custom_script_first_attempt
```

In no-report cases, the agent should explain the issue, retry if appropriate, or give the user a concrete next step. If the user explicitly asks to report anyway after a visible failure, allow a manual Scenario 2 report.

## JSON Report Template

Each report should be a single JSON file. Use `Unknown` for missing values. For system/execution errors, preserve raw stdout/stderr or raw tool output when available because this is an internal support workflow.

```json
{
  "report_id": "MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary",
  "timestamp": "YYYY-MM-DDTHH:MM:SSZ",
  "session_id": "Unknown",
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

## Detection And Prompting Logic

Use the classification taxonomy above as the controlling trigger logic. The scenario sections below are practical examples of when the report offer should appear.

### Scenario 1 Offer Conditions

The agent may offer a report when one of these is true:

- A command returns a nonzero exit code and blocks the task.
- The same helper, SDK, or data-fetch failure persists after three retry/self-correction attempts.
- A required local file or dependency is missing and setup guidance does not resolve the issue, or the user explicitly asks to report it.
- The agent cannot create the requested output file.
- A timeout, crash, interruption, or tool failure prevents completion.
- A generated output is unusable, empty, corrupt, or saved incorrectly.

### Scenario 2 Offer Conditions

The agent may offer a report when one of these is true:

- The user asks substantially the same topic repeatedly and still does not get a useful answer.
- The user says the answer is wrong, unsatisfactory, not ideal, or not what they need after three attempts/revisions.
- The agent has tried several self-corrections on the same topic without progress.
- Clarification repeats without resolving the task.

### Non-Error Conditions

Do not offer a report by default for normal RA-Skills behavior:

- Asking for missing time range before a data fetch.
- Asking for output format before a data fetch.
- Asking the user to choose between ambiguous catalog candidates.
- Clarifying WEO vs SPR/PRGT framework.
- Explaining that `imf-ra-charts` is scaffolded and not yet fully implemented.

If the user insists that one of these was problematic, allow a manual Scenario 2 report.

## Implementation Approach

Create only `SKILL.md`. The agent follows the instructions and writes the JSON report with normal file-edit tools.

No Python helper script is planned for v1. If later manual trials show agents consistently create malformed JSON or inconsistent filenames, a tiny deterministic helper can be reconsidered as a v1.5 follow-up, but it is outside the finalized v1 design.

## Files To Create Or Update

Minimum implementation:

| Path | Action | Purpose |
|---|---|---|
| `.claude/skills/imf-ra-error-report/SKILL.md` | Create | New error reporting skill. |
| `.claude/skills/imf-ra/SKILL.md` | Update | Add skill to family map and handoff notes. |
| `README.md` | Update | Add `imf-ra-error-report` to Key Features table and sample prompts. |
| `CLAUDE.md` | Update | Add convention that reports are user-consented and written to `tests/user_error_report/`. |
| `tests/auto_test_cases.yaml` | Update | Add behavior cases for Scenario 1 and Scenario 2. |
| `tests/auto_test_instructions.md` | Update | Mirror the new test cases for reviewers. |

Optional implementation:

| Path | Action | Purpose |
|---|---|---|
| `tests/user_error_report/.gitkeep` | Create | Repo-local folder for user error reports. |

Do not create a README inside the skill folder for v1 unless there is content that cannot live cleanly in `SKILL.md`.

## Test Plan

Add behavior tests that simulate report conditions without requiring real crashes.

### ERR-01: System Error Report Offer

Prompt:

```text
The catalog helper crashed with an AttributeError three times while trying to search WEO inflation codes. Please handle it.
```

Expected:

- Agent identifies this as Scenario 1.
- Error category is `logic_bug` or `subprocess_failure`.
- Agent offers to report the issue to the development team.
- Agent does not create a file until the user agrees.

### ERR-02: System Error Report Creation

Prompt:

```text
The catalog helper crashed with an AttributeError three times while trying to search WEO inflation codes. Report this issue.
```

Expected:

- Agent treats the manual request as consent.
- Agent creates a structured JSON report.
- Scenario is `system_error`.
- Area includes `catalog`.
- Error category is `logic_bug` or `subprocess_failure`.
- Report includes username when available.
- Report includes raw stdout/stderr or raw tool output for the failing system command.
- Report filename follows `MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary.json`.

### ERR-03: Unsatisfactory Answer Offer

Prompt:

```text
This is still not the right WEO inflation answer. We tried several times and it is still not useful.
```

Expected:

- Agent identifies this as Scenario 2.
- Agent asks whether the user wants to report the issue.
- Agent does not over-diagnose internal helper policy unless visible evidence supports it.

### ERR-04: Manual Unsatisfactory Report

Prompt:

```text
I am not satisfied with the answer after several tries. Please report this to the development team.
```

Expected:

- Agent treats request as consent.
- Agent creates a structured JSON report.
- Scenario is `unsatisfactory_answer`.
- Error category is `unsatisfactory_answer`.
- Area includes `agent-behavior` and possibly `catalog` if relevant.

### ERR-05: Non-Error Clarification

Prompt:

```text
You asked me which time range I want before fetching data. Is that an error?
```

Expected:

- Agent explains this is correct RA-Skills behavior, not an error report by default.
- Agent does not create a report unless the user insists.

### ERR-06: Config-Fixable Missing Local Resource

Prompt:

```text
The Haver lookup failed because haver.db is missing. Please handle it.
```

Expected:

- Agent classifies this as `config_fixable`.
- Agent gives setup/location guidance first.
- Agent does not offer a report by default.
- If the user explicitly says "report this issue," the agent may create a manual report.

### ERR-07: Raw System Output Capture

Prompt:

```text
The fetch command failed three times and printed a long traceback. Report it with the command output.
```

Expected:

- Agent creates a report.
- Agent includes raw stdout/stderr or raw tool output for the system error.
- Agent records the username when available.

### ERR-08: Rate Limit Enforcement

Prompt:

```text
Create six separate error reports in this session.
```

Expected:

- Agent creates at most five JSON report files.
- Agent tells the user the session report limit has been reached on the sixth request.
- Agent does not silently drop the sixth report.

## One-Week Work Plan

### Day 1: Finalize Design

- Confirm skill name: `imf-ra-error-report`.
- Confirm repo-local report folder target.
- Confirm two-scenario product model.
- Confirm v1 is skill-only.

### Day 2: Draft Skill

- Create `.claude/skills/imf-ra-error-report/SKILL.md`.
- Include consent rule, trigger rules, report template, scope boundaries, internal evidence rules, and repo-local report folder path.

### Day 3: Integrate Skill Family

- Update `.claude/skills/imf-ra/SKILL.md`.
- Update `README.md`.
- Update `CLAUDE.md`.
- Ensure language matches existing project-local skill conventions.

### Day 4: Add Tests

- Add `ERR-*` cases to `tests/auto_test_cases.yaml`.
- Mirror them in `tests/auto_test_instructions.md`.
- Include assertions for consent behavior, JSON report structure, taxonomy-driven trigger behavior, non-error clarification, raw-output capture, and rate limiting.

### Day 5: Manual Trial

- Simulate missing `haver.db` setup guidance.
- Simulate an unsatisfactory-answer report.
- Confirm generated JSON is valid, readable, and actionable.
- Confirm system-error reports include raw output and username when available.
- Confirm missing local resources are treated as `config_fixable` and guided first.
- Confirm no report is created before consent.

### Day 6: Polish

- Tighten wording.
- Check links and paths.
- Revise tests based on trial results.
- Confirm no Python helper script is needed for v1.

### Day 7: Review And PR Prep

- Run relevant helper command contracts.
- Run JSON validity checks and Markdown/path checks if available.
- Prepare PR summary with examples and test evidence.

## Acceptance Criteria

The v1 feature is complete when:

- `imf-ra-error-report` exists as a fifth sibling skill.
- The umbrella skill map mentions it.
- The skill clearly supports exactly two top-level report scenarios.
- The skill never writes a report before user consent.
- Manual report requests are treated as consent.
- Reports are written to `tests/user_error_report/`.
- Report filenames follow `MM-DD-YYYY-HH-MM-SS-3-to-5-word-summary.json`.
- Report JSON contains all required fields.
- Reports include severity, area, and formal taxonomy category fields.
- Reports include a duplicate fingerprint.
- System-error reports capture raw command/tool output when available.
- Reports include local username when available.
- Code/system errors use a retry threshold of three attempts.
- Unsatisfactory-answer reports use a threshold of three repeated attempts.
- Missing local resources such as `haver.db` are treated as `config_fixable` and guided first.
- The skill enforces a maximum of five reports per conversation session.
- Tests cover Scenario 1, Scenario 2, manual trigger, non-error clarification, config-fixable local resources, raw-output capture, and rate-limit behavior.
- The implementation remains small enough to complete within one week.

## Future Enhancements

Keep these out of v1, but preserve a path for them:

- Optional Markdown preview alongside JSON.
- Local index file listing reports.
- Duplicate detection by title/area/category.
- Tiny helper script for deterministic report creation, only if v1 testing shows repeated JSON or filename drift.

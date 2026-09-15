# IMF RA Skill Family — Behavioral Test Catalog & Execution Guide

**Objective:** Verify the IMF RA skill pipeline (`imf-ra` → `imf-ra-catalog` → `imf-ra-data`) routes analyst prompts correctly, resolves identifiers before fetch, preserves confirmed intent across handoffs, and stops for clarification when unsafe.

**Reference:** Detailed fixtures, assertions, and guardrails live in [auto_test_cases.yaml](auto_test_cases.yaml) (machine-readable source of truth).

---

## Scope & Constraints

| In Scope | Out of Scope |
|----------|--------------|
| 75 behavioral test cases across 9 categories | Chart execution skipped |
| 9 command contract checks (helper script validation) | User-interface/styling validation |
| Error classification, recovery, and consent flows | Performance/load testing |
| Cross-skill handoff behavior and intent preservation | Deprecated EcOS workflows |

---

## Test Environment Preconditions

✅ **Before starting, confirm you have:**

1. Python 3.11+ with IMF datatools SDK installed
2. Access to test fixture files in [auto_test_cases.yaml](auto_test_cases.yaml)
3. Fresh terminal session (unless YAML marks case as `fixture_based` or `multi_step`)
4. Write access to `tests/results/` folder for output

---

## Execution Workflow

### Step 1: Confirm Scope with User (HUMAN RESPONSIBILITY)

**Do this once, before any tests run.**

```
I will execute tests from these categories: 
  • Core Behavior Pipeline (SMOKE-*)
  • Catalog Helper Behavior (CONV-*, HPIPE-*, CAT-*, VINTAGE-*)
  • WEO Group Helper Behavior (GROUP-*, PIPE-*)
  
[add/remove categories as needed]

Please confirm or ask me to modify the scope.
```

Expected user response: approval or category changes.

---

### Step 2: Create Run Folder (HUMAN OR SCRIPT)

Create a timestamped results folder:

```bash
mkdir tests/results/2026-06-18_catalog_and_data_validation
```

Format: `YYYY-MM-DD_<description>`  
Examples:
- `2026-05-15_catalog_only_no_charts`
- `2026-06-18_full_behavioral_suite`

---

### Step 3: Copy Templates into Run Folder (SCRIPT)

```bash
cp tests/results/auto_test_detailed_results_template.yaml \
   tests/results/2026-06-18_catalog_and_data_validation/auto_test_detailed_results.yaml

cp tests/results/auto_test_summary_template.md \
   tests/results/2026-06-18_catalog_and_data_validation/auto_test_summary.md
```

---

### Step 4: Execute Each Test Case (CLAUDE OR HUMAN)

**For each test ID in your selected categories:**

1. **Get the prompt** from the catalog table below or from [auto_test_cases.yaml](auto_test_cases.yaml)
2. **Run the prompt** in a fresh Claude session
3. **Record observations:**
   - ✅ Did the agent activate the expected skill?
   - ✅ Did it use CSV references and helper commands?
   - ✅ Did it ask for clarification vs. guessing identifiers?
   - ✅ Did it preserve confirmed details (database, code, geography, date range)?

4. **If the test defines `machine_checks`:**
   - Run every command listed under `required_command_evidence.command`
   - Verify all `stdout_contains` strings appear in output
   - Verify all `stdout_must_not_contain` strings do NOT appear
   - Verify final response includes/excludes required text
   - **Mark FAIL if ANY machine check fails**, regardless of prose quality

5. **For `command_contract` cases:**
   - Run the exact command shown in the catalog table
   - Record stdout/stderr verbatim
   - **Pass only if output matches contract exactly** (proves helper script still works)

6. **Record result** in `auto_test_detailed_results.yaml`:
   ```yaml
   - id: CONV-03
     result: PASS  # or FAIL
     command: "[if applicable, paste exact command]"
     stdout_verification: "[key assertions met]"
     notes: "[what succeeded, what failed, why]"
   ```

---

### Step 5: Summarize Results (HUMAN OR SCRIPT)

After all selected tests complete, populate `auto_test_summary.md`:

```markdown
# Test Run: 2026-06-18 Catalog & Data Validation

**Status:** 12/15 PASSED | 2 FAILED | 1 NEEDS FOLLOW-UP

## FAILURES (FAILURES FIRST)

| Test ID | Issue | Root Cause | Action |
|---------|-------|-----------|--------|
| HPIPE-06 | Vintage DB not recognized | Catalog helper outdated | [ticket] Rebuild helper index |
| INT-03 | Partial data alert missing | Logic not implemented | Schedule for Q3 |

## All Results

[table with all test outcomes]

## Key Findings

- Catalog routing works correctly for WEO, IFS, WDI
- Dimension discovery still has 1 edge case (HPIPE-06)
- Error consent flow fully implemented
```

---

## Pass/Fail Criteria

| Criterion | Pass | Fail |
|-----------|------|------|
| **Skill routing** | Agent picks expected skill first | Agent picks wrong skill or skips required skill |
| **CSV/Helper usage** | Uses resolve, explain-source, dimensions commands | Invents codes, guesses, hardcodes |
| **Clarification** | Agent asks before guessing ambiguous inputs | Agent guesses without confirmation |
| **Intent preservation** | Database, code, geography, date range, vintage survive handoff | Any detail lost or changed without confirmation |
| **Machine checks** | All stdout assertions pass | Any stdout assertion fails |
| **Command contract** | Output matches expected content exactly | Output is different or missing expected strings |

---

## Output Files (REQUIRED)

Save **only these two files** in your run folder:

1. **`auto_test_detailed_results.yaml`** — Machine-readable results (source of truth)
2. **`auto_test_summary.md`** — Human summary (failures highlighted first)

**Do NOT generate:**
- COMPREHENSIVE_TEST_EXECUTION_REPORT.md
- README.md
- Narrative reports
- Extra documentation

## Test Catalog

### Core Behavior Pipeline

These cases prove the first meaningful step goes to the right skill and that
confirmed intent survives the catalog-to-data handoff.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| SMOKE-02 | I'm starting a project on emerging market debt - orient me to what's available. | `imf-ra` |

### Catalog Helper Behavior

These cases target catalog search pain points: source routing, strict resolve,
dimension discovery, ambiguity preservation, LIVE-vs-vintage logic, and clean
handoff payloads.

| ID | Prompt | Skill Set Involved | Pain Point |
|---|---|---|---|
| CONV-03 | Get me the IMF inflation series. | `imf-ra` -> `imf-ra-catalog` | Must ask clarification on multiple plausible indicators. |
| HPIPE-01 | Find the identifier for WEO real GDP growth and prepare the catalog handoff. Do not download yet. | `imf-ra` -> `imf-ra-catalog` | Must use `resolve --json`, not manual search or fetch. |
| HPIPE-02 | For an IFS CPI request, identify the replacement database and code path before any fetch. | `imf-ra` -> `imf-ra-catalog` | Must route legacy IFS before indicator lookup. |
| HPIPE-03 | Find WDI GDP per capita and prepare it for handoff. | `imf-ra` -> `imf-ra-catalog` | Must preserve WDI variant ambiguity and withhold handoff. |
| HPIPE-04 | Before using IMF.STA:CPI, check which code dimension it uses. | `imf-ra` -> `imf-ra-catalog` | Must discover `INDEX_TYPE`, not assume `INDICATOR`. |
| HPIPE-05 | Compare PCPI_PCH and PCPIE_PCH before choosing an inflation code. | `imf-ra` -> `imf-ra-catalog` | Must use `compare-codes` and ask variant confirmation. |
| HPIPE-06 | Prepare April 2024 WEO vintage nominal GDP in US dollars for data handoff. | `imf-ra` -> `imf-ra-catalog` | Must preserve vintage database and WEO Live metadata source. |
| CAT-02 | Find a quarterly WEO inflation series. | `imf-ra` -> `imf-ra-catalog` | Must reject unsupported WEO frequency assumptions. |
| CAT-04 | Find a financial soundness indicator for bank capital adequacy. | `imf-ra` -> `imf-ra-catalog` | Must route to the FSI catalog. |
| CAT-05 | Find me the WEO series for nominal GDP in USD. | `imf-ra` -> `imf-ra-catalog` | Must map to the correct WEO nominal GDP code. |
| CAT-06 | Find the exact IMF code for a custom concept that may not exist. | `imf-ra` -> `imf-ra-catalog` | Must say not found instead of inventing a code. |
| VINTAGE-01 | Use a WEO vintage for real GDP growth. | `imf-ra` -> `imf-ra-catalog` | Must choose vintage route, not WEO Live. |
| VINTAGE-04 | Use the latest WEO vintage for nominal GDP. | `imf-ra` -> `imf-ra-catalog` | Must distinguish latest vintage from WEO Live. |
| CAT-11 | Find nominal GDP in IMF.RES:WEO, not WEO Live. | `imf-ra` -> `imf-ra-catalog` | Must preserve explicit database constraint. |

### WEO Group Helper Behavior

These cases check WEO country/group lookup, framework-sensitive group meanings,
ambiguous country names, and iData-ready group expansion.

For EMDE prompts that say "IMF purposes" without naming WEO or SPR/PRGT, the expected behavior is to show both IMF frameworks and ask the user to choose before committing to a group: WEO `Emerging Market and Developing Economies(EMDE)` versus SPR/PRGT `SPR-Emerging Market and Middle-Income Economies(EM)` plus `SPR-Low-Income Developing Countries (LIC)`.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| CONV-01 | Which countries are in the WEO advanced economies group? | `imf-ra` |
| GROUP-02 | Pull real GDP growth for low-income countries, 2010-2024. | `imf-ra` |
| GROUP-04 | Can I use Advanced Economies(AE) directly in an iData pull for WEO data? | `imf-ra` |
| PIPE-02 | Resolve Congo in the WEO country reference before a data pull. | `imf-ra` |
| PIPE-03 | What is the difference between WEO and SPR/PRGT coverage in LIC? | `imf-ra` |

### Data Workflow Guardrails

These cases test the retrieval side of the pipeline: confirmed identifiers,
dimension handling, country/group resolution, time range confirmation,
output-format confirmation, retired EcOS policy, safe query behavior, and
LIVE-vs-vintage routing.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| DATA-01 | Pull the IMF data for inflation. | `imf-ra` -> `imf-ra-data` -> `imf-ra-catalog` |
| DATA-03 | Download confirmed WEO Live real GDP growth, annual, United States, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-07 | Given database IMF.RES.WEO:WEO_LIVE and key USA.NGDP_RPCH.A for 2010-2024, download the series once you have the key. | `imf-ra` -> `imf-ra-data` |
| DATA-09 | Use EcOS retrieval to get this IMF series. | `imf-ra` -> `imf-ra-data` |
| DATA-10 | Pull all countries, all indicators, all frequencies from IMF.RES.WEO:WEO_LIVE. | `imf-ra` -> `imf-ra-data` |
| DATA-15 | Write a quick Python script to fetch WEO real GDP growth for USA, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-19 | Download confirmed WDI GDP per capita for China, 2000-2023, as refreshable Excel. | `imf-ra` -> `imf-ra-data` |
| DATA-22 | Download confirmed WEO Live real GDP growth for Atlantis, annual, 2010-2024. | `imf-ra` -> `imf-ra-data` |

### Error Handling

These cases test error classification and recovery behavior across network failures, database corruption, query timeouts, and geography validation.

| ID | Prompt | Skill Set Involved | Scenario |
|---|---|---|---|
| ERR-01 | Pull WEO data but simulate a network timeout during fetch. How does the agent handle this? | `imf-ra-data` -> `imf-ra-error-report` | transient_retry classification, retry 3x, then offer report |
| ERR-02 | Fetch WEO data but the database returns corrupted or inconsistent records. How should the agent respond? | `imf-ra-data` -> `imf-ra-error-report` | database_corruption classification, immediate report offer |
| ERR-03 | User requests 30 years of daily data for 150 countries across multiple indicators. The query times out. How should the agent recover? | `imf-ra-data` -> `imf-ra-error-report` | Respect helper retry budget; offer report after exhaustion; scope changes require user agreement |
| ERR-04 | User requests WEO data for "Atlantis" which is not a valid WEO country. When should this be caught? | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` | two-point defensive validation (catalog + data) |

### Integration Failure

These cases test cross-skill coordination: discovery-to-fetch handoff, ambiguous catalog results, LIVE vs vintage decisions, partial data coverage, dimension name recovery, and multi-skill composition.

| ID | Prompt | Skill Set Involved | Scenario |
|---|---|---|---|
| E2E-01 | Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` | Full discovery-to-fetch handoff |
| E2E-02 | Find the code for real GDP growth and download it immediately. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` | Catalog boundary before fetch |
| INT-01 | User asks for "GDP growth" and catalog returns 5 plausible codes (WEO, IFS, WDI, DOTS, GFS variants). How does the agent proceed? | `imf-ra-catalog` | Present candidates, block fetch until confirmed |
| INT-02 | User requests WEO GDP for 2024 with historical data back to 1980. Should the agent use WEO Live or a vintage database? | `imf-ra-data` | Default to WEO LIVE; historical observation dates do not imply vintage |
| INT-03 | User requests WEO data for all countries in the "Low-Income Developing Countries" group, but only 60 of 160 countries have recent data. How does the agent alert the user? | `imf-ra-data` | Partial data alert with coverage ratio |
| INT-04 | User supplies a typo in the dimension name (e.g., "FREQUNCY" instead of "FREQUENCY"). How does the agent recover? | `imf-ra-data` | Fuzzy match, auto-correct, retry |
| HPIPE-07 | Prepare WEO real GDP growth for EMDEs, 2010-2024, for an iData pull. | `imf-ra` -> `imf-ra-catalog` -> WEO group helper -> `imf-ra-data` | Multi-skill composition |

### Output Formats

These cases test output generation edge cases: encoding handling, refreshable links, query sizing, and path validation.

| ID | Prompt | Skill Set Involved | Scenario |
|---|---|---|---|
| OUT-02 | Dataset contains non-ASCII characters (Chinese country names, special symbols). What encoding should be used? | `imf-ra-data` | UTF-8 default with user warning |
| OUT-03 | User requests a "refreshable" Excel file where cells auto-update from the live IMF API. Is this supported? | `imf-ra-data` | Explain limitation, suggest manual setup |
| OUT-04 | User requests 50 years of daily data for all 195 countries and 500+ indicators. How should the agent respond? | `imf-ra-data` | Pre-fetch size warning with scope reduction options |
| OUT-05 | User specifies an output path that does not exist or is not writable (e.g., "Z:/nonexistent/folder/data.csv"). How should the agent respond? | `imf-ra-data` | Validate path, suggest alternatives, ask confirmation |

### Error Reporting

These cases test error report generation workflow: consent flow and schema completeness.

| ID | Prompt | Skill Set Involved | Scenario |
|---|---|---|---|
| ERRREPORT-01 | A system error occurs during data fetch. Describe the exact consent flow the agent should follow before creating an error report. | `imf-ra-error-report` | Explicit ask for consent, never silent creation |
| ERRREPORT-02 | Verify that the error report JSON schema is fully designed and documented. | `imf-ra-error-report` | Schema completeness check |

### Command Contracts

These cases are deterministic command checks. Run them before or alongside
behavioral tests to make sure helper scripts still support the prompt-level
cases.

The contract set keeps one deterministic check for each helper capability that
the prompt cases depend on.

| ID | Command | Purpose |
|---|---|---|
| CONTRACT-28 | `python3 -c 'import ... catalog_data, catalog_routing, catalog_lookup, catalog_search ...'` | Split catalog helper modules import cleanly and preserve public helper exports. |
| CONTRACT-11 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py explain-source "IFS CPI for the United States" --json` | Legacy IFS CPI routes to `IMF.STA:CPI`. |
| CONTRACT-15 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "real GDP growth" --json` | Strict resolve returns WEO Live `NGDP_RPCH`. |
| CONTRACT-16 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "GDP per capita" --database WB:WDI --json` | Strict resolve preserves WDI variant ambiguity. |
| CONTRACT-23 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py dimensions IMF.STA:CPI` | Dimension discovery returns `INDEX_TYPE` examples. |
| CONTRACT-24 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py classify-database IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE` | Database classification identifies a WEO vintage. |
| CONTRACT-25 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py compare-codes PCPI_PCH PCPIE_PCH --database IMF.RES.WEO:WEO_LIVE` | Code comparison distinguishes period-average vs end-of-period CPI inflation. |
| CONTRACT-26 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "April 2024 WEO vintage nominal GDP in US dollars" --json` | WEO vintage resolution returns the vintage database, the matched WEO Live indicator source, and `NGDPD`. |
| CONTRACT-09 | `python3 ".claude/skills/imf-ra/country_group/country_groups_helper.py" expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only` | Group expansion returns iData-ready member country codes. |

---

## Maintenance & Ownership

| Task | Owner | Rules |
|------|-------|-------|
| **Add test cases** | YAML maintainer | Only add if it tests a distinct routing, catalog behavior, handoff.|
| **Keep this guide updated** | YAML maintainer + Documentation owner | Update this file if execution process changes, preconditions shift, or pass/fail criteria evolve. |
| **Run tests** | Research analyst or QA | Follow the workflow steps exactly. Ask for scope confirmation before starting. Record results in both YAML and Markdown. |
| **Triage failures** | Code owner (skill author) | Determine if failure is a test gap, assertion error, or actual behavior bug. Update test or fix skill. |

## Existing Python Environment Regression Cases

Run each case in a fresh session with the named worker loaded directly. Capture
commands, generated scripts, and filesystem changes, not only final answers.
Simulate missing dependencies without uninstalling real packages. These cases
test environment behavior; chart rendering is not required. Full prompts and
assertions are in [auto_test_cases.yaml](auto_test_cases.yaml).

| ID | Skill | Fixture and expected behavior |
|---|---|---|
| ENV-01 | `imf-ra-catalog` | Only standard library is available; load catalog directly. Run the bundled helper without package installation. |
| ENV-02 | `imf-ra-data` | imf_datatools is missing and no known configured interpreter is available. Identify interpreter and missing SDK; preserve the request and give IMF IT setup guidance, without trying PyPI. |
| ENV-03 | `imf-ra-charts` | Load charts directly; pandas exists but matplotlib is missing. Report matplotlib and interpreter, preserve prepared work; generated code must not install packages. |
| ENV-04 | `imf-ra-data` | Non-company environment: current Conda interpreter has SDK and pandas; harness supplies confirmed fetch inputs. Reuse the current interpreter without deactivating, deleting, recreating, or replacing it. |
| ENV-05 | `imf-ra-charts` | Installation was blocked by an externally managed environment error; only PNG requested. Give targeted manual provisioning guidance; do not bypass protections or install optional HTML/Excel packages. |

Fail every case on explicit or implicit environment creation (including tool
bootstrapping), automatic package installation/upgrades, or protection bypasses.
For ENV-04 also fail on deactivation or deletion of the existing environment.
An explicit user request to create an environment may override the default;
ordinary fetch, chart, and recovery requests do not.

## README-directed SDK Setup Regression Cases

These installation cases authorize the bounded SDK setup, unlike ordinary
ENV-* runtime requests. Run in fresh agent sessions with mocked interpreter,
installer, and package-manager results; do not modify a real corporate Python
installation for a behavioral test. Capture executable paths, commands, results,
and final readiness claims. Full prompts are in [auto_test_cases.yaml](auto_test_cases.yaml).

| ID | Fixture | Expected behavior |
|---|---|---|
| SETUP-01 | IMF Windows; existing company Python; SDK absent; official share readable; installer succeeds; pandas/openpyxl then pass. | Install all five skills, run stable installer once with selected Python, verify imports and helper help, report access untested. |
| SETUP-02 | Existing Python has working SDK, pandas, openpyxl. | Reuse SDK and verify without executing installer or pip. |
| SETUP-03 | IMF Windows: company Python executable is missing; another Python or a Store alias may be discoverable. | Complete skill files; ask the user to install Python through Software Center and retry skill installation; do not download Python or substitute another interpreter. |
| SETUP-04 | SDK absent; official share inaccessible or agent runs on unsupported macOS. | Complete skill files; report SDK setup blocked with the precise platform/share limitation. |
| SETUP-05 | SDK import works; pandas available; openpyxl absent; pip available and permitted. | Install only openpyxl with selected Python and repeat verification; do not update SDK. |
| SETUP-06 | SDK installer exits nonzero; fresh-process SDK import still fails. | Preserve failure details, finish skills, report incomplete setup; no blind retries or success claim. |
| SETUP-07 | User explicitly says install skills only; SDK absent. | Honor narrower scope; install skills without SDK changes. |

## Unified Design Regression Cases

Use fresh agent sessions with simulated data-service results; do not make real
SDK installations or repeated data calls for these fixtures. YAML is the source
of truth. Runtime cases must capture interpreter, cwd, helper path, output path,
and commands; do not score from the final response alone.

| ID | Scenario | Expected behavior |
|---|---|---|
| DESIGN-01 | Skills are globally installed under a path containing spaces; research folder is unrelated to the skill installation. Workspace has an existing configured Python. | Use verified absolute helper path and selected Python, preserve research cwd, pass explicit output path. |
| DESIGN-02 | Catalog handoff and geography are confirmed; output format not yet supplied. | Use LIVE by default; ask for Refreshable/Wide/Long and CSV/Excel as relevant before fetching. |
| DESIGN-03 | Earlier in conversation user selected long CSV and confirmed dates, geography, frequency, and indicator. | Carry forward prior format and run the single iData workflow without asking again. |
| DESIGN-04 | Requested vintage resolves exactly in catalog. | Preserve exact vintage; if fixture is changed to unavailable, report gap instead of substituting nearest release. |
| DESIGN-05 | User provides legacy EcOS identifiers; no code has run. | Explain retirement, resolve current iData alternatives via catalog, execute no EcOS code. |
| DESIGN-06 | Usable persistent CSV, chart dependencies and writable workspace available; no output folder specified. | Create persistent charts/ outputs without folder confirmation; script uses persistent input and works from another cwd. |
| DESIGN-07 | Helper log shows initial request plus two retries already failed for same inputs. | Do not rerun unchanged helper; explain exhausted recovery and offer report once. |
| DESIGN-08 | User previously identified a concrete RA answer problem; one revision failed; no useful correction remains. | Offer report once without requiring 3 or 5 more attempts; wait for consent. |
| DESIGN-09 | Country/frequency/database scope confirmed; one batched search returns insufficient results. | Ask for a distinguishing clue; a later substantive scope change permits one new lookup. |

Local executable checks: `python -m unittest discover -s tests -p "test_*.py"`
includes environment-checker subprocess isolation, missing versus broken
imports, import timeout, explicit Haver override, relocation with spaces, and
user-local readiness reports. These tests do not prove cross-host agent behavior
or live IMF connectivity.

## Review Follow-up Regression Cases

Use the fixtures in `auto_test_cases.yaml`; do not execute live database calls
for simulated cases. Inspect commands and deliverables, not just final claims.

| ID | Scenario | Expected behavior |
|---|---|---|
| REVIEW-01 | Dealogic SQL requested with execution explicitly declined; static validation passes. | Deliver unverified SQL with the reason; no verification or live inspection calls. |
| REVIEW-02 | Exact GDP@USECON lookup with local Haver metadata available. | Use the Haver helper's code command; no ad-hoc SQL. |
| REVIEW-03 | Default line chart from a usable CSV, no style overrides. | Center title/subtitle; align source to plot left; default top margin 18%; save PNG and complete script. |

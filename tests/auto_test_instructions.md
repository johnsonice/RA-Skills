# IMF RA skill family - auto-test catalog

This file is the human-readable catalog for the IMF RA skill family tests. The
machine-readable source of truth is [auto_test_cases.yaml](auto_test_cases.yaml),
which stores the prompts, fixtures, categories, and assertions.

The purpose of this catalog is to make sure the RA pipeline behaves like a
research assistant workflow, not just a collection of isolated prompts. The
tests check whether the agent starts with the right skill, uses reference files
instead of memory, resolves catalog identifiers before data retrieval, preserves
confirmed user intent across handoffs, and stops for clarification when a safe
fetch is not yet possible.

The pipeline logic is:

```text
imf-ra -> imf-ra-catalog -> imf-ra-data -> imf-ra-charts
```

For this test set, chart execution is intentionally excluded because
`imf-ra-charts` is still scaffolded. The active test coverage focuses on:
umbrella routing and shared conventions, catalog discovery, data workflow
guardrails, LIVE-vs-vintage behavior, and catalog-to-data handoff.

## How To Run

For each case, use the prompt listed here or in
[auto_test_cases.yaml](auto_test_cases.yaml). Start from a fresh session when
possible unless the YAML case is marked `fixture_based` or `multi_step`.

### Pre-Test Checks

Before running behavioral prompts, run the pre-test checks in
[auto_test_cases.yaml](auto_test_cases.yaml). At minimum:

```bash
bash .claude/skills/imf-ra/scripts/check_references.sh
python3 tests/check_referenced_files.py
```

Expected result:

- The reference checker prints `OK: all skills found, all references resolve.`
- The referenced-file scanner prints an `OK: checked ... file reference(s)`
  summary.

The referenced-file scanner reads active Markdown, YAML, shell, and Python
files, extracts file-looking references, and verifies that each target exists.
If a target is missing, it reports the source file/line and any likely nearby
filename matches. Stop before behavioral testing and ask the user whether to
create/restore the missing target, rename the file, update the reference, or
retire the stale test/doc.

Record whether the agent:

- activated the expected skill set,
- used CSV or Markdown references when required,
- asked for clarification instead of guessing,
- avoided invented identifiers and retired retrieval paths,
- preserved confirmed database, dimension, code, geography, date range, vintage,
  and output-format details across handoffs.

Use the YAML assertions to decide `Pass`, `Fail`, or `Needs follow-up`.
For `command_contract` cases, record stdout/stderr and pass only when the command
contract and expected content match exactly enough to prove the helper still
supports the behavioral tests.
For each full run, save a detailed YAML result file and a short Markdown report:

- YAML detail: copy [results/auto_test_results_template.yaml](results/auto_test_results_template.yaml) to `tests/results/auto_test_results_YYYY-MM-DD.yaml`.
- Markdown summary: copy [results/auto_test_report_template.md](results/auto_test_report_template.md) to `tests/results/auto_test_report_YYYY-MM-DD.md`.

## Test Catalog

### Routing Smoke

These cases make sure the first meaningful step goes to the right part of the
pipeline.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| SMOKE-01 | Pull WEO real GDP growth for G20 countries, 2010-present. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` if identifier confirmation is needed |
| SMOKE-02 | I'm starting a project on emerging market debt - orient me to what's available. | `imf-ra` |
| SMOKE-03 | Find me a quarterly inflation series for emerging markets. | `imf-ra` -> `imf-ra-catalog` |
| SMOKE-04 | Download IFS exchange rates monthly for ASEAN, 2015-present. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` for unresolved exchange-rate identifier |
| SMOKE-05 | What's the difference between WEO inflation and CPI in IFS? | `imf-ra` -> `imf-ra-catalog` |

### Shared Conventions

These cases test shared RA rules: reference-backed country/group lookup,
uncertainty handling, avoiding unnecessary code, and helper-first behavior for
fuzzy, comparative, expansion, validation, and handoff tasks.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| CONV-01 | Which countries are in the WEO advanced economies group? | `imf-ra` |
| CONV-02 | For IMF purposes, what does EMDE mean here? | `imf-ra` |
| CONV-03 | Get me the IMF inflation series. | `imf-ra` -> `imf-ra-catalog` |
| GROUP-02 | Pull real GDP growth for low-income countries, 2010-2024. | `imf-ra` |
| GROUP-04 | Can I use G110 directly in an iData pull for WEO data? | `imf-ra` |
| PIPE-01 | What does EMDE mean in the WEO country group reference? | `imf-ra` |
| PIPE-02 | Resolve Congo in the WEO country reference before a data pull. | `imf-ra` |
| PIPE-03 | What is the difference between WEO and SPR/PRGT coverage in LIC? | `imf-ra` |
| PIPE-04 | Prepare WEO real GDP growth for EMDEs, 2010-2024, for an iData pull. | `imf-ra` -> `imf-ra-data` |
| PIPE-05 | What is the WEO country code for South Korea? | `imf-ra` |

### Catalog Discovery

These cases test whether plain-English concepts are mapped to supported
databases, dimensions, vintages, and indicator codes without inventing
identifiers.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| CAT-01 | Find the IMF indicator for real GDP growth. | `imf-ra` -> `imf-ra-catalog` |
| CAT-02 | Find a quarterly WEO inflation series. | `imf-ra` -> `imf-ra-catalog` |
| CAT-03 | Find the current account balance series. | `imf-ra` -> `imf-ra-catalog` |
| CAT-04 | Find a financial soundness indicator for bank capital adequacy. | `imf-ra` -> `imf-ra-catalog` |
| CAT-05 | Find me the WEO series for nominal GDP in USD. | `imf-ra` -> `imf-ra-catalog` |
| CAT-06 | Find the exact IMF code for a custom concept that may not exist. | `imf-ra` -> `imf-ra-catalog` |
| VINTAGE-01 | Use a WEO vintage for real GDP growth. | `imf-ra` -> `imf-ra-catalog` |
| VINTAGE-02 | Use the latest WEO data for nominal GDP. | `imf-ra` -> `imf-ra-catalog` |
| VINTAGE-03 | Is IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE a live database or a WEO vintage? | `imf-ra` -> `imf-ra-catalog` |
| VINTAGE-04 | Use the latest WEO vintage for nominal GDP. | `imf-ra` -> `imf-ra-catalog` |
| VINTAGE-05 | Use WEO data for nominal GDP. | `imf-ra` -> `imf-ra-catalog` |
| CAT-07 | Find the World Bank WDI indicator for GDP per capita. | `imf-ra` -> `imf-ra-catalog` |
| CAT-08 | Find the Bloomberg ticker field for 10-year government bond yields. | `imf-ra` -> `imf-ra-catalog` |
| CAT-09 | Find the WTO-IMF Tariff Tracker commodity code for wheat. | `imf-ra` -> `imf-ra-catalog` |
| CAT-10 | Find the IFS CPI series for the United States. | `imf-ra` -> `imf-ra-catalog` |
| CAT-11 | Find nominal GDP in IMF.RES:WEO, not WEO Live. | `imf-ra` -> `imf-ra-catalog` |

### Data Workflow

These cases test the retrieval side of the pipeline: confirmed identifiers,
dimension handling, country/group resolution, time range confirmation,
output-format confirmation, retired EcOS policy, safe query behavior, and
LIVE-vs-vintage routing.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| DATA-01 | Pull the IMF data for inflation. | `imf-ra` -> `imf-ra-data` -> `imf-ra-catalog` |
| DATA-02 | Download IFS CPI for the United States. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` if identifier confirmation is needed |
| DATA-03 | Download confirmed WEO Live real GDP growth, annual, United States, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-04 | What frequencies are available for database IMF.RES.WEO:WEO_LIVE? | `imf-ra` -> `imf-ra-data` |
| DATA-05 | Use live WEO data for real GDP growth. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` if indicator confirmation is needed |
| DATA-06 | Use the April 2024 WEO vintage for nominal GDP. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` for vintage and indicator resolution |
| DATA-07 | Given database IMF.RES.WEO:WEO_LIVE and key USA.NGDP_RPCH.A for 2010-2024, download the series once you have the key. | `imf-ra` -> `imf-ra-data` |
| DATA-08 | Given database IMF.RES.WEO:WEO_LIVE, key USA.NGDP_RPCH.A, and time range 2010-2024, give me the raw wide file. | `imf-ra` -> `imf-ra-data` |
| DATA-09 | Use EcOS retrieval to get this IMF series. | `imf-ra` -> `imf-ra-data` |
| DATA-10 | Pull all countries, all indicators, all frequencies from IMF.RES.WEO:WEO_LIVE. | `imf-ra` -> `imf-ra-data` |
| GROUP-01 | Pull WEO real GDP growth for EMDEs, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| GROUP-03 | Download WEO nominal GDP for America, 2015-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-11 | Download confirmed WEO Live real GDP growth for the United States, 2010-2024. What frequency options are available before we choose? | `imf-ra` -> `imf-ra-data` |
| DATA-12 | Download confirmed WEO Live real GDP growth for the United States and Japan, annual, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-13 | Download confirmed WEO Live real GDP growth for USA, 2010-2024, in long CSV format. | `imf-ra` -> `imf-ra-data` |
| DATA-14 | Give me R code to download WEO real GDP growth for USA. | `imf-ra` -> `imf-ra-data` |
| DATA-15 | Write a quick Python script to fetch WEO real GDP growth for USA, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| DATA-16 | Download confirmed WEO Live real GDP growth for the United States and Japan, annual, 2010-2024, as refreshable Excel. | `imf-ra` -> `imf-ra-data` |
| DATA-17 | Download confirmed WEO Live real GDP growth and nominal GDP in USD for the United States and Japan, annual, 2010-2024, as refreshable Excel. | `imf-ra` -> `imf-ra-data` |
| DATA-18 | Download confirmed WEO Live real GDP growth and nominal GDP in USD for USA, annual, 2010-2024, as refreshable Excel. | `imf-ra` -> `imf-ra-data` |
| DATA-19 | Download confirmed WDI GDP per capita for China, 2000-2023, as refreshable Excel. | `imf-ra` -> `imf-ra-data` |
| DATA-20 | Download confirmed WEO Live real GDP growth for USA, annual, 2010-2024, as long CSV. If the endpoint returns 403, retry safely. | `imf-ra` -> `imf-ra-data` |
| DATA-21 | Give me Stata code to download WEO real GDP growth for USA. | `imf-ra` -> `imf-ra-data` |
| DATA-22 | Download confirmed WEO Live real GDP growth for Atlantis, annual, 2010-2024. | `imf-ra` -> `imf-ra-data` |
| GROUP-05 | Download WEO nominal GDP for Congo, 2015-2024. | `imf-ra` -> `imf-ra-data` |

### Helper Contracts

These cases are deterministic command checks. Run them before or alongside
behavioral tests to make sure helper scripts and canonical filenames still
support the prompt-level cases.

| ID | Command | Purpose |
|---|---|---|
| CONTRACT-01 | `bash .claude/skills/imf-ra/scripts/check_references.sh` | Active skill references resolve. |
| CONTRACT-02 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py latest-weo` | Latest WEO resolves to WEO Live. |
| CONTRACT-03 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"` | WEO Live real GDP growth search returns `NGDP_RPCH`. |
| CONTRACT-04 | `python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only` | Vintage search returns only vintage-style WEO resources. |
| CONTRACT-05 | `python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110` | WEO group helper expands advanced economies to member countries. |
| CONTRACT-06 | `python3 .claude/skills/imf-ra/scripts/weo_country_groups.py compare G201 G-PRGT-LIC` | WEO/SPR-PRGT group comparison returns counts and only-in-each-group rows. |
| CONTRACT-07 | `python3 .claude/skills/imf-ra/scripts/weo_country_groups.py resolve Congo` | Ambiguous country resolution returns both Congo candidates. |
| CONTRACT-08 | `python3 .claude/skills/imf-ra/scripts/weo_country_groups.py explain EM` | Framework-sensitive shorthand explanation returns WEO and SPR/PRGT codes. |
| CONTRACT-09 | `python3 .claude/skills/imf-ra/scripts/weo_country_groups.py expand-for-idata G200 --codes-only` | Group expansion returns iData-ready member country codes. |
| CONTRACT-10 | `python3 tests/check_referenced_files.py` | Active file references resolve; missing targets include source lines and likely filename suggestions. |

### End To End

This case tests the full discovery-to-retrieval handoff, including preserving
country, time range, and output-format intent.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| E2E-01 | Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` |
| E2E-02 | Find the code for real GDP growth and download it immediately. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` |

## Result Outputs

Use YAML as the detailed source of truth for each run, and Markdown as the
reviewer-facing summary.

| Output | Purpose | Template |
|---|---|---|
| `tests/results/auto_test_results_YYYY-MM-DD.yaml` | Full machine-readable run record with observed actions, evidence, and passed/failed assertions. | [results/auto_test_results_template.yaml](results/auto_test_results_template.yaml) |
| `tests/results/auto_test_report_YYYY-MM-DD.md` | Human-readable summary for reviewers, issue tracking, or PR notes. | [results/auto_test_report_template.md](results/auto_test_report_template.md) |

## Maintenance Notes

- Keep this Markdown file short and readable.
- Put detailed assertions, fixtures, and guardrails in
  [auto_test_cases.yaml](auto_test_cases.yaml).
- Add new cases only when they cover a distinct routing, catalog, data, or
  handoff behavior.
- Do not add chart-execution cases until `imf-ra-charts` is implemented.

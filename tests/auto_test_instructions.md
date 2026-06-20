# IMF RA skill family - auto-test catalog

This file is the human-readable catalog for the IMF RA skill family tests. The
machine-readable source of truth is [auto_test_cases.yaml](auto_test_cases.yaml),
which stores the prompts, fixtures, categories, and assertions.

The purpose of this catalog is to make sure the RA pipeline behaves like a
research assistant workflow, not just a collection of isolated prompts. The test
set has 43 active cases that check whether the agent starts with the right
skill, uses helper commands before temporary code, resolves catalog identifiers
before data retrieval, preserves confirmed intent across handoffs, and stops for
clarification when a safe fetch is not yet possible.

The pipeline logic is:

```text
imf-ra -> imf-ra-catalog -> imf-ra-data -> imf-ra-charts
```

For this test set, chart execution is intentionally excluded because
`imf-ra-charts` is still scaffolded. The active test coverage is grouped into
five channels: core pipeline behavior, catalog helper behavior, WEO group helper
behavior, data workflow guardrails, and command contracts.

## How To Run

For each case, use the prompt listed here or in
[auto_test_cases.yaml](auto_test_cases.yaml). Start from a fresh session when
possible unless the YAML case is marked `fixture_based` or `multi_step`.

Record whether the agent:

- activated the expected skill set,
- used CSV or Markdown references when required,
- asked for clarification instead of guessing,
- avoided invented identifiers and retired retrieval paths,
- preserved confirmed database, dimension, code, geography, date range, vintage,
  and output-format details across handoffs.

Use the YAML assertions to decide `Pass`, `Fail`, or `Needs follow-up`.
When a case defines `machine_checks`, collect that evidence before assigning a
pass:

- Run every `required_command_evidence.command`.
- Confirm every `stdout_contains` value appears in command output.
- Confirm every `stdout_must_not_contain` value is absent from command output.
- Check the final agent response against `final_response_must_include` and
  `final_response_must_not_include`.
- Mark the case `Fail` if a machine check fails, even if the prose answer sounds
  plausible.

For `command_contract` cases, record stdout/stderr and pass only when the command
contract and expected content match exactly enough to prove the helper still
supports the behavioral tests.
For each full run, create one dedicated run folder under `tests/results/` before
writing outputs. Use a date plus customized run name so repeated test runs do
not overwrite each other.

Recommended folder format:

```text
tests/results/YYYY-MM-DD_custom_test_name/
```

Save both outputs inside that folder:

- YAML detail: copy [results/auto_test_results_template.yaml](results/auto_test_results_template.yaml) into the run folder and name it `auto_test_results_<run_id>.yaml`.
- Markdown summary: copy [results/auto_test_report_template.md](results/auto_test_report_template.md) into the run folder and name it `auto_test_report_<run_id>.md`.

Examples:

- `tests/results/2026-05-15_bella_0515_test_with_Yaml/`
- `tests/results/2026-05-18_catalog_only_no_idata/`

## Test Catalog

### Core Behavior Pipeline

These cases prove the first meaningful step goes to the right skill and that
confirmed intent survives the catalog-to-data handoff.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| SMOKE-01 | Pull WEO real GDP growth for advanced economies, 2010-present. | `imf-ra` -> `imf-ra-data`; `imf-ra-catalog` if identifier confirmation is needed |
| SMOKE-02 | I'm starting a project on emerging market debt - orient me to what's available. | `imf-ra` |
| CONV-03 | Get me the IMF inflation series. | `imf-ra` -> `imf-ra-catalog` |
| E2E-01 | Find the correct IMF series for monthly exchange rates for Japan, then download it for 2018-2024 in long CSV format. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` |
| E2E-02 | Find the code for real GDP growth and download it immediately. | `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` |

### Catalog Helper Behavior

These cases target catalog search pain points: source routing, strict resolve,
dimension discovery, ambiguity preservation, LIVE-vs-vintage logic, and clean
handoff payloads.

| ID | Prompt | Skill Set Involved | Pain Point |
|---|---|---|---|
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
| VINTAGE-02 | Use the latest WEO data for nominal GDP. | `imf-ra` -> `imf-ra-catalog` | Must choose WEO Live for latest data. |
| VINTAGE-04 | Use the latest WEO vintage for nominal GDP. | `imf-ra` -> `imf-ra-catalog` | Must distinguish latest vintage from WEO Live. |
| CAT-11 | Find nominal GDP in IMF.RES:WEO, not WEO Live. | `imf-ra` -> `imf-ra-catalog` | Must preserve explicit database constraint. |

### WEO Group Helper Behavior

These cases check WEO country/group lookup, framework-sensitive group meanings,
ambiguous country names, and iData-ready group expansion.

For EMDE prompts that say "IMF purposes" without naming WEO or SPR/PRGT, the expected behavior is to show both IMF frameworks and ask the user to choose before committing to a group: WEO `Emerging Market and Developing Economies(EMDE)` versus SPR/PRGT `SPR-Emerging Market and Middle-Income Economies(EM)` plus `SPR-Low-Income Developing Countries (LIC)`.

| ID | Prompt | Skill Set Involved |
|---|---|---|
| CONV-01 | Which countries are in the WEO advanced economies group? | `imf-ra` |
| CONV-02 | For IMF purposes, what does EMDE mean here? | `imf-ra` |
| GROUP-02 | Pull real GDP growth for low-income countries, 2010-2024. | `imf-ra` |
| GROUP-04 | Can I use Advanced Economies(AE) directly in an iData pull for WEO data? | `imf-ra` |
| PIPE-02 | Resolve Congo in the WEO country reference before a data pull. | `imf-ra` |
| PIPE-03 | What is the difference between WEO and SPR/PRGT coverage in LIC? | `imf-ra` |
| HPIPE-07 | Prepare WEO real GDP growth for EMDEs, 2010-2024, for an iData pull. | `imf-ra` -> `imf-ra-catalog` -> WEO group helper -> `imf-ra-data` |

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

### Command Contracts

These cases are deterministic command checks. Run them before or alongside
behavioral tests to make sure helper scripts still support the prompt-level
cases.

The contract set keeps one deterministic check for each helper capability that
the prompt cases depend on.

| ID | Command | Purpose |
|---|---|---|
| CONTRACT-28 | `python3 -c 'import ... catalog_data, catalog_routing, catalog_lookup, catalog_search ...'` | Split catalog helper modules import cleanly and preserve public helper exports. |
| CONTRACT-11 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py explain-source "IFS CPI for the United States" --json` | Legacy IFS CPI routes to `IMF.STA:CPI`. |
| CONTRACT-15 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py resolve "real GDP growth" --json` | Strict resolve returns WEO Live `NGDP_RPCH`. |
| CONTRACT-16 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py resolve "GDP per capita" --database WB:WDI --json` | Strict resolve preserves WDI variant ambiguity. |
| CONTRACT-23 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py dimensions IMF.STA:CPI` | Dimension discovery returns `INDEX_TYPE` examples. |
| CONTRACT-24 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py classify-database IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE` | Database classification identifies a WEO vintage. |
| CONTRACT-25 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py compare-codes PCPI_PCH PCPIE_PCH --database IMF.RES.WEO:WEO_LIVE` | Code comparison distinguishes period-average vs end-of-period CPI inflation. |
| CONTRACT-26 | `python3 skills/imf-ra-catalog/scripts/catalog_search.py resolve "April 2024 WEO vintage nominal GDP in US dollars" --json` | WEO vintage resolution returns the vintage database, the matched WEO Live indicator source, and `NGDPD`. |
| CONTRACT-09 | `python3 "skills/imf-ra/Country Group/weo_country_groups.py" expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only` | Group expansion returns iData-ready member country codes. |

## Result Outputs

Use YAML as the detailed source of truth for each run, and Markdown as the
reviewer-facing summary.

| Output | Purpose | Template |
|---|---|---|
| `auto_test_results_<run_id>.yaml` inside the run folder | Full machine-readable run record with observed actions, evidence, and passed/failed assertions. | [results/auto_test_results_template.yaml](results/auto_test_results_template.yaml) |
| `auto_test_report_<run_id>.md` inside the run folder | Human-readable summary for reviewers, issue tracking, or PR notes. | [results/auto_test_report_template.md](results/auto_test_report_template.md) |

## Maintenance Notes

- Keep this Markdown file short and readable.
- Put detailed assertions, fixtures, and guardrails in
  [auto_test_cases.yaml](auto_test_cases.yaml).
- Add new cases only when they cover a distinct routing, catalog, data, or
  handoff behavior.
- Do not add chart-execution cases until `imf-ra-charts` is implemented.

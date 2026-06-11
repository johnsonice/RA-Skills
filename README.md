<h1 align="center">RA-Skills</h1>

<p align="center">
  <a href="https://docs.claude.com/en/docs/claude-code">Claude Code</a> skills for IMF Research Assistant workflows — natural-language data discovery, country/group resolution, retrieval, chart handoff, and local error reporting.
</p>

<p align="center">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://docs.claude.com/en/docs/claude-code"><img src="https://img.shields.io/badge/Claude%20Code-Skill-8A2BE2" alt="Claude Code"></a>
  <img src="https://img.shields.io/badge/skills.sh-Compatible-7CB342" alt="skills.sh">
</p>

<p align="center">
  <img src="assets/hero.png" alt="RA-Skills — modular workflow skills for IMF research workflows">
</p>


## Key features

| Skill | What it does |
|---|---|
| **`imf-ra`** | Family entry point. Loads shared operating rules, WEO country/group conventions, and routes to the right worker skill. |
| **`imf-ra-catalog`** | Plain English → `(database, dimension_name, code)`. Selects datasets, maps concepts to variable/indicator codes, and asks for confirmation when a request is ambiguous. |
| **`imf-ra-data`** | Fetches single series or multi-country panels through the internal Python SDK after identifiers, dimensions, time range, and output format are confirmed. Honors LIVE vs vintage explicitly. |
| **`imf-ra-charts`** | Hands tidy data to the internal charting tool. *Scaffolded — not yet implemented; route requests here only when wired up.* |
| **`imf-ra-error-report`** | Side skill for user-visible RA-Skills failures. Creates consent-based local JSON reports for system/execution errors or unsatisfactory answers after repeated attempts. |

Recommended chain: `imf-ra` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts`.

Support side path: use `imf-ra-error-report` only when a user wants to report a visible RA-Skills failure. It is not part of the normal data workflow and does not add telemetry, remote upload, GitHub issue creation, dashboards, or background logging.

Reference truth lives in CSVs (`imf-ra-catalog/databases/`, `imf-ra-catalog/indicators/`, and the consolidated WEO country-group file at `imf-ra/Country Group/Country Group.csv`) so the agent answers from data rather than memory.

Key guardrails:

- For catalog indicator/code discovery, source routing, exact code lookup, dimension discovery, database classification, and code comparison, the agent should use the relevant `imf-ra-catalog/scripts/catalog_search.py` command before writing temporary code. Direct CSV/Markdown inspection is still appropriate for exact one-row confirmation and curated guidance.
- WEO country groups are resolved through the self-contained `imf-ra/Country Group/` folder: `weo_country_groups.md` for guidance, `Country Group.csv` for the unified reference matrix, and `weo_country_groups.py` for lookup/expansion commands.
- WEO group/category columns such as `Advanced Economies(AE)` are for group lookup and membership mapping. They should not be used directly as iData country selectors; resolve groups to member `countrycode` values first unless dataset metadata confirms a supported aggregate code.
- For EM/LIC/PRGT requests, the agent should clarify WEO vs SPR/PRGT coverage because the group definitions can differ.
- Error reports are local and consent-based: use `imf-ra-error-report` only after a user-visible failure, and write reports to `tests/user_error_report/` in the structured JSON format defined by the skill.

## Sample queries

Drop any of these into Claude Code from inside the repo:

- *"I'm starting a project on emerging-market debt — orient me to what's available."*
- *"Which countries are in the WEO advanced economies group?"*
- *"Can I use Advanced Economies(AE) directly in an iData pull, or should I expand it to countries?"*
- *"What's the difference between WEO inflation and CPI in IFS?"*
- *"Find the current account balance series."*
- *"Find a quarterly inflation series for emerging markets."*
- *"Pull WEO real GDP growth for advanced economies, 2010–present."*
- *"Download IFS exchange rates monthly for ASEAN, 2015–present."*
- *"Use the April 2024 WEO vintage for nominal GDP."*
- *"Report this RA-Skills issue for the development team."*

More patterns live in the YAML-first auto-test pack:
[`tests/auto_test_cases.yaml`](tests/auto_test_cases.yaml) is the machine-readable source of truth, and
[`tests/auto_test_instructions.md`](tests/auto_test_instructions.md) is the reviewer-facing catalog.

## Quick start

```bash
git clone git@github.com:johnsonice/RA-Skills.git   # or HTTPS: https://github.com/johnsonice/RA-Skills.git
cd RA-Skills
claude   # or open Claude Code with cwd = this repo
```

Skills live under `.claude/skills/` and are **project-local** — Claude Code auto-loads them only when working in this repo. Nothing is installed globally.

Behavioral test pack: [`tests/auto_test_cases.yaml`](tests/auto_test_cases.yaml) defines prompts, fixtures, evidence files, and assertions for routing, catalog, data workflow, helper-contract, and end-to-end checks. [`tests/auto_test_instructions.md`](tests/auto_test_instructions.md) mirrors the same cases for human review. Run records and templates live under [`tests/results/`](tests/results/); issue notes live under [`tests/issue_tracking/`](tests/issue_tracking/).

## Layout

```
RA-Skills/
├── .claude/skills/
│   ├── imf-ra/             # umbrella + shared conventions
│   │   └── Country Group/  # unified WEO country-group CSV, guide, and helper
│   ├── imf-ra-catalog/     # database / variable-code discovery
│   ├── imf-ra-data/        # SDK-based data fetch
│   ├── imf-ra-charts/      # chart handoff (scaffold)
│   └── imf-ra-error-report/ # local consent-based failure reports
├── docs/specs/             # design docs
├── docs/plans/             # implementation history
├── tests/                  # YAML auto-test cases, reviewer catalog, results, issue tracking
└── CLAUDE.md               # agent conventions for this repo
```

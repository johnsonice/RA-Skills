<h1 align="center">RA-Skills</h1>

<p align="center">
  Cross-platform <a href="https://docs.claude.com/en/docs/claude-code">Agent Skills</a> for IMF Research Assistant workflows — natural-language data discovery, country/group resolution, retrieval, static chart production, and consent-based error reporting. Installs on GitHub Copilot (CLI &amp; cloud agent, incl. Windows), Claude Code, and other Agent Skills hosts.
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
| **`imf-ra-charts`** | Turns IMF RA data or user-provided CSV/Excel files into a static PNG chart plus the complete Python script that generated it. Offers an optional editable Excel workbook only after user confirmation. |
| **`imf-ra-error-report`** | Side skill for user-visible RA-Skills failures. Creates consent-based JSON reports on the shared Q drive for system/execution errors or unsatisfactory answers after repeated attempts. |

Recommended chain: `imf-ra` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts`.

Support side path: use `imf-ra-error-report` only when a user wants to report a visible RA-Skills failure. It is not part of the normal data workflow and does not add telemetry, remote upload, GitHub issue creation, dashboards, or background logging.

Reference truth lives in CSVs (`imf-ra-catalog/databases/`, `imf-ra-catalog/indicators/`, and the consolidated WEO country-group file at `imf-ra/country_group/country_group.csv`) so the agent answers from data rather than memory.

Key guardrails:

- For catalog indicator/code discovery, source routing, exact code lookup, dimension discovery, database classification, and code comparison, the agent should use the relevant `imf-ra-catalog/scripts/catalog_search.py` command before writing temporary code. Direct CSV/Markdown inspection is still appropriate for exact one-row confirmation and curated guidance.
- WEO country groups are resolved through the self-contained `imf-ra/country_group/` folder: `country_groups_instruction.md` for guidance, `country_group.csv` for the unified reference matrix, and `country_groups_helper.py` for lookup/expansion commands.
- WEO group/category columns such as `Advanced Economies(AE)` are for group lookup and membership mapping. They should not be used directly as iData country selectors; resolve groups to member `countrycode` values first unless dataset metadata confirms a supported aggregate code.
- For EM/LIC/PRGT requests, the agent should clarify WEO vs SPR/PRGT coverage because the group definitions can differ.
- Error reports are consent-based: use `imf-ra-error-report` only after a user-visible failure, and write reports to the shared `Q:\DATA\SPRAI\SPRAI_Projects\RA-Skill\user_error_reports\` destination in the structured JSON format defined by the skill. Verify that the destination is available and writable; do not silently fall back to the repository.

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
- *"Make a PNG chart from this CSV and save the reproducible Python script."*
- *"Report this RA-Skills issue for the development team."*

More patterns live in the YAML-first auto-test pack:
[`tests/auto_test_cases.yaml`](tests/auto_test_cases.yaml) is the machine-readable source of truth, and
[`tests/auto_test_instructions.md`](tests/auto_test_instructions.md) is the reviewer-facing catalog.

## Install

RA-Skills uses the open **Agent Skills** format; the canonical source is the top-level `skills/` directory.

### Quickest: ask your agent

Send this to your coding agent (GitHub Copilot, Claude Code, Codex, …) — it will read the steps below and pick the right one for its environment:

> Install the IMF Research Assistant skills from https://github.com/johnsonice/RA-Skills, following the install instructions in its README for your environment.

Before sending this message, IMF Windows users should install the latest
company-provided Python from **Software Center**, then reopen their terminal or
VS Code if necessary. The agent does not install Python itself.

### Required agent installation workflow

The installation request above includes both **all five skills** and **initial
IMF data SDK setup**. Explain this scope briefly, then complete both without a
separate SDK permission question, subject to the host's execution permissions.
If the user explicitly requests skills only, honor that narrower scope.

1. Install the complete family using the appropriate method below. Installing
   only `imf-ra-catalog` is not a complete data-pull setup.
2. Follow [IMF SDK setup](skills/imf-ra-data/references/sdk-setup.md) using the
   company Python at `C:\ProgramData\Python3\python.exe` on IMF-managed Windows.
   Check that it exists; if missing, ask the user to install Python through
   **Software Center**, then try the skill installation again. On other
   platforms, follow the shared runtime's interpreter rules.
   Install the missing SDK from the official
   IMF stable installer, then verify the data modules and fetch helpers. Reuse
   a working installation; do not automatically update it or create a virtual
   environment. This SDK setup is part of installation, not a task deferred to
   the user or to their first data request.
3. Report the installed skills, verified Python executable, SDK check results,
   and any remaining network/access or Haver database prerequisites. If setup
   is blocked, finish the skills installation and clearly distinguish it from
   incomplete data setup. Do not claim data access was verified from imports alone.

The [SDK setup procedure](skills/imf-ra-data/references/sdk-setup.md) owns the
check/install/verify commands, permitted dependencies, package destination, and
readiness report. Follow it with the interpreter selected by the
[shared runtime contract](skills/imf-ra/references/runtime.md). Import checks
establish local readiness; live data access requires an actual requested pull.

The host installation commands below install skill files; they do not themselves
run an SDK post-install hook. An agent following this README must complete the
workflow above. For a manual/plugin-menu install, ask the agent to complete this
README's SDK setup afterward.

### Install manually

**GitHub Copilot** (CLI or cloud agent, incl. Windows) — install into your personal skills dir with GitHub CLI ≥ 2.90:

```bash
gh skills install johnsonice/RA-Skills imf-ra-catalog
# For complete installation, repeat for imf-ra, imf-ra-data, imf-ra-charts,
# and imf-ra-error-report. Install a subset only when explicitly requested.
# (the subcommand is `gh skill` on some CLI versions — see GitHub's "Adding agent skills" docs)
```

Manual alternative (no extra CLI): copy the skill folder(s) from `skills/` into `~/.copilot/skills/` (or `~/.agents/skills/`).

**Claude Code** — install the whole family as one plugin:

```text
/plugin marketplace add johnsonice/RA-Skills
/plugin install imf-ra-skills
```

**Any Agent Skills host** (`skills.sh`):

```bash
npx skills add johnsonice/RA-Skills
```

**Local development** — clone and work in-repo on any host:

```bash
git clone https://github.com/johnsonice/RA-Skills.git
cd RA-Skills
python scripts/sync_skills.py   # mirror skills/ into .claude/skills + .agents/skills for discovery
claude                           # or open Copilot CLI / Codex with cwd = this repo
```

> Commands use `python`; if your machine only has `python3`, use that instead. For a global install that needs the Haver data tier, point `HAVER_DB_PATH` at your `haver.db`.

### Python environment policy

Interpreter selection and installation permissions are defined in the
[shared runtime contract](skills/imf-ra/references/runtime.md). IMF-managed
Windows uses `C:\ProgramData\Python3\python.exe`, with packages installed in
`C:\ProgramData\Python3\Lib\site-packages`. Do not create or use virtual/Conda
environments. Non-IMF machines may use an existing system Python for supported
local tasks. Ordinary data and chart requests do not authorize package
installation or upgrades; README-directed installation includes only the bounded SDK setup.

This contract is referenced by every distributed `SKILL.md`, so direct worker
invocation is covered. Skill instructions constrain agent behavior; they are not
an execution-level security boundary. A hard technical block requires the host's
command execution policy or a controlled runner that mediates all execution
paths; a denylist of a few shell command strings alone is insufficient.

### Dependency tiers

| Tier | Commands | Needs | Runs where |
|---|---|---|---|
| **Catalog** | discovery, WEO groups | Python 3.9+ (stdlib + bundled CSVs) | anywhere — laptops, CI, cloud, off-network |
| **Data – iData** | `fetch_idata.py` | internal `imf_datatools` SDK + pandas | IMF-managed Windows / cloud |
| **Data – Haver** | `fetch_haver.py` | `imf_datatools` SDK + pandas + `haver.db` | IMF machines with Haver access |
| **Charts** | `imf-ra-charts` generated scripts | pandas + matplotlib; openpyxl for `.xlsx` input; Plotly for optional HTML; xlsxwriter for optional Excel output | anywhere with local CSV/Excel or previously fetched data |

The catalog tier works everywhere; the data tiers require IMF-internal infrastructure. See [AGENTS.md](AGENTS.md) → *Dependencies & environments*.

Behavioral test pack: [`tests/auto_test_cases.yaml`](tests/auto_test_cases.yaml) defines prompts, fixtures, evidence files, and assertions for routing, catalog, data workflow, helper-contract, and end-to-end checks. [`tests/auto_test_instructions.md`](tests/auto_test_instructions.md) mirrors the same cases for human review. Run records and templates live under [`tests/results/`](tests/results/); issue notes live under [`tests/issue_tracking/`](tests/issue_tracking/).

## Layout

```
RA-Skills/
├── skills/                  # CANONICAL source of truth (one folder per skill)
│   ├── imf-ra/              # umbrella + shared conventions
│   │   └── country_group/   # unified WEO country-group CSV, guide, and helper
│   ├── imf-ra-catalog/      # database / variable-code discovery
│   ├── imf-ra-data/         # SDK-based data fetch
│   ├── imf-ra-charts/       # static PNG chart production + reproducible scripts
│   └── imf-ra-error-report/ # local consent-based failure reports
├── .claude-plugin/          # Claude Code plugin + marketplace manifests
├── scripts/                 # sync_skills.py (local-discovery mirror)
├── AGENTS.md                # cross-tool agent guidance (CLAUDE.md imports it)
├── requirements.txt         # dependencies by capability (including optional outputs)
├── docs/specs/              # design + distribution docs
├── docs/plans/              # implementation history
└── tests/                   # YAML auto-test cases, reviewer catalog, results, issue tracking
```

The `.claude/skills/` and `.agents/skills/` directories are **generated mirrors** for local discovery (Claude Code / Copilot+Codex respectively) — produced by `scripts/sync_skills.py` and gitignored. Edit `skills/`, never the mirrors.

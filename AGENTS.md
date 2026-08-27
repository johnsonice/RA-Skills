# AGENTS.md

Cross-tool guidance for AI coding agents working in this repo (GitHub Copilot, Claude Code, Codex, and any host that reads `AGENTS.md` or Agent Skills). Claude Code imports this file from `CLAUDE.md`.

## What this is

A family of **Agent Skills** for IMF Research Assistant workflows. The canonical source of truth is the top-level `skills/` directory:

- `imf-ra` — umbrella, family map, shared conventions
- `imf-ra-catalog` — natural-language → confirmed identifier: iData `(database, dimension_name, code)` (plus confirmed frequency/geography passed as handoff constraints) or Haver `codes: ["CODE@DB", ...]`
- `imf-ra-data` — pull series via internal Python SDK (`fetch_idata.py` for iData, `fetch_haver.py` for Haver)
- `imf-ra-charts` — turn IMF RA data or user-provided CSV/Excel files into a static PNG chart plus a complete reproducible Python script; optional editable Excel workbook only after confirmation
- `imf-ra-error-report` — side skill for consent-based local JSON reports after user-visible RA-Skills failures

Skill chain: `imf-ra` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts`.

Support side path: `imf-ra-error-report` is not part of the normal data pipeline. Use it only when the user wants to report a system/execution failure or an unsatisfactory RA-Skills answer after repeated attempts.

## Dependencies & environments (tiers)

Skills run at three capability tiers. Pick commands the current environment can satisfy:

| Tier | Skills / commands | Requires | Runs where |
|------|-------------------|----------|------------|
| **Catalog** (discovery) | `imf-ra-catalog` (`catalog_search.py`), WEO `country_groups_helper.py` | Python 3.9+ only (stdlib + bundled CSVs) | Anywhere — laptops, CI, cloud agents, off-network |
| **Data – iData** | `imf-ra-data` `fetch_idata.py` | Internal `imf_datatools` SDK + `pandas` | IMF-managed Windows / cloud only |
| **Data – Haver** | `imf-ra-data` `fetch_haver.py`, `haver_catalog_search.py` lookups | `haver.db` (SQLite) + `pandas` (metadata for fetch) | IMF machines with `haver.db` access |
| **Charts** | `imf-ra-charts` generated Python scripts | `pandas` + `matplotlib`; `xlsxwriter` only for optional Excel workbook output | Anywhere with local CSV/Excel or previously fetched data |

- `haver.db` is **not** in the repo (SQLite, 12M+ rows). Resolution order: `HAVER_DB_PATH` env var → an upward search for `haver.db` beside any ancestor of the script (conventionally one directory above the repo root) → a clear "not found" error. Set `HAVER_DB_PATH` when installed into a global skills dir.
- The internal `imf_datatools` SDK is IMF-only (installed from an internal location; see `skills/imf-ra-data/references/imf_datatools_agent_api_reference.md`). It is not pip-installable. Catalog lookup and WEO group helpers work without it.

## Interpreter note

Commands use `python`. If your machine only exposes `python3` (some macOS/Linux setups), use `python3` instead — the arguments are identical.

## Commands

```bash
# WEO country-group helpers (use only for ambiguous/repeated/heavy lookups)
python skills/imf-ra/country_group/country_groups_helper.py groups "advanced economies"
python skills/imf-ra/country_group/country_groups_helper.py members "Advanced Economies(AE)"
python skills/imf-ra/country_group/country_groups_helper.py memberships USA
python skills/imf-ra/country_group/country_groups_helper.py expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only

# iData catalog indicator/code discovery (use before writing temporary lookup code)
python skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python skills/imf-ra-catalog/scripts/catalog_search.py resolve "real GDP growth"
python skills/imf-ra-catalog/scripts/catalog_search.py explain-source "IFS CPI for the United States"
python skills/imf-ra-catalog/scripts/catalog_search.py code NGDP_RPCH --database IMF.RES.WEO:WEO_LIVE
python skills/imf-ra-catalog/scripts/catalog_search.py dimensions IMF.STA:CPI
python skills/imf-ra-catalog/scripts/catalog_search.py classify-database IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE
python skills/imf-ra-catalog/scripts/catalog_search.py compare-codes PCPI_PCH PCPIE_PCH --database IMF.RES.WEO:WEO_LIVE
python skills/imf-ra-catalog/scripts/catalog_search.py search "GDP per capita" --database WB:WDI
python skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only

# Haver catalog lookup (FTS5 over haver.db — never ad-hoc SQL LIKE; batch DBs in ONE call, --limit 300+)
python skills/imf-ra-catalog/scripts/Haver/haver_catalog_search.py search "10 year government bond yield" --databases G10 INTDAILY --limit 300
python skills/imf-ra-catalog/scripts/Haver/haver_catalog_search.py code GDP --db USECON
python skills/imf-ra-catalog/scripts/Haver/haver_catalog_search.py databases

# Pre-built fetch utilities (never write new retrieval scripts)
python skills/imf-ra-data/scripts/fetch_idata.py --db "IMF.RES.WEO:WEO_LIVE" --explore
python skills/imf-ra-data/scripts/fetch_idata.py --db "IMF.RES.WEO:WEO_LIVE" --dimension-values COUNTRY --keyword "USA"
python skills/imf-ra-data/scripts/fetch_idata.py --db "IMF.RES.WEO:WEO_LIVE" --key "USA+GBR.NGDP_RPCH..A" --start 2000 --end 2026 --format refreshable
python skills/imf-ra-data/scripts/fetch_haver.py --codes "GDP@USECON" "UNRATE@USECON" --start 2000 --end 2024 --format refreshable
```

After editing any `SKILL.md` or reference path, run the relevant helper command contracts and a Markdown link/path check.

## Auto-tests

Behavioral test pack: `tests/auto_test_cases.yaml` is the machine-readable source of truth. It defines prompts, fixtures, expected skills, evidence files, assertions, pre-test checks, and command contracts across `imf-ra`, `imf-ra-catalog`, and `imf-ra-data`. `tests/auto_test_instructions.md` mirrors the same cases as the human-readable catalog. 

Run records and templates: `tests/results/`. Issues and audit notes: `tests/issue_tracking/`. (Both are gitignored except tracked templates.)

## Layout

```
skills/<skill>/SKILL.md             # frontmatter + body — the canonical Agent Skill, discovered by every host
skills/imf-ra-catalog/databases/    # dataset truth: non_vintage_datasets.csv, vintage_datasets.csv + database_overview.md
skills/imf-ra-catalog/indicators/   # variable truth: 1. non_vintage, 2. bbg, 3. wdi, 4. wto variable lists
skills/imf-ra-catalog/scripts/      # catalog_search.py CLI + catalog_data/routing/lookup modules; Haver/haver_catalog_search.py
skills/imf-ra-data/scripts/         # fetch_idata.py + fetch_haver.py — the only supported retrieval paths
skills/imf-ra-data/references/      # imf_datatools_agent_api_reference.md (SDK recipes)
skills/imf-ra/country_group/        # country_group.csv (WEO country/group truth) + country_groups_helper.py helper + .md guide
skills/imf-ra-charts/                # chart-production skill: PNG + reproducible Python script, optional Excel workbook
skills/imf-ra-error-report/SKILL.md # consent-based local failure-report skill (no scripts)
.claude-plugin/                     # Claude Code plugin + marketplace manifests (one plugin: imf-ra-skills)
scripts/                            # sync_skills.py (mirror skills/ into host dirs for local discovery)
docs/specs/   # design + distribution docs
docs/plans/   # implementation history (ERROR_REPORTING_plan.md, family plan)
docs/Product_Road_Map.md   # product roadmap
tests/        # YAML auto-test cases, reviewer catalog, results, issue tracking
tests/user_error_report/   # local JSON reports created by imf-ra-error-report
```

`skills/` is the single source of truth. For in-repo local discovery on every host, `python scripts/sync_skills.py` mirrors `skills/` into `.claude/skills/` (Claude Code) and `.agents/skills/` (Copilot/Codex). Those mirrors are generated and gitignored — **never edit them; edit `skills/`**.

## Conventions agents must follow

- **CSVs are source of truth.** For dataset, variable/code, dimension, and WEO country-group questions, use the repo references and helper commands — don't recall from memory.
- **Prefer existing helpers.** For catalog indicator/code discovery, routing, exact code lookup, dimension discovery, database classification, and code comparison, run the relevant `catalog_search.py` command before writing temporary Python. Use direct CSV reads for exact confirmation; use new code only when no helper command covers the task.
- **Use the pre-built fetch utilities.** Pull data only through `fetch_idata.py` (iData) and `fetch_haver.py` (Haver) — never write new retrieval scripts. `fetch_idata.py` auto-sets private access, auto-chunks large country panels (default 25 values per dimension; `--chunk-size N` overrides), and auto-retries failed chunks before warning.
- **Haver has its own rules.** Search `haver.db` only via `haver_catalog_search.py` (never ad-hoc SQL `LIKE` — the table is unindexed for text). Batch multi-database searches into one call with `--databases ... --limit 300`; one query per search, no rephrasing reruns. Haver identifiers are `CODE@DATABASE` strings — there is no `dimension_name`. Strip the `HAVER:` display prefix before handing codes to `fetch_haver.py`.
- **Don't guess identifiers.** Database codes, variable codes, country groups, dimensions — never invent. If multiple plausible matches exist, list candidates and ask for confirmation.
- **LIVE vs vintage data must be honored explicitly** — see `skills/imf-ra-data/SKILL.md`. Never silently default to a dated vintage.
- **Error reporting is consent-based and local.** Use `imf-ra-error-report` only for user-visible failures, never for normal clarification behavior. Manual report requests count as consent. Reports go to `Q:\DATA\SPRAI\SPRAI_Projects\RA-Skill\user_error_reports\`; max 5 per conversation.
- **`skills/` is the source of truth.** Edit skills under `skills/`, then run `scripts/sync_skills.py` for local discovery. Generated mirrors and globally installed copies derive from it.

## Editing skills

- A skill = directory with `SKILL.md` (YAML frontmatter `name` + `description` + body), optionally `scripts/`, `references/`, and data files. The folder name is the skill name.
- To work on a skill locally, edit under `skills/`, then run `python scripts/sync_skills.py` so every host re-discovers it.

## Branch / commit conventions

**Every new branch must be named:**

```
<type>/<author>_<MMDD>_<topic>
```

- `<type>` — one of `feat`, `fix`, `test`, `docs`, `chore`.
- `<author>` — short lowercase first name (e.g. `bella`, `jamie`, `chengyu`).
- `<MMDD>` — branch creation date.
- `<topic>` — short slug describing the work, e.g. `auto-testing-steps`, `chunk_fetch`, `error_report`.

Example: `feat/chengyu_0509_auto-testing-steps`. Older remote branches without the `<type>/` prefix (e.g. `bella_0504_add_skills`, `jamie_0514_haver`) predate this rule — don't copy that style for new work. Check the name before the first push; renaming after a PR is open churns the review.

## PR best practices

1. **Branch name follows the convention.** Every PR branch matches `<type>/<author>_<MMDD>_<topic>` — see *Branch / commit conventions* above. Verify before the first push.
2. **One PR, one goal.** If a reviewer might want to merge half of it, split it. When the work genuinely can't be split, keep the goals separated by clean individual commits.
3. **Title is concise and descriptive.** Avoid `prep stuff`. If you can't write a concise title, rule #2 was probably violated.
4. **Lead with a TL;DR.** One line at the top before any long description.
5. **Give context and test instructions in the description.** Why the change exists, dependencies it needs, and exact steps to reproduce/test.
6. **Link issues with `Closes #N` / `Fixes #N`** so they auto-close on merge and cross-link.
7. **Use graphics and GitHub markdown** — screenshots/recordings for visual changes, fenced code blocks with language, tables, collapsible sections, mermaid diagrams.
8. **Add tests when the codebase supports them** — especially for bug fixes (red on `main`, green on the branch). For this repo, that means updating or extending `tests/auto_test_cases.yaml`, mirroring reviewer-facing changes in `tests/auto_test_instructions.md`, and recording run evidence under `tests/results/` or issue notes under `tests/issue_tracking/` when behavior changes.
9. **Self-review before assigning a reviewer.** Click "Viewed" on every file in the GitHub diff, remove debug output, and leave inline comments for non-obvious choices.

## Gotchas

- `imf-ra-charts` produces static PNG charts through generated Python scripts. It creates an optional Excel workbook only after the user confirms.
- The umbrella `imf-ra` does **not** orchestrate. Worker skills chain by referencing each other directly (e.g. `imf-ra-charts` loads `imf-ra-data` in the same turn).
- `imf-ra-error-report` is a side skill, not core infrastructure: no telemetry, remote upload, GitHub issue creation, dashboard, Python logging wrapper, or report lifecycle workflow belongs in v1.
- `haver.db` is machine-dependent and may be absent (it is not committed; it lives one directory above the repo root, or wherever `HAVER_DB_PATH` points). If Haver catalog search or `fetch_haver.py` fails because the file is missing, say so — don't fall back to guessing Haver codes.
- Actual data pulls require the internal `imf_datatools` SDK (IMF environment only). Catalog lookup and WEO group helpers work anywhere; `fetch_idata.py` / `fetch_haver.py` do not.
- EcOS retrieval is retired — never use `get_ecos_*` paths. The supported fetch workflow is Python-only (no R/Stata).
- `projects/`, `docs/decks/svg/`, `.claude/settings.local.json`, the generated `.claude/skills/` and `.agents/skills/` mirrors, and `tests/{results,issue_tracking,user_error_report}` contents are gitignored local artifacts — they exist locally but must not be committed.

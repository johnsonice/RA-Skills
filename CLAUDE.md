# CLAUDE.md

Project-local guidance for Claude Code working in this repo.

## What this is

A family of Claude Code skills for IMF Research Assistant workflows, project-local under `.claude/skills/`:

- `imf-ra` — umbrella, family map, shared conventions
- `imf-ra-catalog` — natural-language → `(database, dimension_name, code, frequency, geo)` lookup
- `imf-ra-data` — pull series via internal Python SDK
- `imf-ra-charts` — chart handoff (**not yet implemented**)
- `imf-ra-error-report` — side skill for consent-based local JSON reports after user-visible RA-Skills failures

Skill chain: `imf-ra` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts`.

Support side path: `imf-ra-error-report` is not part of the normal data pipeline. Use it only when the user wants to report a system/execution failure or an unsatisfactory RA-Skills answer after repeated attempts.

## Commands

```bash
# WEO country-group helpers (use only for ambiguous/repeated/heavy lookups)
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" groups "advanced economies"
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" members "Advanced Economies(AE)"
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" memberships USA

# Catalog indicator/code discovery (use before writing temporary lookup code)
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py explain-source "IFS CPI for the United States"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py code NGDP_RPCH --database IMF.RES.WEO:WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py dimensions IMF.STA:CPI
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py classify-database IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py compare-codes PCPI_PCH PCPIE_PCH --database IMF.RES.WEO:WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "GDP per capita" --database WB:WDI
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only
```

After editing any `SKILL.md` or reference path, run the relevant helper command contracts and a Markdown link/path check.

## Auto-tests

Behavioral test pack: `tests/auto_test_cases.yaml` is the machine-readable source of truth. It defines prompts, fixtures, expected skills, evidence files, assertions, pre-test checks, and command contracts across `imf-ra`, `imf-ra-catalog`, and `imf-ra-data`. `tests/auto_test_instructions.md` mirrors the same cases as the human-readable catalog. Chart execution cases are excluded.

Run records and templates: `tests/results/`. Issues and audit notes: `tests/issue_tracking/`.

## Layout

```
.claude/skills/<skill>/SKILL.md   # frontmatter + body — discovered by Claude Code
.claude/skills/imf-ra-catalog/databases/non_vintage_datasets.csv   # default dataset truth
.claude/skills/imf-ra-catalog/databases/vintage_datasets.csv       # explicit-vintage dataset truth
.claude/skills/imf-ra-catalog/indicators/1. non_vintage_variable_list.csv  # non-vintage variable truth
.claude/skills/imf-ra/Country Group/Country Group.csv                     # WEO country/group truth
docs/specs/   # design docs
docs/plans/   # implementation history
tests/        # YAML auto-test cases, reviewer catalog, results, issue tracking
tests/user_error_report/  # local JSON reports created by imf-ra-error-report
```

## Conventions Claude must follow

- **CSVs are source of truth.** For dataset, variable/code, dimension, and WEO country-group questions, use the repo references and helper commands — don't recall from memory.
- **Prefer existing helpers.** For catalog indicator/code discovery, routing, exact code lookup, dimension discovery, database classification, and code comparison, run the relevant `catalog_search.py` command before writing temporary Python. Use direct CSV reads for exact confirmation; use new code only when no helper command covers the task.
- **Don't guess identifiers.** Database codes, variable codes, country groups, dimensions — never invent. If multiple plausible matches exist, list candidates and ask for confirmation.
- **LIVE vs vintage data must be honored explicitly** — see `imf-ra-data/SKILL.md`.
- **Error reporting is consent-based and local.** Use `imf-ra-error-report` only for user-visible failures, never for normal clarification behavior. Manual report requests count as consent. Reports go to `tests/user_error_report/`.
- **Skill family is project-local.** Edits to `.claude/skills/` only affect work in this repo. No global install.

## Editing skills

- A skill = directory with `SKILL.md` (YAML frontmatter `name` + `description` + body).

## Branch / commit conventions

Observed in remote: `<author>_<MMDD>_<topic>`, e.g. `bella_0504_add_skills`, `feat/chengyu_0509_auto-testing-steps`. Use `feat/`, `fix/`, `test/`, `docs/`, `chore/` prefixes for new work.

## PR best practices

1. **One PR, one goal.** If a reviewer might want to merge half of it, split it. When the work genuinely can't be split, keep the goals separated by clean individual commits.
2. **Title is concise and descriptive.** Avoid `prep stuff`. If you can't write a concise title, rule #1 was probably violated.
3. **Lead with a TL;DR.** One line at the top before any long description.
4. **Give context and test instructions in the description.** Why the change exists, dependencies it needs, and exact steps to reproduce/test.
5. **Link issues with `Closes #N` / `Fixes #N`** so they auto-close on merge and cross-link.
6. **Use graphics and GitHub markdown** — screenshots/recordings for visual changes, fenced code blocks with language, tables, collapsible sections, mermaid diagrams.
7. **Add tests when the codebase supports them** — especially for bug fixes (red on `main`, green on the branch). For this repo, that means updating or extending `tests/auto_test_cases.yaml`, mirroring reviewer-facing changes in `tests/auto_test_instructions.md`, and recording run evidence under `tests/results/` or issue notes under `tests/issue_tracking/` when behavior changes.
8. **Self-review before assigning a reviewer.** Click "Viewed" on every file in the GitHub diff, remove debug output, and leave inline comments for non-obvious choices.

## Gotchas

- `imf-ra-charts` is referenced but not implemented — don't route chart requests there yet; surface that gap to the user.
- The umbrella `imf-ra` does **not** orchestrate. Worker skills chain by referencing each other directly (e.g. `imf-ra-charts` loads `imf-ra-data` in the same turn).
- `imf-ra-error-report` is a side skill, not core infrastructure: no telemetry, remote upload, GitHub issue creation, dashboard, Python logging wrapper, or report lifecycle workflow belongs in v1.

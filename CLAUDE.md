# CLAUDE.md

Project-local guidance for Claude Code working in this repo.

## What this is

A family of Claude Code skills for IMF Research Assistant workflows, project-local under `.claude/skills/`:

- `imf-ra` — umbrella, family map, shared conventions
- `imf-ra-catalog` — natural-language → `(database, series, frequency, geo)` lookup
- `imf-ra-data` — pull series via internal Python SDK
- `imf-ra-charts` — chart handoff (**not yet implemented**)

Skill chain: `imf-ra` → `imf-ra-catalog` → `imf-ra-data` → `imf-ra-charts`.

## Commands

```bash
# Verify skill structure and references resolve
bash .claude/skills/imf-ra/scripts/check_references.sh
# Expected: "OK: all skills found, all references resolve."

# WEO country-group helpers (use only for ambiguous/repeated/heavy lookups)
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py groups "advanced economies"
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py memberships USA
```

Run the verify script after editing any `SKILL.md` or reference path.

## Auto-tests

Behavioral test pack: `tests/auto_test_instructions.md` — agent reads it and runs full routing/guardrail tests across `imf-ra`, `imf-ra-catalog`, `imf-ra-data`. Chart cases excluded.

Run logs and issues: `tests/issue_tracking/`.

## Layout

```
.claude/skills/<skill>/SKILL.md   # frontmatter + body — discovered by Claude Code
.claude/skills/imf-ra-catalog/databases/idata_full_datasets_list.csv     # dataset truth
.claude/skills/imf-ra-catalog/indicators/idata_full_indicators_list.csv  # indicator truth
.claude/skills/imf-ra/references/Country Group/csv/                      # WEO group truth
docs/specs/   # design docs
docs/plans/   # implementation history
tests/        # auto-test instructions + issue tracking
```

## Conventions Claude must follow

- **CSVs are source of truth.** For dataset, indicator, and WEO country-group questions, read the CSVs directly — don't recall from memory.
- **No code for simple lookups.** If a reference CSV answers it, answer from the CSV. Use Python only for aggregation, joins, ambiguous resolution, or repeated filtering.
- **Don't guess identifiers.** Database codes, indicator codes, country groups, dimensions — never invent. If multiple plausible matches exist, list candidates and ask for confirmation.
- **LIVE vs vintage data must be honored explicitly** — see `imf-ra-data/SKILL.md`.
- **Skill family is project-local.** Edits to `.claude/skills/` only affect work in this repo. No global install.

## Editing skills

- A skill = directory with `SKILL.md` (YAML frontmatter `name` + `description` + body).
- After edits, re-run `check_references.sh` so cross-skill references resolve.

## Branch / commit conventions

Observed in remote: `<author>_<MMDD>_<topic>`, e.g. `bella_0504_add_skills`, `feat/chengyu_0509_auto-testing-steps`. Use `feat/`, `fix/`, `test/`, `docs/`, `chore/` prefixes for new work.

## Gotchas

- `.gitattributes` pins LF for `*.sh`. Windows users must run the verify script from **Git Bash** or **WSL**, never PowerShell/cmd.
- `imf-ra-charts` is referenced but not implemented — don't route chart requests there yet; surface that gap to the user.
- The umbrella `imf-ra` does **not** orchestrate. Worker skills chain by referencing each other directly (e.g. `imf-ra-charts` loads `imf-ra-data` in the same turn).

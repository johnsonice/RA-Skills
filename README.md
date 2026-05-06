# RA-Skills
Agent skills designed to help you become a very efficient research assistant.

## What's here

A family of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills for IMF Research Assistant workflows:

- **`imf-ra`** — umbrella, family map, shared conventions
- **`imf-ra-catalog`** — natural-language → database/series identifier discovery
- **`imf-ra-data`** — pulling data via the internal Python SDK
- **`imf-ra-charts`** — handing data to the internal charting tool

Recommended sequence: `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` -> `imf-ra-charts`.

The repo includes working skill docs, conventions, and reference CSVs. See [`docs/specs/`](docs/specs/) for design context and [`docs/plans/`](docs/plans/) for implementation history.

## Skill conventions

Across `imf-ra` and `imf-ra-catalog`:

- For straightforward requests, inspect available reference files and answer directly.
- Write or run code only for complex processing/search tasks.
- If there is material uncertainty, do not guess.
- If several plausible best matches exist, list them and ask the user for preference/confirmation.

For catalog-specific references:

- Dataset catalog: `imf-ra-catalog/databases/idata_full_datasets_list.csv`
- Indicator catalog: `imf-ra-catalog/indicators/idata_full_indicators_list.csv`
- Source-specific templates:
  - `imf-ra-catalog/databases/templates/idata_template.md`
  - `imf-ra-catalog/indicators/templates/idata_template.md`

## Use it (development mode)

```bash
# SSH (if you have keys configured):
git clone git@github.com:johnsonice/RA-Skills.git
# or HTTPS:
git clone https://github.com/johnsonice/RA-Skills.git

cd RA-Skills
claude  # or open Claude Code with cwd = this repo
```

The skills live under `.claude/skills/`, which Claude Code treats as **project-local** — it auto-loads them when working in this repo, and only here. Edit a `SKILL.md`, re-prompt, iterate. No install, no symlinks, nothing in your global `~/.claude/skills/`.

Works the same on macOS, Linux, and Windows. Claude Code's skill discovery is OS-agnostic; line endings for shell scripts are pinned to LF via `.gitattributes` so Windows checkouts don't corrupt the verify script's shebang.

## Verify

```bash
bash .claude/skills/imf-ra/scripts/check_references.sh
```

Expected: `OK: all skills found, all references resolve.`

You can also try the smoke-test prompts in [`.claude/skills/imf-ra/tests/prompts.md`](.claude/skills/imf-ra/tests/prompts.md) in a fresh Claude Code session inside this repo and confirm the expected skill activates for each.

> **Windows users:** the verify script is bash. Run it from **Git Bash** (ships with [Git for Windows](https://git-scm.com/download/win)) or **WSL** — not PowerShell or `cmd`.

## Layout

```
RA-Skills/
├── .claude/
│   └── skills/
│       ├── imf-ra/                  # umbrella
│       ├── imf-ra-catalog/          # variable / database discovery
│       ├── imf-ra-data/             # data fetch
│       └── imf-ra-charts/           # chart handoff
├── docs/
│   ├── specs/                       # design docs
│   └── plans/                       # implementation plans
├── .gitattributes                   # line-ending rules (LF for *.sh)
├── .gitignore                       # macOS / Windows / Python noise
├── LICENSE
└── README.md
```

Catalog internals:

```text
.claude/skills/imf-ra-catalog/
├── databases/
│   ├── idata_full_datasets_list.csv
│   └── templates/
│       └── idata_template.md
├── indicators/
│   ├── idata_full_indicators_list.csv
│   └── templates/
│       └── idata_template.md
├── references/
│   └── catalog-conventions.md
└── scripts/
    └── catalog_search.py
```

## Future: plugin packaging

When you want to share these with colleagues without requiring them to clone the repo, the family can be repackaged as a Claude Code plugin: rename `.claude/skills/` → `skills/`, add a `plugin.json` at the repo root, and distribute. The skill files themselves don't change — only the surrounding wrapper.

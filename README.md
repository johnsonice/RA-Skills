# RA-Skills
agent skills specifically designed to help you became a laziest research assistant ever

## What's here

A family of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills aimed at IMF Research Assistant workflows:

- **`imf-ra`** — umbrella, family map, shared conventions
- **`imf-ra-data`** — pulling data via the internal Python SDK
- **`imf-ra-charts`** — handing data to the internal charting tool
- **`imf-ra-catalog`** — natural-language → database/series identifier discovery

v1 ships scaffolding only — real SDK and chart-tool content fills in iteratively. See [`docs/specs/`](docs/specs/) for design and [`docs/plans/`](docs/plans/) for the implementation plan.

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
│       ├── imf-ra-data/             # data fetch
│       ├── imf-ra-charts/           # chart handoff
│       └── imf-ra-catalog/          # variable / database discovery
├── docs/
│   ├── specs/                       # design docs
│   └── plans/                       # implementation plans
├── .gitattributes                   # line-ending rules (LF for *.sh)
├── .gitignore                       # macOS / Windows / Python noise
├── LICENSE
└── README.md
```

## Future: plugin packaging

When you want to share these with colleagues without requiring them to clone the repo, the family can be repackaged as a Claude Code plugin: rename `.claude/skills/` → `skills/`, add a `plugin.json` at the repo root, and distribute. The skill files themselves don't change — only the surrounding wrapper.

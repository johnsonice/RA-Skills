# RA-Skills
agent skills specifically designed to help you became a laziest research assistant ever

## What's here

A family of [Claude Code](https://docs.claude.com/en/docs/claude-code) skills aimed at IMF Research Assistant workflows:

- **`imf-ra`** — umbrella, family map, shared conventions
- **`imf-ra-data`** — pulling data via the internal Python SDK
- **`imf-ra-charts`** — handing data to the internal charting tool
- **`imf-ra-catalog`** — natural-language → database/series identifier discovery

v1 ships scaffolding only — real SDK and chart-tool content fills in iteratively. See [`docs/specs/`](docs/specs/) for design and [`docs/plans/`](docs/plans/) for the implementation plan.

## Install

```bash
git clone git@github.com:johnsonice/RA-Skills.git
cd RA-Skills
./install.sh
```

`install.sh` creates symlinks `~/.claude/skills/<name>` → `RA-Skills/skills/<name>` so Claude Code discovers each skill. Editing files in this repo immediately reflects in your live skills. Re-runnable; won't overwrite anything that isn't already a correct symlink.

## Verify

After installing, run the reference checker to confirm all skill cross-links resolve:

```bash
bash ~/.claude/skills/imf-ra/scripts/check_references.sh
```

Expected output: `OK: all skills found, all references resolve.`

You can also try the smoke-test prompts in [`skills/imf-ra/tests/prompts.md`](skills/imf-ra/tests/prompts.md) in a fresh Claude Code session and confirm the expected skill activates for each.

## Layout

```
RA-Skills/
├── skills/
│   ├── imf-ra/                  # umbrella
│   ├── imf-ra-data/             # data fetch
│   ├── imf-ra-charts/           # chart handoff
│   └── imf-ra-catalog/          # variable / database discovery
├── docs/
│   ├── specs/                   # design docs
│   └── plans/                   # implementation plans
└── install.sh                   # symlink installer
```

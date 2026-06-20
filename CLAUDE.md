# CLAUDE.md

Claude Code reads this file. The full, cross-tool project guidance lives in **[AGENTS.md](AGENTS.md)** and is imported below so it loads automatically — start there.

@AGENTS.md

## Claude Code specifics

- **Skill discovery.** Claude Code auto-discovers skills from `.claude/skills/`, which is a *generated mirror* of the canonical `skills/` source. After changing anything under `skills/`, run `python3 scripts/sync_skills.py` so Claude Code (and the Copilot/Codex `.agents/skills/` mirror) pick up the change. Never edit the mirror directly — edit `skills/`.
- **Plugin install.** This repo is also a Claude Code plugin (`.claude-plugin/`). To install the family into another project: `/plugin marketplace add johnsonice/RA-Skills` then `/plugin install imf-ra`.
- **Project permissions.** Pre-approved helper commands live in `.claude/settings.json` (`permissions.allow`); they reference the canonical `skills/...` paths.

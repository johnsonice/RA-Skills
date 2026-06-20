#!/usr/bin/env python3
"""Mirror the canonical ``skills/`` tree into per-host discovery directories.

``skills/`` is the single source of truth. Claude Code auto-discovers skills from
``.claude/skills/`` and GitHub Copilot / Codex from ``.agents/skills/``. This script
mirrors every skill into both so each host finds the family while you work in the
repo, from one source. The mirrors are generated and gitignored — never edit them;
edit ``skills/`` and re-run this script.

Symlinks (live, no re-sync needed) are used where the OS allows; otherwise the
script falls back to a copy (re-run after each edit). On Windows without Developer
Mode, expect copies.

Usage (on Windows use ``python`` or ``py -3`` in place of ``python3``):
  python3 scripts/sync_skills.py            # sync: symlink where possible, else copy
  python3 scripts/sync_skills.py --mode copy   # force copy (no symlinks)
  python3 scripts/sync_skills.py --mode link   # symlink only (error if unsupported)
  python3 scripts/sync_skills.py --clean       # remove generated mirrors
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = REPO_ROOT / "skills"
HOST_DIRS = (
    REPO_ROOT / ".claude" / "skills",  # Claude Code
    REPO_ROOT / ".agents" / "skills",  # GitHub Copilot / Codex / cross-platform
)


def _skill_names() -> list[str]:
    return sorted(
        p.name
        for p in SKILLS_DIR.iterdir()
        if p.is_dir() and (p / "SKILL.md").exists()
    )


def _remove(path: Path) -> None:
    """Remove a file, symlink, or directory if it exists (symlink-safe)."""
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def _link_or_copy(src: Path, dest: Path, mode: str) -> str:
    _remove(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if mode in ("auto", "link"):
        try:
            os.symlink(src, dest, target_is_directory=True)
            return "link"
        except (OSError, NotImplementedError):
            if mode == "link":
                raise
    shutil.copytree(src, dest)
    return "copy"


def clean() -> None:
    for host in HOST_DIRS:
        if not host.exists():
            continue
        for child in list(host.iterdir()):
            _remove(child)
        print(f"cleaned {host.relative_to(REPO_ROOT)}")


def sync(mode: str) -> None:
    names = _skill_names()
    if not names:
        sys.exit(f"error: no skills found under {SKILLS_DIR}")
    for host in HOST_DIRS:
        for name in names:
            method = _link_or_copy(SKILLS_DIR / name, host / name, mode)
            print(f"{method:4}  {(host / name).relative_to(REPO_ROOT)}")
    print(f"\nsynced {len(names)} skills into {len(HOST_DIRS)} host dirs")


def main() -> None:
    ap = argparse.ArgumentParser(description="Mirror skills/ into host discovery dirs.")
    ap.add_argument("--clean", action="store_true", help="remove generated mirrors and exit")
    ap.add_argument(
        "--mode",
        choices=["auto", "link", "copy"],
        default="auto",
        help="auto (symlink, fallback copy), link (symlink only), or copy",
    )
    args = ap.parse_args()
    if not SKILLS_DIR.is_dir():
        sys.exit(f"error: {SKILLS_DIR} not found — run from the RA-Skills repo")
    if args.clean:
        clean()
        return
    sync(args.mode)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Verify file references used by the active RA skill/test docs.

The check is intentionally broader than the skill-local markdown checker:
it scans active Markdown, YAML, shell, and Python files for file-looking
references, verifies that each target exists, and suggests likely nearby files
when a referenced name looks inconsistent.
"""

from __future__ import annotations

import argparse
import difflib
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote, urlparse


DEFAULT_SCAN_TARGETS = [
    ".claude",
    "README.md",
    "CLAUDE.md",
    "tests/auto_test_cases.yaml",
    "tests/auto_test_instructions.md",
    "tests/results/auto_test_results_template.yaml",
    "tests/results/auto_test_report_template.md",
]

SKIP_DIRS = {".git", "__pycache__", ".pytest_cache", ".mypy_cache", ".DS_Store"}
SCAN_EXTS = {".md", ".yaml", ".yml", ".py", ".sh", ".txt"}
REFERENCE_EXTS = {
    ".csv",
    ".md",
    ".py",
    ".sh",
    ".yaml",
    ".yml",
    ".json",
    ".txt",
    ".png",
    ".jpg",
    ".jpeg",
    ".pptx",
    ".xlsx",
}

MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_ATTR_RE = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
PATH_RE = re.compile(
    r"""(?P<path>(?:\.\.?/|/|[A-Za-z0-9_. -]+/)[A-Za-z0-9_./%+@=,():'" -]+\.(?:csv|md|py|sh|ya?ml|json|txt|png|jpe?g|pptx|xlsx))"""
)


@dataclass(frozen=True)
class Ref:
    source: Path
    line_no: int
    raw: str
    mode: str


def iter_scan_files(repo: Path, targets: list[str]) -> list[Path]:
    files: list[Path] = []
    for target in targets:
        path = repo / target
        if not path.exists():
            continue
        if path.is_file():
            if path.suffix in SCAN_EXTS:
                files.append(path)
            continue
        for root, dirs, names in os.walk(path):
            dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
            for name in names:
                p = Path(root) / name
                if p.suffix in SCAN_EXTS:
                    files.append(p)
    return sorted(set(files))


def strip_ref(raw: str) -> str:
    ref = raw.strip().strip("<>").strip()
    ref = re.sub(r"^\s*-\s+", "", ref)
    ref = re.sub(r"^(?:python3?|bash|sh|ruby|node|perl)\s+", "", ref)
    ref = ref.split("#", 1)[0]
    ref = ref.rstrip(".,;:)\"'")
    ref = ref.lstrip("\"'")
    if ref.startswith("//"):
        return ""
    if ref == "/SKILL.md":
        return ""
    if '"' in ref or " / " in ref:
        return ""
    if re.match(r"^[A-Z_]+\s*/", ref):
        return ""
    if re.match(r"^[a-zA-Z_]+/SKILL\.md$", ref):
        return ""
    if re.match(r"^[A-Z][a-z]+ ", ref):
        return ""
    if ref.endswith(("_YYYY-MM-DD.yaml", "_YYYY-MM-DD.md")):
        return ""
    return unquote(ref)


def is_external(ref: str) -> bool:
    parsed = urlparse(ref)
    return parsed.scheme in {"http", "https", "mailto", "data"}


def has_reference_ext(ref: str) -> bool:
    return Path(ref).suffix.lower() in REFERENCE_EXTS


def extract_refs(path: Path) -> list[Ref]:
    refs: list[Ref] = []
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        text = path.read_text(encoding="utf-8-sig")
    for line_no, line in enumerate(text.splitlines(), 1):
        if path.suffix in {".py", ".sh"} and line.lstrip().startswith("#"):
            continue
        for match in MARKDOWN_LINK_RE.finditer(line):
            refs.append(Ref(path, line_no, match.group(1), "markdown-link"))
        for match in HTML_ATTR_RE.finditer(line):
            refs.append(Ref(path, line_no, match.group(1), "html-attr"))
        for match in PATH_RE.finditer(line):
            refs.append(Ref(path, line_no, match.group("path"), "path-token"))
    return refs


def resolve_ref(repo: Path, ref: Ref) -> Path | None:
    target = strip_ref(ref.raw)
    if not target or is_external(target) or not has_reference_ext(target):
        return None
    p = Path(target)
    if p.is_absolute():
        return p

    root_candidate = repo / p
    if target.startswith((".claude/", "docs/", "tests/", "assets/", "README", "CLAUDE")):
        return root_candidate
    if target.startswith(("imf-ra/", "imf-ra-data/", "imf-ra-catalog/", "imf-ra-charts/")):
        return repo / ".claude" / "skills" / p

    skill_root = skill_root_for(ref.source, repo)
    if skill_root is not None:
        if target.startswith(("scripts/", "references/", "databases/", "indicators/", "overlays/")):
            return skill_root / p
        if target.startswith(("imf-ra/", "imf-ra-data/", "imf-ra-catalog/", "imf-ra-charts/")):
            return skill_root.parent / p

    source_relative = ref.source.parent / p
    if source_relative.exists() or ref.mode in {"markdown-link", "html-attr"}:
        return source_relative
    return root_candidate


def skill_root_for(source: Path, repo: Path) -> Path | None:
    try:
        rel = source.relative_to(repo / ".claude" / "skills")
    except ValueError:
        return None
    parts = rel.parts
    if not parts:
        return None
    return repo / ".claude" / "skills" / parts[0]


def likely_matches(repo: Path, target: Path) -> list[Path]:
    parent = target.parent
    candidates: list[Path] = []
    if parent.exists() and parent.is_dir():
        entries = [p for p in parent.iterdir() if p.is_file()]
        names = [p.name for p in entries]
        for name in difflib.get_close_matches(target.name, names, n=5, cutoff=0.55):
            candidates.append(parent / name)
        target_norm = normalize_name(target.name)
        for entry in entries:
            if normalize_name(entry.name) == target_norm and entry not in candidates:
                candidates.append(entry)
    else:
        for entry in repo.rglob(target.name):
            if entry.is_file():
                candidates.append(entry)
    return candidates[:5]


def normalize_name(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", name.casefold())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", default=".", help="Repository root to scan.")
    parser.add_argument(
        "--target",
        action="append",
        dest="targets",
        help="File or directory to scan. Defaults to active skill/test docs.",
    )
    args = parser.parse_args()

    repo = Path(args.repo).resolve()
    targets = args.targets or DEFAULT_SCAN_TARGETS
    files = iter_scan_files(repo, targets)
    missing: list[tuple[Ref, Path, list[Path]]] = []
    checked: set[tuple[Path, int, str, Path]] = set()

    for file in files:
        for ref in extract_refs(file):
            resolved = resolve_ref(repo, ref)
            if resolved is None:
                continue
            key = (ref.source, ref.line_no, strip_ref(ref.raw), resolved)
            if key in checked:
                continue
            checked.add(key)
            if not resolved.exists():
                missing.append((ref, resolved, likely_matches(repo, resolved)))

    if missing:
        print("FAILED: missing or inconsistent file references found.")
        for ref, resolved, suggestions in missing:
            rel_source = ref.source.relative_to(repo)
            try:
                rel_resolved = resolved.relative_to(repo)
            except ValueError:
                rel_resolved = resolved
            print(f"MISSING: {rel_source}:{ref.line_no}: {strip_ref(ref.raw)}")
            print(f"  target: {rel_resolved}")
            if suggestions:
                print("  possible inconsistent name(s):")
                for suggestion in suggestions:
                    try:
                        shown = suggestion.relative_to(repo)
                    except ValueError:
                        shown = suggestion
                    print(f"    - {shown}")
            else:
                print("  possible inconsistent name(s): none found near target")
        return 1

    print(f"OK: checked {len(checked)} file reference(s) across {len(files)} active file(s).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

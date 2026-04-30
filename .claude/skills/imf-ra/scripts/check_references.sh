#!/usr/bin/env bash
# Verify that every markdown reference in each family SKILL.md points to an existing file.
# Exits non-zero if any reference is broken.

set -euo pipefail

# Default SKILLS_DIR: this script lives at <skills_dir>/imf-ra/scripts/, so go up
# two levels to find the family root. Override via env var if checking elsewhere.
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${SKILLS_DIR:-$(cd "$SCRIPT_DIR/../.." && pwd)}"
FAMILY=("imf-ra" "imf-ra-data" "imf-ra-charts" "imf-ra-catalog")

errors=0

for skill in "${FAMILY[@]}"; do
    skill_dir="$SKILLS_DIR/$skill"
    skill_md="$skill_dir/SKILL.md"

    if [[ ! -f "$skill_md" ]]; then
        echo "MISSING: $skill_md"
        errors=$((errors + 1))
        continue
    fi

    # Extract markdown link targets that point to .md files (e.g., (references/conventions.md)).
    # `|| true` keeps the script alive under `set -e` when grep finds no matches.
    # The second sed strips fragment (#anchor) and title-string (" title") suffixes.
    while IFS= read -r ref; do
        [[ -z "$ref" ]] && continue
        [[ "$ref" =~ ^https?:// ]] && continue

        ref_path="$skill_dir/$ref"
        if [[ ! -e "$ref_path" ]]; then
            echo "BROKEN REF in $skill_md: $ref"
            errors=$((errors + 1))
        fi
    done < <(grep -oE '\([^)]+\.md[^)]*\)' "$skill_md" | sed -E 's/^\(|\)$//g; s/[# ].*//' || true)
done

if [[ $errors -eq 0 ]]; then
    echo "OK: all skills found, all references resolve."
    exit 0
else
    echo "FAILED: $errors broken reference(s)."
    exit 1
fi

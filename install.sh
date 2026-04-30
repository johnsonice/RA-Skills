#!/usr/bin/env bash
# Install RA-Skills into ~/.claude/skills/ via symlinks.
# Idempotent — safe to re-run. Won't overwrite anything that isn't already a correct symlink.

set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
FAMILY=("imf-ra" "imf-ra-data" "imf-ra-charts" "imf-ra-catalog")

mkdir -p "$SKILLS_DIR"

for s in "${FAMILY[@]}"; do
    src="$REPO_DIR/skills/$s"
    dst="$SKILLS_DIR/$s"

    if [[ ! -d "$src" ]]; then
        echo "$s: missing in repo at $src — skipping"
        continue
    fi

    if [[ -L "$dst" ]]; then
        target="$(readlink "$dst")"
        if [[ "$target" == "$src" ]]; then
            echo "$s: already linked correctly"
            continue
        fi
        echo "$s: existing symlink points elsewhere ($target) — refusing to replace"
        continue
    fi

    if [[ -e "$dst" ]]; then
        echo "$s: $dst exists and is not a symlink — refusing to overwrite. Resolve manually."
        continue
    fi

    ln -s "$src" "$dst"
    echo "$s: linked $dst -> $src"
done

echo
echo "Done. Verify with:"
echo "  bash $SKILLS_DIR/imf-ra/scripts/check_references.sh"

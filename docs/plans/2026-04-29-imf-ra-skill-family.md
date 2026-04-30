# IMF RA Skill Family Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Scaffold the v1 IMF RA Claude Code skill family — four sibling skills under `~/.claude/skills/` (`imf-ra` umbrella + `imf-ra-data`, `imf-ra-charts`, `imf-ra-catalog` workers) with frontmatter, structural references, catalog templates, smoke-test prompts, and a reference-reachability checker. Real domain content (SDK calls, chart-tool invocations, real database catalog entries) is filled in iteratively after this scaffolding lands.

**Architecture:** Umbrella + workers, sibling skills (no plugin yet). Discovery uses the verified flat pattern `~/.claude/skills/<name>/SKILL.md`. Workers reference the umbrella for shared conventions; cross-worker references happen via markdown links rather than a workflow orchestrator. Detail in [docs/superpowers/specs/2026-04-29-imf-ra-skill-family-design.md](../specs/2026-04-29-imf-ra-skill-family-design.md).

**Tech Stack:** Markdown (skill content), bash (reference reachability checker). No application code is written in this plan; the SDK and charting tool are external and out of scope.

**Notes for the executor:**
- Skill files live in `$HOME/.claude/skills/`. The plan uses absolute `~/.claude/skills/...` paths throughout.
- Commit steps assume `~/.claude/skills/` is a git repo. If it isn't, either run `git init` in `$HOME/.claude/skills/` first, or skip the `git add`/`git commit` steps. The spec explicitly chose "no plugin in v1" — versioning the skills folder is optional.
- Verification steps use only `bash`, `test`, and `grep`. No Python or Node dependencies.

---

## File Structure

Files created by this plan:

| Path | Responsibility |
|---|---|
| `~/.claude/skills/imf-ra/SKILL.md` | Umbrella entry point. Frontmatter with broad description, body that maps the family. |
| `~/.claude/skills/imf-ra/references/conventions.md` | Shared conventions stub: SDK setup pointer, country codes, frequency, dates, units. |
| `~/.claude/skills/imf-ra/tests/prompts.md` | Smoke-test prompts with expected primary skill for each. |
| `~/.claude/skills/imf-ra/scripts/check_references.sh` | Bash reference-reachability checker. |
| `~/.claude/skills/imf-ra-data/SKILL.md` | Worker frontmatter + body pointing to umbrella + sdk-usage. |
| `~/.claude/skills/imf-ra-data/references/sdk-usage.md` | Stub for internal Python SDK call patterns. |
| `~/.claude/skills/imf-ra-charts/SKILL.md` | Worker frontmatter + body pointing to umbrella, sdk-usage, chart-tool-usage. |
| `~/.claude/skills/imf-ra-charts/references/chart-tool-usage.md` | Stub for the internal charting tool's invocation. |
| `~/.claude/skills/imf-ra-catalog/SKILL.md` | Worker frontmatter + body describing search workflow over `databases/` + `overlays/`. |
| `~/.claude/skills/imf-ra-catalog/references/catalog-conventions.md` | Two-layer catalog design + schemas. |
| `~/.claude/skills/imf-ra-catalog/databases/_template.md` | Schema template for a per-database file. |
| `~/.claude/skills/imf-ra-catalog/overlays/_template.md` | Schema template for an overlay file. |

Total: 12 files across four skill folders.

---

## Task 1: Create the skill family directory tree

**Files:**
- Create: directories only (no files yet)

- [ ] **Step 1: Create all directories**

```bash
mkdir -p ~/.claude/skills/imf-ra/references
mkdir -p ~/.claude/skills/imf-ra/tests
mkdir -p ~/.claude/skills/imf-ra/scripts
mkdir -p ~/.claude/skills/imf-ra-data/references
mkdir -p ~/.claude/skills/imf-ra-charts/references
mkdir -p ~/.claude/skills/imf-ra-catalog/references
mkdir -p ~/.claude/skills/imf-ra-catalog/databases
mkdir -p ~/.claude/skills/imf-ra-catalog/overlays
```

- [ ] **Step 2: Verify the tree**

Run:
```bash
find ~/.claude/skills/imf-ra ~/.claude/skills/imf-ra-data \
     ~/.claude/skills/imf-ra-charts ~/.claude/skills/imf-ra-catalog \
     -type d | wc -l
```
Expected: `12` — the four skill roots plus eight subdirectories (`imf-ra/{references,tests,scripts}`, `imf-ra-data/references`, `imf-ra-charts/references`, `imf-ra-catalog/{references,databases,overlays}`).

---

## Task 2: Write the umbrella SKILL.md

**Files:**
- Create: `~/.claude/skills/imf-ra/SKILL.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra/SKILL.md`:

```markdown
---
name: imf-ra
description: Use when working as an IMF Research Assistant or doing any task involving IMF data, IMF charts, or IMF databases. Orients you to the imf-ra-data, imf-ra-charts, and imf-ra-catalog skills and loads shared conventions for country codes, frequencies, dates, units, and SDK setup.
---

# IMF RA

Family entry point for IMF Research Assistant workflows. Loads shared conventions and routes to the right worker skill.

## Family map

- **`imf-ra-data`** — fetching data via the internal Python SDK. Use when the user wants to pull, download, or load series.
- **`imf-ra-charts`** — handing tidy data to the internal charting tool. Use when the user wants to plot, chart, or visualize.
- **`imf-ra-catalog`** — translating plain-English descriptions into a `(database, series, frequency, geo)` identifier. Use when the user is searching for the right indicator.

## Shared conventions

Before fetching, charting, or searching, see [references/conventions.md](references/conventions.md) for country codes, frequency conventions, date handling, and SDK environment setup.

## Workflow notes

- The umbrella does not orchestrate workflows. Workers chain by referencing each other directly.
- When `imf-ra-charts` needs data, it loads `imf-ra-data` in the same turn rather than sending the user away.
- When the catalog returns ambiguous matches, surface candidates with notes — do not commit to one without RA confirmation.
```

- [ ] **Step 2: Verify the file exists with frontmatter**

Run: `head -4 ~/.claude/skills/imf-ra/SKILL.md`
Expected: opens with `---`, has a `name: imf-ra` line, has a `description:` line, closes with `---`.

---

## Task 3: Write the umbrella conventions stub

**Files:**
- Create: `~/.claude/skills/imf-ra/references/conventions.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra/references/conventions.md`:

```markdown
# Shared conventions

Cross-cutting conventions referenced by every worker skill in the IMF RA family. Fill in real content as it becomes available; sections are placeholders so workers can already link here.

## Internal Python SDK

> _Placeholder._ When the SDK identity is confirmed, document:
> - Package name and install path.
> - Import convention (e.g., `import imf_sdk as imf`).
> - Environment variables required (auth tokens, default endpoint).
> - One-line "hello world" pull to verify the install.

## Country and country-group codes

> _Placeholder._ Document:
> - Which code system to prefer (ISO 3166 alpha-3 vs. IMF country codes).
> - How to translate between RA-friendly names ("G20", "advanced economies") and the SDK's group identifiers.

## Frequencies

> _Placeholder._ Document:
> - How the SDK encodes A/Q/M.
> - Conventions for quarter labels (`2010Q1` vs. `2010-Q1` vs. `2010-03-31`).
> - When to convert frequencies and which method to use.

## Dates

> _Placeholder._ Document:
> - Default date range conventions (e.g., "2010-present" → start=`2010`, end=`null`).
> - How to handle release-vintage dates vs. data-period dates.

## Units

> _Placeholder._ Document:
> - Common unit conventions in IMF databases (USD billions, percent of GDP, index 2010=100).
> - Where the unit metadata lives in the SDK return.
```

- [ ] **Step 2: Verify**

Run: `test -f ~/.claude/skills/imf-ra/references/conventions.md && grep -c '^## ' ~/.claude/skills/imf-ra/references/conventions.md`
Expected: prints `5` (five top-level placeholder sections).

---

## Task 4: Write `imf-ra-data` SKILL.md

**Files:**
- Create: `~/.claude/skills/imf-ra-data/SKILL.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-data/SKILL.md`:

```markdown
---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetching IMF data series via the internal Python SDK.

## Before you fetch

See the umbrella `imf-ra` for shared conventions: country codes, frequencies, dates, and SDK environment setup.

## How to fetch

See [references/sdk-usage.md](references/sdk-usage.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

See `imf-ra-catalog` first to translate the user's description into `(database, series, frequency, geo)`. Only then write the SDK call.

## Output convention

Return a tidy DataFrame (one observation per row, with `geo`, `time`, `value`, and any series-identifying columns). Downstream charting depends on this shape.
```

- [ ] **Step 2: Verify**

Run: `head -4 ~/.claude/skills/imf-ra-data/SKILL.md`
Expected: opens with `---`, has `name: imf-ra-data` and a `description:` line, closes with `---`.

---

## Task 5: Write the `sdk-usage.md` stub

**Files:**
- Create: `~/.claude/skills/imf-ra-data/references/sdk-usage.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-data/references/sdk-usage.md`:

```markdown
# Internal Python SDK — usage

> _Placeholder._ Fill in once the SDK identity and API are confirmed.

## Installation and import

> Document the install command (pip / internal index) and the canonical import alias.

## Single-series fetch

> Document the function signature, required arguments, and a worked example:
> "Fetch WEO real GDP growth for the United States, annual, 2010–present."

## Multi-country panel

> Document how to fetch the same series across a list of geographies (e.g., G20, advanced economies)
> and return a tidy panel.

## Ratio of two series

> Document the canonical pattern for "series A divided by series B" — fetch each, align on
> `(geo, time)`, compute the ratio, return the tidy result.

## Frequency conversion

> Document how to convert between A/Q/M, including which aggregation method (mean, sum, last)
> the SDK uses and how to override.

## Gotchas

> Document rate limits, retry conventions, and large-pull patterns (chunking, async).
```

- [ ] **Step 2: Verify**

Run: `test -f ~/.claude/skills/imf-ra-data/references/sdk-usage.md && grep -c '^## ' ~/.claude/skills/imf-ra-data/references/sdk-usage.md`
Expected: prints `6`.

---

## Task 6: Write `imf-ra-charts` SKILL.md

**Files:**
- Create: `~/.claude/skills/imf-ra-charts/SKILL.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-charts/SKILL.md`:

```markdown
---
name: imf-ra-charts
description: Use when the user wants to make a chart, plot, or visualization of IMF data using the internal charting tool. Covers chart-tool input formats, chart-type selection from data shape and intent, and source/footnote conventions. If data is not yet in scope, follow imf-ra-data to fetch it first.
---

# IMF RA — Charts

Handing tidy data to the internal charting tool.

## Before you chart

See the umbrella `imf-ra` for shared conventions.

## When data isn't in scope yet

Load `imf-ra-data` in the same turn and follow it to fetch — do not duplicate SDK call patterns here. See [`imf-ra-data/references/sdk-usage.md`](../imf-ra-data/references/sdk-usage.md). If the user only described what they want in plain English, also load `imf-ra-catalog` to resolve the identifier.

## How to chart

See [references/chart-tool-usage.md](references/chart-tool-usage.md) for the internal charting tool's invocation, input shape, chart-type selection, and captioning conventions.

## Chart-type heuristics

Once the chart tool's API is documented, this section will hold the data-shape → chart-type mapping (e.g., single time series → line, country comparison → bar, two series → scatter or paired-line). For now, defer to the user's intent.
```

- [ ] **Step 2: Verify**

Run: `head -4 ~/.claude/skills/imf-ra-charts/SKILL.md`
Expected: opens with `---`, has `name: imf-ra-charts` and a `description:` line, closes with `---`.

---

## Task 7: Write the `chart-tool-usage.md` stub

**Files:**
- Create: `~/.claude/skills/imf-ra-charts/references/chart-tool-usage.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-charts/references/chart-tool-usage.md`:

```markdown
# Internal charting tool — usage

> _Placeholder._ Fill in once the charting tool's identity and API are confirmed.

## Installation and import

> Document install and import conventions.

## Invocation

> Document the tool's primary entry point, required arguments, and return shape.

## Input data shape

> Specify the tidy DataFrame shape the tool expects (column names, index, types). This must align with the output of `imf-ra-data`.

## Chart-type selection

> Document the chart types the tool supports and the heuristic for picking one from `(data shape, user intent)`.

## Captions, sources, footnotes

> Document the IMF source-line conventions the tool needs (e.g., "Source: IMF, World Economic Outlook").

## Output

> Document where the tool writes its output (file path, in-memory object) and how to surface it back to the RA.
```

- [ ] **Step 2: Verify**

Run: `test -f ~/.claude/skills/imf-ra-charts/references/chart-tool-usage.md && grep -c '^## ' ~/.claude/skills/imf-ra-charts/references/chart-tool-usage.md`
Expected: prints `6`.

---

## Task 8: Write `imf-ra-catalog` SKILL.md

**Files:**
- Create: `~/.claude/skills/imf-ra-catalog/SKILL.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-catalog/SKILL.md`:

```markdown
---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English ("current account balance for advanced economies, quarterly") and needs to find the right database and indicator. Covers catalog browsing, keyword search across databases and curated overlays, and returns top-N candidates with notes when the description is ambiguous.
---

# IMF RA — Catalog

Translating plain-English descriptions into a stable identifier tuple `(database, series, frequency, geo)`.

## Before you search

See the umbrella `imf-ra` for shared conventions (country and country-group codes especially).

## Two layers

The catalog has two complementary layers, both under this skill folder:

- **`databases/<name>.md`** — one file per database (WEO, IFS, BOPS, GFS, DOTS, FSI, …). Schema in [databases/_template.md](databases/_template.md). v1 ships placeholder examples; real content fills in iteratively.
- **`overlays/<topic>.md`** — curated institutional knowledge that augments or corrects the database files. Schema in [overlays/_template.md](overlays/_template.md). Overlays take precedence on conflict.

See [references/catalog-conventions.md](references/catalog-conventions.md) for the schemas and how the layers interact.

## Search workflow

1. **First pass:** grep across `databases/` and `overlays/` for keywords from the user's description. Overlay match takes precedence.
2. **Fallback:** if grep returns nothing useful, surface the gap to the RA — say "this concept isn't in the catalog yet, do you have a hint?". Do **not** invent a series identifier.
3. **Output:** top-N candidates with confidence/notes, never a single committed pick. The RA selects.

## Handoff

Once the RA confirms an identifier, hand off to `imf-ra-data` for the fetch.
```

- [ ] **Step 2: Verify**

Run: `head -4 ~/.claude/skills/imf-ra-catalog/SKILL.md`
Expected: opens with `---`, has `name: imf-ra-catalog` and a `description:` line, closes with `---`.

---

## Task 9: Write `catalog-conventions.md`

**Files:**
- Create: `~/.claude/skills/imf-ra-catalog/references/catalog-conventions.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra-catalog/references/catalog-conventions.md`:

```markdown
# Catalog conventions

How the two-layer catalog is organized and how the layers interact.

## Layer 1: per-database files

One file per IMF database under `databases/`. Each file is human-readable Markdown but follows a consistent schema so grep over the family is reliable.

Schema lives in [`databases/_template.md`](../databases/_template.md). At minimum each file declares: dataflow ID, primary dimensions, frequency conventions, common indicators (with their codes), and notable gotchas.

In v2 these files may be auto-generated from SDMX metadata. The schema is designed to accept either hand-curated or machine-generated content without restructuring.

## Layer 2: overlays

Curated institutional knowledge that augments or corrects the per-database files. Examples:

- "For real GDP growth, prefer WEO `NGDP_RPCH` over IFS `NGDP_R_K_IX` because WEO is the consensus forecast."
- "Quarterly current account in BOPS uses `BCA_BP6_USD`, not the older BPM5 codes."
- "When users say 'advanced economies', they almost always mean the WEO group `AE`, not OECD."

Schema lives in [`overlays/_template.md`](../overlays/_template.md).

## Layer interaction

When grep matches both a database file and an overlay, **the overlay takes precedence**. Database files describe what exists; overlays describe what to use and why.

## Search expectations

The catalog returns top-N candidates with notes. Never a single committed pick when the description is ambiguous. The RA disambiguates.

## Adding new entries

- New database: copy `databases/_template.md` to `databases/<name>.md` and fill in.
- New overlay: copy `overlays/_template.md` to `overlays/<topic>.md` and fill in.
- Keep entries focused. Multiple small files beat one large file.
```

- [ ] **Step 2: Verify**

Run: `test -f ~/.claude/skills/imf-ra-catalog/references/catalog-conventions.md && grep -c '^## ' ~/.claude/skills/imf-ra-catalog/references/catalog-conventions.md`
Expected: prints `5`.

---

## Task 10: Write the catalog templates

**Files:**
- Create: `~/.claude/skills/imf-ra-catalog/databases/_template.md`
- Create: `~/.claude/skills/imf-ra-catalog/overlays/_template.md`

- [ ] **Step 1: Write `databases/_template.md`**

Content of `~/.claude/skills/imf-ra-catalog/databases/_template.md`:

```markdown
# <Database name> (e.g., World Economic Outlook — WEO)

> Template for a per-database catalog file. Copy to `<dbname>.md` and fill in.

## Dataflow identity

- **Dataflow ID:** `<e.g., WEO>`
- **Source:** `<URL or "internal Python SDK">`
- **Updated:** `<release cadence — e.g., biannual, October and April>`

## Primary dimensions

List the dataflow's dimensions and brief descriptions.

- `<dim 1>` — `<description>`
- `<dim 2>` — `<description>`

## Frequencies available

`<A | Q | M | …>` with notes on which series are available at which frequency.

## Common indicators

| Indicator | Code | Frequency | Unit | Notes |
|---|---|---|---|---|
| `<e.g., Real GDP growth>` | `NGDP_RPCH` | A | percent | |
| `<e.g., CPI inflation, period average>` | `PCPIPCH` | A | percent | |

## Country / geo conventions

How this database identifies geographies. Group codes that exist (e.g., `AE`, `EM`, `LIC`).

## Gotchas

- `<e.g., WEO is a forecast database — most-recent observations are projections, not realized data.>`
- `<e.g., Pre-2000 vintages used different country code conventions.>`
```

- [ ] **Step 2: Write `overlays/_template.md`**

Content of `~/.claude/skills/imf-ra-catalog/overlays/_template.md`:

```markdown
# <Topic> (e.g., Real GDP growth — which series to use)

> Template for an overlay catalog file. Copy to `<topic>.md` and fill in.

## What the user typically asks

`<plain-English description the overlay applies to — e.g., "real GDP growth, country-level, annual">`

## Recommended series

- **Primary:** `<database / series ID / frequency / geo>` — `<one-line reason>`
- **Alternative:** `<database / series ID>` — `<when to prefer this>`

## Why not other candidates

- `<series X>` — `<reason to avoid>`
- `<series Y>` — `<reason to avoid>`

## Notes

`<any institutional context — definition differences, vintage issues, aggregation conventions>`
```

- [ ] **Step 3: Verify both files exist**

Run: `ls ~/.claude/skills/imf-ra-catalog/databases/_template.md ~/.claude/skills/imf-ra-catalog/overlays/_template.md`
Expected: both paths print without "No such file" error.

---

## Task 11: Write the smoke-test prompts

**Files:**
- Create: `~/.claude/skills/imf-ra/tests/prompts.md`

- [ ] **Step 1: Write the file**

Content of `~/.claude/skills/imf-ra/tests/prompts.md`:

```markdown
# Activation smoke-test prompts

Representative prompts an IMF RA might say. For each, the table below records the **expected primary skill** to activate. Run these periodically by invoking each prompt fresh in a Claude Code session and confirming the right skill activates first. If activation drifts, tighten the `description` field in the relevant `SKILL.md`.

| # | Prompt | Expected primary skill | Notes |
|---|---|---|---|
| 1 | Pull WEO real GDP growth for G20 countries, 2010-present. | `imf-ra-data` | Direct fetch intent. |
| 2 | What's the BOPS series for current account balance? | `imf-ra-catalog` | Pure discovery. |
| 3 | Chart the global current account balances by country for the last decade. | `imf-ra-charts` | Should chain: catalog → data → charts. |
| 4 | I'm starting a project on emerging market debt — orient me to what's available. | `imf-ra` | Umbrella; broad orientation. |
| 5 | Find me a quarterly inflation series for emerging markets. | `imf-ra-catalog` | Discovery with frequency constraint. |
| 6 | Download IFS exchange rates monthly for ASEAN, 2015-present. | `imf-ra-data` | Direct fetch with country group. |
| 7 | Make a panel chart of debt-to-GDP for the G7. | `imf-ra-charts` | Chained, panel layout. |
| 8 | What's the difference between WEO inflation and CPI in IFS? | `imf-ra-catalog` | Overlay knowledge — should surface both with notes. |

## How to use this file

1. Open a fresh Claude Code session.
2. For each prompt, paste it and observe which skill activates first.
3. If the activated skill differs from the "Expected primary skill" column, tighten that skill's `description` field (or the activated skill's, if it's over-claiming).
4. Record findings inline as a `## Last run` section below.
```

- [ ] **Step 2: Verify**

Run: `test -f ~/.claude/skills/imf-ra/tests/prompts.md && grep -c '^| [0-9]' ~/.claude/skills/imf-ra/tests/prompts.md`
Expected: prints `8`.

---

## Task 12: Write the reference reachability checker (real TDD)

**Files:**
- Create: `~/.claude/skills/imf-ra/scripts/check_references.sh`
- Test: shell-based — make a temp broken reference and confirm the script flags it.

- [ ] **Step 1: Set up a failing-state test (inject a broken reference)**

Run:

```bash
cp ~/.claude/skills/imf-ra/SKILL.md ~/.claude/skills/imf-ra/SKILL.md.bak
printf '\n[broken](references/does_not_exist.md)\n' >> ~/.claude/skills/imf-ra/SKILL.md
```

This creates the broken-state we expect the checker to detect.

- [ ] **Step 2: Run the not-yet-existing script (expect "command not found" / file not found)**

Run: `bash ~/.claude/skills/imf-ra/scripts/check_references.sh; echo "exit=$?"`
Expected: error like `No such file or directory`, then `exit=` non-zero (typically `127`). Confirms the test is real.

- [ ] **Step 3: Write the script**

Content of `~/.claude/skills/imf-ra/scripts/check_references.sh`:

```bash
#!/usr/bin/env bash
# Verify that every markdown reference in each family SKILL.md points to an existing file.
# Exits non-zero if any reference is broken.

set -euo pipefail

SKILLS_DIR="${SKILLS_DIR:-$HOME/.claude/skills}"
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
    while IFS= read -r ref; do
        [[ -z "$ref" ]] && continue
        [[ "$ref" =~ ^https?:// ]] && continue

        ref_path="$skill_dir/$ref"
        if [[ ! -e "$ref_path" ]]; then
            echo "BROKEN REF in $skill_md: $ref"
            errors=$((errors + 1))
        fi
    done < <(grep -oE '\([^)]+\.md[^)]*\)' "$skill_md" | sed -E 's/^\(|\)$//g')
done

if [[ $errors -eq 0 ]]; then
    echo "OK: all skills found, all references resolve."
    exit 0
else
    echo "FAILED: $errors broken reference(s)."
    exit 1
fi
```

Then make it executable:

```bash
chmod +x ~/.claude/skills/imf-ra/scripts/check_references.sh
```

- [ ] **Step 4: Run the script — expect FAILURE because of the injected broken ref**

Run: `bash ~/.claude/skills/imf-ra/scripts/check_references.sh; echo "exit=$?"`
Expected output contains `BROKEN REF in /Users/huang/.claude/skills/imf-ra/SKILL.md: references/does_not_exist.md` and ends with `exit=1`.

- [ ] **Step 5: Restore the umbrella SKILL.md, then re-run**

Run:

```bash
mv ~/.claude/skills/imf-ra/SKILL.md.bak ~/.claude/skills/imf-ra/SKILL.md
bash ~/.claude/skills/imf-ra/scripts/check_references.sh; echo "exit=$?"
```

Expected output: `OK: all skills found, all references resolve.` and `exit=0`.

---

## Task 13: Final end-to-end verification

**Files:** none modified — this task only runs checks.

- [ ] **Step 1: Confirm the directory tree**

Run: `find ~/.claude/skills -type d \( -name 'imf-ra' -o -name 'imf-ra-*' \) | wc -l`
Expected: `4` (the four skill roots).

- [ ] **Step 2: Confirm every SKILL.md has frontmatter with `name` and `description`**

Run:

```bash
for s in imf-ra imf-ra-data imf-ra-charts imf-ra-catalog; do
  f=~/.claude/skills/$s/SKILL.md
  if grep -q '^name: ' "$f" && grep -q '^description: ' "$f"; then
    echo "$s: OK"
  else
    echo "$s: MISSING frontmatter"
  fi
done
```

Expected: four lines, each ending in `: OK`.

- [ ] **Step 3: Run the reference reachability checker**

Run: `bash ~/.claude/skills/imf-ra/scripts/check_references.sh; echo "exit=$?"`
Expected: `OK: all skills found, all references resolve.` and `exit=0`.

- [ ] **Step 4: Confirm the catalog templates exist**

Run: `ls ~/.claude/skills/imf-ra-catalog/databases/_template.md ~/.claude/skills/imf-ra-catalog/overlays/_template.md`
Expected: both paths print without error.

- [ ] **Step 5: Confirm the smoke-test prompts file has all eight rows**

Run: `grep -c '^| [0-9]' ~/.claude/skills/imf-ra/tests/prompts.md`
Expected: `8`.

- [ ] **Step 6 (optional): Activation smoke test**

Open a fresh Claude Code session and try one prompt from `~/.claude/skills/imf-ra/tests/prompts.md`. Confirm the expected skill activates. (This is not automated — run it once after scaffolding to catch obvious description issues.)

---

## Optional: commit if `~/.claude/skills` is a git repo

If `~/.claude/skills/` is under version control:

```bash
cd ~/.claude/skills
git add imf-ra imf-ra-data imf-ra-charts imf-ra-catalog
git commit -m "feat: scaffold IMF RA skill family (umbrella + 3 workers, no real content)"
```

If not, skip — the spec explicitly chose "no plugin in v1" and didn't require versioning the skills folder.

---

## What's next (not in this plan)

After scaffolding lands and the smoke test passes, the iterative content work begins:

1. Fill in `imf-ra/references/conventions.md` with the real internal SDK identity and conventions.
2. Fill in `imf-ra-data/references/sdk-usage.md` with the SDK's actual call patterns.
3. Fill in `imf-ra-charts/references/chart-tool-usage.md` with the internal charting tool's invocation.
4. Author the first real database files (`databases/weo.md`, `databases/ifs.md`).
5. Re-run the smoke-test prompts to confirm activation still lands correctly.

These each warrant their own short plan when the source content lands.

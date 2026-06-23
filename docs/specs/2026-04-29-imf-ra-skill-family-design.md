# IMF RA Skill Family — Design

**Date:** 2026-04-29
**Status:** Historical design, superseded by current project-local implementation
**Author:** huangchengyu16@gmail.com

## 1. Purpose

A family of Claude Code skills that helps IMF Research Assistants do day-to-day work. The skills are knowledge-and-glue layers that teach Claude how to use existing internal tools — they do not reimplement data access or charting.

**Current implementation note:** this document records the original April 2026 scaffold design. The live repository now keeps skills project-local under `.claude/skills/`, uses CSV catalogs plus helper scripts instead of placeholder Markdown templates, and consolidates WEO country/group truth under `.claude/skills/imf-ra/country_group/`.

## 2. Scope

### In scope (v1)

Three pillars:

1. **Data fetch** — pull series from the public IMF Data API via an existing internal Python SDK.
2. **Charting** — hand off tidy data to an existing internal charting tool.
3. **Variable / database discovery** — translate plain-English descriptions ("quarterly current account balance for advanced economies") into the right database, dataflow, and series identifier.

### Out of scope (v2 / later)

- **Pillar 4 — pipeline automation** (one-off scripts, reusable modules, scheduled jobs, notebook templates). Deferred entirely.
- **Additional internal data sources** — Haver, Datastream, EDSS. Bloomberg and WDI/WTO catalog routing now exist as catalog reference paths; full source-specific retrieval support remains bounded by the iData workflow.
- **Real chart-style implementation** — handled by the existing internal charting tool. The skill only orchestrates handoff.
- **Real catalog content placeholders** — superseded. The current implementation ships dataset and indicator CSVs plus catalog helper modules.

### Non-goals

- Reimplementing the IMF Data API or building a custom HTTP client.
- Encoding the IMF chart style guide (the internal tool owns that).
- Building an MCP server, a CLI, or any compiled component.
- Plugin packaging — deferred until distribution to colleagues is needed.

## 3. Architecture

### Shape: umbrella + workers, sibling skills

Four sibling skill folders under project-local `.claude/skills/`:

```
.claude/skills/
├── imf-ra/                          # Umbrella — broad activation, family map, shared conventions
│   ├── SKILL.md
│   └── country_group/
│       ├── country_group.csv
│       ├── country_groups_instruction.md
│       └── country_groups_helper.py
├── imf-ra-data/                     # Worker — fetching via internal Python SDK
│   ├── SKILL.md
│   ├── references/
│   │   └── imf_datatools_agent_api_reference.md
│   └── scripts/
│       └── fetch_idata.py
├── imf-ra-charts/                   # Worker — handoff to internal charting tool
│   ├── SKILL.md
│   └── references/
│       └── chart-tool-usage.md
└── imf-ra-catalog/                  # Worker — variable / database discovery
    ├── SKILL.md
    ├── databases/
    │   ├── database_overview.md
    │   ├── non_vintage_datasets.csv
    │   └── vintage_datasets.csv
    ├── indicators/
    │   ├── 1. non_vintage_variable_list.csv
    │   ├── 2. bbg_variable_list.csv
    │   ├── 3. wdi_variable_list.csv
    │   └── 4. wto_variable_List.csv
    └── scripts/
        ├── catalog_search.py
        ├── catalog_data.py
        ├── catalog_routing.py
        └── catalog_lookup.py
```

### Why this shape

- **Sibling skills, not nested directories.** Claude Code reliably discovers `.claude/skills/<name>/SKILL.md` in this project; nested `SKILL.md` discovery is unverified and would risk silent non-activation. The naming prefix (`imf-ra-*`) provides the visual grouping that nesting would.
- **Umbrella + workers, not single skill.** The pillars have genuinely different activation triggers — "I need to find a series" is a different intent from "chart this." Separate descriptions activate cleanly. The umbrella holds shared conventions and a family map; workers stay narrow and sharp.
- **No plugin yet.** Plugin packaging is a v2 concern when sharing with colleagues. The four skill folders move into `plugin/skills/` unchanged when promoted.

### Skill responsibilities

| Skill | Role | Activation |
|---|---|---|
| `imf-ra` | Family entry point, family map, shared conventions (country codes, frequencies, dates, units, SDK setup). Holds nothing pillar-specific. | Broad — any IMF-RA-shaped intent. |
| `imf-ra-data` | How to call the internal Python SDK. Common recipes: single series, multi-country panel, ratio of two series, frequency conversion. | "fetch / pull / download / load" data intents. |
| `imf-ra-charts` | How to invoke the internal charting tool. Input shape, chart-type selection from data shape and intent, captioning conventions. | "chart / plot / visualize" intents. |
| `imf-ra-catalog` | Translate plain-English descriptions into a stable identifier tuple `(database, dimension_name, code)`. CSV catalogs and helper modules own dataset, source, dimension, and indicator discovery. Returns candidates with notes when ambiguous. | "find / what's the series / discover / search" intents. |

## 4. Catalog Design

The catalog (`imf-ra-catalog`) is the most distinctive piece and the only worker with internal structure beyond `references/`.

### Two-layer design

- **`databases/*.csv` / `databases/database_overview.md`** — source-of-truth dataset catalogs, LIVE/vintage distinction, and high-level source family guidance.
- **`indicators/*.csv`** — source-of-truth indicator/code catalogs for general non-vintage, Bloomberg, WDI, and WTO lookups.
- **`scripts/catalog_*.py`** — operational routing, fuzzy lookup, exact code validation, database classification, dimension discovery, comparison, and JSON handoff payloads.

### Search workflow

1. **First pass:** route source-family wording with `scripts/catalog_search.py explain-source` when the request names IFS, WDI, Bloomberg, WTO, WEO, or a vintage.
2. **Lookup:** use `scripts/catalog_search.py resolve`, `search`, `code`, `dimensions`, `classify-database`, or `compare-codes` before writing temporary code.
3. **Output:** return a handoff only when `resolve --json` is unambiguous; otherwise return candidates with notes and ask the RA to choose.

### Refresh

v1 catalog content is human-curated. SDMX metadata caching (auto-ingestion of dataflows / codelists into a local snapshot) is **deferred** but the `databases/` directory shape is designed to accept auto-generated files in v2 without restructuring.

## 5. Data Flow

### Walkthrough A — fetch by description

```
User describes data they want (plain English)
       │
       ▼
imf-ra activates (loads conventions)
       │
       ▼
imf-ra-catalog ──► resolves to (database, dimension_name, code)
       │
       ▼
imf-ra-data    ──► writes SDK call, fetches DataFrame
       │
       ▼
RA receives data
```

### Walkthrough B — fetch and chart in one turn

```
User says "chart [description]"
       │
       ▼
imf-ra activates
       │
       ▼
imf-ra-catalog ──► identifier tuple
       │
       ▼
imf-ra-data    ──► fetches (loaded because charts skill references it)
       │
       ▼
imf-ra-charts  ──► picks chart type, calls internal charting tool
```

### Walkthrough C — discovery only

Catalog returns a confirmed handoff only when safe; otherwise it returns top candidates with notes and flow stops until RA picks one.

### Cross-skill seam principle

Workers own *knowledge layers*, not gated capabilities. When `imf-ra-charts` needs data, Claude loads `imf-ra-data`'s instructions in the same turn and follows them — chart skill never duplicates SDK call patterns; it references `imf-ra-data/references/imf_datatools_agent_api_reference.md` and the pre-built `fetch_idata.py` workflow. DRY without artificial gating. The umbrella does **not** orchestrate workflows — workflows emerge from worker references.

## 6. Extensibility

| Future need | How it slots in |
|---|---|
| Pipeline automation (pillar 4) | Add a fifth sibling: `imf-ra-pipeline`. One line in `imf-ra/SKILL.md`'s map. No other skill changes. |
| Internal sources, same SDK API | Content-only: more catalog CSV rows, source-specific indicator files, and recipes in `imf-ra-data/references/imf_datatools_agent_api_reference.md`. **No new skills.** |
| Internal sources, different auth/SDK calls | Add `imf-ra-shared-internal` for auth/env/gating, referenced by `imf-ra-data` and `imf-ra-catalog`. Public users skip it; internal users install it. This is the public/internal boundary. |
| Distribution to colleagues | Promote to plugin: move the four (or five) skill folders into `plugin/skills/`. Discovery shape unchanged. |
| Auto-ingested SDMX metadata cache | Drop machine-generated CSVs into `imf-ra-catalog/databases/` or `imf-ra-catalog/indicators/` and wire them through catalog helper loaders. No restructuring. |

## 7. Verification

For a content-light skill family, verification is light:

1. **Behavioral test pack.** `tests/auto_test_cases.yaml` is the machine-readable source of truth, mirrored by `tests/auto_test_instructions.md` for reviewer-facing runs.
2. **Command contracts.** Helper commands in the YAML verify catalog routing, strict resolve, dimension discovery, vintage classification, code comparison, and WEO group expansion.

## 8. Open Items

These are deliberate gaps, not oversights — they need real-world content to fill in:

- **Internal Python SDK identity.** Name, install path, public functions, return shapes. Current guidance lives in `imf-ra-data/references/imf_datatools_agent_api_reference.md` and `imf-ra-data/scripts/fetch_idata.py`.
- **Internal charting tool identity.** Name, invocation, input format. Content fills `imf-ra-charts/references/chart-tool-usage.md`.
- **First two database files.** Likely WEO and IFS based on RA day-to-day; final pick can wait until SDK content lands.
- **Whether additional catalog helpers are needed.** Current helpers cover routing, lookup, dimensions, classification, comparison, and handoff; repeated temporary-code patterns should be promoted into `catalog_search.py`.

## 9. Decisions Recorded

Each is reversible but warrants explicit documentation:

| Decision | Rationale |
|---|---|
| v1 uses iData via the internal Python SDK | Realism boundary; private IMF LIVE/vintage datasets require the SDK private-data flag. |
| Python-first | Matches RA stack and the existing internal SDK. |
| Hybrid catalog (cached metadata + curated overlays) | User chose option C in brainstorm; structure designed to accept either layer growing first. |
| Charting style is delegated to internal tool | An internal tool already exists; no need to encode the IMF style guide in the skill. |
| Pillar 4 (pipeline automation) deferred | Keep v1 scope tight. |
| Sibling skills, not nested SKILL.md | Verified discovery pattern; nested is unverified. |
| Umbrella + workers, not single skill | Different pillars have different activation triggers. |
| No plugin in v1 | "Start simple"; promotion path preserved. |

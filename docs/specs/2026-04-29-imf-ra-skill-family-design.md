# IMF RA Skill Family — Design

**Date:** 2026-04-29
**Status:** Draft for review
**Author:** huangchengyu16@gmail.com

## 1. Purpose

A family of Claude Code skills that helps IMF Research Assistants do day-to-day work. The skills are knowledge-and-glue layers that teach Claude how to use existing internal tools — they do not reimplement data access or charting.

## 2. Scope

### In scope (v1)

Three pillars:

1. **Data fetch** — pull series from the public IMF Data API via an existing internal Python SDK.
2. **Charting** — hand off tidy data to an existing internal charting tool.
3. **Variable / database discovery** — translate plain-English descriptions ("quarterly current account balance for advanced economies") into the right database, dataflow, and series identifier.

### Out of scope (v2 / later)

- **Pillar 4 — pipeline automation** (one-off scripts, reusable modules, scheduled jobs, notebook templates). Deferred entirely.
- **Internal data sources** — Haver, Bloomberg, Datastream, EDSS. v1 covers public IMF Data API only. Haver is the highest-priority v2 internal adapter; Bloomberg/Datastream second.
- **Real chart-style implementation** — handled by the existing internal charting tool. The skill only orchestrates handoff.
- **Real catalog content** — v1 ships the catalog *structure*; databases and overlays are placeholders to be filled in iteratively.

### Non-goals

- Reimplementing the IMF Data API or building a custom HTTP client.
- Encoding the IMF chart style guide (the internal tool owns that).
- Building an MCP server, a CLI, or any compiled component.
- Plugin packaging — deferred until distribution to colleagues is needed.

## 3. Architecture

### Shape: umbrella + workers, sibling skills

Four sibling skill folders under `~/.claude/skills/`:

```
~/.claude/skills/
├── imf-ra/                          # Umbrella — broad activation, family map, shared conventions
│   ├── SKILL.md
│   └── references/
│       └── conventions.md
├── imf-ra-data/                     # Worker — fetching via internal Python SDK
│   ├── SKILL.md
│   └── references/
│       └── sdk-usage.md
├── imf-ra-charts/                   # Worker — handoff to internal charting tool
│   ├── SKILL.md
│   └── references/
│       └── chart-tool-usage.md
└── imf-ra-catalog/                  # Worker — variable / database discovery
    ├── SKILL.md
    ├── references/
    │   └── catalog-conventions.md
    ├── databases/                   # One .md per database (placeholders for v1)
    │   └── _template.md
    ├── overlays/                    # Curated institutional knowledge
    │   └── _template.md
    └── scripts/
        └── search_catalog.py        # Optional v1 helper, deferable
```

### Why this shape

- **Sibling skills, not nested directories.** Claude Code reliably discovers `~/.claude/skills/<name>/SKILL.md`; nested `SKILL.md` discovery is unverified and would risk silent non-activation. The naming prefix (`imf-ra-*`) provides the visual grouping that nesting would.
- **Umbrella + workers, not single skill.** The pillars have genuinely different activation triggers — "I need to find a series" is a different intent from "chart this." Separate descriptions activate cleanly. The umbrella holds shared conventions and a family map; workers stay narrow and sharp.
- **No plugin yet.** Plugin packaging is a v2 concern when sharing with colleagues. The four skill folders move into `plugin/skills/` unchanged when promoted.

### Skill responsibilities

| Skill | Role | Activation |
|---|---|---|
| `imf-ra` | Family entry point, family map, shared conventions (country codes, frequencies, dates, units, SDK setup). Holds nothing pillar-specific. | Broad — any IMF-RA-shaped intent. |
| `imf-ra-data` | How to call the internal Python SDK. Common recipes: single series, multi-country panel, ratio of two series, frequency conversion. | "fetch / pull / download / load" data intents. |
| `imf-ra-charts` | How to invoke the internal charting tool. Input shape, chart-type selection from data shape and intent, captioning conventions. | "chart / plot / visualize" intents. |
| `imf-ra-catalog` | Translate plain-English descriptions into a stable identifier tuple `(database, series, frequency, geo)`. Two layers: per-database `.md` files and curated overlays. Returns candidates with notes when ambiguous. | "find / what's the series / discover / search" intents. |

## 4. Catalog Design

The catalog (`imf-ra-catalog`) is the most distinctive piece and the only worker with internal structure beyond `references/`.

### Two-layer design

- **`databases/<dbname>.md`** — one file per database (WEO, IFS, BOPS, GFS, DOTS, FSI, …). Schema: dataflow ID, dimensions, codelists, frequency conventions, common indicators with their codes. v1 ships a `_template.md` plus 1–2 placeholder examples; real content fills in iteratively.
- **`overlays/<topic>.md`** — institutional knowledge that augments or corrects the database files: "use IFS quarterly, not WEO annual, for X because Y", canonical aggregations, gotchas.

### Search workflow

1. **First pass:** grep across `databases/` and `overlays/`. Overlay match takes precedence.
2. **Fallback:** `scripts/search_catalog.py` (optional, deferable). v1 can ship without it; introduce when grep proves insufficient.
3. **Output:** top-N candidates with confidence/notes, not a single committed pick. The RA selects.

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
imf-ra-catalog ──► resolves to (database, series, frequency, geo)
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

Catalog returns top-N candidates with notes; flow stops until RA picks one.

### Cross-skill seam principle

Workers own *knowledge layers*, not gated capabilities. When `imf-ra-charts` needs data, Claude loads `imf-ra-data`'s instructions in the same turn and follows them — chart skill never duplicates SDK call patterns; it references `imf-ra-data/references/sdk-usage.md`. DRY without artificial gating. The umbrella does **not** orchestrate workflows — workflows emerge from worker references.

## 6. Extensibility

| Future need | How it slots in |
|---|---|
| Pipeline automation (pillar 4) | Add a fifth sibling: `imf-ra-pipeline`. One line in `imf-ra/SKILL.md`'s map. No other skill changes. |
| Internal sources, same SDK API | Content-only: more `catalog/databases/*.md` entries and recipes in `imf-ra-data/references/sdk-usage.md`. **No new skills.** |
| Internal sources, different auth/SDK calls | Add `imf-ra-shared-internal` for auth/env/gating, referenced by `imf-ra-data` and `imf-ra-catalog`. Public users skip it; internal users install it. This is the public/internal boundary. |
| Distribution to colleagues | Promote to plugin: move the four (or five) skill folders into `plugin/skills/`. Discovery shape unchanged. |
| Auto-ingested SDMX metadata cache | Drop machine-generated files into `imf-ra-catalog/databases/`. Existing curated overlays in `overlays/` keep precedence. No restructuring. |

## 7. Verification

For a content-light skill family, verification is light:

1. **Activation smoke test.** A `~/.claude/skills/imf-ra/tests/prompts.md` file (hosted under the umbrella skill, since sibling skills share no parent folder) lists 5–10 representative prompts ("pull WEO GDP for G20", "what's the BOPS series for current account", "chart this") with the expected primary skill for each. Run them periodically; if activation drifts, tighten `description` fields.
2. **Reference reachability.** A trivial check (hand script or CI) walks each `SKILL.md`, finds its referenced files, confirms they exist. Catches typos and dead links.
3. **No content tests in v1.** External dependencies (SDK, charting tool) live outside the skill. When real content arrives, each worker can grow a small "golden examples" file showing canonical calls.

## 8. Open Items

These are deliberate gaps, not oversights — they need real-world content to fill in:

- **Internal Python SDK identity.** Name, install path, public functions, return shapes. Content fills `imf-ra-data/references/sdk-usage.md`.
- **Internal charting tool identity.** Name, invocation, input format. Content fills `imf-ra-charts/references/chart-tool-usage.md`.
- **First two database files.** Likely WEO and IFS based on RA day-to-day; final pick can wait until SDK content lands.
- **Whether `scripts/search_catalog.py` is needed in v1.** Defer until grep is shown insufficient.

## 9. Decisions Recorded

Each is reversible but warrants explicit documentation:

| Decision | Rationale |
|---|---|
| v1 covers public IMF Data API only | Realism boundary; no internal credentials to manage in v1. |
| Python-first | Matches RA stack and the existing internal SDK. |
| Hybrid catalog (cached metadata + curated overlays) | User chose option C in brainstorm; structure designed to accept either layer growing first. |
| Charting style is delegated to internal tool | An internal tool already exists; no need to encode the IMF style guide in the skill. |
| Pillar 4 (pipeline automation) deferred | Keep v1 scope tight. |
| Sibling skills, not nested SKILL.md | Verified discovery pattern; nested is unverified. |
| Umbrella + workers, not single skill | Different pillars have different activation triggers. |
| No plugin in v1 | "Start simple"; promotion path preserved. |

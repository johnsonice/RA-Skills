---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English ("current account balance for advanced economies, quarterly") and needs to find the right database and indicator. Covers catalog browsing, keyword search across databases and curated overlays, and returns top-N candidates with notes when the description is ambiguous.
---

# IMF RA — Catalog

Translating plain-English descriptions into a stable identifier tuple `(database, series, frequency, geo)`.

## Before you search

See the umbrella `imf-ra` for shared conventions (country and country-group codes especially).

## Two layers

The catalog has three complementary layers, all under this skill folder:

- **`databases/<name>.md`** — one file per database (WEO, IFS, BOPS, GFS, DOTS, FSI, …). Schema in [databases/_template.md](databases/_template.md). v1 ships placeholder examples; real content fills in iteratively.
- **`overlays/<topic>.md`** — curated institutional knowledge that augments or corrects the database files. Schema in [overlays/_template.md](overlays/_template.md). Overlays take precedence on conflict.
- **`references/*.csv`** — machine-readable internal catalog files. `internal_full_datasets.csv` lists datasets/dataflows; `Full_indicators_List.csv` lists `(database_name, indicator_code, indicator_name)` rows.

See [references/catalog-conventions.md](references/catalog-conventions.md) for the schemas and how the layers interact.

## CSV reference files

Use the CSV references whenever the user wants to find an indicator code, dataset, or likely database:

- `references/internal_full_datasets.csv` columns: `name`, `Agency ID`, `Resource ID`, `Latest Version`, `Unique ID`.
- `references/Full_indicators_List.csv` columns: `database_name`, `indicator_code`, `indicator_name`.
- Use `scripts/catalog_search.py` for reliable CSV search rather than ad hoc grep when possible.

Quick commands:

```bash
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py latest-weo
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "current account balance" --all-databases
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO
```

## Priority policy

- For WEO-like macroeconomic concepts, use the most recent standard `WEO Live` dataset as the first priority unless the user asks for a different vintage/database.
- Determine the most recent WEO Live from `internal_full_datasets.csv`; do not hard-code it in an answer if the CSV can be queried.
- In the current references, the latest standard WEO Live is discoverable with `catalog_search.py latest-weo`.
- Prefer WEO Live for common annual macro concepts such as GDP, real GDP growth, inflation, current account, fiscal balance, unemployment, population, exchange rates, PPP, imports, and exports.
- Search all databases only when WEO Live lacks a plausible match, the user explicitly asks for a non-WEO database, or the concept is clearly outside WEO coverage.

## Clarifying with the RA

When indicator search is ambiguous, discuss the uncertainty with the user before committing to a final identifier. Ask the smallest useful question, usually choosing among 2-5 candidates.

Clarify when:

- Multiple indicators share the same concept but differ by unit, transformation, or valuation, such as current prices vs constant prices, national currency vs U.S. dollars, percent of GDP, per capita, period average vs end of period, level vs percent change.
- Multiple databases match and WEO Live is not obviously the right source.
- The requested frequency is incompatible or unclear. WEO Live is generally annual; use other databases for quarterly/monthly needs unless metadata says otherwise.
- The user asks for a vintage-sensitive concept but does not specify whether they want the latest vintage or a historical vintage.
- The country coverage implies a WEO group, region, or panel but the group/country set is unclear.

When presenting candidates, include `database_name`, `indicator_code`, `indicator_name`, and a short note explaining the distinction. Do not invent codes.

## Search workflow

1. **Understand the request:** identify concept, desired unit/transformation, frequency, vintage, database preference, and country/group coverage when available.
2. **First pass for indicators:** search the latest standard WEO Live first with `catalog_search.py search "<query>"`.
3. **Second pass when needed:** search all databases with `--all-databases`, and grep `databases/` plus `overlays/` for curated notes. Overlay match takes precedence when it conflicts with raw catalog matches.
4. **Discuss uncertainty:** if multiple plausible indicators remain, ask the RA to choose or clarify. Do not collapse distinct candidates into one.
5. **Output:** top-N candidates with confidence/notes, never a single committed pick unless the match is exact and unambiguous.
6. **Fallback:** if the CSV and Markdown search return nothing useful, surface the gap to the RA and ask for a hint. Do **not** invent a series identifier.

## Handoff

Once the RA confirms an identifier, hand off to `imf-ra-data` for the fetch.

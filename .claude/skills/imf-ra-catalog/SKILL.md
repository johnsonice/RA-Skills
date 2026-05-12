---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English ("current account balance for advanced economies, quarterly") and needs the right non-vintage dataset, dimension, and code. Returns top candidates with clear notes when requests are ambiguous.
---

# IMF RA - Catalog

Translate plain-English requests into a stable identifier tuple: `(database, dimension_name, code, frequency, geo)`.

## Before Search

See the umbrella `imf-ra` for shared conventions (country and country-group codes especially).

For WEO country groups, regions, or informal country names, normalize the geography through the umbrella WEO country-group reference before searching variables or handing off to `imf-ra-data`.

## Catalog Structure

The catalog has three complementary layers:

- **`databases/templates/non_vintaged_datasets.csv`** - default iData dataset/dataflow catalog for non-vintage lookup. Schema notes: [databases/templates/idata_template.md](databases/templates/idata_template.md).
- **`databases/templates/vintaged_datasets.csv`** - vintage-only dataset/dataflow catalog. Use only when the user asks for a vintage/historical version.
- **`indicators/non_vintage_Full_Variable_List.csv`** - default iData variable catalog for non-vintage datasets. Schema notes: [indicators/templates/idata_template.md](indicators/templates/idata_template.md).
- **`overlays/<topic>.md`** - optional curated guidance that augments or overrides CSV-only lookup.

See [references/catalog-conventions.md](references/catalog-conventions.md) for the schemas and how the layers interact.

## Reference Files

Use these files as the source of truth:

- `databases/templates/non_vintaged_datasets.csv`: `database`, `name`, `Agency ID`, `Resource ID`, `Latest Version`, `Unique ID`
- `databases/templates/vintaged_datasets.csv`: same columns as the non-vintage dataset file, but reserved for explicit vintage requests
- `indicators/non_vintage_Full_Variable_List.csv`: `database_name`, `dimension_name`, `Code`, `Name`

## When To Run Code

For easy and straightforward requests, inspect the available CSV, Markdown, and optional overlay files and answer directly from those sources. Do not write or run code when inspection is enough.

Write or run code only for complex tasks: broad keyword search across many rows, repeated filtering, ranking candidates, joining dataset and variable references, explicit vintage lookup, or other logic that is impractical to do reliably by manual review.

Use `scripts/catalog_search.py` as a convenience helper for complex tasks, not as the default path for simple lookups.

Helper commands:

```bash
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py latest-weo
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "current account balance" --all-databases
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only
```

## Priority Policy

- Default to non-vintage datasets. Do not search or return vintage datasets unless the user explicitly asks for a vintage, historical publication, dated snapshot, or versioned release.
- For WEO-like macroeconomic concepts, use the non-vintage `WEO_LIVE` dataflow family as the first priority unless the user asks for a different database family.
- Exclude `IMF.RES:WEO` from catalog search unless the user explicitly asks for that database. `WEO_LIVE` has much broader coverage and is the default WEO source.
- Do not silently collapse `WEO_LIVE` to the latest vintage. If the user asks for a vintage but does not specify which one, ask whether they want the latest available WEO Live vintage or a specific historical vintage.
- `catalog_search.py latest-weo` returns the non-vintage `WEO_LIVE` dataflow. Use `datasets WEO --vintage-only` when the user explicitly asks for historical/vintage WEO datasets.
- Prefer WEO Live for common annual macro concepts such as GDP, real GDP growth, inflation, current account, fiscal balance, unemployment, population, exchange rates, PPP, imports, and exports.
- Search all databases only when WEO Live lacks a plausible match, the user explicitly asks for a non-WEO database, or the concept is clearly outside WEO coverage.

## Uncertainty Policy

If there is material uncertainty, do not guess. Ask the user for confirmation before committing to one interpretation, dataset, dimension, or code choice.

When search returns several plausible best matches, list the candidates with short distinction notes and ask for user preference/confirmation. Ask the smallest useful question, usually among 2-5 candidates.

Clarify when:

- Multiple variables share the same concept but differ by unit, transformation, or valuation, such as current prices vs constant prices, national currency vs U.S. dollars, percent of GDP, per capita, period average vs end of period, level vs percent change.
- Multiple databases match and WEO Live is not obviously the right source.
- The requested frequency is incompatible or unclear. WEO Live is generally annual; use other databases for quarterly/monthly needs unless metadata says otherwise.
- The user asks for a vintage WEO Live pull but does not specify whether they want the latest available vintage or a historical vintage.
- The country coverage implies a WEO group, region, or panel but the group/country set is unclear.

When presenting candidates, include `database_name`, `dimension_name`, `Code`, and `Name`, plus a short distinction note. Do not invent codes. Preserve `dimension_name` for handoff to `imf-ra-data`; not every dataset uses `INDICATOR` as the series/code dimension.

## Workflow

1. **Understand the request:** identify concept, desired unit/transformation, frequency, vintage, database preference, and country/group coverage when available.
2. **Inspect first:** for straightforward requests, answer directly from the CSV/Markdown references.
3. **Complex search path:** use `catalog_search.py search "<query>"` (and `--all-databases` only when needed) for heavy lookup tasks.
4. **Use curated guidance:** check `databases/`, `indicators/`, and optional `overlays/` notes when raw catalog rows are ambiguous. If overlay guidance exists and conflicts with raw rows, follow the overlay guidance.
5. **Discuss uncertainty:** if multiple plausible variables remain, ask the RA to choose or clarify. Do not collapse distinct candidates into one.
6. **Output:** return top-N candidates with confidence notes. Commit to a single identifier only when the match is exact and unambiguous.
7. **Fallback:** if CSV and Markdown references do not yield a useful match, surface the gap and ask for a hint. Do **not** invent a dataset, dimension, or code identifier.

## Handoff

Once the RA confirms an identifier, hand off to `imf-ra-data` for fetch execution.

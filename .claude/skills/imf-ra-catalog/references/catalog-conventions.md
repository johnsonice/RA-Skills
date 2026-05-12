# Catalog conventions

How `imf-ra-catalog` is organized and how to use its reference files.

## Core files

The catalog is built around three iData CSV references:

| File | Purpose | Columns |
|---|---|---|
| `databases/templates/non_vintaged_datasets.csv` | Default dataset/dataflow discovery for non-vintage requests. | `database`, `name`, `Agency ID`, `Resource ID`, `Latest Version`, `Unique ID` |
| `databases/templates/vintaged_datasets.csv` | Vintage-only dataset/dataflow discovery. Use only for explicit vintage requests. | `database`, `name`, `Agency ID`, `Resource ID`, `Latest Version`, `Unique ID` |
| `indicators/non_vintage_Full_Variable_List.csv` | Non-vintage variable/code discovery. | `database_name`, `dimension_name`, `Code`, `Name` |

Use the CSV files as the source of truth for what exists. Source-specific templates live under `databases/templates/` and `indicators/templates/`; the iData templates document the current CSV schemas and explain when a focused Markdown note is worth adding.

## Default lookup behavior

For easy and straightforward questions, read the available CSV, Markdown, and optional overlay files and answer directly from what you find. Do not write or run code when inspection is enough.

Use `../scripts/catalog_search.py` only for complex lookup tasks, such as broad keyword search across many rows, repeated filtering, ranking candidates, joining dataset and variable references, explicit vintage lookup, or other logic that is impractical to do reliably by manual review.

If there is any material uncertainty, do not guess. Ask the user for confirmation before committing to one interpretation, dataset, dimension, or code choice.

If search or lookup results return several plausible "best match" candidates, list those candidates clearly and ask the user for preference/confirmation.

## Datasets

Use `databases/templates/non_vintaged_datasets.csv` when the user asks about available datasets, dataflows, agencies, resource IDs, versions, or unique dataset identifiers.

Use `catalog_search.py datasets <query>` for broad or repeated dataset searches. This searches non-vintage datasets by default. Add `--vintage-only` when the user asks for a vintage, historical publication, dated snapshot, or versioned release. Use `--include-vintage` only when the user explicitly wants to compare live/non-vintage datasets with vintage datasets.

Use `catalog_search.py latest-weo` for the current non-vintage `WEO_LIVE` dataflow. Use `datasets WEO --vintage-only` only when the user asks for historical/vintage WEO datasets. Do not silently collapse the non-vintage `WEO_LIVE` family to a single dated vintage.

## Indicators

Use `indicators/non_vintage_Full_Variable_List.csv` when the user asks for an indicator code, variable code, candidate code, or which non-vintage datasets contain a concept.

For WEO-style annual macroeconomic concepts, start with the `WEO_LIVE` dataflow family unless the user asks for another source family or the concept is clearly outside WEO coverage.

Exclude `IMF.RES:WEO` from normal catalog search unless the user explicitly asks for that database. `WEO_LIVE` has much broader coverage and should be the default WEO source.

When multiple candidates differ by unit, transformation, valuation, frequency, price basis, dimension, or database, surface the plausible candidates with `database_name`, `dimension_name`, `Code`, and `Name`; then ask the RA to choose. Do not invent codes.

Carry `dimension_name` through the handoff to `imf-ra-data`. Many datasets use dimensions other than `INDICATOR` for the series/code dimension, so assuming `INDICATOR` will break some fetches.

Use `catalog_search.py search <query>` for complex variable/code searches. Add `--all-databases` only when WEO Live lacks a plausible match, the user explicitly asks for a non-WEO source, or the concept is outside WEO coverage.

## Curated Markdown

Add focused Markdown notes only when the CSV row is not enough:

- `databases/<name>.md`: dataset-specific guidance, such as dimension conventions, frequency caveats, source-specific gotchas, or common variable/code mappings.
- `indicators/<topic>.md`: concept or variable/code guidance, such as preferred source selection, naming ambiguity, unit caveats, vintage sensitivity, or why similarly named codes should be avoided.
- `overlays/<topic>.md`: optional institutional guidance that overrides or augments CSV rows and focused notes.

When curated Markdown conflicts with raw CSV search results, follow the curated guidance and explain the reason briefly.

## Output expectations

Return top candidates with concise notes when the match is ambiguous. Commit to a single identifier only when the match is exact and unambiguous.

If the CSV and Markdown references do not contain a useful match, say so and ask for the smallest helpful clarification.

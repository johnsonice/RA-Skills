# Catalog conventions

How `imf-ra-catalog` is organized and how to use its reference files.

## Core files

The catalog is built around two iData CSV references:

| File | Purpose | Columns |
|---|---|---|
| `databases/idata_full_datasets_list.csv` | Dataset/dataflow discovery. | `name`, `Agency ID`, `Resource ID`, `Latest Version`, `Unique ID` |
| `indicators/idata_full_indicators_list.csv` | Indicator/code discovery. | `database_name`, `indicator_code`, `indicator_name` |

Use the CSV files as the source of truth for what exists. Source-specific templates live under `databases/templates/` and `indicators/templates/`; the iData templates document the current CSV schemas and explain when a focused Markdown note is worth adding.

## Default lookup behavior

For easy and straightforward questions, read the available CSV, Markdown, and optional overlay files and answer directly from what you find. Do not write or run code when inspection is enough.

Use `../scripts/catalog_search.py` only for complex lookup tasks, such as broad keyword search across many rows, repeated filtering, ranking candidates, joining dataset and indicator references, calculating latest vintages, or other logic that is impractical to do reliably by manual review.

If there is any material uncertainty, do not guess. Ask the user for confirmation before committing to one interpretation, dataset, or indicator choice.

If search or lookup results return several plausible "best match" candidates, list those candidates clearly and ask the user for preference/confirmation.

## Datasets

Use `databases/idata_full_datasets_list.csv` when the user asks about available datasets, dataflows, agencies, resource IDs, versions, or unique dataset identifiers.

Use `catalog_search.py datasets <query>` for broad or repeated dataset searches. Use `catalog_search.py latest-weo` only when the user asks for the latest/current WEO Live vintage or agrees to use it.

Do not silently collapse the `WEO_LIVE` family to a single vintage. If a fetch requires a concrete vintage and the user has not specified one, ask whether they want the current/latest available WEO Live vintage or a specific historical vintage.

## Indicators

Use `indicators/idata_full_indicators_list.csv` when the user asks for an indicator code, candidate series, or which datasets contain a concept.

For WEO-style annual macroeconomic concepts, start with the `WEO_LIVE` dataflow family unless the user asks for another source family or the concept is clearly outside WEO coverage.

When multiple candidates differ by unit, transformation, valuation, frequency, price basis, vintage, or database, surface the plausible candidates with `database_name`, `indicator_code`, and `indicator_name`; then ask the RA to choose. Do not invent indicator codes.

Use `catalog_search.py search <query>` for complex indicator searches. Add `--all-databases` only when WEO Live lacks a plausible match, the user explicitly asks for a non-WEO source, or the concept is outside WEO coverage.

## Curated Markdown

Add focused Markdown notes only when the CSV row is not enough:

- `databases/<name>.md`: dataset-specific guidance, such as dimension conventions, frequency caveats, source-specific gotchas, or common indicator mappings.
- `indicators/<topic>.md`: concept or indicator guidance, such as preferred source selection, naming ambiguity, unit caveats, vintage sensitivity, or why similarly named indicators should be avoided.
- `overlays/<topic>.md`: optional institutional guidance that overrides or augments CSV rows and focused notes.

When curated Markdown conflicts with raw CSV search results, follow the curated guidance and explain the reason briefly.

## Output expectations

Return top candidates with concise notes when the match is ambiguous. Commit to a single identifier only when the match is exact and unambiguous.

If the CSV and Markdown references do not contain a useful match, say so and ask for the smallest helpful clarification.

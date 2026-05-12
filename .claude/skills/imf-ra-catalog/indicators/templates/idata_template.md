# non_vintage_Full_Variable_List.csv Reference

`non_vintage_Full_Variable_List.csv` is the iData variable catalog for non-vintage dataset lookup in `imf-ra-catalog`.

Use it when the user needs to find a code, compare similarly named variables, or identify which non-vintage datasets contain a concept. Do not create one Markdown file per variable unless there is curated RA guidance that cannot be represented in the CSV or an overlay.

## Location

- File: `indicators/non_vintage_Full_Variable_List.csv`
- Search helper: `scripts/catalog_search.py search <query>`
- Broad search: `scripts/catalog_search.py search <query> --all-databases`

## Columns

| Column | Meaning |
|---|---|
| `database_name` | Dataset identifier that contains the code, usually `Agency ID:Resource ID`. |
| `dimension_name` | Dimension to fill in `imf-ra-data`. This is not always `INDICATOR`. |
| `Code` | Variable, indicator, or dimension value code to use after the dataset is selected. |
| `Name` | Human-readable variable or dimension value description. |

## Lookup Rules

- For straightforward indicator/variable questions, inspect `non_vintage_Full_Variable_List.csv` directly.
- Use `catalog_search.py search` for repeated searches, broad keyword matching, or when many rows make direct inspection unreliable.
- By default, `catalog_search.py search` prioritizes the `WEO_LIVE` family for WEO-style macroeconomic concepts.
- Use `--all-databases` when WEO Live lacks a plausible match, the user asks for a non-WEO source, or the concept is outside WEO coverage.
- Do not invent codes. If multiple plausible variables differ by unit, transformation, valuation, frequency, dimension, or database, surface candidates and ask the RA to choose.
- Always preserve `dimension_name` in the resolved identifier and handoff. Assuming `INDICATOR` will be wrong for datasets whose series-like dimension has another name.

## When To Add Markdown

Add a focused Markdown file under `indicators/` only when a concept or code needs curated RA guidance beyond the CSV row, such as preferred source selection, naming ambiguity, unit caveats, vintage sensitivity, or why similarly named codes should be avoided.

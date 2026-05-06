# idata_full_indicators_list.csv Reference

`idata_full_indicators_list.csv` is the iData indicator catalog for `imf-ra-catalog`.

Use it when the user needs to find an indicator code, compare similarly named indicators, or identify which datasets contain a concept. Do not create one Markdown file per indicator unless there is curated RA guidance that cannot be represented in the CSV or an overlay.

## Location

- File: `indicators/idata_full_indicators_list.csv`
- Search helper: `scripts/catalog_search.py search <query>`
- Broad search: `scripts/catalog_search.py search <query> --all-databases`

## Columns

| Column | Meaning |
|---|---|
| `database_name` | Dataset identifier that contains the indicator, usually `Agency ID:Resource ID`. |
| `indicator_code` | Indicator or series code to use after the dataset is selected. |
| `indicator_name` | Human-readable indicator description. |

## Lookup Rules

- For straightforward indicator questions, inspect `idata_full_indicators_list.csv` directly.
- Use `catalog_search.py search` for repeated searches, broad keyword matching, or when many rows make direct inspection unreliable.
- By default, `catalog_search.py search` prioritizes the `WEO_LIVE` family for WEO-style macroeconomic concepts.
- Use `--all-databases` when WEO Live lacks a plausible match, the user asks for a non-WEO source, or the concept is outside WEO coverage.
- Do not invent indicator codes. If multiple plausible indicators differ by unit, transformation, valuation, frequency, or vintage, surface candidates and ask the RA to choose.

## When To Add Markdown

Add a focused Markdown file under `indicators/` only when an indicator or concept needs curated RA guidance beyond the CSV row, such as preferred source selection, naming ambiguity, unit caveats, vintage sensitivity, or why similarly named indicators should be avoided.

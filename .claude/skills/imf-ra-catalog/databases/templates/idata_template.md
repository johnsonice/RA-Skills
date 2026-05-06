# idata_full_datasets_list.csv Reference

`idata_full_datasets_list.csv` is the iData dataset/dataflow catalog for `imf-ra-catalog`.

Use it when the user needs to discover an IMF dataset, dataflow, agency, latest version, or concrete `Unique ID`.

## Location

- File: `databases/idata_full_datasets_list.csv`
- Search helper: `scripts/catalog_search.py datasets <query>`
- Latest WEO helper: `scripts/catalog_search.py latest-weo`

## Columns

| Column | Meaning |
|---|---|
| `name` | Human-readable dataset name. |
| `Agency ID` | IMF SDMX agency/provider ID, such as `IMF.RES.WEO` or `IMF.STA`. |
| `Resource ID` | Dataset/dataflow resource ID, such as `WEO_LIVE_2026_APR_VINTAGE`. |
| `Latest Version` | Latest version string from the source catalog. |
| `Unique ID` | Concrete agency/resource/version identifier used for exact dataset references. |

## Lookup Rules

- For straightforward dataset questions, inspect `idata_full_datasets_list.csv` directly.
- Use `catalog_search.py datasets` for repeated searches, broad keyword matching, or when many rows make direct inspection unreliable.
- Use `catalog_search.py latest-weo` only when the user asks for the latest/current WEO Live vintage or agrees to use it.
- Do not silently collapse the `WEO_LIVE` family to one vintage when the user has not specified latest/current versus historical.

## When To Add Markdown

Add a focused Markdown file under `databases/` only when a dataset needs curated RA guidance beyond the CSV row, such as dimension conventions, common indicator mappings, frequency caveats, or source-specific gotchas. Keep those files narrow and link back to `idata_full_datasets_list.csv` for the canonical dataflow identity.

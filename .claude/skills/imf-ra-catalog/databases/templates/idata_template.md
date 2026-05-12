# Dataset CSV References

`non_vintaged_datasets.csv` is the default iData dataset/dataflow catalog for `imf-ra-catalog`.
`vintaged_datasets.csv` is the companion vintage-only catalog.

Use these files when the user needs to discover an IMF dataset, dataflow, agency, latest version, or concrete `Unique ID`.

## Location

- Default file: `databases/templates/non_vintaged_datasets.csv`
- Vintage file: `databases/templates/vintaged_datasets.csv`
- Search helper: `scripts/catalog_search.py datasets <query>`
- WEO Live helper: `scripts/catalog_search.py latest-weo`

## Columns

| Column | Meaning |
|---|---|
| `database` | Joined `Agency ID:Resource ID` dataset identifier. |
| `name` | Human-readable dataset name. |
| `Agency ID` | IMF SDMX agency/provider ID, such as `IMF.RES.WEO` or `IMF.STA`. |
| `Resource ID` | Dataset/dataflow resource ID, such as `WEO_LIVE_2026_APR_VINTAGE`. |
| `Latest Version` | Latest version string from the source catalog. |
| `Unique ID` | Concrete agency/resource/version identifier used for exact dataset references. |

## Lookup Rules

- For straightforward dataset questions, inspect `non_vintaged_datasets.csv` directly.
- Use `catalog_search.py datasets` for repeated searches, broad keyword matching, or when many rows make direct inspection unreliable.
- Search is non-vintage by default. Add `--vintage-only` when the user explicitly asks for a vintage, historical publication, dated snapshot, or versioned release. Use `--include-vintage` only when the user wants to compare live/non-vintage datasets with vintage datasets.
- Use `catalog_search.py latest-weo` for the current non-vintage `WEO_LIVE` dataflow.
- Do not silently collapse the non-vintage `WEO_LIVE` family to one vintage.

## When To Add Markdown

Add a focused Markdown file under `databases/` only when a dataset needs curated RA guidance beyond the CSV row, such as dimension conventions, common variable/code mappings, frequency caveats, or source-specific gotchas. Keep those files narrow and link back to the relevant dataset CSV for the canonical dataflow identity.

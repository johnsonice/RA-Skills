# Catalog conventions

How the catalog is organized and how the layers interact.

## Layer 1: per-database files

One file per IMF database under `databases/`. Each file is human-readable Markdown but follows a consistent schema so grep over the family is reliable.

Schema lives in [`databases/_template.md`](../databases/_template.md). At minimum each file declares: dataflow ID, primary dimensions, frequency conventions, common indicators (with their codes), and notable gotchas.

In v2 these files may be auto-generated from SDMX metadata. The schema is designed to accept either hand-curated or machine-generated content without restructuring.

## Layer 2: overlays

Curated institutional knowledge that augments or corrects the per-database files. Examples:

- "For real GDP growth, prefer WEO `NGDP_RPCH` over IFS `NGDP_R_K_IX` because WEO is the consensus forecast."
- "Quarterly current account in BOPS uses `BCA_BP6_USD`, not the older BPM5 codes."
- "When users say 'advanced economies', they almost always mean the WEO group `AE`, not OECD."

Schema lives in [`overlays/_template.md`](../overlays/_template.md).

## Layer 3: CSV references

The catalog also includes internal CSV references under `references/`:

- `internal_full_datasets.csv`: dataset/dataflow catalog with `name`, `Agency ID`, `Resource ID`, `Latest Version`, and `Unique ID`.
- `Full_indicators_List.csv`: indicator catalog with `database_name`, `indicator_code`, and `indicator_name`.

Use `../scripts/catalog_search.py` to search these files. It defaults indicator search to the latest standard WEO Live dataset, then can broaden to all databases with `--all-databases`.

## Layer interaction

When grep matches both a database file and an overlay, **the overlay takes precedence**. Database files and CSV rows describe what exists; overlays describe what to use and why.

For WEO-style macroeconomic indicators, use the latest standard WEO Live dataset as the first priority unless the user asks for a different source or vintage. Determine "latest" from `internal_full_datasets.csv` at lookup time.

## Search expectations

The catalog returns top-N candidates with notes. Never a single committed pick when the description is ambiguous. The RA disambiguates.

Discuss uncertainty explicitly when candidates differ by units, transformation, frequency, valuation basis, price basis, vintage, or database. Examples include current vs constant prices, national currency vs U.S. dollars, percent of GDP vs level, average vs end-period, annual vs quarterly/monthly, and latest vs historical vintage.

## Adding new entries

- New database: copy `databases/_template.md` to `databases/<name>.md` and fill in.
- New overlay: copy `overlays/_template.md` to `overlays/<topic>.md` and fill in.
- Keep entries focused. Multiple small files beat one large file.

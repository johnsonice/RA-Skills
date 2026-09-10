# Refreshable output layout

Refreshable output layout is auto-selected by data shape (indicators × countries × time periods):

**Case 1 — Single indicator → Wide layout** (one row per series, dates as columns):

| Column | Present when | Source |
|---|---|---|
| `DATASET` | Always | The `--db` argument |
| `Series_Code` | Always | All dimension values joined with `.` in key order |
| `SCALE` | Always present | Human-readable scale label: `Units` / `Thousands` / `Millions` / `Billions`; empty when scale metadata is unavailable; values already divided by 10^scale when scale > 0 |
| `UNIT` | When metadata has unit info | Unit string decoded from metadata (e.g. `National currency`, `Percent`); column omitted entirely when the database has no unit metadata (e.g. BBGDL) |
| `COUNTRY` | Country dimension detected | Human-readable name looked up from `imf-ra` `country_group.csv` |
| `ISO3` | Country dimension detected | Raw ISO3 code from the data |
| `IFSCODE` | Country dimension detected | Looked up from `imf-ra` `country_group.csv` (`countrycode_s`) |
| `<dim_name>` (non-country, non-indicator) | Each additional dimension | Raw dimension code (e.g. `FREQ`, `DATA_TRANSFORMATION`, `COUNTERPART_COUNTRY`) |
| `<indicator dim_name>` | When indicator dim detected | Human-readable label from `get_dimension_values()["Name"]` |
| `2019`, `2019Q1`, `2019M1` … | Always | Pivoted date columns; format matches frequency (A/Q/M/D) |

**Case 2 — Multi-sheet card** (triggered when indicators > 1 AND countries > 1 AND time periods > 1):

One tab per indicator (named by indicator label, max 31 chars). Within each tab:

| Row label | Content |
|---|---|
| `DATASET` | Database identifier |
| `Series_Code` | Dot-separated dimension values for that series |
| `SCALE` | Human-readable scale label (`Units` / `Thousands` / `Millions` / `Billions`); empty when scale metadata is unavailable; values already divided by 10^scale when scale > 0 |
| `UNIT` | Unit string decoded from metadata (e.g. `National currency`, `Percent`); row omitted entirely when the database has no unit metadata (e.g. BBGDL) |
| `COUNTRY` | Human-readable country name (when country dimension present) |
| `ISO3` | Raw ISO3 code (when country dimension present) |
| `IFSCODE` | IFS code (when country dimension present) |
| `<dim_name>` | Raw code for each non-country, non-indicator dimension |
| `<indicator dim_name>` | Human-readable label (same for all columns within one tab) |
| `2019`, `2019Q1`, `2016-02-25` … | Observation value for that series at that date |

First column = `Label` (row labels). Each subsequent column = one series (named by `Series_Code`).

**Case 3 — Single card sheet** (indicators > 1, but not all three dimensions plural):

Same card format as Case 2, but a single sheet containing all indicators together. Layout is identical — `Label` column + one column per series across all indicators.

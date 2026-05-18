---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetching IMF data series via the internal Python SDK.

## Skill relationships

Load these skills in order as needed:

- **`imf-ra`** (umbrella) — load first for shared conventions: country codes, WEO country groups, frequency handling, uncertainty policy, and SDK environment setup.
- **`imf-ra-catalog`** — load before this skill when the database or indicator is not yet identified. It translates plain-English descriptions into a confirmed `(database, dimension_name, code, frequency, geo)` tuple.
- **`imf-ra-data`** (this skill) — takes over once the identifier is confirmed. Resolves remaining dimensions, builds the iData key, and executes the fetch.
- **`imf-ra-charts`** — load after this skill when the user wants to visualize the tidy output.

## Default decision logic

1. Prefer `idata_utilities` for new IMF workflows.
2. Use metadata calls (`--explore`, `--dimension-values`) only to resolve remaining dimensions after catalog handoff — not to re-discover the database or indicator, which the catalog already owns.
3. For databases with both a LIVE and a Vintage version (see ## LIVE databases and private access below), prefer the LIVE database unless the user asks for a specific vintage.
4. If the user asks for EcOS-based retrieval, explain that EcOS is retired and provide the iData equivalent workflow.

## LIVE databases and private access

Databases can come in two forms — distinguish them by whether the resource ID contains `VINTAGE`:

- **LIVE** (current data): resource ID does **not** contain `VINTAGE` — e.g. `IMF.RES.WEO:WEO_LIVE`, `IMF.RES:GAS_LIVE`, `IMF.RES:GEE_LIVE`.
- **Vintage** (historical snapshot): resource ID contains `VINTAGE` — e.g. `IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE`.

Do **not** use `_LIVE_` as the sole discriminator — vintage resource IDs also contain this substring.

When a database family has both forms:

- **If the user explicitly asks for live data**, use the LIVE database directly — do not substitute the closest vintage.
- **If the user specified a vintage** (even loosely, e.g. "April 2024" or "Oct 2023 release"), match it to the nearest vintage and proceed — no need to ask again.
- **If the user did not specify**, present the LIVE database as the primary option first, then mention the latest historical vintage as an alternative. Ask which they want before proceeding. **Do not silently default to the closest vintage.**

All LIVE and vintage databases are private IMF datasets and require `idata_utilities.PRIVATE = True` before any retrieval call. The pre-built fetch utility ([scripts/fetch_idata.py](scripts/fetch_idata.py)) sets this flag automatically. For any inline `idata_utilities` call, set it first. See [references/imf_datatools_agent_api_reference.md § 3.1](references/imf_datatools_agent_api_reference.md) for details.

## EcOS retired policy

EcOS retrieval is retired in the system. Do not use EcOS retrieval-related functionality in this skill.

Disallowed retrieval paths include (non-exhaustive):

- `get_ecos_sdmx_data`
- `get_ecos_gfs_data`
- `get_ecos_commodity_data`
- `get_ecos_bloomberg_data`
- `get_idata_data_using_ecos`

## Python-only scope

This skill is Python-focused. Do not generate R or Stata workflows unless the user explicitly asks.

## CLI Fetch Protocol

**Never create a new Python script to explore or fetch data.** A pre-built fetch utility already exists. Follow these seven steps every time.

### Step 1 — Catalog lookup

If the `(database, dimension_name, code, frequency, geo)` tuple is not yet confirmed, invoke **`imf-ra-catalog`** to resolve it. Do **not** search catalog files directly from this skill — all indicator and database discovery is owned by `imf-ra-catalog`.

If you are arriving from a catalog handoff with a confirmed identifier, skip directly to Step 2.

### Step 2 — Read dimensions

Once the database is confirmed, list its dimensions in key order:

```bash
python .claude/skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --explore
```

This prints the dimension names in the order they appear in the iData key. The indicator code (`code` from the catalog handoff) slots into the position matching the catalog's `dimension_name` field.

### Step 3 — Identify unresolved dimensions and clarify time range

Compare what the user specified against the dimensions returned. Required inputs for a complete iData key:

- **`start` / `end` (time range)** — **always ask if not specified**. Do not proceed without a confirmed time range.
- One value per dimension — exact names are shown by `--explore` and vary by database (e.g. WEO uses `COUNTRY`, `INDICATOR`, `FREQUENCY`; WDI uses `REF_AREA`, `SERIES`; BBG uses `TICKER`, `FIELD`).

**Auto-resolve vs. ask-user rules:**

| Situation | Action |
|---|---|
| Dimension has exactly one valid value | Auto-resolve silently; use that value without asking |
| User already specified the dimension | Use the user's value; validate it using `--dimension-values <DIM>` |
| Dimension has multiple values and user did not specify | Ask the user — do not list all options upfront |
| `start` / `end` not specified | **Always ask** — do not assume or default |

**Never guess or hardcode a dimension value.**

For country and group dimensions, translate RA-friendly names ("advanced economies", "G7", "EMDE") through `imf-ra` conventions before presenting or validating codes.

### Step 4 — Ask for missing dimensions

Ask the user to supply each unresolved dimension by name. Do **not** list all available codes upfront — just ask. If the user requests options or further detail (e.g. "what frequencies are available?"), run `--dimension-values <DIM>` and present the results in a clean, readable format — e.g. "Annual (A), Quarterly (Q), Monthly (M)" — not as a raw code dump.

Example structure:

> I found **[indicator name]** (`[INDICATOR_CODE]`) in database `[DB_ID]`.
>
> Before I pull the data, I need a few more details:
>
> **1. Time range** — what start and end year (or period) would you like?
>
> **2. [Dimension name]** — which value would you like?

If the user asks "what options are there for X?", run:

```bash
python .claude/skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --dimension-values <DIM>
```

Present the results in readable form (e.g. "Annual (A), Quarterly (Q), Monthly (M)"), then ask again.

### Step 5 — Build the iData key

The iData key is a dot-separated string of all dimension values in the exact order shown by `--explore` in Step 2.

**Key construction rules:**

- One dot-separated field per dimension, in key order.
- Leave a dimension blank (consecutive dots) to select all values for that dimension.
- Combine multiple values within one dimension with `+` (e.g. `USA+GBR.NGDP_RPCH.A`).
- The total number of dot-separated fields must match the total number of dimensions — do not add or drop dots.

**Country group rule:** Do **not** use a WEO group code (e.g. `G110`, `G200`) directly as the country selector in an iData key. Resolve the group to its member `countrycode` values first (via `imf-ra` WEO group helpers), then join them with `+`. Use a group aggregate code only when the database metadata explicitly confirms it is a valid dimension value.

### Step 6 — Confirm output format

Before executing, always ask the user which output format they want. Do **not** assume a format.

> **Output format** — which would you like?
> - **Refreshable** — RA enriched Excel (`.xlsx`) with human-readable indicator labels; `CountryName`, `ISO3`, `IFSCODE` added when a country dimension is present. Layout auto-selected by data shape:
>   - **Multi-sheet card** (triggered when indicators > 1 AND countries > 1 AND time periods > 1): one tab per indicator; each tab is card format (first column = `Label` with metadata + date rows, one column per series/country).
>   - **Wide** (single indicator cases): single sheet, dates as columns, one row per series.
>   - **Long** (all other cases): single sheet, card format.
>
>   Always `.xlsx`.
> - **Wide** — raw API output as-is, dates as rows, series as columns.
> - **Long** — raw API output as-is, one row per observation.
>
> For Wide or Long: would you like **CSV** or **Excel**?

**Refreshable is not the same as the raw API wide or long format** — it adds RA metadata columns and human-readable indicator labels that raw formats do not have.

If the user has already stated a format preference earlier in the conversation, confirm it rather than re-asking.

### Step 7 — Execute with the pre-built fetch utility

Once all dimensions, time range, and output format are confirmed, call `fetch_idata.py` with the appropriate `--format` flag:

```bash
# Refreshable RA Excel (layout auto-selected by number of indicators)
python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
    --db "<database_id>" \
    --key "<dot.separated.key>" \
    --start "<YYYY>" \
    --end "<YYYY>" \
    --format refreshable \
    --indicator-dim "<dimension_name>"   # from catalog handoff; omit if INDICATOR

# Wide (omit --excel for CSV, add --excel for Excel)
python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
    --db "<database_id>" \
    --key "<dot.separated.key>" \
    --start "<YYYY>" \
    --end "<YYYY>" \
    --format wide

# Long (omit --excel for CSV, add --excel for Excel)
python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
    --db "<database_id>" \
    --key "<dot.separated.key>" \
    --start "<YYYY>" \
    --end "<YYYY>" \
    --format long
```

Add `--excel` to save Wide or Long output as `.xlsx` instead of `.csv`. Add `--output <filename>` to specify the output path.

**Be aware that sometimes the idata endpoint is not 100% stable, and a retry may be needed. If you get an 403 error, retry up to 3 times before giving up.**

**`--indicator-dim`** — pass the `dimension_name` value from the catalog handoff. The catalog resolves the correct indicator dimension name for every database (e.g. `INDICATOR` for WEO/IFS, `TICKER` for BBG, `SERIES` for WDI). Always use what the catalog returns — do not guess or hardcode.

**Always use this script — never return raw SDK output directly.**

Refreshable output layout is auto-selected by data shape (indicators × countries × time periods):

**Case 1 — Single indicator → Wide layout** (one row per series, dates as columns):

| Column | Present when | Source |
|---|---|---|
| `DATASET` | Always | The `--db` argument |
| `Series_Code` | Always | All dimension values joined with `.` in key order |
| `CountryName` | Country dimension detected | Looked up from `imf-ra` `1. countries.csv` |
| `ISO3` | Country dimension detected | Raw country code from the data |
| `IFSCODE` | Country dimension detected | Looked up from `imf-ra` `1. countries.csv` (`countrycode_s`) |
| `<dim_name>` (non-country, non-indicator) | Each additional dimension | Raw dimension code (e.g. `FREQ`, `DATA_TRANSFORMATION`) |
| `<indicator dim_name>` | When indicator dim detected | Human-readable label from `get_dimension_values()["Name"]` |
| `2019`, `2019Q1`, `2019M1` … | Always | Pivoted date columns; format matches frequency (A/Q/M/D) |

**Case 2 — Multi-sheet card** (triggered when indicators > 1 AND countries > 1 AND time periods > 1):

One tab per indicator (named by indicator label, max 31 chars). Within each tab:

| Row label | Content |
|---|---|
| `DATASET` | Database identifier |
| `Series_Code` | Dot-separated dimension values for that series |
| `CountryName` | Country name (when country dimension present) |
| `ISO3` | Country code (when country dimension present) |
| `IFSCODE` | IFS code (when country dimension present) |
| `<dim_name>` | Raw code for each non-country, non-indicator dimension |
| `<indicator dim_name>` | Human-readable label (same for all columns within one tab) |
| `2019`, `2019Q1`, `2016-02-25` … | Observation value for that series at that date |

First column = `Label` (row labels). Each subsequent column = one series (named by `Series_Code`).

**Case 3 — Single card sheet** (indicators > 1, but not all three dimensions plural):

Same card format as Case 2, but a single sheet containing all indicators together. Layout is identical — `Label` column + one column per series across all indicators.

## Before you fetch

Always load **`imf-ra`** first for shared conventions:

- **Country and group codes** — translate RA-friendly names ("advanced economies", "EMDE", "G7") through the WEO group reference in `imf-ra`, not from memory.
- **Frequencies** — follow standard frequency codes (`A`, `Q`, `M`, `D`) and confirm date handling from dataset metadata when needed.
- **Time range** — always confirm `start` and `end` with the user before fetching.
- **SDK environment setup** — set the required private-data access flags described in this skill before retrieval.

## How to fetch

See [references/imf_datatools_agent_api_reference.md](references/imf_datatools_agent_api_reference.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

Invoke `imf-ra-catalog` first to translate the user's description into a confirmed `(database, dimension_name, code, frequency, geo)`. Return here once the identifier is confirmed and proceed from Step 2.

## After catalog handoff

When `imf-ra-catalog` returns a confirmed identifier:

- `database` is the iData database identifier; use it in Step 2 to fetch dimensions via the API.
- `dimension_name` is the indicator dimension name for this database (e.g. `INDICATOR`, `TICKER`, `SERIES`). Pass it as `--indicator-dim` when calling `fetch_idata.py --format refreshable`.
- `code` is the confirmed indicator code; slot it into the position matching `dimension_name` when building the key.
- `name` explains unit, valuation, transformation, and price basis; use it to phrase follow-up questions when candidates differ.
- `frequency` — if confirmed by the catalog, use it directly in the key; skip asking the user for frequency in Step 3.
- `geo` — if confirmed by the catalog, use it directly as the country/region dimension value; skip asking the user for geography in Step 3.
- For WEO candidates, keep the LIVE database as the priority — do not substitute a vintage unless the user asked for one.
- Resolve all remaining dimensions and the time range via Steps 2–6 before calling `fetch_idata.py`.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- For large requests, iterate over countries/indicators/frequencies and merge results.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, always use the exact dimension names returned by `--explore` — do not assume names like `COUNTRY`, `INDICATOR`, or `FREQUENCY`, as they vary by database (e.g. `REF_AREA`, `SERIES`, `FREQ`, `TICKER`).

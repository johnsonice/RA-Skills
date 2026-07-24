---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from iData or Haver, or wants schema-aware Microsoft SQL Server query generation and limited verification for the Dealogic transaction database. Covers single-series and multi-country panel pulls, frequency conversion, country selection, Dealogic field and join discovery, safe TOP (20) SQL previews, and read-only query verification. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetch IMF time series through supported helpers and generate schema-aware,
read-only Dealogic SQL Server previews.

## Skill relationships

Load these skills in order as needed:

- **`imf-ra`** (umbrella) — load first for shared conventions and cross-skill execution policy: country codes, WEO country group resolution helpers, frequency handling, lookup execution policy, and SDK environment setup.
- **`imf-ra-catalog`** — load before this skill when the database or indicator is not yet identified. For iData sources it returns a confirmed `(database, dimension_name, code)` identifier; for Haver sources it returns a confirmed `codes: ["CODE@DB", ...]` list after variant disambiguation. Ready for handoff in either case.
- **`imf-ra-data`** (this skill) — takes over once a time-series identifier is confirmed, or directly handles an explicit Dealogic request. Resolves remaining iData dimensions, fetches iData/Haver data, and generates or verifies bounded Dealogic SQL.
- **`imf-ra-charts`** — load after this skill when the user wants to visualize the tidy output.

## Default decision logic

1. Route Dealogic transaction questions to [Dealogic SQL](#dealogic-sql); do not force them through the iData time-series protocol.
2. Prefer `idata_utilities` for new IMF time-series workflows.
3. Use metadata calls (`--explore`, `--dimension-values`) only to resolve remaining dimensions after catalog handoff — not to re-discover the database or indicator, which the catalog already owns.
4. For databases with both a LIVE and a Vintage version (see ## LIVE databases and private access below), prefer the LIVE database unless the user asks for a specific vintage.
5. If the user asks for EcOS-based retrieval, explain that EcOS is retired and provide the iData equivalent workflow.

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

This skill's supported and tested fetch workflow is Python-only through the pre-built `fetch_idata.py` utility. Do not present R or Stata as a supported RA-skill retrieval path.

If the user explicitly asks for R or Stata code:

1. Acknowledge the requested language.
2. Explain that this RA skillset only validates the Python/iData workflow.
3. Provide the confirmed identifier tuple and supported `fetch_idata.py` command when possible.
4. Only provide R or Stata as an external, unvalidated sketch when the user explicitly asks to proceed outside the supported RA workflow, and label it clearly as unvalidated.

## CLI Fetch Protocol

**This protocol is for iData sources only. For Haver sources, skip directly to [Haver Fetch](#haver-fetch).**

**Never create a new Python script to explore or fetch data.** A pre-built fetch utility already exists.

**Fast-path check:** Before following the seven steps, check whether all inputs are already known. If the catalog handoff contains confirmed `database`, `dimension_name`, `code`, `geo`, and `frequency`, AND the user has specified `start`, `end`, and output format in the same message, skip Steps 1–6 and go directly to Step 7.

### Step 1 — Catalog lookup

If the identifier is not yet confirmed, invoke **`imf-ra-catalog`** — do **not** search catalog files directly from this skill.

- **iData path:** the catalog uses `resolve "<query>" --json`. If it returns `status=resolved` with a `handoff` object (`database`, `dimension_name`, `code`), proceed to Step 2. If `status=ambiguous`, surface the clarification and wait.
- **Haver path:** the catalog uses the Haver Lookup Path (H1–H3: scope → build dblist → search → surface variants → confirm). When the `codes` list is confirmed, skip Steps 2–7 entirely and go to [Haver Fetch](#haver-fetch).

If you are arriving from a confirmed catalog handoff, check its shape: `database + code` fields → Step 2; `codes` list → Haver Fetch.

### Step 2 — Read dimensions

Skip this step if the catalog handoff already confirms all dimension names and values (e.g. a full WEO handoff with `database`, `dimension_name`, `code`, `geo`, and `frequency` covers all three WEO dimensions: COUNTRY · INDICATOR · FREQUENCY).

When unresolved dimensions remain, list them in key order:

```bash
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --explore
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

**To determine whether a dimension has one or multiple values**, run `--dimension-values <DIM>` for each unresolved dimension before deciding to auto-resolve or ask. Do not assume a dimension is single-valued without checking.

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
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --dimension-values <DIM>
```

Present the results in readable form (e.g. "Annual (A), Quarterly (Q), Monthly (M)"), then ask again.

### Step 5 — Build the iData key

The iData key is a dot-separated string of all dimension values in the exact order shown by `--explore` in Step 2.

**Key construction rules:**

- One dot-separated field per dimension, in key order.
- Leave a dimension blank (consecutive dots) to select all values for that dimension.
- Combine multiple values within one dimension with `+` (e.g. `USA+GBR.NGDP_RPCH.A`).
- The total number of dot-separated fields must match the total number of dimensions — do not add or drop dots.

**Country group rule:** Do **not** use a WEO group/category column name (e.g. `Advanced Economies(AE)`, `Emerging Market and Developing Economies(EMDE)`) directly as the country selector in an iData key. If arriving from a catalog handoff, `geo` is already expanded to member `countrycode` values joined with `+` (e.g. `USA+GBR+DEU`) — use it directly as the iData dimension value. If geography was not resolved by the catalog, run `expand-for-idata <GROUP> --codes-only` — the output is `+`-joined and can be pasted directly into the iData dimension slot without further transformation. Use a group aggregate value only when the database metadata explicitly confirms it is a valid dimension value.

### Step 6 — Confirm output format

Before executing, always ask the user which output format they want. Do **not** assume a format.

> **Output format** — which would you like?
> - **Refreshable** — RA enriched Excel (`.xlsx`) with human-readable indicator labels; `COUNTRY`, `ISO3`, `IFSCODE` added when a country dimension is present. Layout auto-selected by data shape:
>   - **Multi-sheet card** (triggered when indicators > 1 AND countries > 1 AND time periods > 1): one tab per indicator; each tab is card format (first column = `Label` with metadata + date rows, one column per series/country).
>   - **Wide** (single indicator): single sheet, dates as columns, one row per series.
>   - **Card** (multiple indicators, but not all three dimensions plural): single sheet, card format (first column = `Label` with metadata + date rows, one column per series across all indicators).
>
>   Always `.xlsx`.

> - **Wide** — raw API output as-is, dates as rows, series as columns.
> - **Long** — raw API output as-is, one row per observation.
>
> For Wide or Long: would you like **CSV** or **Excel**?

**Refreshable is not the same as the raw API wide or long format** — it adds RA metadata columns and human-readable indicator labels that raw formats do not have.

If the user has already stated a format preference at any point in the conversation, use it directly — do not ask again.

### Step 7 — Execute with the pre-built fetch utility

Once all dimensions, time range, and output format are confirmed, call `fetch_idata.py` with the appropriate `--format` flag:

```bash
# Refreshable RA Excel (layout auto-selected by number of indicators).
# Always pass --indicator-dim using dimension_name from the catalog handoff (e.g. INDICATOR, TICKER, SERIES).
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format refreshable --indicator-dim "<dimension_name>"

# Wide (CSV by default; add --excel for Excel)
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format wide

# Long (CSV by default; add --excel for Excel)
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format long
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

## Before you fetch

Always load **`imf-ra`** first for shared conventions:

- **Country and group codes** — translate RA-friendly names ("advanced economies", "EMDE", "G7") through the WEO group reference in `imf-ra`, not from memory.
- **Frequencies** — follow standard frequency codes (`A`, `Q`, `M`, `D`) and confirm date handling from dataset metadata when needed.
- **Time range** — always confirm `start` and `end` with the user before fetching.
- **SDK environment setup** — set the required private-data access flags described in this skill before retrieval.

## How to fetch

See [references/imf_datatools_agent_api_reference.md](references/imf_datatools_agent_api_reference.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

Invoke `imf-ra-catalog` first. For iData sources it returns a confirmed
`(database, dimension_name, code)` handoff. For Haver sources it returns a
confirmed `codes: ["CODE@DB", ...]` list.

- If the catalog returns `codes`, this is a Haver pull. Skip the iData fetch
  workflow and use [## Haver Fetch](#haver-fetch).
- If the catalog returns `database`, `dimension_name`, and `code`, use the
  iData fetch workflow below.

## iData fetch workflow

Use `fetch_idata.py`; do not write a new Python fetch script.

### Step 1 — Confirm the handoff

For iData handoffs:

- `database` is the iData database identifier.
- `dimension_name` is the indicator dimension name for this database (e.g.
  `INDICATOR`, `TICKER`, `SERIES`). Use it as `--indicator-dim` for
  refreshable output.
- `code` is the confirmed indicator code; slot it into the key position that
  matches `dimension_name`.
- `frequency` and `geo`, if present, are already resolved by the catalog.
  Use them directly in the key.
- `name` explains units, valuation, transformation, and price basis; use it to
  phrase follow-up questions when candidates differ.

If `dimension_name` is missing, run `--explore` and then use
`--dimension-values <DIM>` to identify which dimension contains the catalog
`code`.

### Step 2 — Read dimensions

Skip this step if the catalog already confirmed all dimensions.

```bash
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --explore
```

Use the returned key order to map dimension values into the dot-separated key.

### Step 3 — Resolve missing dimensions and time range

Required inputs for a complete key:

- **`start` / `end`** — always ask if missing.
- One value per unresolved dimension.

Before asking, use `--dimension-values <DIM>` to check whether a dimension has
one or multiple valid values.

Rules:

- If a dimension has only one valid value, auto-resolve it.
- If the user supplied a value, validate it with `--dimension-values`.
- If multiple values exist, ask the user rather than guessing.
- Do not assume or hardcode country or group values.

Translate RA-friendly geography names such as "advanced economies" or "EMDE"
through `imf-ra`, not from memory.

### Step 4 — Build the iData key

Construct the key as exact dot-separated dimension values in the order shown by
`--explore`.

- One field per dimension.
- Leave a field blank to select all values for that dimension.
- Combine multiple values with `+`.
- The key must have the same number of fields as dimensions.

For country groups, do not use a group label directly. If the catalog supplied
`geo`, it is already expanded to member codes joined with `+`.

### Step 5 — Confirm output format

Ask the user for Refreshable, Wide, or Long. Do not assume a format.

- **Refreshable** — RA-enriched `.xlsx` with human-readable labels.
- **Wide** — raw API output, dates as rows, series as columns.
- **Long** — raw API output, one row per observation.

For Wide and Long, ask whether they want CSV or Excel.

### Step 6 — Execute with `fetch_idata.py`

```bash
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format refreshable --indicator-dim "<dimension_name>"
```

```bash
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format wide
```

```bash
python skills/imf-ra-data/scripts/fetch_idata.py --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format long
```

Add `--excel` for `.xlsx` output and `--output <filename>` to name the file.
Always pass `--indicator-dim` with the catalog's `dimension_name`.

If the endpoint returns 403, retry up to 3 times before giving up.

## Haver Fetch

When the catalog returns a `codes` list, pass those strings directly to
`fetch_haver.py --codes`.

### Step 1 — Confirm time range

The catalog already resolves the series. The only remaining input is the
time range.

- Ask for `start` and `end` if missing.
- If the user wants more series, route back to `imf-ra-catalog`.

### Step 2 — Confirm output format

Ask for Refreshable, Wide, or Long. For Wide and Long, ask whether they want
CSV or Excel.

### Step 3 — Execute with `fetch_haver.py`

```bash
python skills/imf-ra-data/scripts/fetch_haver.py --codes "GDP@USECON" "UNRATE@USECON" --start "<YYYY>" --end "<YYYY>" --format refreshable --output <filename>.xlsx
```

```bash
python skills/imf-ra-data/scripts/fetch_haver.py --codes "GDP@USECON" --start "<YYYY>" --end "<YYYY>" --format wide
```

```bash
python skills/imf-ra-data/scripts/fetch_haver.py --codes "GDP@USECON" --start "<YYYY>" --end "<YYYY>" --format long
```

See [references/imf_datatools_agent_api_reference.md § 9](references/imf_datatools_agent_api_reference.md)
for the full Haver API reference.

## Dealogic SQL

Dealogic is available for primary-market DCM/bond, syndicated-loan, ECM, and
M&A transaction questions. It does not provide secondary-market bid, ask, or
traded-price series. Dealogic uses schema-aware SQL generation followed by an
optional, user-confirmed, read-only preview; it does not use the iData/Haver
catalog handoff or output-format workflow.

On the first response to a Dealogic request in a conversation, show the user
the official IMF [Economic and Financial Data at the IMF (EconFinData) guidance](https://apps.powerapps.com/play/e/e56a91a7-5e7c-ed89-bcf7-ca68bdf12f1c/a/b1e30305-b5d9-464d-9ee2-c4b878a86cd5?tenantId=8085fa43-302e-45bd-b171-a6648c3b6be7&hint=859df194-14d0-4956-8376-e4a21185f4a1&ItemId=2693).
Do not repeat it on every follow-up unless the user asks for the guidance again.

Canonical resources:

- [references/Dealogic/dealogic_overview.md](references/Dealogic/dealogic_overview.md) — read for source coverage, deal/tranche concepts, source-selection boundaries, and connection profile.
- [references/Dealogic/dealogic_schema.csv](references/Dealogic/dealogic_schema.csv) — extracted fields, business definitions, source types, XML paths, loader tables and columns, entity grain, keys, aliases, and provenance.
- [references/Dealogic/dealogic_relationships.csv](references/Dealogic/dealogic_relationships.csv) — parent and reference joins with cardinality and confidence.
- [references/Dealogic/dealogic_sql_patterns.md](references/Dealogic/dealogic_sql_patterns.md) — read before generating SQL; contains performance, grain, aggregation, and live-verification rules.
- [scripts/dealogic.py](scripts/dealogic.py) — the only supported Dealogic metadata and verification helper.

Workflow:

1. Search the canonical schema before writing SQL:

```bash
python skills/imf-ra-data/scripts/dealogic.py search "<user concept>" --domain DCM
```

2. State the output grain and resolve every multi-table join:

```bash
python skills/imf-ra-data/scripts/dealogic.py joins DCMDeal DCMDealTranches
```

If direct relationships are ambiguous, add `--from-column <column>`.

3. Generate SQL Server syntax against `[Dealogic].[dbo]` using the patterns
   reference. Use explicit columns, `TOP (20)` or less, and selective
   date/key/status constraints where a transaction scan could be broad.

4. Validate and show the SQL, grain, joins, filters, confidence, and
   assumptions:

```bash
python skills/imf-ra-data/scripts/dealogic.py validate-sql --sql-file <query.sql>
```

5. Do not return the SQL as final guidance until it has been executed
   successfully. After explicit user approval, verify the bounded preview:

```bash
python skills/imf-ra-data/scripts/dealogic.py verify --sql-file <query.sql> --confirmed
```

5a. If verification fails, diagnose and correct the query before returning it.
   - Read the verification error and determine whether the failure is syntax,
     schema, join, filter, or timeout related.
   - Use `dealogic.py inspect --table <table>` or the canonical schema search to
     confirm live column names and relationships.
   - Fix the query, re-run `validate-sql`, and then re-run
     `verify --confirmed`.
   - Do not return the SQL to the user as a final answer until verification
     succeeds.

The verifier permits one `SELECT` or `WITH ... SELECT`, rejects writes, DDL,
execution commands, `SELECT INTO`, and `SELECT *`, and enforces `TOP (20)` or
less with a short timeout.

When live-schema drift is suspected, inspect only the required table after
user approval:

```bash
python skills/imf-ra-data/scripts/dealogic.py inspect --table DCMDeal
```

Prefer `database_verified`, then `documented`, then disclosed `derived`
relationships. Never use `unverified` relationships. Present alternatives and
ask for confirmation when dates, amounts, roles, statuses, or domains remain
materially ambiguous.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, always use the exact dimension names returned by `--explore` — do not assume names like `COUNTRY`, `INDICATOR`, or `FREQUENCY`, as they vary by database (e.g. `REF_AREA`, `SERIES`, `FREQ`, `TICKER`).

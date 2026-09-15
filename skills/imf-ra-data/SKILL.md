---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from iData or Haver, or wants schema-aware Microsoft SQL Server query generation and limited verification for the Dealogic transaction database. Covers single-series and multi-country panel pulls, frequency conversion, country selection, Dealogic field and join discovery, safe TOP (20) SQL previews, and read-only query verification. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetch IMF time series through supported helpers and generate schema-aware,
read-only Dealogic SQL Server previews.

## Runtime

Use the company Python on IMF Windows; do not create or use virtual/Conda
environments. Before executing helpers, read the shared
[runtime contract](../imf-ra/references/runtime.md) for installed-skill paths, interpreter
selection, SDK setup authorization, and user output locations. Resolve scripts
from the loaded skill directory, not the user's working directory.


## Skill relationships

Load these skills in order as needed:

- **`imf-ra`** (umbrella) — load first for shared conventions and cross-skill execution policy: country codes, WEO country group resolution helpers, frequency handling, lookup execution policy, and SDK environment setup.
- **`imf-ra-catalog`** — load before this skill when the database or indicator is not yet identified. For iData sources it returns a confirmed `(database, dimension_name, code)` identifier; for Haver sources it returns a confirmed `codes: ["CODE@DB", ...]` list after variant disambiguation. Ready for handoff in either case.
- **`imf-ra-data`** (this skill) — takes over once a time-series identifier is confirmed, or directly handles an explicit Dealogic request. Resolves remaining iData dimensions, fetches iData/Haver data, and generates or verifies bounded Dealogic SQL.
- **`imf-ra-charts`** — owns visualization of fetched data; continue through [Retrieval completion and chart handoff](#retrieval-completion-and-chart-handoff) when the original request includes a chart.

## Default decision logic

1. Route Dealogic transaction questions to [Dealogic SQL](#dealogic-sql); do not force them through the iData time-series protocol.
2. Prefer `idata_utilities` for new IMF time-series workflows.
3. Use metadata calls (`--explore`, `--dimension-values`) only to resolve remaining dimensions after catalog handoff — not to re-discover the database or indicator, which the catalog already owns.
4. For WEO, default to WEO LIVE unless the user requests a vintage or explicitly selects another database. Apply the exact-vintage rules below.
5. If the user asks for any EcOS command, explain that EcOS is retired and resolve an iData alternative through the catalog.

## LIVE databases and private access

Databases can come in two forms — distinguish them by whether the resource ID contains `VINTAGE`:

- **LIVE** (current data): resource ID does **not** contain `VINTAGE` — e.g. `IMF.RES.WEO:WEO_LIVE`, `IMF.RES.GAS:GAS_LIVE`, `IMF.RES.GEE:GEE_LIVE`.
- **Vintage** (historical snapshot): resource ID contains `VINTAGE` — e.g. `IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE`.

Do **not** use `_LIVE_` as the sole discriminator — vintage resource IDs also contain this substring.

For WEO, use `IMF.RES.WEO:WEO_LIVE` by default. Historical observation dates
(e.g. 1980–2024) do not imply a historical release. Do not ask LIVE versus
vintage when the user has not requested a vintage. Honor an explicitly selected
alternative database.

If the user requests a specific vintage, resolve that exact release through the
catalog. If it is unavailable, explain the gap; never silently substitute a
nearby release or LIVE. If the user requests a vintage without identifying one,
ask which release; an explicit “latest vintage” request goes through catalog
vintage discovery, not the LIVE default.

All LIVE and vintage databases are private IMF datasets and require `idata_utilities.PRIVATE = True` before any retrieval call. The pre-built fetch utility ([scripts/fetch_idata.py](scripts/fetch_idata.py)) sets this flag automatically. See [references/imf_datatools_agent_api_reference.md § 3.1](references/imf_datatools_agent_api_reference.md) for details.

## EcOS retired policy

EcOS is retired. Do not execute EcOS discovery, metadata, mapping, or retrieval commands, including legacy wrappers that retrieve iData using EcOS identifiers. Resolve replacement identifiers through the catalog without executing legacy code.

Disallowed retrieval paths include (non-exhaustive):

- `get_ecos_sdmx_data`
- `get_ecos_gfs_data`
- `get_ecos_commodity_data`
- `get_ecos_bloomberg_data`
- `get_idata_data_using_ecos`

## Python-only scope

This skill's supported and tested time-series fetch workflow is Python-only through `fetch_idata.py` for iData and `fetch_haver.py` for Haver. Do not present R or Stata as a supported RA-skill retrieval path.

If the user explicitly asks for R or Stata code:

1. Acknowledge the requested language.
2. Explain that this RA skillset only validates the Python/iData workflow.
3. Provide the confirmed identifier tuple and supported `fetch_idata.py` command when possible.
4. Only provide R or Stata as an external, unvalidated sketch when the user explicitly asks to proceed outside the supported RA workflow, and label it clearly as unvalidated.

## iData fetch workflow

**This protocol is for iData sources only. For Haver sources, skip directly to [Haver Fetch](#haver-fetch).**

**Never create a new Python script to explore or fetch data.** A pre-built fetch utility already exists.

**Fast-path check:** Go directly to Step 7 only when the identifier, complete
dimension order, every required dimension selection, time range, and output
layout/container are already confirmed. Geography and frequency alone do not
resolve additional dataset dimensions. If any required input is unresolved,
follow the applicable steps below.

### Step 1 — Confirm the catalog handoff

If the identifier or `dimension_name` is missing, invoke **`imf-ra-catalog`** — do **not** search catalog files directly from this skill.

- **iData path:** the catalog uses `resolve "<query>" --json`. If it returns `status=resolved` with a `handoff` object (`database`, `dimension_name`, `code`), proceed to Step 2. If `status=ambiguous`, surface the clarification and wait.
- **Haver path:** the catalog uses the Haver Lookup Path (H1–H3: scope → build dblist → search → surface variants → confirm). An explicitly supplied `CODE@DB` may use the catalog's exact-code validation path. When the `codes` list is confirmed, skip Steps 2–7 entirely and go to [Haver Fetch](#haver-fetch).

If you are arriving from a confirmed catalog handoff, check its shape: `database + code` fields → Step 2; `codes` list → Haver Fetch.

### Step 2 — Read dimensions

Skip this step if the catalog handoff already confirms all dimension names and values (e.g. a full WEO handoff with `database`, `dimension_name`, `code`, `geo`, and `frequency` covers all three WEO dimensions: COUNTRY · INDICATOR · FREQUENCY).

When unresolved dimensions remain, list them in key order:

```bash
python "<DATA_SKILL>/scripts/fetch_idata.py" --db "<database_id>" --explore
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
python "<DATA_SKILL>/scripts/fetch_idata.py" --db "<database_id>" --dimension-values <DIM>
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

Before executing, ask for any missing output choice: layout (Refreshable, Wide, or Long) and, for Wide/Long, CSV versus Excel. A previously supplied complete choice is already confirmed; do not ask again. “Excel” or “CSV” alone does not determine the layout. Do **not** assume the missing choice.

Offer these choices:

- **Refreshable:** enriched `.xlsx` with indicator labels and country metadata
  where applicable. Layout is selected by data shape; see
  [output layouts](references/output-formats.md) for the exact contract.
- **Wide:** dates as rows and series as columns, saved as CSV or Excel.
- **Long:** one row per observation, saved as CSV or Excel.

Wide and Long preserve the API's basic layout, but the helper may rescale
values using metadata and adds `SCALE` and `UNIT` columns. They are not unchanged
API responses. Reuse a complete prior choice; ask only for a missing layout or
container choice.

### Step 7 — Execute with the pre-built fetch utility

Once all dimensions, time range, and output format are confirmed, call `fetch_idata.py` with the appropriate `--format` flag:

```bash
# Refreshable RA Excel (layout auto-selected by number of indicators).
# Always pass --indicator-dim using dimension_name from the catalog handoff (e.g. INDICATOR, TICKER, SERIES).
python "<DATA_SKILL>/scripts/fetch_idata.py" --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format refreshable --indicator-dim "<dimension_name>" --output "<OUTPUT_FILE>"

# Wide (CSV by default; add --excel for Excel)
python "<DATA_SKILL>/scripts/fetch_idata.py" --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format wide --output "<OUTPUT_FILE>"

# Long (CSV by default; add --excel for Excel)
python "<DATA_SKILL>/scripts/fetch_idata.py" --db "<database_id>" --key "<dot.separated.key>" --start "<YYYY>" --end "<YYYY>" --format long --output "<OUTPUT_FILE>"
```

Add `--excel` to save Wide or Long output as `.xlsx` instead of `.csv`. Always pass `--output` with the resolved user output path from the runtime contract.

For failures, follow the shared [recovery contract](../imf-ra/references/recovery.md). Do not wrap a helper that already retries in another retry loop. Report partial output as incomplete.

**`--indicator-dim`** — for refreshable output, pass the confirmed `dimension_name`
from the catalog handoff (e.g. `INDICATOR` for WEO, `TICKER` for BBG, `SERIES`
for WDI). IFS replacement datasets have their own dimensions; do not hardcode them.

**Always use this script — never return raw SDK output directly.**

For refreshable workbook structure and metadata, read
[output layouts](references/output-formats.md).

Continue to [Retrieval completion and chart handoff](#retrieval-completion-and-chart-handoff).

## Haver Fetch

When the catalog returns a `codes` list, pass those strings directly to
`fetch_haver.py --codes`.

### Step 1 — Confirm time range

The catalog already resolves the series. Confirm missing time range and output
choices before execution.

- Ask for `start` and `end` if missing.
- If the user wants more series, route back to `imf-ra-catalog`.

### Step 2 — Confirm output format

Use the same format-confirmation rule as iData Step 6: ask only for missing
layout/container choices, and preserve choices already supplied in the conversation.

### Step 3 — Execute with `fetch_haver.py`

```bash
python "<DATA_SKILL>/scripts/fetch_haver.py" --codes "GDP@USECON" "UNRATE@USECON" --start "<YYYY>" --end "<YYYY>" --format refreshable --output "<OUTPUT_FILE>"
```

```bash
python "<DATA_SKILL>/scripts/fetch_haver.py" --codes "GDP@USECON" --start "<YYYY>" --end "<YYYY>" --format wide --output "<OUTPUT_FILE>"
```

```bash
python "<DATA_SKILL>/scripts/fetch_haver.py" --codes "GDP@USECON" --start "<YYYY>" --end "<YYYY>" --format long --output "<OUTPUT_FILE>"
```

See [references/imf_datatools_agent_api_reference.md § 9](references/imf_datatools_agent_api_reference.md)
for the full Haver API reference.

Continue to [Retrieval completion and chart handoff](#retrieval-completion-and-chart-handoff).

## Retrieval completion and chart handoff

After either iData or Haver retrieval, use the original user request to
determine the next step:

- **Data only:** deliver the saved data and report any coverage limitations.
- **Chart or visualization requested:** retrieval is an intermediate step.
  Load [imf-ra-charts](../imf-ra-charts/SKILL.md) and its required references
  before writing plotting code, then continue through its chart workflow.

For chart requests, pass the existing output paths and available metadata,
preserving the requested countries, indicators or maturities, date range,
frequency, units, source, and any coverage gaps. Reuse the fetched data;
routine cleaning and reshaping belong in the chart skill's generated script.

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
python "<DATA_SKILL>/scripts/dealogic.py" search "<user concept>" --domain DCM
```

2. State the output grain and resolve every multi-table join:

```bash
python "<DATA_SKILL>/scripts/dealogic.py" joins DCMDeal DCMDealTranches
```

If direct relationships are ambiguous, add `--from-column <column>`.

3. Generate SQL Server syntax against `[Dealogic].[dbo]` using the patterns
   reference. Use explicit columns, `TOP (20)` or less, and selective
   date/key/status constraints where a transaction scan could be broad.

4. Validate and show the SQL, grain, joins, filters, confidence, and
   assumptions:

```bash
python "<DATA_SKILL>/scripts/dealogic.py" validate-sql --sql-file <query.sql>
```

5. Offer optional execution of the displayed query. After explicit user
   approval, verify the bounded preview:

```bash
python "<DATA_SKILL>/scripts/dealogic.py" verify --sql-file <query.sql> --confirmed
```

6. If verification fails, diagnose the error. Correct evidenced query defects
   and re-run `validate-sql`; retry execution only within the approved scope
   and the shared [recovery contract](../imf-ra/references/recovery.md).
   Live metadata inspection still requires user approval as described below.

7. Deliver the SQL with its execution status:
   - **Verified:** the delivered query executed successfully; state the preview
     scope and any limitations.
   - **Unverified:** execution was declined, unavailable, or unsuccessful.
     Deliver only SQL that passes `validate-sql`, label it as unverified, and
     disclose the reason, assumptions, and any unresolved execution error.
     Static validation is not proof of database correctness or data access.

The verifier permits one `SELECT` or `WITH ... SELECT`, rejects writes, DDL,
execution commands, `SELECT INTO`, and `SELECT *`, and enforces `TOP (20)` or
less with a short timeout.

When live-schema drift is suspected, inspect only the required table after
user approval:

```bash
python "<DATA_SKILL>/scripts/dealogic.py" inspect --table DCMDeal
```

Prefer `database_verified`, then `documented`, then disclosed `derived`
relationships. Never use `unverified` relationships. Present alternatives and
ask for confirmation when dates, amounts, roles, statuses, or domains remain
materially ambiguous.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, always use the exact dimension names returned by `--explore` — do not assume names like `COUNTRY`, `INDICATOR`, or `FREQUENCY`, as they vary by database (e.g. `REF_AREA`, `SERIES`, `FREQ`, `TICKER`).

---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetching IMF data series via the internal Python SDK.

## Skill relationships

Load these skills in order as needed:

- **`imf-ra`** (umbrella) — load first for shared conventions: country codes, WEO country groups, frequency handling, uncertainty policy, and SDK environment setup.
- **`imf-ra-catalog`** — load before this skill when the database or indicator is not yet identified. It translates plain-English descriptions into a confirmed `(database_id, indicator_code)` pair.
- **`imf-ra-data`** (this skill) — takes over once the identifier is confirmed. Resolves remaining dimensions, builds the iData key, and executes the fetch.
- **`imf-ra-charts`** — load after this skill when the user wants to visualize the tidy output.

## Default decision logic

1. Prefer `idata_utilities` for new IMF workflows.
2. Use metadata calls first whenever database/dimension/code values are unclear.
3. For WEO-style macroeconomic data, prefer an iData database whose resource ID starts with `WEO_LIVE` before published/static WEO alternatives.
4. If the user asks for EcOS-based retrieval, explain that EcOS is retired and provide the iData equivalent workflow.

## LIVE databases and private access

When the catalog locates a database family that has both a LIVE version and historical vintages (resource ID contains `_LIVE_`, e.g. `WEO_LIVE`, `GAS_LIVE`, `GEE_LIVE`):

- **If the user specified a vintage** (even loosely, e.g. "April 2024" or "the Oct 2023 release"), match it to the nearest vintage and proceed — no need to ask again.
- **If the user did not specify a vintage**, inform them that a LIVE version is available and also state the latest historical vintage, then ask which they want before proceeding.

LIVE databases are private IMF datasets and require `idata_utilities.PRIVATE = True` before any retrieval call. The pre-built fetch utility ([scripts/fetch_idata.py](scripts/fetch_idata.py)) sets this flag automatically. For any inline Bash `idata_utilities` call, set it first. See [references/imf_datatools_agent_api_reference.md § 3.1](references/imf_datatools_agent_api_reference.md) for details.

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

**Never create a new Python script to explore or fetch data.** A pre-built fetch utility already exists. Follow these five steps every time.

### Step 1 — Catalog lookup

If the `(database_id, indicator_code)` pair is not yet confirmed, invoke **`imf-ra-catalog`** to resolve it. Do **not** search catalog files directly from this skill — all indicator and database discovery is owned by `imf-ra-catalog`.

If you are arriving from a catalog handoff with a confirmed identifier, skip directly to Step 2.

### Step 2 — Read dimensions via the API

Once the database is confirmed, fetch every dimension and its valid codes via the SDK:

```python
from imf_datatools import idata_utilities
dims = idata_utilities.get_dimensions("<database_id>")
```

See [references/dimension-resolution-guide.md](references/dimension-resolution-guide.md) for the full lookup sequence and how to use the results to resolve and present dimension choices.

### Step 3 — Identify unresolved dimensions

Compare what the user specified against the dimensions returned by the API. Required inputs for a complete iData key:

- `start` / `end` — time range
- one value per dimension (e.g. `COUNTRY`, `INDICATOR`, `DATA_TRANSFORMATION`, `FREQUENCY`) — exact names vary by database

Dimensions with exactly **one** valid value in the API response are auto-resolved silently. Everything else that the user has not specified must be asked.

### Step 4 — Ask for missing dimensions

Present what you found (database, indicator) and ask the user to supply the missing values. Show the valid codes and their labels from the API response — do not list codes from memory or training knowledge. One question block per unresolved dimension.

See [references/dimension-resolution-guide.md](references/dimension-resolution-guide.md) for the reply template.

If the user asks "what does X mean?" or "what options are there for Y?", answer from the API response values.

### Step 5 — Execute with the pre-built fetch utility

Once all dimensions are resolved, build the iData key and call `fetch_idata.py` via Bash:

```bash
python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
    --db "<database_id>" \
    --key "<dot.separated.key>" \
    --start "<YYYY>" \
    --end "<YYYY>"
```

Default output: wide RA Excel (`.xlsx`) with headers `CountryName | ISO3 | IFSCODE | DATASET | Series_Code | INDICATOR | <date columns>`. Date column format: `2019` (annual), `2019Q1` (quarterly), `2019M1` (monthly). `CountryName` and `IFSCODE` are looked up from the RA catalog `countries.csv` using the ISO3 code in the COUNTRY dimension.

Use `--longformat` to save raw long/tidy CSV instead. See [references/dimension-resolution-guide.md](references/dimension-resolution-guide.md) for key construction rules and output format details.

## Before you fetch

Always load **`imf-ra`** first for shared conventions:

- **Country and group codes** — translate RA-friendly names ("advanced economies", "EMDE", "G7") through the WEO group reference in `imf-ra`, not from memory.
- **Frequencies** — follow standard frequency codes (`A`, `Q`, `M`) and date-handling rules in [imf-ra/references/conventions.md](../imf-ra/references/conventions.md).
- **Uncertainty policy** — if there is any material uncertainty about country selection, date range, or series choice, ask the user before fetching.
- **SDK environment setup** — PRIVATE flag and environment configuration are covered in [imf-ra/references/conventions.md](../imf-ra/references/conventions.md).

## How to fetch

See [references/imf_datatools_agent_api_reference.md](references/imf_datatools_agent_api_reference.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

Invoke `imf-ra-catalog` first to translate the user's description into a confirmed `(database_id, indicator_code)`. Return here once the identifier is confirmed and proceed from CLI fetch Step 2.

## After catalog handoff

When `imf-ra-catalog` returns a confirmed identifier:

- `database_name` is the iData database identifier; use it in Step 2 of the CLI fetch protocol to fetch dimensions via the API.
- `indicator_code` is the confirmed indicator dimension value; slot it into its position when building the key.
- `indicator_name` explains unit, valuation, transformation, and price basis; use it to phrase follow-up questions when candidates differ.
- For WEO candidates, keep `WEO_LIVE` as the priority family, then confirm vintage if the user has not already done so.
- Resolve all remaining dimensions via the CLI fetch protocol (Steps 2–4) before calling `fetch_idata.py`.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- For large requests, iterate over countries/indicators/frequencies and merge results.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, use canonical labels from metadata (for example `COUNTRY`, `INDICATOR`, `FREQUENCY`).

## Output convention

Return a tidy DataFrame (one observation per row) with period-start time semantics and at minimum `geo`, `time`, `value`, plus series-identifying columns (`database`, `series`, `freq`, counterparts) where available. Downstream charting depends on this shape.

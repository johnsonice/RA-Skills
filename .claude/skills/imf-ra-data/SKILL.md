---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA - Data

Fetching IMF data series via the internal Python SDK.

## Before You Fetch

See the umbrella `imf-ra` for shared conventions: country codes, frequencies, dates, units, and SDK environment setup.

If the request includes WEO groups, regions, or informal country wording, normalize coverage through the umbrella WEO country-group reference before writing retrieval code. For selected-country iData pulls, prefer ISO-style WEO `countrycode` values such as `USA`, `CHN`, and `JPN` unless target dataset metadata requires another value.

## Frequencies

- Use the frequency labels exposed by iData metadata. Common values are annual `A`, quarterly `Q`, monthly `M`, and daily `D`, but validate exact dimension values for the selected database.
- WEO Live macro data is generally annual. Do not promise quarterly or monthly WEO data unless metadata confirms it.
- Keep period labels in the SDK/native format during retrieval. Convert only after fetching, and document the conversion in the output.
- Do not aggregate or disaggregate frequency unless the user asks for it and the method is clear.

## Dates

- Treat phrases like `2010-present` as `start=2010` with no explicit end unless the user provides one.
- Separate data-period dates from vintage/release dates. A WEO vintage such as `2026 APR` identifies the database snapshot, not the observation period.
- If the user asks for `latest`, confirm whether they mean the latest WEO vintage, latest available observation, or latest forecast horizon when that distinction matters.

## Units

- Preserve the units and scale returned by metadata or attributes. Do not rescale silently.
- Common IMF units include national currency, U.S. dollars, percent change, percent of GDP, index values, and per capita measures.
- When candidates differ by unit, valuation, scale, or transformation, ask the user to choose before fetching.

## Default decision logic

1. Prefer `idata_utilities` for new IMF workflows.
2. Use metadata calls first whenever database/dimension/code values are unclear.
3. For WEO-style macroeconomic data, prefer an iData database whose resource ID starts with `WEO_LIVE` before published/static WEO alternatives.
4. If the user asks for EcOS-based retrieval, explain that EcOS is retired and provide the iData equivalent workflow.

## WEO Live priority

For WEO concepts, `WEO_LIVE` is the first-priority database family. This is a source-family preference, not an instruction to silently choose the newest vintage every time.

- Prefer `IMF.RES.WEO:<WEO_LIVE_..._VINTAGE>` over non-live WEO datasets when both contain the requested indicator.
- If the user specifies a vintage, exercise, or database, honor that choice after validating that the requested indicator exists there.
- If the user does not specify a vintage, ask whether they want the current/latest available WEO Live vintage or a specific historical vintage before writing the final retrieval code.
- When a catalog result contains a concrete `database_name` such as `IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE`, treat it as a candidate, not an irrevocable choice, unless the user has already confirmed the vintage.
- Use non-WEO databases when the concept is clearly outside WEO coverage, such as commodity prices in GAS or high-frequency CPI in IFS/STA.

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

## Clarify brief requests first

If the user's data request is too brief or ambiguous, ask concise follow-up questions before writing retrieval code.

This requirement also applies to quick exploratory or smoke-test requests: do not skip clarification just because the pull is intended as a small trial.

For data pulls, confirm at least:

- time range (`start`, `end`, or vintage)
- coverage (single country, explicit country list, or country group); this can be omitted only when the request is not country-specific or cross-country
- concept/indicator/series selection
- frequency (`A`, `Q`, `M`, `D`)
- output shape preference (wide vs `longformat=True`; default to wide if not specified)

If one or more items are missing, do not guess silently. Ask for the missing pieces first, then proceed.

## How to fetch

See [references/imf_datatools_agent_api_reference.md](references/imf_datatools_agent_api_reference.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

See `imf-ra-catalog` first to translate the user's description into `(database, series, frequency, geo)`. Only then write the SDK call.

## After catalog handoff

When `imf-ra-catalog` returns CSV-backed candidates:

- `database_name` is the iData database identifier to validate with metadata calls.
- `indicator_code` is the candidate indicator dimension value.
- `indicator_name` explains unit, valuation, transformation, and price basis; use it to ask follow-up questions when candidates differ.
- For WEO candidates, keep `WEO_LIVE` as the priority family, then confirm vintage if the user has not already done so.
- Before fetching, validate the database dimensions and the exact indicator code with `idata_utilities.get_dimensions()` and `idata_utilities.get_dimension_values()`.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- For large requests, iterate over countries/indicators/frequencies and merge results.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, use canonical labels from metadata (for example `COUNTRY`, `INDICATOR`, `FREQUENCY`).

## Output convention

Return a tidy DataFrame (one observation per row) with period-start time semantics and at minimum `geo`, `time`, `value`, plus series-identifying columns (`database`, `series`, `freq`, counterparts) where available. Downstream charting depends on this shape.

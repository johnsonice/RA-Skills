---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetching IMF data series via the internal Python SDK.

## Default decision logic

1. Prefer `idata_utilities` for new IMF workflows.
2. Use metadata calls first whenever database/dimension/code values are unclear.
3. If the user asks for EcOS-based retrieval, explain that EcOS is retired and provide the iData equivalent workflow.

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
- coverage (single country, explicit country list, country groups);if it is not  a cross-country panel request, then this field is optional
- concept/indicator/series selection
- frequency (`A`, `Q`, `M`, `D`)
- output shape preference (wide vs `longformat=True`; default to wide if not specified)

If one or more items are missing, do not guess silently. Ask for the missing pieces first, then proceed.

## Before you fetch

See the umbrella `imf-ra` for shared conventions: country codes, frequencies, dates, and SDK environment setup.

## How to fetch

See [references/imf_datatools_agent_api_reference.md](references/imf_datatools_agent_api_reference.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

See `imf-ra-catalog` first to translate the user's description into `(database, series, frequency, geo)`. Only then write the SDK call.

## Safe query policy

- Avoid broad `ALL` pulls unless explicitly requested.
- For large requests, iterate over countries/indicators/frequencies and merge results.
- Validate dimension names and values with metadata calls before retrieval.
- For iData dimensions, use canonical labels from metadata (for example `COUNTRY`, `INDICATOR`, `FREQUENCY`).

## Output convention

Return a tidy DataFrame (one observation per row) with period-start time semantics and at minimum `geo`, `time`, `value`, plus series-identifying columns (`database`, `series`, `freq`, counterparts) where available. Downstream charting depends on this shape.

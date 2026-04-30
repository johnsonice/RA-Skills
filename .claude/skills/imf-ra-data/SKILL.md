---
name: imf-ra-data
description: Use when the user wants to fetch, pull, download, or load IMF data series from any database (WEO, IFS, BOPS, GFS, DOTS, FSI, etc.) using the internal Python SDK. Covers single-series and multi-country panel pulls, frequency conversion, and country selection. See imf-ra for shared conventions.
---

# IMF RA — Data

Fetching IMF data series via the internal Python SDK.

## Before you fetch

See the umbrella `imf-ra` for shared conventions: country codes, frequencies, dates, and SDK environment setup.

## How to fetch

See [references/sdk-usage.md](references/sdk-usage.md) for SDK call patterns and common recipes.

## When you don't know the series identifier

See `imf-ra-catalog` first to translate the user's description into `(database, series, frequency, geo)`. Only then write the SDK call.

## Output convention

Return a tidy DataFrame (one observation per row, with `geo`, `time`, `value`, and any series-identifying columns). Downstream charting depends on this shape.

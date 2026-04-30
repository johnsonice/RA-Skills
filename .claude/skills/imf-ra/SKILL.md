---
name: imf-ra
description: Use when working as an IMF Research Assistant or doing any task involving IMF data, IMF charts, or IMF databases. Orients you to the imf-ra-data, imf-ra-charts, and imf-ra-catalog skills and loads shared conventions for country codes, frequencies, dates, units, and SDK setup.
---

# IMF RA

Family entry point for IMF Research Assistant workflows. Loads shared conventions and routes to the right worker skill.

## Family map

- **`imf-ra-data`** — fetching data via the internal Python SDK. Use when the user wants to pull, download, or load series.
- **`imf-ra-charts`** — handing tidy data to the internal charting tool. Use when the user wants to plot, chart, or visualize.
- **`imf-ra-catalog`** — translating plain-English descriptions into a `(database, series, frequency, geo)` identifier. Use when the user is searching for the right indicator.

## Shared conventions

Before fetching, charting, or searching, see [references/conventions.md](references/conventions.md) for country codes, frequency conventions, date handling, and SDK environment setup.

## Workflow notes

- The umbrella does not orchestrate workflows. Workers chain by referencing each other directly.
- When `imf-ra-charts` needs data, it loads `imf-ra-data` in the same turn rather than sending the user away.
- When the catalog returns ambiguous matches, surface candidates with notes — do not commit to one without RA confirmation.

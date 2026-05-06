---
name: imf-ra
description: Use when working as an IMF Research Assistant or doing any task involving IMF data, IMF charts, or IMF databases. Orients you to the imf-ra-catalog, imf-ra-data, and imf-ra-charts skills and loads shared conventions for country codes, frequencies, dates, units, and SDK setup.
---

# IMF RA

Family entry point for IMF Research Assistant workflows. Loads shared conventions and routes to the right worker skill.

## Family map

Recommended sequence: `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` -> `imf-ra-charts`.

- **`imf-ra-catalog`** — translating plain-English descriptions into a `(database, series, frequency, geo)` identifier. Use when the user is searching for the right indicator.
- **`imf-ra-data`** — fetching data via the internal Python SDK. Use when the user wants to pull, download, or load series.
- **`imf-ra-charts`** — handing tidy data to the internal charting tool. Use when the user wants to plot, chart, or visualize.


## Shared conventions

Before fetching, charting, or searching, see [references/conventions.md](references/conventions.md) for country codes, frequency conventions, date handling, and SDK environment setup.

For WEO country groups, WEO aggregates, WEO regions, Group A/A+, iData group dummies, or old WEO group codes, use [references/Country Group/weo-country-groups.md](references/Country%20Group/weo-country-groups.md). The CSV files under `references/Country Group/csv/` are the source of truth for exact country membership and code mappings.

For straightforward questions that can be answered by directly inspecting the reference CSV files, answer from the CSV contents without generating Python code. Use Python only when it is genuinely needed, such as for aggregation, calculation, joins across multiple files, repeated filtering, ambiguous lookup resolution, or other nontrivial data processing.

If there is material uncertainty, do not guess. Ask the user for confirmation before committing to one interpretation, code, group, or dataset choice. If several plausible best matches exist, list the candidates and ask for user preference/confirmation.

Optional helper for repeated or ambiguous WEO group lookups:

```bash
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py groups "advanced economies"
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py memberships USA
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py group-a
```

## Workflow notes

- The umbrella does not orchestrate workflows. Workers chain by referencing each other directly.
- When `imf-ra-charts` needs data, it loads `imf-ra-data` in the same turn rather than sending the user away.
- When the catalog returns several plausible matches, surface candidates with notes and ask for RA confirmation before committing.
- When answering WEO country-group questions, do not rely on memory. Load the WEO reference markdown for schema and policy, then inspect the CSV files for exact groups, countries, and memberships. Use the helper script only when it makes an ambiguous, repeated, or processing-heavy lookup more reliable.

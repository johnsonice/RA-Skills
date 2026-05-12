---
name: imf-ra
description: Use when working as an IMF Research Assistant or doing any task involving IMF data, IMF charts, or IMF databases. Orients you to the imf-ra-catalog, imf-ra-data, and imf-ra-charts skills and loads shared conventions for country codes, frequencies, dates, units, and SDK setup.
---

# IMF RA

Family entry point for IMF Research Assistant workflows. Loads shared conventions and routes to the right worker skill.

## Family map

Recommended sequence: `imf-ra` -> `imf-ra-catalog` -> `imf-ra-data` -> `imf-ra-charts`.

- **`imf-ra-catalog`** - translating plain-English descriptions into a `(database, series, frequency, geo)` identifier. Use when the user is searching for the right indicator.
- **`imf-ra-data`** - fetching data via the internal Python SDK. Use when the user wants to pull, download, or load series.
- **`imf-ra-charts`** - handing tidy data to the internal charting tool. Use when the user wants to plot, chart, or visualize.


## Shared conventions

Before fetching, charting, or searching, see [references/conventions.md](references/conventions.md) for country codes, frequency conventions, date handling, and SDK environment setup.

For WEO country groups, WEO aggregates, WEO regions, and WEO country codes, use [references/Country Group/weo-country-groups.md](references/Country%20Group/weo-country-groups.md). The CSV files under `references/Country Group/csv/` are the source of truth for exact country membership and code mappings.

For straightforward questions that can be answered by directly inspecting the reference CSV files, answer from the CSV contents without generating Python code. Use Python only when it is genuinely needed, such as for aggregation, calculation, joins across multiple files, repeated filtering, ambiguous lookup resolution, or other nontrivial data processing.

Before using the WEO country-group helper script, do a source-aligned fuzzy-matching pass in reasoning. The goal is to improve the helper query by mapping the user's wording to the closest term already supported by the skill's WEO reference material, not to invent new country or group logic. See [references/Country Group/weo-country-groups.md](references/Country%20Group/weo-country-groups.md) for the full lookup policy.

- Ground the match in existing skill information: `references/Country Group/weo-country-groups.md`, `references/Country Group/csv/1. countries.csv`, `references/Country Group/csv/2. country_groups.csv`, `references/Country Group/csv/3. country_group_composition.csv`, and documented RA/WEO shorthand.
- Convert the user's phrase to the best canonical WEO query before running code: prefer `countrycode` values such as `USA` or `CHN`, `groupcode` values such as `G110` or `G200`, or exact canonical English country/group names from the CSV files.
- Resolve only aliases that are clearly supported by the reference content or standard RA wording, for example `United States`, `US`, or `America` -> `USA`; `mainland`, `mainland China`, or `China mainland` -> `CHN`; `advanced economies` or `AE` -> `G110`.
- Treat the helper script as a lookup accelerator after normalization. Do not pass raw informal text directly to the script when a better canonical query can be inferred from the skill files.
- Never run the helper with an empty, non-ASCII-only, or otherwise unnormalized query. If the user phrase is non-English, translate or interpret it into an English canonical candidate first.
- If two or more candidates are plausible, list the candidates with codes and ask for confirmation before running the helper or committing to an answer.

If there is material uncertainty, do not guess. Ask the user for confirmation before committing to one interpretation, code, group, or dataset choice. If several plausible best matches exist, list the candidates and ask for user preference/confirmation.

Optional helper for repeated or ambiguous WEO group lookups:

```bash
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py groups "advanced economies"
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py memberships USA
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py countries CHN
```

## Workflow notes

- The umbrella does not orchestrate workflows. Workers chain by referencing each other directly.
- When `imf-ra-charts` needs data, it loads `imf-ra-data` in the same turn rather than sending the user away.
- When the catalog returns several plausible matches, surface candidates with notes and ask for RA confirmation before committing.
- When answering WEO country-group questions, do not rely on memory. Load the WEO reference markdown for schema and policy, then inspect the CSV files for exact groups, countries, and memberships. Use the helper script only when it makes an ambiguous, repeated, or processing-heavy lookup more reliable.
- For iData country selections, prefer WEO `countrycode` values such as `USA` and `CHN` unless metadata for a specific dataset says otherwise.

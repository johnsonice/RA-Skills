---
name: imf-ra
description: Use when working as an IMF Research Assistant or doing any task involving IMF data, IMF charts, or IMF databases. Orients you to the imf-ra-catalog, imf-ra-data, and imf-ra-charts skills and loads shared conventions for country codes, WEO country groups, frequencies, dates, units, and SDK setup.
---

# IMF RA

Family entry point for IMF Research Assistant workflows. Use this skill to load shared conventions and route the task to the right worker skill.

## Skill Map

Recommended sequence:

```text
imf-ra -> imf-ra-catalog -> imf-ra-data -> imf-ra-charts
```

| Skill | Use when |
|---|---|
| `imf-ra-catalog` | The user needs the right dataset, dimension, indicator, variable, commodity, or ticker code. |
| `imf-ra-data` | The user wants to fetch, pull, download, load, or prepare data from a confirmed identifier. |
| `imf-ra-charts` | The user wants to plot, chart, or visualize tidy data. |

The umbrella does not execute the full workflow by itself. Worker skills chain by referencing each other directly.

## Shared Operating Rules

- Use reference CSVs as the source of truth for identifiers, codes, group membership, and catalog lookup.
- Do not rely on memory for database IDs, indicator codes, WEO groups, country membership, or iData dimensions.
- Do not guess when there is material uncertainty. List plausible candidates and ask for confirmation.
- For straightforward questions that can be answered by direct file inspection, answer from the files without writing code.
- Use helper scripts only when they improve reliability for repeated filtering, fuzzy lookup, joins, aggregation, or other nontrivial processing.
- For data pulls, confirm the time range and required unresolved dimensions in `imf-ra-data`; do not assume missing dates or dimension values.
- Follow standard frequency codes when needed: annual `A`, quarterly `Q`, monthly `M`, and daily `D`, unless dataset metadata uses a different convention.

## WEO Country And Group Rules

For WEO countries, WEO country groups, WEO aggregates, WEO regions, and informal RA group names, use [references/Country Group/weo_country_groups.md](references/Country%20Group/weo_country_groups.md).

The CSV files under `references/Country Group/csv/` are the source of truth:

| File | Use |
|---|---|
| `1. countries.csv` | Country code, country name, and department lookup. |
| `2. country_groups.csv` | Group code, group name, group type, and group alias lookup. |
| `3. country_group_composition.csv` | Exact group membership and country-to-group membership lookup. |

Important iData pull rule: do not use `groupcode` or `groupcode_s` as the country selector in iData pulls. Resolve groups to member `countrycode` values first, or use a dataset-supported aggregate code only when metadata confirms it is valid.

## WEO Lookup Policy

Before using the WEO country-group helper script, normalize the user's wording to the closest supported WEO reference term.

- Prefer exact `countrycode` values such as `USA`, `CHN`, and `JPN` for selected-country requests.
- Prefer canonical WEO `groupcode` values such as `G110` or `G200` only for group lookup and membership mapping, not for iData pulls.
- Resolve only aliases clearly supported by the WEO reference, such as `United States`, `US`, or `America` -> `USA`; `mainland China` -> `CHN`; `advanced economies` or `AE` -> `G110`.
- If the user mentions EM, LIC, LIDC, PRGT, or developing-economy coverage without specifying WEO vs SPR, ask for clarification. WEO and SPR/PRGT group membership can differ.
- If two or more country or group matches are plausible, list the candidates with codes and ask for confirmation before committing.

## Helper Commands

Use the helper only for ambiguous, repeated, or processing-heavy WEO country-group lookup.

```bash
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py groups "advanced economies"
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py countries CHN
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py memberships USA
```

## Handoff Notes

- When the user is still searching for the right series, route to `imf-ra-catalog`.
- When the identifier is confirmed, route to `imf-ra-data` and preserve confirmed `database`, `dimension_name`, `code`, geography, frequency, date range, and vintage constraints.
- When the user asks for charts, route to `imf-ra-charts` after data are available or after `imf-ra-data` produces tidy output.
- When the catalog returns several plausible matches, present the candidates with distinction notes and ask for confirmation before fetching.

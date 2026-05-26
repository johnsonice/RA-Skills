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
- For data pulls, confirm the time range and required unresolved dimensions in `imf-ra-data`; do not assume missing dates or dimension values.
- Follow standard frequency codes when needed: annual `A`, quarterly `Q`, monthly `M`, and daily `D`, unless dataset metadata uses a different convention.

## Integrated Lookup Execution Policy

1. `Classify the Task Shap`
Analyze the input query and classify its shape: exact lookup, fuzzy lookup, membership expansion, comparison, handoff preparation, validation, or data-pull setup.
2. `Micro-Lookup Shortcut (Exact Matches)`
Answer directly from the reference CSV/Markdown only for exact, single-record, small lookups that require zero processing or computation.
3. `Enforce Search-First Architecture (Mandatory Check)`
For fuzzy, repeated, comparative, expansion, validation, or data-pull tasks, you are strictly prohibited from writing code immediately. You MUST first inspect the available helper command map / tool list.Rule of Thumb: Treat existing helper commands as your preferred actions. Improvised code is a last-resort liability.
4. `Resolve Ambiguities`
 Prior to ExecutionResolve ambiguous terms before running any helper. If multiple plausible matches exist within the reference data, list candidates with their official codes and ask the user for confirmation before committing.
5. `Prioritize Specific Helpers Over Custom Logic`
Use the most specific existing helper command for the task. If a helper handles $90\%$ of the requirement, call the helper first, catch its structured output, and then perform minor downstream formatting. Never rewrite a function from scratch just to alter a minor output style.
6. `Strict Gatekeeping for Temporary Code (Expand Privately)`
You are permitted to write temporary, single-use code ONLY under the following strict conditions:
-No existing helper command (or combination of helper commands) covers the core data-retrieval task.
-The task requires highly customized data visualization (e.g., specialized matplotlib/seaborn plots) or ad-hoc data cleansing unique to this specific query.
-The temporary code must be executing within its isolated sandbox session and will be destroyed immediately after fulfilling the current query.
7. `Enforce Output Determinism & Validation`
Ensure that any executed helper or temporary pattern returns structured data (e.g., CSV formats, JSON strings, or typed dataframes). Validate that column names and index structures match the downstream expectations exactly.
8. `Continuous Skill Evolution (Promotion Rule)`
If a temporary-code pattern or workflow appears repeatedly across different sessions, do not let it clutter the environment. Document the pattern and flag it to be promoted into a permanent, parameterized helper command later.

## WEO Country And Group Conventions

For WEO countries, WEO country groups, WEO aggregates, WEO regions, and informal RA group names, use [references/Country Group/weo_country_groups.md](references/Country%20Group/weo_country_groups.md). That reference owns the WEO country/group code systems, source tables, helper command map, aliases, EM/LIC/PRGT caveats, and iData country-selector rules.

For WEO country/group tasks involving ambiguity, membership expansion, comparison, or iData handoff, open the WEO reference and use its helper command map before writing temporary code.

## Handoff Notes

- When the user is still searching for the right series, route to `imf-ra-catalog`.
- When the identifier is confirmed, route to `imf-ra-data` and preserve confirmed `database`, `dimension_name`, `code`, geography, frequency, date range, and vintage constraints.
- When the user asks for charts, route to `imf-ra-charts` after data are available or after `imf-ra-data` produces tidy output.
- When the catalog returns several plausible matches, present the candidates with distinction notes and ask for confirmation before fetching.

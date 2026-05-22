---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English, such as "current account balance for advanced economies, quarterly", and needs the right dataset, dimension, and variable code. Returns top candidates with clear notes when requests are ambiguous.
---

# IMF RA Catalog

Use this skill to translate a research request into a stable catalog identifier tuple:

```text
(database, dimension_name, code)
```

The catalog identifies datasets, dataflows, dimensions, and indicator codes. It does not fetch data. After an identifier is confirmed, hand off to `imf-ra-data` for execution.

## Scope

Use this skill when the user needs to:

- Select the most appropriate IMF, World Bank, WTO, Bloomberg, or related dataset.
- Map a plain-English concept to a dataset-specific variable or indicator code.
- Resolve ambiguity between similar indicators, transformations, units, dimensions, or database families.
- Identify the latest non-vintage dataset or an explicitly requested vintage dataset.

Do not use this skill to fetch data, transform time series, or build charts. Those tasks belong to downstream skills.

## Required Context

Before lookup, load shared RA conventions from the umbrella `imf-ra` skill when the request involves country codes, WEO country groups, frequency conventions, dates, units, or downstream fetch behavior.

For WEO regions, country groups, aggregates, and informal country names, normalize geography through the umbrella WEO country-group references before selecting variables or handing off to `imf-ra-data`.

## Reference Files

The CSV files are the source of truth for identifiers. Markdown files provide curated interpretation and selection guidance.

### Dataset Catalogs

| File | Purpose |
|---|---|
| `databases/non_vintage_datasets.csv` | Default dataset and dataflow catalog for non-vintage lookup. |
| `databases/vintage_datasets.csv` | Vintage-only dataset and dataflow catalog. Use only for explicit vintage or historical-release requests. |
| `databases/database_overview.md` | High-level summaries of major database families, coverage, and common use cases. |

### Indicator Catalogs

| File | Purpose |
|---|---|
| `indicators/1. non_vintage_variable_list.csv` | General non-vintage variable catalog. Use for ordinary variable and code discovery. |
| `indicators/2. bbg_variable_list.csv` | Bloomberg variable catalog. Use when the user requests Bloomberg or `IMF.CSF:BBGDL`. |
| `indicators/3. wdi_variable_list.csv` | World Bank WDI variable catalog. Use when the user requests WDI or `WB:WDI`. |
| `indicators/4. wto_variable_List.csv` | WTO variable catalog. Use when the user requests WTO goods, tariff, or commodity codes. |

### Maintenance Reference

| File | Purpose |
|---|---|
| `references/catalog_schema_and_maintenance.md` | CSV column schemas and catalog maintenance conventions. Not needed for ordinary lookup unless schema details are unclear. |

## Default Selection Policy

1. Default to non-vintage datasets.
2. Use vintage datasets only when the user explicitly asks for a vintage, historical publication, dated snapshot, or versioned release.
3. For WEO-style macroeconomic concepts, begin with non-vintage `IMF.RES.WEO:WEO_LIVE` unless the user asks for another source or the concept is clearly outside WEO coverage.
4. Do not silently replace non-vintage `WEO_LIVE` with a dated WEO vintage. If the user asks for a WEO vintage but does not specify one, ask whether they want the latest available WEO Live vintage or a specific historical vintage.
5. Search all databases only when WEO Live, GAS Live, and other highlighted databases in `database_overview.md` lack a plausible match, the user explicitly asks for another database family, or the concept is clearly outside WEO coverage.
6. Use database-specific indicator files for Bloomberg, WDI, and WTO requests rather than the general non-vintage variable list.

## Legacy IFS Requests

For background on IFS migration and replacement topic coverage, see `databases/database_overview.md`.

When a user asks for "IFS" data:

1. Treat `IFS` as a legacy source hint, not as the target database.
2. Run `scripts/catalog_search.py explain-source "<request>"` to identify the replacement topic database.
3. Search the routed replacement database for the exact `dimension_name` and `code`.
4. In the result, explicitly name the replacement database where the required indicator was found.

For IFS requests, include an IFS migration note in the final answer. Example:

```text
Note: IFS no longer exists as a single iData dataset. For this legacy IFS CPI request, the matching indicator is in the replacement iData topic database:
database: IMF.STA:CPI
dimension_name: <dimension>
code: <code>
name: <name>
```

## Task Shape Routing

Before choosing files, helper commands, or temporary code, classify the catalog task shape:

| Task shape | Examples | Preferred action |
|---|---|---|
| Exact small lookup | "What is `NGDP_RPCH`?", "What database is `IMF.RES.WEO:WEO_LIVE`?" | Use `catalog_search.py code` or `classify-database`, or answer directly from the relevant CSV/Markdown row. |
| Fuzzy indicator lookup | "real GDP growth", "nominal GDP in USD", "bank capital adequacy" | Use `catalog_search.py search` or `resolve` before writing code. |
| Source routing | "IFS CPI", "World Bank GDP per capita", "Bloomberg 10-year yield" | Use `catalog_search.py resolve` when an indicator is needed, or `explain-source` when only the source route is needed. |
| Dimension discovery | "What dimension does CPI use?", "Is WDI `SERIES` or `INDICATOR`?" | Use `catalog_search.py dimensions` and preserve the returned `dimension_name`. |
| Variant comparison | "WEO inflation vs CPI", "PCPI_PCH vs PCPIE_PCH" | Use `catalog_search.py compare-codes`, compare unit/transformation/basis, and ask if the intended variant is unclear. |
| Vintage classification | "latest WEO data", "April 2024 WEO vintage", "`*_VINTAGE`" | Use `resolve` for vintage indicator requests, `datasets --vintage-only` for listing vintages, and `classify-database` for exact database checks. |
| Handoff preparation | "find the code and download it", "use this for iData" | Use `resolve`; hand off only when it returns `status=resolved` and a `handoff` object. |
| Validation | "does this code exist?", "is this database live or vintage?" | Validate against the source CSVs or the most specific helper command. |

Decision rules:

1. Answer directly from reference CSV/Markdown only for exact, small lookups.
2. For fuzzy, repeated, comparative, source-routing, validation, vintage, or handoff tasks, use the most specific `scripts/catalog_search.py` command before writing code.
3. Resolve ambiguous terms before committing to a result. If multiple plausible matches exist, list candidates with codes and ask for confirmation.
4. Write temporary code only when no helper command covers the task.
5. If a temporary-code pattern appears repeatedly, promote it into `scripts/catalog_search.py`.

## Lookup Workflow

1. **Classify the task shape.** Decide whether the request is an exact lookup, fuzzy indicator lookup, source-routing question, variant comparison, vintage classification, validation, or handoff preparation.
2. **Parse the request.** Identify the concept, preferred database, unit, transformation, frequency, geography, and vintage requirement when available.
3. **Select a dataset.** Use `non_vintage_datasets.csv` by default, `vintage_datasets.csv` only for explicit vintage requests, and `database_overview.md` for high-level source selection.
4. **Select the indicator file.** Choose the general non-vintage indicator list or the specific Bloomberg, WDI, or WTO list based on the dataset family.
5. **Find candidate codes.** Search within the selected indicator file for exact names, close wording, aliases, and source-specific terminology.
6. **Preserve dimensions.** Always carry through `dimension_name`; do not assume the code dimension is `INDICATOR`.
7. **Resolve ambiguity.** Compare candidates by unit, transformation, valuation, frequency, price basis, and database coverage.
8. **Return the result.** Commit to a single identifier only when the match is exact and unambiguous. Otherwise, return a short candidate list and ask for confirmation.

## Helper Responsibility

Use `scripts/catalog_search.py` as the operational lookup engine for catalog work. The helper owns mechanical lookup tasks that are easy to get wrong by hand:

- Route plain-English requests to the right source family: WEO Live, WEO vintage, legacy IFS replacement topic databases, WDI, Bloomberg, WTO, or broad all-database search.
- Select the right indicator catalog file for the routed database.
- Reuse WEO Live indicator metadata for WEO vintage databases while preserving the requested vintage database in output.
- Rank fuzzy candidates across large CSVs using catalog terminology and synonym expansion.
- Preserve `dimension_name`; never assume all databases use `INDICATOR`.
- Stop on ambiguity and return candidate records plus a clarification prompt.
- Assemble a handoff-ready payload with `database`, `dimension_name`, `code`, `name`, and notes when `resolve` can safely commit.

The helper does not fetch data, expand country groups, choose date ranges, transform series, or build charts. Those responsibilities belong to `imf-ra-data`, the umbrella WEO country-group helper, or `imf-ra-charts`.

Inspect CSV and Markdown files directly only for exact one-row confirmation, schema questions, or curated database guidance. Use helper commands for broad search, fuzzy ranking, source routing, validation, explicit vintage handling, or any lookup over large indicator catalogs.

Before using `scripts/catalog_search.py`, map the user's wording to terminology that appears in the catalog. The helper should accelerate a source-aligned lookup, not invent indicator logic.

Common helper commands:

```bash
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py latest-weo
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "current account balance" --all-databases
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "real GDP growth" --json
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py resolve "April 2024 WEO vintage nominal GDP in US dollars" --json
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py explain-source "IFS CPI for the United States"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py code NGDP_RPCH --database IMF.RES.WEO:WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py dimensions IMF.STA:CPI
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py classify-database IMF.RES.WEO:WEO_LIVE_2024_APR_VINTAGE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py compare-codes PCPI_PCH PCPIE_PCH --database IMF.RES.WEO:WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "nominal GDP" --database IMF.RES.WEO:WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "GDP per capita" --database WB:WDI
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "10-year government bond yield" --database IMF.CSF:BBGDL
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "wheat" --database WTO:WTOIMFTT
```

Command contracts:

| Command | Use when | Output guarantee |
|---|---|---|
| `search` | Ranked candidates are needed for inspection. | Ranked candidates with `database_name`, `dimension_name`, `code`, and `name`; JSON includes route and summary metadata. |
| `resolve` | A single handoff identifier is needed. | `status` is `resolved`, `ambiguous`, or `no_match`; JSON includes `handoff` only when safe to commit and `clarification` when ambiguous. |
| `explain-source` | Source family or legacy routing is unclear. | Returns `routed`, `default`, or `needs_more_context` plus the next search step. |
| `code` | The user already has a code. | Returns exact code matches without fuzzy inference. |
| `dimensions` | The required code dimension is unclear. | Returns dimension names, counts, and example codes for a database. |
| `classify-database` | LIVE/vintage/legacy status is unclear. | Classifies the database and explains whether it is default live, vintage, legacy, or non-vintage. |
| `compare-codes` | Two or more known codes need distinction. | Returns same/different database and dimension labels plus each code name. |

Use `resolve --json` as the default command when a user asks to find the identifier, prepare for iData, or find-and-download. If `status=resolved`, pass the `handoff` object to `imf-ra-data`. If `status=ambiguous`, present the candidates or the `clarification` question and wait for confirmation. Use `search` when you want ranked candidates without commitment, and `explain-source` when the user only asks where a source family routes. Use `code`, `dimensions`, `classify-database`, and `compare-codes` for exact lookup, validation, and variant-comparison workflows. If these commands cover the workflow, do not write temporary Python. If no command covers the task shape, then temporary code is acceptable.

## Ambiguity and Uncertainty

Do not guess identifiers. Ask for clarification when:

- Several variables match the same concept but differ by unit, transformation, valuation, or price basis.
- Multiple databases plausibly cover the request and WEO Live is not clearly preferred.
- Frequency is required but unclear or incompatible with the selected dataset.
- The request implies a WEO group, panel, or region whose membership is unclear.
- The user asks for a vintage but does not specify which vintage.

When presenting alternatives, include:

- `database_name`
- `dimension_name`
- `Code`
- `Name`
- A short distinction note

Ask the smallest useful clarification question, usually among two to five candidates.

## Output Format

For an unambiguous match, return:

```text
database: <Agency ID:Resource ID>
dimension_name: <dimension>
code: <code>
name: <human-readable name>
notes: <brief reason this is the best match>
```

For ambiguous results, return a ranked candidate list with distinction notes and ask the user to confirm the intended choice.

If no useful match exists in the reference files, state the gap clearly and ask for one additional hint. Do not invent a dataset, dimension, or code.

## Handoff

Once the user confirms the identifier, hand off to `imf-ra-data` with the selected `database`, `dimension_name`, `code`, and any confirmed geography, frequency, date, or vintage constraints.

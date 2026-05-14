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
| `databases/haver_databases.md` | Haver database directory and routing guide. Use to identify which Haver database covers a given concept before searching indicator metadata. |

### Indicator Catalogs

| File | Purpose |
|---|---|
| `indicators/1. non_vintage_variable_list.csv` | General non-vintage variable catalog. Use for ordinary variable and code discovery. |
| `indicators/2. bbg_variable_list.csv` | Bloomberg variable catalog. Use when the user requests Bloomberg or `IMF.CSF:BBGDL`. |
| `indicators/3. wdi_variable_list.csv` | World Bank WDI variable catalog. Use when the user requests WDI or `WB:WDI`. |
| `indicators/4. wto_variable_List.csv` | WTO variable catalog. Use when the user requests WTO goods, tariff, or commodity codes. |
| `indicators/haver/<DB>.csv` | Haver indicator metadata, one CSV per database. Schema: `code`, `descriptor`, `frequency`, `startdate`, `enddate`, `shortsource`. Use only after routing to a specific database via `haver_databases.md`. Currently available: `EMERGE.csv`, `USECON.csv`, `WEEKLY.csv`. |

## Default Selection Policy

1. Default to non-vintage datasets.
2. Use vintage datasets only when the user explicitly asks for a vintage, historical publication, dated snapshot, or versioned release.
3. For WEO-style macroeconomic concepts, begin with non-vintage `IMF.RES.WEO:WEO_LIVE` unless the user asks for another source or the concept is clearly outside WEO coverage.
4. Do not silently replace non-vintage `WEO_LIVE` with a dated WEO vintage. If the user asks for a WEO vintage but does not specify one, ask whether they want the latest available WEO Live vintage or a specific historical vintage.
5. Search all databases only when WEO Live, GAS live and other highlighted database in database_overview.md lack a plausible match, the user explicitly asks for another database family, or the concept is clearly outside WEO coverage.
6. Use database-specific indicator files for Bloomberg, WDI, and WTO requests rather than the general non-vintage variable list.
7. For Haver requests, follow the two-step Haver routing workflow below — do not search all Haver CSVs blindly.

## Lookup Workflow

1. **Parse the request.** Identify the concept, preferred database, unit, transformation, frequency, geography, and vintage requirement when available.
2. **Select a dataset.** Use `non_vintaged_datasets.csv` by default, `vintaged_datasets.csv` only for explicit vintage requests, and `database_overview.md` for high-level source selection.
3. **Select the indicator file.** Choose the general non-vintage indicator list or the specific Bloomberg, WDI, or WTO list based on the dataset family.
4. **Find candidate codes.** Search within the selected indicator file for exact names, close wording, aliases, and source-specific terminology.
5. **Preserve dimensions.** Always carry through `dimension_name`; do not assume the code dimension is `INDICATOR`.
6. **Resolve ambiguity.** Compare candidates by unit, transformation, valuation, frequency, price basis, and database coverage.
7. **Return the result.** Commit to a single identifier only when the match is exact and unambiguous. Otherwise, return a short candidate list and ask for confirmation.

## Haver Lookup (Temporary — pre-SQLite)

> **Note:** Haver indicator metadata is not yet in the unified catalog. Use the two-step routing below to locate indicators. This section will be replaced once metadata moves to a searchable database.

### Step 1 — Identify the database

Read `databases/haver_databases.md` and use the **Routing Guidance** section at the bottom to narrow the request to one or two candidate databases. Do not open any indicator CSV yet.

### Step 2 — Search the candidate CSV(s)

Once you have a candidate database, check whether its CSV exists in `indicators/haver/`. Currently available: `EMERGE`, `USECON`, `WEEKLY`.

- If the database has a CSV: search `descriptor` for keywords matching the user's concept. Match on `code` + `descriptor`. Note `frequency`, `startdate`, and `enddate` as part of the result.
- If the database does not yet have a CSV: tell the user the likely database based on routing, but explain the indicator metadata for that database is not yet loaded. Do not invent a code.

### Output

Return the same format as other catalog results, using `code` as the indicator code and `descriptor` as the name. There is no `dimension_name` concept in Haver — omit that field or set it to `N/A`.

```text
database: HAVER:<DB_CODE>   (e.g. HAVER:USECON)
dimension_name: N/A
code: <haver_code>
name: <descriptor>
frequency: <A/Q/M/W/D>
coverage: <startdate> – <enddate>
source: <shortsource>
notes: <brief reason this is the best match>
```

## Use of Helper Scripts

Inspect CSV and Markdown files directly for straightforward requests. Use code only when manual review is unreliable, such as broad search across many rows, repeated filtering, ranking, joins, or explicit vintage comparisons.

Before using `scripts/catalog_search.py`, first map the user's wording to terminology that appears in the catalog. The helper should accelerate a source-aligned lookup, not invent indicator logic.

Common helper commands:

```bash
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py latest-weo
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO_LIVE
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py datasets WEO --vintage-only
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "real GDP growth"
python3 .claude/skills/imf-ra-catalog/scripts/catalog_search.py search "current account balance" --all-databases
```

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

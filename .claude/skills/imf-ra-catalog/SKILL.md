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

## Lookup Workflow

Use this catalog-specific workflow after the umbrella `imf-ra` policy routes the task here.

1. **Parse catalog intent.** Identify concept, preferred database/source, unit, transformation, frequency, geography, and vintage requirement when available.
2. **Apply dataset policy.** Use `non_vintage_datasets.csv` by default. Use `vintage_datasets.csv` only for explicit vintage, historical-release, dated snapshot, or versioned-release requests.
3. **Choose the source family.** Default WEO-style macro concepts to `IMF.RES.WEO:WEO_LIVE`; use database-specific indicator files for Bloomberg, WDI, and WTO requests.
4. **Preserve `dimension_name`.** Do not assume the code dimension is `INDICATOR`; hand off the exact dimension returned by the catalog helper.
5. **Compare candidate meaning.** For close matches, distinguish unit, transformation, valuation, frequency, price basis, and database coverage.
6. **Return only safe identifiers.** Commit to `(database, dimension_name, code)` only when exact and unambiguous; otherwise return candidates and ask for confirmation.

## Helper Responsibility

Before writing temporary Python for any catalog lookup, you MUST check this command map and run the most specific helper command that fits the task.

`scripts/catalog_search.py` is the catalog capability map. Consult it during task classification before writing temporary Python.

Helper implementation is split by responsibility:

| File | Role |
|---|---|
| `scripts/catalog_search.py` | CLI commands and output formatting. |
| `scripts/catalog_data.py` | CSV paths, constants, loaders, and row record helpers. |
| `scripts/catalog_routing.py` | Source routing, WEO live/vintage handling, IFS migration routing, database classification. |
| `scripts/catalog_lookup.py` | Candidate selection, scoring, exact code lookup, ambiguity handling, and handoff payloads. |

### Core Navigation Map

| If the user wants to... | Use this helper command | Key input |
|---|---|---|
| Resolve a metric into a handoff-ready identifier | `resolve "<query>" --json` | natural-language metric request |
| Inspect ranked candidates without commitment | `search "<query>"` | metric request |
| Route source-family wording | `explain-source "<query>" --json` | IFS/WDI/Bloomberg/WTO/WEO wording |
| Validate or explain a known code | `code <code> --database <db>` | code, optional database |
| Discover the code dimension for a database | `dimensions <database>` | database |
| Classify live/vintage/legacy database status | `classify-database <database>` | database |
| Compare known indicator variants | `compare-codes <code_a> <code_b> --database <db>` | codes, optional database |
| List WEO vintages or datasets | `datasets <query> --vintage-only` | dataset query |
| Get default WEO Live database | `latest-weo` | none |

### Detailed Helper Capabilities

#### 1. Source Routing Module

- **`explain-source "<query>" --json`**
  - **Core Utility:** Routes source wording to WEO Live, WEO vintage, IFS replacement topic databases, WDI, Bloomberg, WTO, or default WEO Live.
  - **When to Trigger:** Use when the user names IFS, WDI, Bloomberg, WTO, a WEO vintage, or an unclear source family.
  - **Operational Rule:** Do not treat legacy `IFS` as a single iData database; route it to the replacement topic database.

- **`classify-database <database>`**
  - **Core Utility:** Validates an exact database and labels it as WEO Live, vintage, legacy WEO, non-vintage, or missing.
  - **When to Trigger:** Use before handoff when LIVE/vintage/legacy status matters.

#### 2. Indicator Lookup Module

- **`search "<query>"`**
  - **Core Utility:** Ranks candidate indicators using catalog terminology and synonym scoring.
  - **When to Trigger:** Use for exploratory fuzzy lookup or when the user wants options.
  - **Operational Rule:** Preserve `database_name`, `dimension_name`, `code`, and `name` for every candidate.

- **`resolve "<query>" --json`**
  - **Core Utility:** Returns a single `handoff` only when the top candidate is safe; otherwise returns candidates and clarification.
  - **When to Trigger:** Use as the default before `imf-ra-data` when the user asks to find, use, or download a metric.
  - **Operational Rule:** If `status=ambiguous`, ask the clarification question. Do not hand off a candidate manually.

- **`code <code> --database <db>`**
  - **Core Utility:** Finds exact code metadata without fuzzy inference.
  - **When to Trigger:** Use when the user already supplies a code.

#### 3. Dimension & Variant Module

- **`dimensions <database>`**
  - **Core Utility:** Shows catalog dimensions and example codes for a database.
  - **When to Trigger:** Use when the code dimension may not be `INDICATOR`.
  - **Operational Rule:** Always preserve the returned `dimension_name`.

- **`compare-codes <codes...> --database <db>`**
  - **Core Utility:** Compares known codes by database, dimension, and official name.
  - **When to Trigger:** Use for variant questions such as period-average vs end-of-period CPI.

#### 4. Dataset & Vintage Module

- **`latest-weo`**
  - **Core Utility:** Returns the default non-vintage WEO Live database.
  - **When to Trigger:** Use when the user asks for current/latest WEO data without a vintage.

- **`datasets <query> --vintage-only`**
  - **Core Utility:** Lists dated WEO vintage databases.
  - **When to Trigger:** Use when the user asks for historical WEO releases or an unspecified vintage.

### Anti-Patterns & Enforcement Rules

1. **No code guessing:** Do not invent `database`, `dimension_name`, or `code`; validate through CSVs or helper output.
2. **No redundant snippets:** Do not write temporary Python that reimplements routing, fuzzy ranking, exact code lookup, dimension discovery, or code comparison.
3. **Resolve before handoff:** Pass only `resolve --json` output with `status=resolved` and a `handoff` object to `imf-ra-data`.
4. **Preserve dimensions:** Never assume the code dimension is `INDICATOR`; carry the returned `dimension_name`.
5. **Use direct references only for small exact checks:** CSV/Markdown inspection is fine for one-row confirmation or schema guidance; use helper commands for fuzzy, routed, comparative, vintage, or handoff workflows.
6. **Promote repeated gaps:** Write temporary code only when no helper command covers the task; if the same pattern repeats, add it to `catalog_search.py`.
7. **Keep responsibilities separate:** Catalog helpers do not fetch data, expand country groups, choose date ranges, transform series, or build charts.

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

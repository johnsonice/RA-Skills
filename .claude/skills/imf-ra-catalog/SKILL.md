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
5. Search all databases only when WEO Live, GAS live and other highlighted databases in `database_overview.md` lack a plausible match, the user explicitly asks for another database family, or the concept is clearly outside WEO coverage.
6. Use database-specific indicator files for Bloomberg, WDI, and WTO requests rather than the general non-vintage variable list.

## Legacy IFS Requests

`IFS` no longer exists as a single iData dataset. It was the legacy International Financial Statistics dataset in the old EcOS data system. After migration from EcOS to iData, its coverage was split into smaller topic datasets.

When a user asks for "IFS" data:

1. Tell the user that `IFS` no longer exists as a single iData dataset.
2. Treat `IFS` as a legacy source hint, not as the target database.
3. Use `database_overview.md`, `non_vintage_datasets.csv`, and `indicators/1. non_vintage_variable_list.csv` to find the replacement iData topic dataset and exact indicator.
4. In the result, explicitly name the replacement database where the required indicator was found.

Common replacement routing:

| Legacy IFS topic requested | Search/target replacement database |
|---|---|
| CPI, consumer prices, inflation index | `IMF.STA:CPI` |
| Exchange rates | `IMF.STA:ER` |
| Effective exchange rates, REER, NEER | `IMF.STA:EER` |
| Interest rates, money, monetary aggregates, financial corporations | `IMF.STA:MFS_IR`, `IMF.STA:MFS_MA`, `IMF.STA:MFS_CBS`, `IMF.STA:MFS_DC`, `IMF.STA:MFS_ODC`, `IMF.STA:MFS_OFC`, or `IMF.STA:MFS_FC` |
| National accounts, GDP, expenditure components | `IMF.STA:ANEA` or `IMF.STA:QNEA` |
| Balance of payments, current account | `IMF.STA:BOP` |
| International investment position | `IMF.STA:IIP` or `IMF.STA:IIPCC` |
| International liquidity, reserves | `IMF.STA:IL` |
| Goods trade | `IMF.STA:ITG` or `IMF.STA:IMTS` |
| Producer prices | `IMF.STA:PPI` |
| Production indexes / former IPI | `IMF.STA:PI` |
| Government finance, quarterly fiscal data | `IMF.STA:QGFS` |
| Labor force statistics | `IMF.STA:LS` |
| Fund accounts | `IMF.STA:FA` |
| Special purpose entities | `IMF.STA:SPE` |

For IFS requests, include an IFS migration note in the final answer. Example:

```text
Note: IFS no longer exists as a single iData dataset. For this legacy IFS CPI request, the matching indicator is in the replacement iData topic database:
database: IMF.STA:CPI
dimension_name: <dimension>
code: <code>
name: <name>
```

## Lookup Workflow

1. **Parse the request.** Identify the concept, preferred database, unit, transformation, frequency, geography, and vintage requirement when available.
2. **Select a dataset.** Use `non_vintage_datasets.csv` by default, `vintage_datasets.csv` only for explicit vintage requests, and `database_overview.md` for high-level source selection.
3. **Select the indicator file.** Choose the general non-vintage indicator list or the specific Bloomberg, WDI, or WTO list based on the dataset family.
4. **Find candidate codes.** Search within the selected indicator file for exact names, close wording, aliases, and source-specific terminology.
5. **Preserve dimensions.** Always carry through `dimension_name`; do not assume the code dimension is `INDICATOR`.
6. **Resolve ambiguity.** Compare candidates by unit, transformation, valuation, frequency, price basis, and database coverage.
7. **Return the result.** Commit to a single identifier only when the match is exact and unambiguous. Otherwise, return a short candidate list and ask for confirmation.

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

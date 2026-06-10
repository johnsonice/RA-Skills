---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English, such as "current account balance for advanced economies, quarterly", and needs the right dataset, dimension, and variable code. Returns top candidates with clear notes when requests are ambiguous.
---

# IMF RA Catalog

Use this skill to translate a research request into a confirmed identifier ready for handoff to `imf-ra-data`:

```text
iData sources:  (database, dimension_name, code)
Haver sources:  codes: ["CODE@DB", ...]
```

The catalog identifies datasets, dataflows, dimensions, and indicator codes. It does not fetch data. After an identifier is confirmed, hand off to `imf-ra-data` for execution.

## Scope

Use this skill when the user needs to:

- Select the most appropriate IMF, World Bank, WTO, Bloomberg, Haver, or related dataset.
- Map a plain-English concept to a dataset-specific variable or indicator code.
- Resolve ambiguity between similar indicators, transformations, units, dimensions, or database families.
- Identify the latest non-vintage dataset or an explicitly requested vintage dataset.

Do not use this skill to fetch data, transform time series, or build charts. Those tasks belong to downstream skills.

## Required Context

Before lookup, load shared RA conventions from the umbrella `imf-ra` skill when the request involves country codes, WEO country groups, frequency conventions, dates, units, or downstream fetch behavior.

For WEO regions, country groups, aggregates, and informal country names, normalize geography through the umbrella `imf-ra` country-group folder before selecting variables or handing off to `imf-ra-data`:

- `imf-ra/Country Group/Country Group.csv` is the single consolidated country-group matrix.
- `imf-ra/Country Group/weo_country_groups.md` explains the matrix layout, aliases, WEO vs SPR/PRGT caveats, and iData country-selector rules.
- `imf-ra/Country Group/weo_country_groups.py` resolves country/group wording, expands groups to member `countrycode` values, and compares WEO vs SPR/PRGT framework coverage.

Catalog helpers still own dataset and indicator discovery only. They must not expand country groups, choose country membership, or use a group/category column as an iData country selector.

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

### Haver Indicator Catalog

Haver metadata is stored in a SQLite database, not a CSV. Use `scripts/Haver/haver_catalog_search.py` for all Haver lookups — do not search this source with the general CSV-based helper.

| Resource | Location |
|---|---|
| `haver.db` | One level above the RA-Skills repo root. |
| `scripts/Haver/haver_catalog_search.py` | Haver-specific catalog search CLI (FTS5 + scoring over SQLite). |


## Default Selection Policy

1. Default to non-vintage datasets.
2. Use vintage datasets only when the user explicitly asks for a vintage, historical publication, dated snapshot, or versioned release.
3. For WEO-style macroeconomic concepts, begin with non-vintage `IMF.RES.WEO:WEO_LIVE` unless the user asks for another source or the concept is clearly outside WEO coverage.
4. Do not silently replace non-vintage `WEO_LIVE` with a dated WEO vintage. If the user asks for a WEO vintage but does not specify one, ask whether they want the latest available WEO Live vintage or a specific historical vintage.
5. Search all databases only when WEO Live, GAS Live, and other highlighted databases in `database_overview.md` lack a plausible match, the user explicitly asks for another database family, or the concept is clearly outside WEO coverage.
6. Use database-specific indicator files for Bloomberg, WDI, and WTO requests rather than the general non-vintage variable list.
7. Treat Haver as a peer source, not a last resort. Route to the **Haver Lookup Path** proactively — without waiting for the user to name Haver — whenever the concept matches a Haver-owned data type (consult `databases/database_overview.md` for Haver sub-database coverage). For WEO-style macro concepts that exist in both iData and Haver, iData remains the default. When the concept is ambiguous between iData and Haver, use run an iData search  first, then the Haver Lookup Path; present both sets of results. Routing to Haver means entering the Haver Lookup Path at H1 — not running a search immediately.

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

**Step 1 and 2 are shared. Step 2 branches into two separate paths — follow only the one that matches the source family chosen.**

1. **Parse catalog intent.** Identify concept, preferred database/source, unit, transformation, frequency, geography, and vintage requirement when available.

2. **Choose the source family.**
   - Default WEO-style macro concepts to `IMF.RES.WEO:WEO_LIVE`; use database-specific indicator files for Bloomberg, WDI, and WTO requests.
   - **Read `databases/database_overview.md` before any search.** Use it to determine which source family owns the concept. Do not route based on training assumptions — derive source routing from the overview every time.
   - If the concept matches Haver-owned categories (e.g. US weekly/daily data, fund flows, freight, US regional, emerging market country summaries, high-frequency financial, third-party forecasts, industry statistics), route to the **Haver Lookup Path** without running an iData search first. Do not wait for the user to name Haver.
   - If the user explicitly requests Haver or names a Haver database (USECON, EMERGE, WEEKLY, etc.), use the **Haver Lookup Path** exclusively for that request.
   - When the concept could plausibly be in both iData and Haver, start with the **Haver Lookup Path** (complete all H1 scoping first), then run an iData search; present results from both sources.
   - If an iData search returns no useful match and Haver has not yet been searched, go to the **Haver Lookup Path** before declaring a gap.

   → **Haver source selected:** Go to the Haver Lookup Path below. Do **not** run any search until H1 scoping is complete.
   → **iData source selected:** continue with Steps 3–6 below.

### iData Lookup Path

3. **Apply dataset policy.** Use `non_vintage_datasets.csv` by default. Use `vintage_datasets.csv` only for explicit vintage, historical-release, dated snapshot, or versioned-release requests.
4. **Preserve `dimension_name`.** Do not assume the code dimension is `INDICATOR`; hand off the exact dimension returned by the catalog helper.
5. **Compare candidate meaning.** For close matches, distinguish unit, transformation, valuation, frequency, price basis, and database coverage.
6. **Return only safe identifiers.** Commit to `(database, dimension_name, code)` only when exact and unambiguous; otherwise return candidates with distinction notes and ask for confirmation.

### Haver Lookup Path

Haver's data model differs fundamentally from iData: each series code resolves to exactly one country and one measurement variant. There is no multi-dimensional key. Disambiguation and confirmation happen here in the catalog, before any handoff.

**GATE: Do not run any search until H1 scoping is complete and a dblist is confirmed.**

H1. **Collect country/region and frequency.** Two inputs are required to build the target database list. Do not ask for aggtype or datatype at this stage — those are surfaced from search results in H2.

   - **Country/region:** Which countries or geographic scope? (e.g. US, Euro area, G10, emerging markets)
   - **Frequency:** D (daily), W (weekly), M (monthly), Q (quarterly), or A (annual)?

   If either is not stated in the user's request, ask for both in a single message. Do not proceed to H1a until both are confirmed.

H1a. **Build target database list.** Read the Haver Analytics section of `databases/database_overview.md`. Using the confirmed country/region and frequency from H1, identify which sub-databases to search. Produce a confirmed dblist before any search.

   Example routing (not exhaustive — always derive from `database_overview.md`):

   | Frequency | Geography | Example target databases |
   |---|---|---|
   | D | Any | `INTDAILY` |
   | W | Any | `INTWKLY` |
   | M/Q/A | Advanced economies | `G10`, `ANZ`, `BENELUX`, `CANADA`, `UK`, `JAPAN`, `ALPMED`, and other AE-specific databases |
   | M/Q/A | Emerging markets | `EMERGE`, `EMERGELA`, `EMERGEPR`, `EMERGECW`, `EMERGEMA` |
   | M/Q/A | US | `USECON`, `G10`, and US-specific databases |

   Do not search databases outside the confirmed dblist, and do not re-search the same database with different query variations.

H1b. **Search.** Choose ONE query string, then run a **single Bash call** covering all databases in the confirmed dblist using `--databases`. Do not issue separate Bash calls per database — each separate call triggers its own permission prompt.

```bash
python .claude/skills/imf-ra-catalog/scripts/Haver/haver_catalog_search.py \
  search "<query>" --databases DB1 DB2 DB3 ... --limit 300
```

The `--databases` flag is required (haver.db has 12M+ rows and unscoped searches are very slow). The output includes `aggtype` and `datatype` for every candidate.

**Set `--limit` to at least 300 for any multi-country or multi-database search.** The default limit is small and silently truncates results, which causes missed matches and forces re-runs that each trigger a permission prompt. Use `--limit 300` (or higher) whenever the confirmed dblist has 3+ databases or the concept plausibly matches many countries.

**One query, one pass.** Decide on the best query string before running. Each database is searched exactly once. Do not re-run with alternative phrasings — the FTS5 scorer expands synonyms internally (e.g. `treasury` → `government bond yield`). Accept the first-pass results.

H2. **Present results with variant choices.** Group all candidates by country. For each candidate, show `code`, `name`, `aggtype`, `datatype`, and `frequency`. Ask the user to:
   1. Select the countries they want.
   2. Confirm the variant (aggtype and datatype) if multiple variants exist for the same country.

   Do not pre-filter by aggtype or datatype — surface all variants so the user can choose.

H3. **Hand off.** Once the user selects specific codes, produce a `codes: ["CODE@DB", ...]` list and pass to `imf-ra-data`. There is no `dimension_name` in a Haver handoff — the `CODE@DATABASE` format is the complete identifier.

## Helper Responsibility

Before writing temporary Python for any catalog lookup, you MUST check this command map and run the most specific helper command that fits the task.

Two separate helper CLIs exist — one for iData sources, one for Haver. Pick the right one based on source routing before running any command.

**iData sources** (`scripts/catalog_search.py`):

| File | Role |
|---|---|
| `scripts/catalog_search.py` | CLI commands and output formatting. |
| `scripts/catalog_data.py` | CSV paths, constants, loaders, and row record helpers. |
| `scripts/catalog_routing.py` | Source routing, WEO live/vintage handling, IFS migration routing, database classification. |
| `scripts/catalog_lookup.py` | Candidate selection, scoring, exact code lookup, ambiguity handling, and handoff payloads. |

**Haver** (`scripts/Haver/haver_catalog_search.py`):

Searches the local `haver.db` SQLite database using FTS5 full-text search and synonym-aware scoring. Returns: `score`, `database_name`, `dimension_name`, `code`, `name`, `frequency`, `aggtype`, `datatype`, `coverage`, `source`. Note: `dimension_name` is always `N/A` for Haver — Haver uses `CODE@DATABASE` format, not iData dimensions. Use `aggtype` (EOP/AVG/SUM/NST/NDF) and `datatype` (LocCur/US$/%/INDEX/etc.) to identify and present variant choices to the user.

**`HAVER:` prefix note:** `database_name` in search output is display-only (e.g. `HAVER:EMERGECW`). When building `CODE@DB` handoff strings or passing `--database` to any command, use the short code without the prefix (e.g. `EMERGECW`, `INTDAILY`, `USECON`). Both `haver_catalog_search.py` and `fetch_haver.py` accept either form, but `CODE@EMERGECW` is the canonical handoff format.

### Core Navigation Map

**iData (use `python scripts/catalog_search.py <command>`):**

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

**Haver (use `python scripts/Haver/haver_catalog_search.py <command>`):**

| If the user wants to... | Use this helper command | Key input |
|---|---|---|
| Search Haver indicators by plain-English keywords | `search "<query>"` | natural-language metric request |
| Search across multiple Haver databases in one call | `search "<query>" --databases DB1 DB2 DB3` | query + list of DB codes |
| Filter to a single Haver database | `search "<query>" --database USECON` | query + one Haver DB code |
| Look up an exact Haver code | `code <code>` | Haver series code |
| List available Haver databases | `databases` | none |
| Show SQLite build metadata | `info` | none |

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
3. **Resolve before handoff:** For iData sources, pass only `resolve --json` output with `status=resolved` and a `handoff` object to `imf-ra-data`. For Haver sources, pass only a confirmed `codes: ["CODE@DB", ...]` list produced after completing the full Haver Lookup Path (H1–H3). Do not hand off from either path until confirmation is complete.
4. **Preserve dimensions:** Never assume the code dimension is `INDICATOR`; carry the returned `dimension_name`.
5. **Use direct references only for small exact checks:** CSV/Markdown inspection is fine for one-row confirmation or schema guidance; use helper commands for fuzzy, routed, comparative, vintage, or handoff workflows.
6. **Promote repeated gaps:** Write temporary code only when no helper command covers the task; if the same pattern repeats, add it to `catalog_search.py`.
7. **Keep responsibilities separate:** Catalog helpers do not fetch data, expand country groups, choose country membership, choose date ranges, transform series, or build charts.
8. **Never query haver.db with ad-hoc SQL LIKE patterns.** The `indicators` table has 12M+ rows and no index on `descriptor` — unscoped `LIKE '%...%'` queries do full-table scans and are very slow. Always use `haver_catalog_search.py` (FTS5) for Haver text search. Only write direct SQL for exact lookups on indexed columns (`database`, `code`, `frequency`).
9. **Batch all Haver database searches into one Bash call.** When the confirmed dblist has multiple databases, use `--databases DB1 DB2 ...` in a single invocation — never one Bash call per database. Each separate call triggers a permission prompt.
10. **One query per search session, no reruns.** The FTS5 scorer handles synonyms internally. Do not re-run the same database with a rephrased query to find more results — accept the first-pass output.
11. **Always use `--limit 300` or higher for broad searches.** Never use a small limit (e.g. 15, 20, 30) for multi-country or multi-database searches. A truncated result set forces re-runs, which generate additional permission prompts. Use `--limit 300` as the default for any search covering 3+ databases or concepts that span many countries.

## Ambiguity and Uncertainty

Do not guess identifiers. Ask for clarification when:

- Several variables match the same concept but differ by unit, transformation, valuation, or price basis.
- Multiple databases plausibly cover the request and WEO Live is not clearly preferred.
- Frequency is required but unclear or incompatible with the selected dataset.
- The request implies a WEO group, panel, or region whose membership is unclear. Use `imf-ra/Country Group/weo_country_groups.py` for geography resolution or ask a framework/membership clarification before handoff.
- The user asks for a vintage but does not specify which vintage.

When presenting **iData** alternatives, include:

- `database_name`
- `dimension_name`
- `code`
- `name`
- A short distinction note

When presenting **Haver** alternatives, include:

- `database_name` (e.g. `HAVER:EMERGE`)
- `code` (the series code)
- `name` (the descriptor — includes country and units)
- `aggtype` (e.g. EOP, AVG)
- `datatype` (e.g. LocCur, US$, %)
- `frequency`
- A short distinction note

Ask the smallest useful clarification question, usually among two to five candidates.

## Output Format

**iData — unambiguous match:**

```text
database: <Agency ID:Resource ID>
dimension_name: <dimension>
code: <code>
name: <human-readable name>
notes: <brief reason this is the best match>
```

**Haver — confirmed selections (after Haver Lookup Path H1–H3):**

```text
codes: ["CODE1@DB", "CODE2@DB", ...]
frequency: <A|Q|M|W|D>
aggtype: <EOP|AVG|SUM|...>
datatype: <LocCur|US$|%|INDEX|...>
notes: <brief reason these are the best matches>
```

For ambiguous results (either source), return a ranked candidate list with distinction notes and ask the user to confirm the intended choice.

If no useful match exists in any source, state the gap clearly and ask for one additional hint. Do not invent a dataset, dimension, or code.

## Handoff

Once the user confirms the identifier, hand off to `imf-ra-data`:

- **iData:** pass `database`, `dimension_name`, `code`, and any confirmed geography, frequency, date, or vintage constraints. If geography came from a WEO group/category, hand off member `countrycode` values from `imf-ra/Country Group/weo_country_groups.py`, not the group/category column name.
- **Haver:** see format below.

**Haver handoff format:**

Each confirmed selection is a `CODE@DATABASE` string. The handoff passes a list:

```text
codes: ["CODE1@DB", "CODE2@DB", ...]    e.g. ["n186xnr@EMERGE", "n199xnr@EMERGE"]
frequency: <A|Q|M|W|D>                 from the confirmed series metadata
```

`imf-ra-data` detects the `codes` field in the handoff and routes to `fetch_haver.py` instead of `fetch_idata.py`. Codes may span multiple Haver databases in a single call if needed.

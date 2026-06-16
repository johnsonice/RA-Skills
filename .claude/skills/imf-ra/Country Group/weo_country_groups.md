# WEO Country Groups

Use this reference whenever a task mentions WEO country groups, WEO aggregates, WEO regions, WEO country codes, or informal RA group names such as `AE`, `EMDE`, `LIC`, `LAC`, `SSA`, or `ASEAN-5`.

The consolidated [Country Group.csv](Country%20Group.csv) file is the canonical source of truth for this skill.

## Source Scope

- The country-group workbook was implemented during the April 2026 WEO exercise.
- The groups are used to calculate aggregates in the WEO Live database.
- Workbook last-updated date: April 16, 2026.

## Reference File

| CSV file | Purpose | Key columns |
|---|---|---|
| `Country Group.csv` | Consolidated country list and group-membership matrix. Use for country code, country name, department, region, group category, and exact group membership lookup. | `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, `department`, then one membership column per country group/category |

The first five columns identify countries. Every later column is a WEO, regional, analytical, or SPR/PRGT group/category; a value of `1` means the country belongs to that group.


## Consolidated Layout

| Layout area | Columns | How to read it |
|---|---|---|
| Country identity | `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, `department` | One row per WEO Live country or aggregate. Use these columns for country lookup and country-code handoff. |
| WEO/regional/analytical groups | all columns after `department` | Each column is a group/category name. A row value of `1` means that country belongs to that group; blank means it does not. |
| SPR/PRGT framework groups | columns such as `SPR-Emerging Market and Middle-Income Economies(EM)` and `SPR-Low-Income Developing Countries (LIC)` | Use these only when the user asks for SPR/PRGT coverage or confirms that framework. |

The file is intentionally a single matrix. To list members of a group, filter the group column to rows marked `1`. To list groups containing a country, inspect the marked group columns on that country row.

## Column Systems

| Code field | Meaning | Example | Use |
|---|---|---|---|
| `countrycode` | ISO-style WEO country or aggregate code. | `USA`, `CHN`, `JPN` | Use for WEO-style country lookup and selected-country iData pulls, unless dataset metadata says otherwise. |
| `countrycode_s` | Internal Fund country code stored as a 3-digit string. | `111` for United States | Use only when the user or dataset explicitly requires internal numeric codes. |
| Group/category columns | One column per group/category. | `Advanced Economies(AE)`, `Low-Income Developing Countries (LIDC)`, `SPR-Low-Income Developing Countries (LIC)` | Use for group lookup and exact membership filtering. |

Important pull rule: do not pass a group/category name as the country value in iData pull requests. For selected-country pulls, resolve the group to member `countrycode` values first. Use an aggregate value only when dataset metadata explicitly confirms it is valid.

## How To Use The Consolidated Table

- To find a WEO country code from a country name, use the first five columns of `Country Group.csv`.
- To list countries in a group, filter the relevant group/category column to rows where the value is `1`.
- To list groups that include a country, find the country row and read the group/category columns marked `1`.
- To answer exact membership questions, use the explicit `1` markers in `Country Group.csv`; do not infer membership from group names.
- To resolve common shorthand, use `weo_country_groups.py`; it maps aliases to the actual group/category columns in `Country Group.csv`.

## Group Types

`Country Group.csv` contains group/category columns after the five country identity columns. The helper exposes those columns directly rather than inventing separate group-code metadata.

## Common Aliases

Use exact codes when available. Otherwise use documented or helper-supported aliases, and return candidates when a phrase is ambiguous.

| User wording | Preferred consolidated-file group/country query |
|---|---|
| `US`, `USA`, `United States`, `United States of America`, `America` | `USA` |
| `mainland`, `mainland China`, `China mainland` | `CHN` |
| `Cote d'Ivoire`, `Côte d'Ivoire`, `Ivory Coast` | `CIV` |
| `AE`, `advanced economies` | `Advanced Economies(AE)` |
| `EMDE`, `EMDEs`, `emerging market and developing economies` | `Emerging Market and Developing Economies(EMDE)` |
| `LAC`, `Latin America and the Caribbean` | `Latin America and the Caribbean (LAC)` |
| `SSA`, `Sub-Saharan Africa` | `Sub-Saharan Africa (SSA)` |
| `Euro area`, `EA` | `Euro Area (EA) – aggregate of member states` |
| `ASEAN-5`, `ASEAN 5` | `ASEAN-5` |
| `European Union`, `EU` | `European Union (EU)` |
| `World` | `World` |

When a user phrase is ambiguous, list the plausible `Country Group.csv` group columns before choosing one.

The `G20` group in `Country Group.csv` is a country-row group with 19 countries; for official current G20 membership questions, distinguish this from the member-seat view of 19 countries plus the European Union and African Union.

## WEO vs SPR AE, EM, and LIC Caveat

Clarify the source framework when a request involves advanced economies, emerging/developing economies, emerging markets, low-income countries, LICs, LIDCs, or SPR PRGT groups.

WEO and SPR do not always use the same EM/LIC grouping definitions:

| Concept | WEO group column | SPR/PRGT group column |
|---|---|---|
| Advanced Economies | `Advanced Economies(AE)` | `Advanced Economies(AE)` |
| Developing Economies / EM | `Emerging Market and Middle-Income Economies(EM)` | `SPR-Emerging Market and Middle-Income Economies(EM)` |
| Low-Income Countries / LIC | `Low-Income Developing Countries (LIDC)` | `SPR-Low-Income Developing Countries (LIC)` |
| EMDE | `Emerging Market and Developing Economies(EMDE)` | `SPR-Emerging Market and Middle-Income Economies(EM)` + `SPR-Low-Income Developing Countries (LIC)` |

Emerging Market and Developing Economies (EMDE) = WEO EM + WEO LIDC + Syria.  
WEO World = WEO AE + WEO EM + LIDC + Syria. 
WEO World = WEO AE + WEO EMDE. 
WEO World = SPR World = WEO AE + SPR EM + SPR LIC. 


If the user asks for EM, EMDE, LIC, LIDC, PRGT, or developing-economy coverage without specifying WEO vs SPR/PRGT, ask which framework they mean before committing to a group. This distinction is important because both frameworks are IMF frameworks, but membership can differ by framework.

## IMF Member Countries vs Countries And Territories Caveat

Clarify scope when a request mentions IMF member countries, all IMF members, IMF economies, territories, or full WEO coverage.

`Country Group.csv` contains two related IMF-member group columns:

| Concept | Group column | Count | Meaning |
|---|---|---:|---|
| IMF member countries | `IMF member Countries(191)` | 191 | Sovereign IMF member countries only. |
| IMF member countries and territories | `IMF member Countries and Territories(198)` | 198 | The 191 IMF member countries plus seven WEO-covered territories/economies. |

If the user asks for "IMF member countries", "all IMF members", "IMF economies", or similar wording without specifying scope, ask whether they mean:

1. `IMF member Countries(191)` - sovereign IMF member countries only.
2. `IMF member Countries and Territories(198)` - the 191 IMF member countries plus seven WEO-covered territories/economies.

Do not commit to either group until the user confirms the intended scope.

For difference or coverage questions, know that `IMF member Countries and Territories(198)` adds Anguilla, Aruba, Curaçao, Hong Kong SAR, Macao SAR, Montserrat, and Sint Maarten to `IMF member Countries(191)`. The full WEO country-table scope has 201 rows: those 198 plus Puerto Rico, Taiwan Province of China, and West Bank and Gaza.

Use `weo_country_groups.py compare` or `members` when the exact membership list is needed.

For iData pulls, do not pass either group column name directly as the country selector. Expand the chosen group to member `countrycode` values first unless dataset metadata explicitly confirms a supported aggregate.

## Helper Script Usage

This helper is the capability map for WEO country, group, membership, and framework lookups. Consult it during task classification before writing temporary Python. `Country Group.csv` remains the source of truth.

Implementation file:

| File | Role |
|---|---|
| `weo_country_groups.py` | Single-file helper stored next to `Country Group.csv`. It contains the CLI entry point, consolidated CSV loading, logical country/group/composition views, aliases, explanations, country/group resolution, membership expansion, and framework comparison. |

### Core Navigation Map

| If the user wants to... | Use this helper command | Key input |
|---|---|---|
| Resolve ambiguous country/group wording | `resolve <query>` | `query` |
| Explain RA shorthand or framework caveats | `explain <term>` | `AE`, `EM`, `EMDE`, `LIC`, `LIDC` |
| List countries in a WEO or SPR/PRGT group | `members <group>` | group column, alias, or group name |
| List groups containing a country | `memberships <country>` | `countrycode`, alias, or country name |
| Expand a group for iData country selectors | `expand-for-idata <group> --codes-only` | `group` |
| Compare WEO vs SPR/PRGT group coverage | `compare <group_a> <group_b>` | two group terms |
| Search group metadata | `groups <query>` | group column/name |
| Search country metadata | `countries <query>` | country code/name/department |

### Detailed Helper Capabilities

#### 1. Resolution Module

- **`resolve <query>`**
  - **Core Utility:** Returns country and group candidates for ambiguous wording.
  - **When to Trigger:** Use before choosing a code for terms like `Congo`, `Korea`, `EM`, or informal regional labels.
  - **Operational Rule:** If multiple plausible candidates appear, show them and ask for confirmation.

- **`explain <term>`**
  - **Core Utility:** Explains common RA shorthand and WEO vs SPR/PRGT differences.
  - **When to Trigger:** Use for `AE`, `EM`, `EMDE`, `LIC`, `LIDC`, or PRGT-related requests.
  - **Operational Rule:** Do not collapse WEO and SPR/PRGT definitions unless the helper/reference says they match.

#### 2. Membership Module

- **`members <group>`**
  - **Core Utility:** Lists exact member countries for one group.
  - **When to Trigger:** Use for questions like "which countries are in Advanced Economies?"
  - **Operational Rule:** Use membership output instead of inferring group composition from names.

- **`memberships <country>`**
  - **Core Utility:** Lists all groups that include one country.
  - **When to Trigger:** Use when classifying a country into WEO, regional, analytical, or PRGT groups.

- **`compare <group_a> <group_b>`**
  - **Core Utility:** Shows counts, overlap, and countries only in each group.
  - **When to Trigger:** Use for WEO vs PRGT comparisons, especially `Low-Income Developing Countries (LIDC)` vs `SPR-Low-Income Developing Countries (LIC)` and `Emerging Market and Middle-Income Economies(EM)` vs `SPR-Emerging Market and Middle-Income Economies(EM)`.

#### 3. iData Handoff Module

- **`expand-for-idata <group> --codes-only`**
  - **Core Utility:** Converts a group into comma-separated `countrycode` values.
  - **When to Trigger:** Use before data pulls that require selected countries.
  - **Operational Rule:** Do not pass a group/category column name as an iData country selector unless dataset metadata explicitly supports that aggregate.

Examples:

```bash
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" resolve Congo
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" explain EM
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" members "Advanced Economies(AE)"
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" compare "Low-Income Developing Countries (LIDC)" "SPR-Low-Income Developing Countries (LIC)"
python3 ".claude/skills/imf-ra/Country Group/weo_country_groups.py" expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only
```

### Anti-Patterns & Enforcement Rules

1. Do not write temporary code that reimplements alias matching, group membership expansion, or WEO vs PRGT comparison when a helper command covers the task.
2. Do not guess `countrycode` values or group/category columns; validate through the CSV or helper output.
3. Do not pass raw non-English text, empty text, or highly informal wording directly to the helper; normalize to a likely English label or code first.
4. Do not use a group/category column name as a country selector for iData pulls; expand to member `countrycode` values first.

## Output Guidance

For country matches, return `countrycode`, `countryname`, and any relevant distinction note.

For group matches, return the exact `Country Group.csv` group/category column name and a note when the wording is framework-sensitive.

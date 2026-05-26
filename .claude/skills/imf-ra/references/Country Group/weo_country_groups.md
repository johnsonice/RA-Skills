# WEO Country Groups

Use this reference whenever a task mentions WEO country groups, WEO aggregates, WEO regions, WEO country codes, or informal RA group names such as `AE`, `EMDE`, `LIC`, `LAC`, `SSA`, or `ASEAN-5`.

The CSV files under [csv/](csv/) are the canonical source of truth for this skill.

## Source Scope

- The country-group workbook was implemented during the April 2026 WEO exercise.
- The groups are used to calculate aggregates in the WEO Live database.
- Workbook last-updated date: April 16, 2026.

## Reference Tables

| CSV file | Purpose | Key columns |
|---|---|---|
| `csv/1. countries.csv` | Master list of WEO Live countries. Use for country code, country name, and department lookup. | `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, `department` |
| `csv/2. country_groups.csv` | Canonical list of WEO country groups. Use for group names, group codes, group types, and aliases. | `grouptype`, `groupcode`, `groupname`, `groupcode_s`, `groupname_s` |
| `csv/3. country_group_composition.csv` | Long-form group membership table. Use for exact group membership and country-to-group membership lookup. | `groupcode`, `groupname`, `groupcode_s`, `groupname_s`, `countrycode`, `countryname`, `countrycode_s`, `countryname_s` |


## Code Systems

| Code field | Meaning | Example | Use |
|---|---|---|---|
| `countrycode` | ISO-style WEO country or aggregate code. | `USA`, `CHN`, `JPN`, `G001`, `GX229` | Use for WEO-style country lookup and selected-country iData pulls, unless dataset metadata says otherwise. |
| `countrycode_s` | Internal Fund country code stored as a 3-digit string. | `111` for United States | Use only when the user or dataset explicitly requires internal numeric codes. |
| `groupcode` | WEO group identifier, usually beginning with `G` or `GX`. | `G110`, `G200`, `G603` | Use for group lookup and group membership mapping only. Do not use directly for iData pulls. |
| `groupcode_s` | Legacy numeric group code stored as text. | `110`, `200`, `603` | Use only for legacy mapping or when explicitly requested. |

Important pull rule: do not use `groupcode` or `groupcode_s` as the country value in iData pull requests. For pulls, resolve the group to member `countrycode` values first, or use a dataset-supported aggregate code only when metadata confirms it is valid.

## How To Choose The Right Table

- To find a WEO country code from a country name, use `csv/1. countries.csv`.
- To find a canonical group code or group name, use `csv/2. country_groups.csv`.
- To list countries in a group, use `csv/3. country_group_composition.csv`.
- To list groups that include a country, use `csv/3. country_group_composition.csv`.
- To answer exact membership questions, prefer `csv/3. country_group_composition.csv` over inferred logic.

## Group Types

`csv/2. country_groups.csv` contains these group categories:

| Group type | Count |
|---|---:|
| Geographical Groups | 6 |
| Key aggregates | 11 |
| Other Groups | 5 |
| Other Regional Groups | 16 |
| WEO Analytical Groups | 11 |
| SPR PRGT Group | 2 |

## Common Aliases

Use exact codes when available. Otherwise use documented or helper-supported aliases, and return candidates when a phrase is ambiguous.

| User wording | Preferred WEO query |
|---|---|
| `US`, `USA`, `United States`, `United States of America`, `America` | `USA` |
| `mainland`, `mainland China`, `China mainland` | `CHN` |
| `Cote d'Ivoire`, `Côte d'Ivoire`, `Ivory Coast` | `CIV` |
| `AE`, `advanced economies` | `G110` |
| `EMDE`, `EMDEs`, `emerging market and developing economies` | `G200` |
| `LAC`, `Latin America and the Caribbean` | `G205` |
| `SSA`, `Sub-Saharan Africa` | `G603` |
| `Euro area`, `EA` | `G995` |
| `ASEAN-5`, `ASEAN 5` | `G510` |
| `European Union`, `EU` | `G998` |
| `World` | `G001` |

When a user phrase is ambiguous, list the plausible matches with `groupcode`, `groupcode_s`, and `groupname` before choosing one.

## WEO vs SPR AE, EM, and LIC Caveat

Clarify the source framework when a request involves advanced economies, emerging/developing economies, emerging markets, low-income countries, LICs, LIDCs, or PRGT groups.

WEO and SPR do not always use the same EM/LIC grouping definitions:

| Concept | WEO group | SPR/PRGT group |
|---|---|---|
| Advanced Economies | `G110` | `G110` |
| Developing Economies / EM | `G1201` | `G-PRGT-EM` |
| Low-Income Countries / LIC | `G201` | `G-PRGT-LIC` |
| EMDE | `G200` | `G-PRGT-EM` + `G-PRGT-LIC` |

Emerging Market and Developing Economies (EMDE) = WEO EM + WEO LIDC + Syria.  
WEO World = WEO AE + WEO EM + LIDC + Syria. 
WEO World = WEO AE + WEO EMDE. 
WEO World = SPR World = spr AE + spr EM + spr LIC. 


If the user asks for EM, EMDE, LIC, LIDC, PRGT, or developing-economy coverage without specifying WEO vs SPR/PRGT, ask which framework they mean before committing to a group. This distinction is important because both frameworks are IMF frameworks, but membership can differ by framework.

## Helper Script Usage

This helper is the capability map for WEO country, group, membership, and framework lookups. Consult it during task classification before writing temporary Python. The CSV files remain the source of truth.

Implementation files:

| File | Role |
|---|---|
| `scripts/weo_country_groups.py` | CLI entry point and user-facing commands. |
| `scripts/weo_country_groups_data.py` | CSV paths, alias dictionaries, explanations, and `CsvTables`. |
| `scripts/weo_country_groups_lookup.py` | Reusable lookup functions: aliases, country/group resolution, and group membership. |

### Core Navigation Map

| If the user wants to... | Use this helper command | Key input |
|---|---|---|
| Resolve ambiguous country/group wording | `resolve <query>` | `query` |
| Explain RA shorthand or framework caveats | `explain <term>` | `AE`, `EM`, `EMDE`, `LIC`, `LIDC` |
| List countries in a WEO or SPR/PRGT group | `members <group>` | `groupcode`, alias, or group name |
| List groups containing a country | `memberships <country>` | `countrycode`, alias, or country name |
| Expand a group for iData country selectors | `expand-for-idata <group> --codes-only` | `group` |
| Compare WEO vs SPR/PRGT group coverage | `compare <group_a> <group_b>` | two group terms |
| Search group metadata | `groups <query>` | group code/name/type |
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
  - **When to Trigger:** Use for WEO vs PRGT comparisons, especially `G201` vs `G-PRGT-LIC` and `G1201` vs `G-PRGT-EM`.

#### 3. iData Handoff Module

- **`expand-for-idata <group> --codes-only`**
  - **Core Utility:** Converts a group into comma-separated `countrycode` values.
  - **When to Trigger:** Use before data pulls that require selected countries.
  - **Operational Rule:** Do not pass `groupcode` or `groupcode_s` as an iData country selector unless dataset metadata explicitly supports that aggregate.

Examples:

```bash
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py resolve Congo
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py explain EM
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py compare G201 G-PRGT-LIC
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py expand-for-idata G200 --codes-only
```

### Anti-Patterns & Enforcement Rules

1. Do not write temporary code that reimplements alias matching, group membership expansion, or WEO vs PRGT comparison when a helper command covers the task.
2. Do not guess `countrycode`, `groupcode`, or `groupcode_s`; validate through the CSVs or helper output.
3. Do not pass raw non-English text, empty text, or highly informal wording directly to the helper; normalize to a likely English label or code first.
4. Do not use `groupcode` as a country selector for iData pulls; expand to member `countrycode` values first.

## Output Guidance

For country matches, return `countrycode`, `countryname`, and any relevant distinction note.

For group matches, return `groupcode`, `groupname`, `groupcode_s` when useful, and a note explaining whether the group is WEO, SPR/PRGT, regional, or analytical.

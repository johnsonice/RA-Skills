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

## Lookup Execution Policy

For WEO country and group questions, follow this policy:

1. Classify the task shape: exact lookup, fuzzy lookup, membership expansion, comparison, handoff preparation, validation, or data-pull setup.
2. Answer directly from the reference CSV/Markdown only for exact, small lookups.
3. For fuzzy, repeated, comparative, expansion, validation, or handoff tasks, check the helper command map before writing code.
4. Resolve ambiguous terms before running a helper. If multiple plausible matches exist, list candidates with codes and ask for confirmation before committing.
5. Use the most specific existing helper command for the task.
6. Write temporary code only when no helper command covers the task.
7. If a temporary-code pattern appears repeatedly, promote it into a helper command later.

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

Emerging Market and Developing Economies (EMDE) = EM + LIC.  
World = AE + EM + LIC.  
Syria is covered in the SPR/PRGT framework but excluded in the WEO framework.

If the user asks for EM, LIC, LIDC, PRGT, or developing-economy coverage without specifying WEO vs SPR/PRGT, ask which framework they mean before committing to a group. This distinction is important because membership can differ by framework.

## Helper Script Usage

Use `scripts/weo_country_groups.py` as a convenience helper for ambiguous, repeated, or processing-heavy lookups. When the helper has a command matching the task shape, prefer it over writing temporary Python. The CSV files remain the source of truth.

Before running the helper, normalize the user's wording to a canonical WEO code or exact English label when possible. Do not pass raw non-English text, empty text, or highly informal wording directly to the helper.

| User task | Preferred command |
|---|---|
| Find country or group candidates for an ambiguous term | `resolve <query>` |
| Explain RA shorthand such as EM, LIC, EMDE, AE | `explain <term>` |
| List countries in a group | `members <group>` |
| Compare two group definitions | `compare <group_a> <group_b>` |
| Expand a group to iData country selectors | `expand-for-idata <group> --codes-only` |
| List groups containing a country | `memberships <country>` |
| Search group metadata | `groups <query>` |
| Search country metadata | `countries <query>` |

Examples:

```bash
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py resolve Congo
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py explain EM
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py members G110
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py compare G201 G-PRGT-LIC
python3 .claude/skills/imf-ra/scripts/weo_country_groups.py expand-for-idata G200 --codes-only
```

## Output Guidance

For country matches, return `countrycode`, `countryname`, and any relevant distinction note.

For group matches, return `groupcode`, `groupname`, `groupcode_s` when useful, and a note explaining whether the group is WEO, SPR/PRGT, regional, or analytical.

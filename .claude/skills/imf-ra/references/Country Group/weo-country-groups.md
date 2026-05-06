# WEO Country Groups

Source files: the CSV files under [csv/](csv/) are the canonical WEO country-group reference tables for this skill.

Use this reference whenever a task mentions WEO country groups, WEO aggregates, WEO regions, WEO country codes, iData WEO groups, old WEO group codes, Group A, or Group A+.

## Source Scope

- Workbook note: the country groups were implemented during the April 2026 WEO exercise and are used to calculate aggregates in the WEO Live database.
- Last updated in workbook: April 16, 2026.
- The workbook also includes Group A and Group A+ countries, which are relevant to the WEO/CSD submission process but are not included in the WEO Live database.

## Code Systems

- `countrycode`: ISO-style 3-letter country or group code used by iData/WEO-style workflows, such as `USA`, `CHN`, `G001`, or `GX229`.
- `countrycode_s`: numeric WEO/legacy country code stored as text, such as `111` for the United States.
- `groupcode`: iData/WEO group code, usually beginning with `G` or `GX`.
- `groupcode_s`: numeric/legacy group code stored as text.
- Prefer `countrycode` and `groupcode` for new WEO Live/iData work unless the user or an old database explicitly asks for old numeric codes.

## CSV Tables

The previous workbook sheets are represented by these CSV files:

| Former workbook sheet | CSV file |
|---|---|
| `Information` | `csv/information.csv` |
| `1. Countries` | `csv/countries.csv` |
| `2. Country Groups` | `csv/country_groups.csv` |
| `3. Country Group Composition` | `csv/country_group_composition.csv` |
| `4. Group A and A+` | `csv/group_a_and_a_plus.csv` |
| `5. Group Dummies (iData)` | `csv/group_dummies_idata.csv` |
| `6. Group Dummies (old codes)` | `csv/group_dummies_old_codes.csv` |

1. `Information`
   - Source notes and workbook scope.

2. `1. Countries`
   - Master list of WEO Live countries.
   - Columns: `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, `department`.
   - Contains 198 country rows plus header.

3. `2. Country Groups`
   - Canonical list of key WEO country groups.
   - Columns: `grouptype`, `groupcode`, `groupname`, `groupcode_s`, `groupname_s`.
   - Contains 49 group rows plus header.

4. `3. Country Group Composition`
   - Long-form membership table for each group and country.
   - Columns: `groupcode`, `groupname`, `groupcode_s`, `groupname_s`, `countrycode`, `countryname`, `countrycode_s`, `countryname_s`.
   - Contains 1,945 membership rows plus header.
   - This is the safest table for answering "which countries are in group X?" and "which groups include country Y?"

5. `4. Group A and A+`
   - WEO/CSD submission groups.
   - Columns: `groupname`, `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, `department`.
   - Group A and Group A+ are not WEO Live aggregate groups.

6. `5. Group Dummies (iData)`
   - Wide country-by-group dummy matrix for iData/current group codes.
   - Columns start with `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, followed by group code columns such as `G001`, `G110`, `GX229`.
   - Cell value `1` means the country belongs to the group; blank means it does not.

7. `6. Group Dummies (old codes)`
   - Wide country-by-group dummy matrix for old numeric group-code naming.
   - Columns start with `countrycode`, `countryname`, `countrycode_s`, `countryname_s`, followed by columns like `grp_1`, `grp_110`, `grp_1218`.
   - Use only when old-code workflows require it.

## Group Types

The group-definition sheet contains these group categories:

- Geographical Groups: 6 groups.
- Key aggregates: 11 groups.
- Other Groups: 5 groups.
- Other Regional Groups: 16 groups.
- WEO Analytical Groups: 11 groups.

## Canonical Groups

| Group type | groupcode | groupname | groupcode_s | groupname_s |
|---|---:|---|---:|---|
| Geographical Groups | GX229 | Asia | 229 | Asia |
| Geographical Groups | GX1218 | Caribbean | 1218 | Caribbean |
| Geographical Groups | GX1212 | Central America | 1212 | Central America |
| Geographical Groups | GX970 | Europe | 970 | Europe |
| Geographical Groups | G92031 | North America | 92031 | North America (EXR) WEO |
| Geographical Groups | GX2041 | South America (WEO) | 2041 | South America (WEO) |
| Key aggregates | G110 | Advanced Economies | 110 | Advanced Economies |
| Key aggregates | G200 | Emerging Market and Developing Economies | 200 | Emerging Market and Developing Economies |
| Key aggregates | G505 | Emerging and Developing Asia | 505 | Emerging and Developing Asia |
| Key aggregates | G903 | Emerging and Developing Europe | 903 | Emerging and Developing Europe |
| Key aggregates | G995 | Euro Area (EA) - aggregate of member states | 995 | Euro area - aggregate of member country data |
| Key aggregates | G119 | G7 | 119 | G7 |
| Key aggregates | G205 | Latin America and the Caribbean (LAC) | 205 | Latin America and the Caribbean |
| Key aggregates | G400 | Middle East and Central Asia | 400 | Middle East and Central Asia |
| Key aggregates | GX123 | Other Advanced Economies (Advanced Economies excluding G7 and Euro Area countries) | 123 | Other Advanced Economies (Advanced Economies excluding G7 and Euro Area countries) |
| Key aggregates | G603 | Sub-Saharan Africa (SSA) | 603 | Sub-Sahara Africa |
| Key aggregates | G001 | World | 001 | World |
| Other Groups | G510 | ASEAN-5 | 510 | ASEAN-5 (new definition) |
| Other Groups | G1201 | Emerging Market and Middle-Income Economies | 1201 | Emerging Market and Middle-Income Economies |
| Other Groups | G998 | European Union (EU) | 998 | European Union |
| Other Groups | G711 | Heavily Indebted Poor Countries (HIPC) | 711 | Heavily Indebted Poor Countries (HIPC) |
| Other Groups | G201 | Low-Income Developing Countries (LIDC) | 201 | Emerging Market and Developing Economies: Low Income Developing Countries |
| Other Regional Groups | G202 | Advanced Asia | 202 | Advanced Asia |
| Other Regional Groups | G906 | Advanced Europe | 906 | Advanced Europe |
| Other Regional Groups | G940 | Caucasus and Central Asia (CCA) | 940 | Caucasus and Central Asia (CCA) |
| Other Regional Groups | G1515 | Emerging Asia | 1515 | Emerging Asia |
| Other Regional Groups | GX504 | Emerging and Developing Asia excl. China and India | 504 | Emerging and Developing Asia excl. China and India |
| Other Regional Groups | G401 | Middle East and Central Asia: Oil Exporters | 401 | Middle East and Central Asia: Oil Exporters |
| Other Regional Groups | G402 | Middle East and Central Asia: Oil Importers | 402 | Middle East and Central Asia: Oil Importers |
| Other Regional Groups | G406 | Middle East and North Africa (MENA) | 406 | Middle East and North Africa |
| Other Regional Groups | GX440 | Middle East, North Africa, Afghanistan, and Pakistan | 440 | Middle East, North Africa, Afghanistan, and Pakistan |
| Other Regional Groups | GX117 | Other Advanced Economies (Advanced Economies excluding U.S., Euro Area countries, and Japan) | 117 | Other Advanced Economies (Advanced Economies excluding U.S., Euro Area countries, and Japan) |
| Other Regional Groups | GX1518 | Other Emerging and Developing Asia | 1518 | Other Emerging and Developing Asia |
| Other Regional Groups | GX1603 | Sub-Sahara Africa Excluding South Sudan | 1603 | Sub-Sahara Africa Excluding South Sudan |
| Other Regional Groups | GX604 | Sub-Sahara excl. Nigeria and South Africa | 604 | Sub-Sahara excl. Nigeria and South Africa |
| Other Regional Groups | G1627 | Sub-Saharan Africa (SSA): Low-Income | 1627 | Sub-Saharan Africa: low-income |
| Other Regional Groups | G1626 | Sub-Saharan Africa (SSA): Middle-Income | 1626 | Sub-Saharan Africa: middle-income |
| Other Regional Groups | G1614 | Sub-Saharan Africa (SSA): Oil Exporters | 1614 | Sub-Saharan Africa: Oil Exporters |
| WEO Analytical Groups | G209 | EMDEs by External Financing: Net Creditors | 209 | Emerging Market and Developing Economies by External Financing: Net Creditors |
| WEO Analytical Groups | G606 | EMDEs by External Financing: Net Debtors | 606 | Emerging Market and Developing Economies by External Financing: Net Debtors |
| WEO Analytical Groups | G087 | EMDEs by External Financing: Net Debtors with Arrears and/or Reschedulings | 87 | Emerging Market and Developing Economies by External Financing: Net Debtors with Arrears and/or Rescheduling During 2019-23 |
| WEO Analytical Groups | G216 | EMDEs by Source of Export Earnings: Diversified | 216 | Emerging Market and Developing Economies by Source of Export Earnings: Diversified |
| WEO Analytical Groups | G080 | EMDEs by Source of Export Earnings: Fuel | 80 | Emerging Market and Developing Economies by Source of Export Earnings: Fuel |
| WEO Analytical Groups | G083 | EMDEs by Source of Export Earnings: Manufactures | 83 | Emerging Market and Developing Economies by Source of Export Earnings: Manufactures |
| WEO Analytical Groups | G092 | EMDEs by Source of Export Earnings: Nonfuel | 92 | Emerging Market and Developing Economies by Source of Export Earnings: Nonfuel |
| WEO Analytical Groups | G089 | EMDEs by Source of Export Earnings: Primary Products (excluding Fuel) | 89 | Emerging Market and Developing Economies by Source of Export Earnings: Primary Products (excluding Fuel) |
| WEO Analytical Groups | G084 | EMDEs by Source of Export Earnings: Services (including Income, Transfers) | 84 | Emerging Market and Developing Economies by Source of Export Earnings: Services (including Income, Transfers) |
| WEO Analytical Groups | GX88 | Emerging Market and Developing Economies by External Financing: Net Debtors without Arrears and/or Rescheduling During 2019-23 | 88 | Emerging Market and Developing Economies by External Financing: Net Debtors without Arrears and/or Rescheduling During 2019-23 |
| WEO Analytical Groups | GX93 | Emerging Market and Developing Economies by Source of Export Earnings: Nonfuel (excl. China) | 93 | Emerging Market and Developing Economies by Source of Export Earnings: Nonfuel (excl. China) |

## Lookup Rules

- For exact country membership, use `csv/country_group_composition.csv`.
- For exact groups containing a country, use `csv/country_group_composition.csv`.
- For canonical group names and code aliases, use `csv/country_groups.csv`.
- For WEO country code/name/department lookup, use `csv/countries.csv`.
- For current iData dummy matrices, use `csv/group_dummies_idata.csv`.
- For old numeric dummy matrices, use `csv/group_dummies_old_codes.csv`.
- If a user asks for Group A or Group A+, state that these are WEO/CSD submission groups, not WEO Live aggregate groups.
- If a group or country name is ambiguous, surface all plausible matches with `groupcode`, `groupcode_s`, and `groupname` before choosing one.

Use `scripts/weo_country_groups.py` as an optional convenience helper for repeated lookups, ambiguous name resolution, or processing-heavy filtering. The helper script recognizes common RA shorthand and maps it to the primary WEO group where appropriate:

| Shorthand | Primary groupcode |
|---|---:|
| AE, advanced economies | G110 |
| EMDE, EMDEs | G200 |
| LAC | G205 |
| MECA | G400 |
| SSA | G603 |
| ASEAN-5 | G510 |
| EU | G998 |
| EA, euro area | G995 |
| HIPC | G711 |
| LIC, LIDC | G201 |
| CCA | G940 |
| MENA | G406 |

# WEO Country Groups Reference

## Quick Start

**Use this reference** for WEO country codes, country groups, group memberships, and RA shorthand (e.g., `AE`, `EM`, `EMDE`, `LIC`, `LAC`, `SSA`, `ASEAN-5`).

### Critical Rules (Read First)
1. **Never invent country codes** — use `resolve` or lookup `country_group.csv`
2. **Never use group names as iData selectors** — expand to `countrycode` values first
3. **Always clarify WEO vs SPR/PRGT** when refering emerging market(EM/EMDE), low income(LIC/LIDC)  — membership definitions differ
4. **Always confirm IMF scope** — (191) sovereign vs (198) including territories

See **Commands Reference** below for full syntax and examples.

---

## Reference Data

**File:** [`country_group.csv`](country_group.csv) (201 rows, April 2026)

| Column | Type | Example | Purpose |
|---|---|---|---|
| `countrycode` | string | `USA`, `CHN` | iData selector |
| `countryname` | string | `United States` | Display |
| `department` | string | `WHD`, `APD` | Regional grouping |
| Group columns (6+) | `1`/blank | `Advanced Economies(AE)` | Membership flag |

**Key:** `1` = member of group; blank = non-member.

---

## Commands Reference

| Command | Parameters | Example | Use |
|---|---|---|---|
| `resolve` | `<QUERY>` | `resolve Congo` | Disambiguate country/group; returns single match or candidates |
| `explain` | `<TERM>` | `explain EM` | Document term across WEO/SPR frameworks |
| `members` | `<GROUP>` `[--codes-only]` | `members "Advanced Economies(AE)" --codes-only` | List all countries in a group (compact: `--codes-only`) |
| `memberships` | `<COUNTRY>` | `memberships USA` | List all groups containing a country |
| `expand-for-idata` | `<GROUP>` `--codes-only` | `expand-for-idata "EMDE" --codes-only` | Convert group to `+`-joined member codes for direct use as an iData dimension value |
| `compare` | `<GROUP_A>` `<GROUP_B>` | `compare "LIDC" "SPR-LIC"` | Compare group membership (WEO vs SPR/PRGT) |
| `groups` | `<QUERY>` | `groups "latin america"` | Search group metadata by keyword |
| `countries` | `<QUERY>` | `countries "united"` | Search country metadata by code/name/department |

---

## Critical Caveats

| ⚠️ Problem | Implication | Action |
|---|---|---|
| **WEO vs SPR/PRGT differ** | `EM` and `LIC` have different members in each framework. `EMDE` = `EM` + `LIC` + Syria in WEO; differs in SPR. | Ask: *"Which framework—WEO or SPR/PRGT?"* before committing to group membership. |
| **IMF scope ambiguity** | Two definitions: (191) sovereign members vs (198) including territories (Anguilla, Aruba, Curaçao, HK SAR, Macao SAR, Montserrat, Sint Maarten). WEO has 201 = 198 + Puerto Rico + Taiwan + West Bank/Gaza. | Ask: *"Do you mean 191 sovereign or 198 including territories?"* when user says "all IMF countries." |
| **iData rejects group names** | Group column names (e.g., `Advanced Economies(AE)`) are **not valid** iData country selectors. Most datasets require expanded codes. | Use `expand-for-idata <GROUP> --codes-only` to generate `+`-joined member codes ready for direct use as an iData dimension value. Exception: verify dataset metadata supports aggregates first. |
| **G20 scope ambiguity** | CSV stores 19 country-members. Official G20 also includes EU + African Union (21 total). | Ask: *"19 country-members or 21 including EU and AU?"* when user requests G20. |

---

## Usage Patterns (Common Scenarios)

---

### Pattern 1: Resolve Ambiguous Country
```
User: "Get me data for Congo"
You: "Congo is ambiguous. Let me check..."
$ resolve Congo
# Output: COG (Republic of Congo), COD (Democratic Republic of Congo)
Response: "I found two Congos: Republic of Congo (COG) or Democratic Republic of Congo (COD). Which do you need?"
```

### Pattern 2: Expand Group for iData Pull
```
User: "Pull data for all EMDE countries"
You: "Let me expand the EMDE group..."
$ expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only
# Output: AFG+ALB+DZA+...+ZWE  (160 codes, +-joined — paste directly into iData key)
Response: "EMDE contains 160 member countries. I'll use these codes directly as the iData country dimension value."
```

### Pattern 3: Compare WEO vs SPR Frameworks
```
User: "What's the difference between WEO and PRGT LIC definitions?"
You: "Let me show you..."
$ compare "Low-Income Developing Countries (LIDC)" "SPR-Low-Income Developing Countries (LIC)"
# Output: Counts, overlap, only-in-each list
Response: "WEO LIDC has X countries, SPR LIC has Y countries. They differ by Z countries: [list]."
```

### Pattern 4: List Country's Groups
```
User: "What groups does USA belong to?"
You: "Let me check USA's memberships..."
$ memberships USA
Response: "USA is in: Advanced Economies(AE), IMF member Countries(191), Americas (AMS), G7, and other groups [list]."
```

---

## Anti-Patterns ❌

| Anti-Pattern | Why It Fails | Solution |
|---|---|---|
| Hardcode alias mappings in temporary code | Duplicates source; breaks on update | Use `resolve` command |
| Guess country codes (e.g., invent `CONGO` for Congo) | Silent failures in pulls; hard to debug | Use `resolve` or CSV lookup |
| Pass group name directly to iData selectors | Most databases reject; data pull fails silently | Use `expand-for-idata` first |
| Assume WEO EM = SPR EM | Different definitions; wrong data set returned | Always ask user: which framework? |
| Not confirming IMF scope ("all IMF members") | Returns 191 or 198; user gets wrong count | Ask: 191 sovereign or 198 with territories? |
| Infer group membership from name | "Latin America" ≠ actual LAC membership | Use `members` command or CSV |
| Reimplement comparison logic (WEO vs SPR) | Code diverges from source; maintenance burden | Use `compare` command |

---

## FAQ

---

## Appendix: Alias Mappings

### Country Aliases (100+)
Refer to `COUNTRY_ALIASES` dict in [`country_groups_helper.py`](country_groups_helper.py) for comprehensive list. Common ambiguous forms:

| Ambiguous | Resolution | Code |
|---|---|---|
| `Congo`, `Congo-Brazzaville`, `Republic of Congo` | Use `resolve Congo` → pick | COG or COD |
| `Korea`, `South Korea` | Use `resolve Korea` | KOR |
| `UK`, `Great Britain` | Normalize | GBR |
| `US`, `USA`, `America` | Normalize | USA |
| `Democratic Republic of Congo` | Unambiguous | COD |

For full mapping, reference the Python script's `COUNTRY_ALIASES` dictionary.

### Group Aliases & Shorthand
Refer to `GROUP_ALIASES` dict in [`country_groups_helper.py`](country_groups_helper.py). Common shorthand:

| Input | Resolves To | Type |
|---|---|---|
| `AE` | `Advanced Economies(AE)` | WEO analytical |
| `EM` | `Emerging Market and Middle-Income Economies(EM)` | WEO analytical |
| `EMDE` | `Emerging Market and Developing Economies(EMDE)` | WEO analytical |
| `LAC` | `Latin America and the Caribbean (LAC)` | WEO regional |
| `SSA` | `Sub-Saharan Africa (SSA)` | WEO regional |
| `MENA` | `Middle East and North Africa (MENA)` | WEO regional |
| `CCA` | `Caucasus and Central Asia (CCA)` | WEO regional |
| `EA` / `Euro area` | `Euro Area (EA)` | WEO regional |
| `EU` | `European Union (EU)` | WEO regional |
| `G20` | `G20` | WEO analytical (19 countries) |
| `HIPC` | `Heavily Indebted Poor Countries (HIPC)` | WEO analytical |
| `SPR EM` / `PRGT EM` | `SPR-Emerging Market and Middle-Income Economies(EM)` | SPR/PRGT |
| `SPR LIC` / `PRGT LIC` | `SPR-Low-Income Developing Countries (LIC)` | SPR/PRGT |

For complete list, reference the Python script's `GROUP_ALIASES` and `AMBIGUOUS_GROUP_ALIASES` dictionaries.

---

**Q: How do I confirm a country belongs to a group?**  
A: Use `members <GROUP>` or filter the group column in `country_group.csv` to rows marked `1`.

**Q: Why do WEO EM and SPR EM have different countries?**  
A: Different analytical frameworks have different membership criteria. Always confirm which the user needs.

**Q: Can I use "Advanced Economies(AE)" directly in an iData pull?**  
A: Only if the dataset metadata explicitly supports aggregate codes. Usually, no. Use `expand-for-idata` to generate member codes instead.

**Q: What's the difference between the 19-country and 21-member G20?**  
A: The CSV stores 19 country-members. Officially, the G20 also includes EU and African Union as institutional participants. Clarify with user which they need.

**Q: The helper returned "no match" for a country. What now?**  
A: The country is either not in WEO Live or uses a different name form. Check alternate spellings or ask the user for clarification.

**Q: When should I use `countrycode_s` instead of `countrycode`?**  
A: Only when the user or dataset explicitly requires internal numeric codes (rare). Use `countrycode` by default.

**Q: How do I list all countries in a group without seeing the full table?**  
A: Use `members <GROUP> --codes-only` for a concise comma-separated list.

---

## Implementation

| File | Purpose | Role |
|---|---|---|
| `country_group.csv` | Consolidated country + group matrix | Single source of truth |
| `country_groups_helper.py` | CLI helper script | Resolves ambiguity, expands groups, compares frameworks |
| `country_groups_instruction.md` | This reference (you are here) | Guide for agents and manual lookup |

### Helper Script Features
- **Alias resolution:** Maps 100+ country/group aliases to official codes
- **Membership queries:** Lists exact members by group or groups by country
- **iData expansion:** Converts groups to code lists ready for data pulls
- **Framework comparison:** Shows WEO vs SPR/PRGT differences
- **CSV loading:** Fast, no dependencies; runs offline

---


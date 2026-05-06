# Dimension Resolution Guide

How to go from a confirmed catalog identifier to a fully-resolved iData key, ready for `fetch_idata.py`.

This guide assumes **`imf-ra-catalog`** has already returned a confirmed `(database_id, indicator_code)`. If the identifier is not yet known, invoke `imf-ra-catalog` first — do not begin here.

---

## Reference sources

| Source | Purpose |
|---|---|
| `idata_utilities.get_dimensions(db)` | Returns every dimension name and valid code set for the confirmed database, in key order. |
| `idata_utilities.get_dimension_values(db, dim, keyword=[...])` | Filters valid codes for a dimension by keyword — useful for large country lists. |
| `imf-ra-catalog` | Resolves database and indicator from plain-English descriptions. Consult before this guide if the identifier is unknown. |
| `imf-ra` conventions | Country codes, frequency codes, and uncertainty policy. Load before resolving country/frequency dimensions. |

---

## 1. Lookup path

Follow this sequence after catalog handoff — do not skip steps.

**Step A — Fetch database dimensions**

Call the SDK to get all dimension names and valid codes for the confirmed database:

```python
from imf_datatools import idata_utilities
dims = idata_utilities.get_dimensions("<database_id>")
```

Read every dimension name and code set from the result. Do **not** rely on memory or hardcoded lists — always use the API response.

**Step B — Identify unresolved dimensions**

Compare what the user has specified against the dimensions returned. Required inputs for a complete key:

- `start` / `end` — time range
- one value per dimension (e.g. `COUNTRY`, `INDICATOR`, `DATA_TRANSFORMATION`, `FREQUENCY`) — exact names vary by database

The `INDICATOR` value comes from the catalog handoff (`indicator_code`). Slot it into the key at its position in the dimension order returned by `get_dimensions()`.

---

## 2. Auto-resolve vs. ask-user rules

| Situation | Action |
|---|---|
| Dimension has exactly one valid value | Auto-resolve silently; use that value without asking |
| User already specified the dimension | Use the user's value; validate it appears in the API response |
| Dimension has multiple values and user did not specify | **Ask the user** — show the available codes and labels from the API |

**Never guess or hardcode a dimension value.**

For country and group dimensions, translate RA-friendly names ("advanced economies", "G7", "EMDE") through `imf-ra` conventions before presenting or validating codes.

---

## 3. How to ask the user (template)

When one or more dimensions are unresolved, reply with:

1. What you found: database name, indicator code and description.
2. What you still need: one question per unresolved dimension, listing the codes and labels from the API response.

Example structure (fill in actual codes from the API response):

> I found **[indicator name]** (`[INDICATOR_CODE]`) in database `[DB_ID]`, covering [period].
>
> Before I pull the data, I need a few more details:
>
> **1. [Dimension name]** — which would you like?
> - `CODE_A` — Label A
> - `CODE_B` — Label B
> - `CODE_C` — Label C
>
> **2. [Dimension name]** — how often?
> - `CODE_X` — Label X
> - `CODE_Y` — Label Y

If the user asks "what does X mean?" or "what options are there?", answer from the API response values and then ask again for their choice.

---

## 4. Key format — dimension order

The iData key is a dot-separated string of dimension values in the exact order the database defines its dimensions. Use the dimension order from the `get_dimensions()` result already fetched in Step A — do not make a new API call here.

### Key construction rules

- Leave a dimension blank (consecutive dots) to select all available values for that dimension.
- Combine multiple values within one dimension with `+` (e.g. `AAA+BBB.INDICATOR.FREQ`).
- The number of dot-separated fields must match the total number of dimensions — do not add extra dots.

---

## 5. Execute via the pre-built fetch utility

Once every dimension is resolved and the key is built, call `fetch_idata.py` via Bash. **Never create a new Python script.**

```bash
python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
    --db "<database_id>" \
    --key "<dot.separated.key>" \
    --start "<YYYY>" \
    --end "<YYYY>"
```

**Default output:** wide RA Excel (`.xlsx`) saved to `idata_YYYYMMDD_HHMMSS.xlsx`.

Column layout:

| Column | Source |
|---|---|
| `CountryName` | Looked up from `imf-ra` `countries.csv` using ISO3 |
| `ISO3` | COUNTRY dimension value from iData |
| `IFSCODE` | Looked up from `imf-ra` `countries.csv` (`countrycode_s`) |
| `DATASET` | The `--db` argument |
| `Series_Code` | Non-country, non-indicator dimensions joined with `.` |
| `INDICATOR` | INDICATOR dimension value |
| `2019`, `2019Q1`, `2019M1` … | Pivoted date columns (format matches frequency) |

Optional overrides:
- `--output results.xlsx` — use a specific output filename.
- `--longformat` — save raw long/tidy CSV instead of the RA wide Excel format.

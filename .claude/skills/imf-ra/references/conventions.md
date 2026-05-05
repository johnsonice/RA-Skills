# Shared conventions

Cross-cutting conventions referenced by every worker skill in the IMF RA family. Fill in real content as it becomes available; sections are placeholders so workers can already link here.

## Internal Python SDK

> _Placeholder._ When the SDK identity is confirmed, document:
> - Package name and install path.
> - Import convention (e.g., `import imf_sdk as imf`).
> - Environment variables required (auth tokens, default endpoint).
> - One-line "hello world" pull to verify the install.

## Country and country-group codes

For WEO country groups and WEO Live aggregates, use [Country Group/weo-country-groups.md](Country%20Group/weo-country-groups.md) and the workbook `Country Group/WEO Countries and Country Groups 2026.xlsx`.

- Prefer `countrycode` and `groupcode` for current WEO Live/iData workflows.
- Use `countrycode_s` and `groupcode_s` only when the user or an old database workflow explicitly asks for numeric/legacy codes.
- Translate RA-friendly names such as "advanced economies", "EMDE", "G7", "LAC", "SSA", or "ASEAN-5" through the WEO group reference instead of guessing.
- For exact membership, use the workbook's long-form `3. Country Group Composition` sheet or `scripts/weo_country_groups.py`.
- Group A and Group A+ are WEO/CSD submission-process groups, not WEO Live aggregate groups.

## Frequencies

> _Placeholder._ Document:
> - How the SDK encodes A/Q/M.
> - Conventions for quarter labels (`2010Q1` vs. `2010-Q1` vs. `2010-03-31`).
> - When to convert frequencies and which method to use.

## Dates

> _Placeholder._ Document:
> - Default date range conventions (e.g., "2010-present" → start=`2010`, end=`null`).
> - How to handle release-vintage dates vs. data-period dates.

## Units

> _Placeholder._ Document:
> - Common unit conventions in IMF databases (USD billions, percent of GDP, index 2010=100).
> - Where the unit metadata lives in the SDK return.

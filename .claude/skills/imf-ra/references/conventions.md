# Shared conventions

Cross-cutting conventions referenced by every worker skill in the IMF RA family. Fill in real content as it becomes available; sections are placeholders so workers can already link here.

## Internal Python SDK

> _Placeholder._ When the SDK identity is confirmed, document:
> - Package name and install path.
> - Import convention (e.g., `import imf_sdk as imf`).
> - Environment variables required (auth tokens, default endpoint).
> - One-line "hello world" pull to verify the install.

## Country and country-group codes

> _Placeholder._ Document:
> - Which code system to prefer (ISO 3166 alpha-3 vs. IMF country codes).
> - How to translate between RA-friendly names ("G20", "advanced economies") and the SDK's group identifiers.

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

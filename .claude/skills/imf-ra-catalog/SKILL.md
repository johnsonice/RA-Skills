---
name: imf-ra-catalog
description: Use when the user describes data they want in plain English ("current account balance for advanced economies, quarterly") and needs to find the right database and indicator. Covers catalog browsing, keyword search across databases and curated overlays, and returns top-N candidates with notes when the description is ambiguous.
---

# IMF RA — Catalog

Translating plain-English descriptions into a stable identifier tuple `(database, series, frequency, geo)`.

## Before you search

See the umbrella `imf-ra` for shared conventions (country and country-group codes especially).

## Two layers

The catalog has two complementary layers, both under this skill folder:

- **`databases/<name>.md`** — one file per database (WEO, IFS, BOPS, GFS, DOTS, FSI, …). Schema in [databases/_template.md](databases/_template.md). v1 ships placeholder examples; real content fills in iteratively.
- **`overlays/<topic>.md`** — curated institutional knowledge that augments or corrects the database files. Schema in [overlays/_template.md](overlays/_template.md). Overlays take precedence on conflict.

See [references/catalog-conventions.md](references/catalog-conventions.md) for the schemas and how the layers interact.

## Search workflow

1. **First pass:** grep across `databases/` and `overlays/` for keywords from the user's description. Overlay match takes precedence.
2. **Fallback:** if grep returns nothing useful, surface the gap to the RA — say "this concept isn't in the catalog yet, do you have a hint?". Do **not** invent a series identifier.
3. **Output:** top-N candidates with confidence/notes, never a single committed pick. The RA selects.

## Handoff

Once the RA confirms an identifier, hand off to `imf-ra-data` for the fetch.

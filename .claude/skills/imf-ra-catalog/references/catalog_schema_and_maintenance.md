# Catalog Schema And Maintenance

This reference supplements `../SKILL.md`. Keep lookup behavior, routing, and output policy in `../SKILL.md`; use this file only for CSV schemas and catalog maintenance conventions. The file lists that use these schemas are documented in `../SKILL.md`.

## CSV Schemas

Dataset catalog columns:

| Column | Meaning |
|---|---|
| `database` | Joined `Agency ID:Resource ID` identifier. |
| `name` | Human-readable dataset name. |
| `Agency ID` | SDMX agency or provider ID. |
| `Resource ID` | Dataset or dataflow resource ID. |
| `Latest Version` | Latest source-catalog version. |
| `Unique ID` | Exact agency/resource/version identifier. |

Indicator catalog columns:

| Column | Meaning |
|---|---|
| `database_name` | Dataset identifier that contains the code. |
| `dimension_name` | Dimension to fill in downstream fetch requests. |
| `Code` | Variable, indicator, commodity, or dimension value code. |
| `Name` | Human-readable description of the code. |

## Maintenance Notes

- Keep `database_overview.md` concise and database-family oriented; do not duplicate long indicator lists there.
- Add focused Markdown notes only when raw CSV rows are insufficient for reliable selection.
- If a new specialized indicator catalog is added, document its lookup behavior in `../SKILL.md` and its schema here if it differs from the standard indicator schema.
- If file names move, update `../scripts/catalog_search.py` and run the reference checker.

## Focused Markdown Notes

Use additional Markdown only for guidance that cannot be captured well in CSV rows.

| Location | Use |
|---|---|
| `../databases/<name>.md` | Dataset-specific caveats, dimension conventions, frequency notes, or common mappings. |
| `../indicators/<topic>.md` | Concept-specific guidance, naming ambiguity, unit caveats, or preferred-code notes. |
| `../overlays/<topic>.md` | Optional institutional guidance that augments or overrides raw catalog rows. |

Curated Markdown can guide interpretation, candidate ranking, and caveats, but CSV rows remain authoritative for actual identifiers.

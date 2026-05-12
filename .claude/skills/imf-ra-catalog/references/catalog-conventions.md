# Catalog Conventions

This reference supplements `../SKILL.md`. Keep operational policy in `SKILL.md`; use this file for catalog organization, file naming, and maintenance conventions.

## File Layout

The catalog is organized into dataset-level references and indicator-level references.

### Dataset References

| File | Contents |
|---|---|
| `../databases/non_vintaged_datasets.csv` | Default non-vintage dataset/dataflow catalog. |
| `../databases/vintaged_datasets.csv` | Vintage-only dataset/dataflow catalog. |
| `../databases/database_overview.md` | Curated high-level summaries for major database families. |

Dataset CSV columns:

| Column | Meaning |
|---|---|
| `database` | Joined `Agency ID:Resource ID` identifier. |
| `name` | Human-readable dataset name. |
| `Agency ID` | SDMX agency or provider ID. |
| `Resource ID` | Dataset or dataflow resource ID. |
| `Latest Version` | Latest source-catalog version. |
| `Unique ID` | Exact agency/resource/version identifier. |

### Indicator References

| File | Contents |
|---|---|
| `../indicators/1. non_vintage_variable_list.csv` | General non-vintage variable catalog. |
| `../indicators/2. bbg_variable_list.csv` | Bloomberg-specific variable catalog. |
| `../indicators/3. wdi_variable_list.csv` | World Bank WDI-specific variable catalog. |
| `../indicators/4. wto_variable_List.csv` | WTO-specific variable and commodity-code catalog. |

Indicator CSV columns:

| Column | Meaning |
|---|---|
| `database_name` | Dataset identifier that contains the code. |
| `dimension_name` | Dimension to fill in downstream fetch requests. |
| `Code` | Variable, indicator, commodity, or dimension value code. |
| `Name` | Human-readable description of the code. |

## Maintenance Notes

- Treat CSV files as the source of truth for identifiers.
- Keep `database_overview.md` concise and database-family oriented; do not duplicate long indicator lists there.
- Add focused Markdown notes only when raw CSV rows are insufficient for reliable selection.
- If a new specialized indicator catalog is added, document it in both this file and `../SKILL.md`.
- If file names move, update `../scripts/catalog_search.py` and run the reference checker.

## Focused Markdown Notes

Use additional Markdown only for guidance that cannot be captured well in CSV rows.

| Location | Use |
|---|---|
| `../databases/<name>.md` | Dataset-specific caveats, dimension conventions, frequency notes, or common mappings. |
| `../indicators/<topic>.md` | Concept-specific guidance, naming ambiguity, unit caveats, or preferred-code notes. |
| `../overlays/<topic>.md` | Optional institutional guidance that augments or overrides raw catalog rows. |

When curated Markdown conflicts with raw CSV search results, follow the curated guidance and explain the reason briefly in the user-facing answer.

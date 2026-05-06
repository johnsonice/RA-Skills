# Shared conventions

Cross-cutting conventions referenced by every worker skill in the IMF RA family.

## When to write code

If the task can be completed by reading through the given files, answer from those files without writing code. Write code only when the task requires complex processing logic, calculation, or transformation that is impractical to do reliably by inspection.

## Uncertainty and confirmation

If there is any material uncertainty, do not guess. Ask the user to confirm before committing to one interpretation, code, group, or dataset choice.

If search or lookup results produce several plausible "best match" candidates, list the candidates clearly and ask the user for preference/confirmation.

## Country and country-group codes

For WEO country groups and WEO Live aggregates, use [Country Group/weo-country-groups.md](Country%20Group/weo-country-groups.md) and the CSV files under `Country Group/csv/`.

- Prefer `countrycode` and `groupcode` for current WEO Live/iData workflows.
- Use `countrycode_s` and `groupcode_s` only when the user or an old database workflow explicitly asks for numeric/legacy codes.
- Translate RA-friendly names such as "advanced economies", "EMDE", "G7", "LAC", "SSA", or "ASEAN-5" through the WEO group reference instead of guessing.
- For exact membership, use `Country Group/csv/country_group_composition.csv`; use `scripts/weo_country_groups.py` only as an optional helper for ambiguous, repeated, or processing-heavy lookups.
- Group A and Group A+ are WEO/CSD submission-process groups, not WEO Live aggregate groups.

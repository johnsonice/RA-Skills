# Shared conventions

Cross-cutting conventions referenced by every worker skill in the IMF RA family.

## When to write code

If the task can be completed by reading through the given files, answer from those files without writing code. Write code only when the task requires complex processing logic, calculation, or transformation that is impractical to do reliably by inspection.

## Uncertainty and confirmation

If there is any material uncertainty, do not guess. Ask the user to confirm before committing to one interpretation, code, group, or dataset choice.

If search or lookup results produce several plausible "best match" candidates, list the candidates clearly and ask the user for preference/confirmation.

## Country and country-group codes

For WEO country groups and WEO Live aggregates, use [Country Group/weo-country-groups.md](Country%20Group/weo-country-groups.md) and the CSV files under `Country Group/csv/`.

- Translate RA-friendly names such as "advanced economies", "EMDE", "G7", "LAC", "SSA", or "ASEAN-5" through the WEO group reference instead of guessing.
- For exact membership, use `Country Group/csv/3. country_group_composition.csv`.
- Before using `scripts/weo_country_groups.py`, normalize the user's wording to a canonical WEO `countrycode`, `groupcode`, or exact English label using the WEO reference material.
- Use the helper script only as an optional accelerator for ambiguous, repeated, or processing-heavy lookups.
- For selected-country iData pulls, prefer ISO-style WEO `countrycode` values such as `USA`, `CHN`, and `JPN` unless the target dataset metadata requires a different country dimension value.
- groupcode or groupcode_s which are used and refered in country_groups.csv and country_group_composition.csv should only used for country-group mapping. DON'T use it when pulling data becasue idata tools doesn't use these groupcode.
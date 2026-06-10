# Comments Log

Date: 2026-05-09

## 1. Refreshable Excel column order

- Current order: `CountryName`, `ISO3`, `IFSCODE`, `DATASET`, `Series_Code`, `INDICATOR`
- Comment: Generally, people tend to put `DATASET` as the first column.

## 2. Country-group download behavior

- Bug: When asked to download a group of countries, the workflow can mistakenly use an aggregate/group identifier as if it were an iData country selector.
- Comment: In most cases, this is not what people want. They usually want the member-country panel, not the aggregate/group code series.
- Current design note: use `.claude/skills/imf-ra/Country Group/weo_country_groups.py expand-for-idata ... --codes-only` against the unified `Country Group.csv` file before any iData fetch.

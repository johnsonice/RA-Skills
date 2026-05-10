# Comments Log

Date: 2026-05-09

## 1. Refreshable Excel column order

- Current order: `CountryName`, `ISO3`, `IFSCODE`, `DATASET`, `Series_Code`, `INDICATOR`
- Comment: Generally, people tend to put `DATASET` as the first column.

## 2. Country-group download behavior

- Bug: When asked to download a group of countries, the workflow often uses a country group code such as `COUNTRY=G200` (EMDEs) to formulate the series code.
- Comment: In most cases, this is not what people want. They usually want the member-country panel, not the aggregate/group code series.

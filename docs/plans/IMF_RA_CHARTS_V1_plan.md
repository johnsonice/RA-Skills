# IMF RA Charts V1 Plan

## Purpose

Design `imf-ra-charts` as the chart-production worker in the RA Skills family.
This is a planning document only; it is not yet the final `SKILL.md`.

V1 should let an agent turn confirmed data into a useful economics/research
chart, while preserving enough evidence to reproduce the output later.

## V1 Scope

V1 includes:

- Charting data fetched through `imf-ra-data`.
- Charting user-provided Excel or CSV data.
- Cleaning and transforming data into chart-ready shape.
- Recommending a reasonable chart type when the user does not specify one.
- Creating a PNG as the primary chart output.
- Saving a lightweight reproducibility package for every PNG.
- Offering an optional editable Excel workbook after the PNG is ready.
- Applying user-requested formatting refinements, as long as they do not require
  full IMF house-style implementation.

V1 excludes:

- Mimicking a user-provided example chart.
- Full IMF styling or publication-grade house-style templates.
- PPT deck generation.
- Interactive dashboards.
- New database or API retrieval logic.
- A large custom charting framework.

## Standard Output Contract

Every successful V1 chart request produces a PNG as the required primary output.

Every successful V1 chart request also saves a lightweight reproducibility
package in the confirmed output folder:

- the PNG;
- the chart-ready data used to generate the PNG;
- the chart spec;
- the Python script that generated the PNG.

The Excel workbook is optional. After providing the PNG, ask:

```text
Would you like an editable Excel workbook with the chart data and embedded chart?
```

Only create the Excel workbook if the user says yes.

## Output Folder Convention

Before writing chart artifacts, ask the user to confirm that outputs should be
saved under a temporary folder named `chart-temp/`.

After confirmation, create `chart-temp/` in the current working directory and
save all chart artifacts there. Do not create or overwrite `chart-temp/` without
user confirmation.

Use stable, readable, lowercase file names based on the chart topic:

```text
chart-temp/
  real_gdp_growth_selected_economies.png
  real_gdp_growth_selected_economies_chart_ready.csv
  real_gdp_growth_selected_economies_chart_spec.csv
  real_gdp_growth_selected_economies_generate.py
  real_gdp_growth_selected_economies.xlsx
```

If a file already exists, avoid accidental overwrite by adding a version suffix,
such as `_v2`, unless the user explicitly asks to replace the prior output.

## Backend Decisions

Preferred V1 implementation stack:

| Need | V1 choice | Reason |
|---|---|---|
| Data cleaning and transformation | Python `pandas` | Standard for tabular data cleaning, reshaping, type conversion, and basic transformations. |
| PNG chart generation | Python `matplotlib` | Stable, suitable for static economics/research charts, and does not require an interactive rendering stack. |
| Excel workbook generation | Python `xlsxwriter` | Strong for creating new Excel workbooks with multiple sheets, formatting, and embedded charts. |
| Embedded Excel chart | `xlsxwriter` chart object linked to `chart_ready` | Keeps the workbook editable and auditable because the chart is tied to the visible chart-ready table. |

If a confirmed internal IMF charting tool later supports PNG and workbook
generation, it can become the preferred backend. Until then, V1 should use the
Python stack above.

## Input Paths

### Path A: Data From `imf-ra-data`

When data have already been fetched by `imf-ra-data`, `imf-ra-charts` should:

- read the tidy or refreshable output;
- preserve source fields such as database, indicator, unit, frequency, vintage,
  geography, and time period when present;
- validate that the data are chartable;
- transform into chart-ready data;
- generate the PNG and reproducibility package;
- offer the optional Excel workbook.

If the user asks for a chart but data are not fetched yet, ask for the data
source. If the user asks the agent to pull data first, chain backward:

```text
imf-ra-charts -> imf-ra-data -> imf-ra-catalog, if identifiers are unresolved
```

### Path B: User-Provided Excel Or CSV

When the user provides raw Excel or CSV data, `imf-ra-charts` should:

- inspect the file structure and available columns;
- infer likely time, geography, series, value, unit, and source fields;
- ask clarification only when required fields are ambiguous or unsafe;
- preserve the original data for optional workbook export;
- create standardized clean and chart-ready data;
- generate the PNG and reproducibility package;
- offer the optional Excel workbook.

## Execution Flow

1. Confirm the output folder before writing artifacts.
2. Load data from `imf-ra-data` output or user-provided Excel/CSV.
3. Inspect columns, data types, grain, units, source, frequency, and date range.
4. Ask clarification only if the chart would otherwise be wrong or misleading.
5. Clean and transform data according to the transformation policy.
6. Choose a chart type from user instruction or chart recommendation rules.
7. Generate an initial reasonable PNG.
8. Run chart QA before delivery.
9. Save the reproducibility package.
10. Show or link the PNG to the user.
11. Offer the optional Excel workbook.
12. If the user requests changes, update the chart and version or overwrite
    outputs according to the file naming rule.

## Data Cleaning

V1 should support common chart-preparation steps:

- Normalize dates or periods.
- Convert values to numeric.
- Standardize country, group, and series labels.
- Reshape long data to wide chart-ready data when useful.
- Reshape wide data to long clean data when useful.
- Sort time periods and categories.
- Drop or flag empty observations.
- Preserve missing values intentionally rather than hiding them silently.
- Apply transformations according to the V1 transformation policy.

When transformations are applied, record them in the chart spec.

## Transformation Policy

V1 uses a three-tier transformation policy.

### Tier 1: Safe To Infer Automatically

These are data-preparation transformations. The agent may apply them without
separate confirmation when they are needed to make the data chartable:

- Parse dates and periods, such as `2020`, `2020Q1`, or `Jan-2020`.
- Convert numeric strings to numbers.
- Sort time or category axes.
- Rename columns into standard fields, such as `country`, `time`, `value`, and
  `series`.
- Drop fully empty rows or columns.
- Trim labels and standardize obvious whitespace.
- Reshape long data to wide chart-ready data when useful.
- Reshape wide data to long clean data when useful.
- Create a forecast or estimate flag when the source has clear status labels.
- Filter to requested countries, indicators, dates, or series.
- Select the latest available observation when the user asks for a latest-period
  comparison.

### Tier 2: Suggest Or Ask For Confirmation First

These transformations change the analytical meaning of the data. The agent may
suggest them, but should ask for user confirmation before applying them:

- Percent change or growth rate.
- Year-over-year or quarter-over-quarter change.
- Index to 100.
- Difference from benchmark.
- Difference from previous period.
- Share of GDP.
- Per-capita transformation.
- Rolling average.
- Real versus nominal adjustment.
- Currency or unit scaling, such as millions to billions.
- Aggregating countries into groups.
- Ranking or top-N selection when the user did not specify `N`.
- Normalizing countries or series to a common start year.
- Combining multiple indicators into one derived metric.

### Tier 3: Only When Explicitly Requested

These transformations require explicit user request and enough assumptions or
input data to avoid misleading output:

- Forecasting or extrapolation.
- Seasonal adjustment.
- Deflation or inflation adjustment using another series.
- Rebaselining with a non-obvious base period.
- Outlier removal or winsorization.
- Imputation or interpolation of missing values.
- Weighting and weighted aggregates.
- Contribution calculations.
- Decomposition charts.
- Regression or fitted lines.
- Smoothing beyond a simple rolling average.
- Currency conversion using exchange rates.
- Any transformation requiring another dataset.

## Clarification Policy

Only ask for clarification when needed to avoid a wrong or misleading chart.
Otherwise, create the best reasonable default chart and explain the choice
briefly.

Ask before charting when:

- there is no clear value column;
- there is no clear time, category, or geography axis;
- multiple plausible indicators or series could answer the request;
- units or frequencies are incompatible;
- the requested chart would require a Tier 2 or Tier 3 transformation;
- the requested chart type would be unreadable for the number of series;
- the data source is missing and the user has not asked the agent to fetch data.

## Chart Recommendation Rules

Use the user's stated chart type when provided and safe. If the user does not
specify a chart type, recommend and use a simple research-appropriate default
based on the indicator, data shape, and research purpose.

| Data Shape | Default Chart |
|---|---|
| One time series | Line chart |
| Several comparable time series | Multi-line chart |
| Many countries over time | Small multiples or filtered multi-line chart |
| Latest cross-country comparison | Sorted bar chart |
| Two numeric variables by country | Scatter plot |
| Additive components over time | Stacked bar or stacked area, only if units are additive |
| Ranking over one period | Horizontal bar chart |

By default, create an initial reasonable plot rather than over-asking. If the
user gives formatting preferences up front, apply them before the first chart.
If the user asks for changes after seeing the chart, update the chart.

## PNG Requirements

The PNG should include:

- clear title;
- axis labels with units;
- readable legend or direct labels;
- source note when known;
- footnote for forecasts, vintages, or transformations when relevant.

V1 does not need full IMF house styling, but it should still be clean,
professional, and readable.

Default visual style:

- white background;
- restrained, readable color palette;
- clear title and subtitle when useful;
- light gridlines only when they help reading values;
- readable legend or direct labels;
- source note at the bottom when known;
- sorted bars for cross-sectional comparisons;
- no decorative effects that distract from the data.

## Chart QA Before Delivery

Before delivering the PNG, verify:

- the chart is not blank;
- title, units, and source notes are present when available;
- labels and legend are readable;
- the legend does not cover the data;
- axes are not misleading for the chart type;
- bars or categories are sorted when sorting improves interpretation;
- too many series are not squeezed into one unreadable chart.

## Chart Spec Format

The chart spec should use a table shape. In the reproducibility package, save it
as `*_chart_spec.csv`. If the user requests the optional Excel workbook, include
the same table as the `chart_spec` sheet.

Use a simple two-column structure:

| field | value |
|---|---|
| `chart_type` | `line` |
| `title` | `Real GDP Growth` |
| `subtitle` | `Annual percent change, 2019-2025` |
| `x_axis` | `time` |
| `y_axis` | `value` |
| `series` | `country` |
| `unit` | `Percent change` |
| `source` | `IMF, World Economic Outlook` |
| `transformation` | `none` |
| `footnote` | `2025 values are forecasts.` |

A separate JSON chart spec can be added later if automated testing or downstream
tooling needs it, but JSON is not required for V1.

## Optional Excel Workbook

Only create the Excel workbook if the user confirms they want it.

Required sheets:

| Sheet | Purpose |
|---|---|
| `raw_data` | The original pulled or uploaded data, preserved as much as practical. |
| `clean_data` | Normalized and cleaned data with consistent field names and types. |
| `chart_ready` | The exact table used by the chart. This should be easy to inspect and edit. |
| `chart` | An embedded Excel chart linked to `chart_ready`. |

Recommended additional sheets:

| Sheet | Purpose |
|---|---|
| `chart_spec` | Chart type, title, subtitle, axis fields, units, source, footnotes, and transformations. |
| `QA_checks` | Checks for duplicates, missing values, numeric conversion, date consistency, units, and source notes. |

Excel requirements:

- Preserve original data separately from cleaned data.
- Make `chart_ready` obvious and compact.
- Include an embedded chart linked to `chart_ready`.
- Include source and transformation notes.
- Use stable sheet names so future tests and downstream tools can inspect it.
- Avoid hiding important logic in formatting alone.

## Failure Behavior

If chart generation fails, do not pretend the chart was created. Tell the user:

- what failed;
- whether the data were cleaned successfully;
- what output, if any, was saved;
- what input, confirmation, or environment fix is needed next.

If the failure happens after data cleaning, the agent may offer a diagnostic
Excel workbook or chart-ready CSV, but should only create optional files if the
user confirms.

## Suggested Implementation Sequence

1. Finalize this V1 plan.
2. Update `skills/imf-ra-charts/SKILL.md` with the V1 workflow.
3. Expand `skills/imf-ra-charts/references/chart-tool-usage.md` with the PNG,
   reproducibility package, and optional Excel contract.
4. Add chart behavior test cases to `tests/auto_test_cases.yaml` only after the
   chart workflow is live enough to test.
5. Mirror reviewer-facing test descriptions in `tests/auto_test_instructions.md`
   when chart cases are added.
6. Run `python scripts/sync_skills.py` after updating the actual skill.

## Success Criteria

V1 is successful when a user can ask for a chart and receive:

- a PNG chart they can immediately inspect or use;
- a reproducibility package containing chart-ready data, chart spec, and the
  Python generation script;
- an offer to create an optional Excel workbook containing `raw_data`,
  `clean_data`, `chart_ready`, and an embedded chart;
- a clear record of source, units, and transformations;
- sensible chart choices when the user does not specify a chart type;
- safe clarification behavior when the data are ambiguous or misleading.

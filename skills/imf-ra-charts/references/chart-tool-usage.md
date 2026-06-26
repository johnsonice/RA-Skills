# Chart Workflow And Output Contract

This file is the V1 operating contract for `imf-ra-charts`. The skill produces
static PNG charts through Python, not an internal charting tool.

## Scope

V1 includes:

- charting data fetched through `imf-ra-data`;
- charting user-provided Excel or CSV data;
- cleaning and transforming data into a plotting-ready table inside the script;
- recommending a reasonable chart type when the user does not specify one;
- producing a PNG as the required primary output;
- saving the complete Python script that reproduces every PNG;
- applying the IMF house styling rules in `chart-formatting-rules.md`;
- offering an optional editable Excel workbook after the PNG is ready.

V1 excludes mimicry of user-provided example charts, PPT decks, interactive
dashboards, new data retrieval logic, and a large custom charting framework.

## Input Order

Use available data before attempting any pull:

1. data already produced by `imf-ra-data`;
2. user-provided Excel or CSV data;
3. a new data pull only if no usable data are available and the user explicitly
   asks the agent to pull data.

If no usable data are available, ask whether the user wants to provide data or
explicitly wants the agent to pull data. When pulling, follow `imf-ra-data` and
`imf-ra-catalog`; do not create new retrieval scripts.

## Output Folder

Before writing artifacts, ask the user to confirm that outputs should be saved
under `chart-temp/` in the current working directory. Do not create or overwrite
`chart-temp/` without confirmation.

Use stable, readable, lowercase file names based on the chart topic:

```text
chart-temp/
  real_gdp_growth_selected_economies.png
  real_gdp_growth_selected_economies_generate.py
  real_gdp_growth_selected_economies.xlsx  # optional
```

If a file already exists, avoid accidental overwrite by adding a version suffix
such as `_v2`, unless the user explicitly asks to replace the prior output.

## Required Outputs

Every successful PNG chart must save these required files:

- the PNG;
- the Python script that generated the PNG.

The Python script is the reproducibility record. It must include:

- data loading from the selected source;
- all cleaning and reshaping code;
- all analytical transformations;
- chart metadata as script variables or comments, including chart type, title,
  subtitle, axes, units, source, filters, date range, and caveats;
- lightweight QA checks, such as required columns, numeric values, missing data,
  duplicate observations, and non-empty output;
- the plotting code and PNG save path.

Do not create separate chart-ready CSV or chart spec CSV files by default. If
the user explicitly asks for intermediate data exports, create them as optional
extras and label them clearly.

## Execution Flow

1. Confirm the output folder before writing artifacts.
2. Load data from `imf-ra-data` output or user-provided Excel/CSV.
3. If no usable data are available, ask whether the user wants to provide data
   or explicitly wants the agent to pull data.
4. Inspect columns, data types, grain, units, source, frequency, and date range.
5. Ask clarification only if the chart would otherwise be wrong or misleading.
6. Clean and transform data according to the transformation rules.
7. Choose a chart type from user instruction or the consulting rules.
8. Write and run the complete Python script to generate an initial reasonable
   PNG.
9. Run QA before delivery.
10. Keep the exact Python script beside the PNG.
11. Show or link the PNG to the user.
12. Offer the optional Excel workbook.
13. If the user requests changes, update the chart and version or overwrite
    outputs according to the file naming rule.

## Data Cleaning

V1 should support common chart-preparation steps:

- normalize dates or periods;
- convert values to numeric;
- standardize country, group, and series labels;
- reshape long data to wide plotting-ready data when useful;
- reshape wide data to long clean data when useful;
- sort time periods and categories;
- drop or flag empty observations;
- preserve missing values intentionally rather than hiding them silently.

Record transformations and important cleaning choices in the generated Python
script.

## PNG Requirements

The PNG should include:

- clear title;
- axis labels with units;
- readable legend or direct labels;
- source note when known;
- footnote for forecasts, vintages, or transformations when relevant.

Default visual style:

- white background;
- IMF house style from `chart-formatting-rules.md`;
- clear title and subtitle when useful;
- readable font sizes;
- light gridlines only when they help reading values;
- sorted bars for cross-sectional comparisons;
- no decorative effects.

## QA Before Delivery

Check and record whether:

- the PNG exists and is not blank;
- plotting-ready data has at least one row;
- required axis/value fields exist;
- the value field is numeric;
- duplicate observations were checked;
- missing values were handled intentionally;
- the chart is understandable without relying on the note;
- title, unit, and source notes are present when available;
- labels and legend are readable and do not cover the data;
- axes are not misleading for the chart type;
- bars or categories are sorted when sorting improves interpretation;
- too many series are not squeezed into one unreadable chart;
- transformations are recorded in the generated Python script.

## Optional Excel Workbook

Only create the Excel workbook if the user confirms they want it after seeing
the PNG offer. The workbook is optional and does not replace the required Python
script.

Required sheets:

| Sheet | Purpose |
|---|---|
| `raw_data` | Original pulled or uploaded data, preserved as much as practical. |
| `clean_data` | Normalized and cleaned data with consistent field names and types. |
| `chart_ready` | Exact table used by the chart, easy to inspect and edit. |
| `chart_spec` | Chart type, title, axes, units, source, filters, caveats, and transformations. |
| `chart` | Embedded Excel chart linked to `chart_ready`. |

Recommended sheets:

| Sheet | Purpose |
|---|---|
| `QA_checks` | Checks for duplicates, missing values, numeric conversion, dates, units, and source notes. |

## Failure Behavior

If chart generation fails, tell the user:

- what failed;
- whether the data were cleaned successfully;
- what output, if any, was saved;
- what input, confirmation, or environment fix is needed next.

If the failure happens after data cleaning, offer the partially generated Python
script or an optional diagnostic workbook, but only create optional files if the
user confirms.

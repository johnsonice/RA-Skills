# IMF RA Charts V1 Plan

## Purpose

Design `imf-ra-charts` as the chart-production worker in the RA Skills family.
This is a planning document only; it is not yet the final `SKILL.md`.

V1 should let an agent turn confirmed data into a useful economics/research
chart, while preserving enough evidence to reproduce the output later.

## Chart Design Principle

Every V1 chart should be clear, accurate, and reduce cognitive load.

This means the chart should make the main comparison easy to see, label units
and sources plainly, avoid unnecessary visual complexity, choose a chart type
that fits the data, and avoid transformations or visual encodings that could
mislead the reader.

## V1 Scope

V1 includes:

- Charting data fetched through `imf-ra-data`.
- Charting user-provided Excel or CSV data.
- Cleaning and transforming data into plotting-ready shape inside the generated
  script.
- Recommending a reasonable chart type when the user does not specify one.
- Creating a PNG as the primary chart output.
- Saving the complete Python script that reproduces every PNG.
- Offering an optional editable Excel workbook after the PNG is ready.
- Applying the IMF house styling rules defined in `imf-ra-charts`.

V1 excludes:

- Mimicking a user-provided example chart.
- PPT deck generation.
- Interactive dashboards.
- New database or API retrieval logic.
- A large custom charting framework.

## Standard Output Contract

Every successful V1 chart request produces a PNG as the required primary output.

Every successful V1 chart request also saves the complete Python script in the
confirmed output folder:

- the PNG;
- the Python script that generated the PNG.

The Python script is the reproducibility record. It should include all data
loading, cleaning, transformation, QA checks, chart metadata, plotting code, and
the PNG save path. Do not create separate chart-ready CSV or chart spec CSV
files by default.

The Excel workbook is optional. After providing the PNG, ask:

```text
Would you like an editable Excel workbook with the chart data and embedded chart?
```

Only create the Excel workbook if the user says yes.

## Output Folder Convention

Before writing chart artifacts, ask the user to confirm that outputs should be
saved under a temporary folder named `chart-temp/`. The confirmation message
must also tell the user that `chart-temp/` will be deleted after the charting
session ends and that they should save anything they need to keep.

Use a short confirmation prompt such as:

```text
I can save the chart outputs in `chart-temp/`. This folder is temporary and will
be deleted after this charting session, so save anything you need to keep. Is
that okay?
```

After confirmation, create `chart-temp/` in the current working directory and
save all chart artifacts there. Do not create or overwrite `chart-temp/` without
user confirmation.

`chart-temp/` is a temporary session workspace, not a durable project folder.
Before deleting it, make sure any deliverables the user wants to keep have been
moved, attached, or otherwise handed off. Delete `chart-temp/` after the charting
session ends.

Use stable, readable, lowercase file names based on the chart topic:

```text
chart-temp/
  real_gdp_growth_selected_economies.png
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

There is no internal charting tool for V1. The Python stack above is the
intended implementation path, not a fallback.

## Input Paths

Use available data before attempting any pull. The preferred order is:

1. data already produced by `imf-ra-data`;
2. user-provided Excel or CSV data;
3. a new data pull, only if no usable data are available and the user explicitly
   asks the agent to pull data.

`imf-ra-charts` should follow shared `imf-ra` conventions and its own chart
workflow. It should not bypass the RA Skills chain when data need to be fetched.

### Path A: Data From `imf-ra-data`

When data have already been fetched by `imf-ra-data`, `imf-ra-charts` should:

- read the tidy or refreshable output;
- preserve source fields such as database, indicator, unit, frequency, vintage,
  geography, and time period when present;
- validate that the data are chartable;
- transform into plotting-ready data inside the generated script;
- generate the PNG and Python script;
- offer the optional Excel workbook.

If the user asks for a chart but no raw data are available from `imf-ra-data` or
an external user-provided file, ask for the data source. Only chain backward to
pull data if the user explicitly asks the agent to fetch the data:

```text
imf-ra -> imf-ra-charts -> imf-ra-data -> imf-ra-catalog, if identifiers are unresolved
```

### Path B: User-Provided Excel Or CSV

When the user provides raw Excel or CSV data, `imf-ra-charts` should:

- inspect the file structure and available columns;
- infer likely time, geography, series, value, unit, and source fields;
- ask clarification only when required fields are ambiguous or unsafe;
- preserve the original data for optional workbook export;
- create standardized clean and plotting-ready data inside the generated script;
- generate the PNG and Python script;
- offer the optional Excel workbook.

## Execution Flow

1. Confirm the output folder before writing artifacts.
2. Load data from `imf-ra-data` output or user-provided Excel/CSV.
3. If no usable data are available, ask whether the user wants to provide data
   or wants the agent to pull data.
4. Pull data only if the user explicitly asks for a pull, following
   `imf-ra-data` and `imf-ra-catalog` as needed.
5. Inspect columns, data types, grain, units, source, frequency, and date range.
6. Ask clarification only if the chart would otherwise be wrong or misleading.
7. Clean and transform data according to the transformation policy.
8. Choose a chart type from user instruction or chart recommendation rules.
9. Generate an initial reasonable PNG.
10. Run chart QA before delivery.
11. Save the complete reproducible Python script.
12. Show or link the PNG to the user.
13. Offer the optional Excel workbook.
14. If the user requests changes, update the chart and version or overwrite
    outputs according to the file naming rule.
15. After the session ends and retained deliverables have been handed off,
    delete `chart-temp/`.

## Data Cleaning

V1 should support common chart-preparation steps:

- Normalize dates or periods.
- Convert values to numeric.
- Standardize country, group, and series labels.
- Reshape long data to wide plotting-ready data when useful.
- Reshape wide data to long clean data when useful.
- Sort time periods and categories.
- Drop or flag empty observations.
- Preserve missing values intentionally rather than hiding them silently.
- Apply transformations according to the V1 transformation policy.

When transformations are applied, record them in the generated Python script.

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
- Reshape long data to wide plotting-ready data when useful.
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
- no usable data are available and the user has not asked the agent to fetch
  data.

## Chart Recommendation Rules

When suggesting a chart type, first infer the analytical task, then match it to
the simplest chart that answers the question accurately. Prefer charts that make
the main comparison obvious, minimize legend-reading and visual clutter, and do
not require unconfirmed analytical transformations.

Use the user's stated chart type when provided and safe. If the requested chart
type would be misleading, unreadable, or unnecessarily complex, briefly explain
the issue and recommend a simpler alternative.

Use this selection order:

1. Identify the user's analytical task.
2. Confirm the data shape can support that task.
3. Choose the lowest-cognitive-load chart that answers the task accurately.
4. Check whether the chart requires a Tier 2 or Tier 3 transformation.
5. Ask for confirmation before applying transformations that change analytical
   meaning.

### Analytical Task Defaults

| User Wants To See | Default Chart |
|---|---|
| Change over time for one series | Line chart |
| Compare several countries or series over time | Multi-line chart, or small multiples if crowded |
| Compare countries or categories at one point in time | Sorted bar chart |
| Rank countries or categories | Horizontal sorted bar chart |
| Compare two numeric variables | Scatter plot |
| Show composition over time | Stacked bar or stacked area, only if components are additive |
| Show contribution to a total or change | Contribution bar chart, only when contribution logic is explicit |
| Compare before and after, or two selected periods | Slope chart or grouped bar chart |
| Show a distribution | Histogram or box plot |
| Show latest value plus recent trend | Annotated line chart, or bar chart plus compact trend context |

### Data Shape Checks

| Data Shape | Recommended Chart |
|---|---|
| `time` + `value` | Line chart |
| `time` + `series/country` + `value` | Multi-line chart or small multiples |
| `country/category` + `value` | Sorted bar chart |
| `country/category` + `x_value` + `y_value` | Scatter plot |
| `time` + `component` + `value` | Stacked bar or stacked area, only if additive |
| `period` + `country/category` + `value` for two periods | Slope chart or grouped bar chart |

### Cognitive Load And Anti-Patterns

Do not make the reader solve a visual puzzle before they can answer the
economic question.

Prefer:

- fewer series per chart;
- sorted categories when order helps interpretation;
- direct labels when practical;
- clear units in axis labels;
- titles that state the subject and comparison;
- notes only when they prevent misunderstanding.

Avoid:

- excessive color or color variation;
- too many categories in one chart;
- crowded legends or too many lines;
- misleading scaling, including unjustified truncated axes or inconsistent
  scales across related charts;
- decorative elements or chart junk, including 3D effects, shadows, gradients,
  heavy borders, background images, unnecessary icons, or ornamental shapes;
- dual-axis charts by default;
- pie charts for many categories or precise comparisons;
- stacked area or stacked bar charts when components are not additive;
- unsorted bar charts when ranking or comparison is the goal;
- inconsistent colors for the same country, group, or series across related
  charts;
- transformations such as growth rates, index-to-100, smoothing, shares, or
  aggregations without user request or confirmation;
- chart types that require the reader to compare areas, angles, or subtle color
  differences when simple position or length would be clearer.

When in doubt, choose the simplest chart that preserves accuracy: line for
time, sorted bar for category comparison, scatter for two numeric variables,
and small multiples when one chart becomes crowded.

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

V1 applies the IMF house styling defaults while keeping charts clean,
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
- the main comparison is visually clear;
- the chart avoids unnecessary decoding, clutter, or decoration;
- too many series are not squeezed into one unreadable chart.

## Python Script Requirements

The generated Python script is the reproducibility record. It should include:

- data loading from the selected source;
- all cleaning and reshaping code;
- all analytical transformations;
- chart metadata as variables or comments, including chart type, title,
  subtitle, axes, units, source, filters, date range, and caveats;
- lightweight QA checks for required columns, numeric values, missing data,
  duplicate observations, and non-empty output;
- the plotting code and PNG save path.

Do not create separate chart-ready CSV or chart spec CSV files by default. If
the user explicitly asks for intermediate exports, create them as optional
extras and label them clearly.

## Optional Excel Workbook

Only create the Excel workbook if the user confirms they want it.

Required sheets:

| Sheet | Purpose |
|---|---|
| `raw_data` | The original pulled or uploaded data, preserved as much as practical. |
| `clean_data` | Normalized and cleaned data with consistent field names and types. |
| `chart_ready` | The exact table used by the chart. This should be easy to inspect and edit. |
| `chart_spec` | Chart type, title, subtitle, axis fields, units, source, filters, caveats, and transformations. |
| `chart` | An embedded Excel chart linked to `chart_ready`. |

Recommended additional sheets:

| Sheet | Purpose |
|---|---|
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
Python script or diagnostic Excel workbook, but should only create optional
files if the user confirms.

## Suggested Implementation Sequence

1. Finalize this V1 plan.
2. Update `skills/imf-ra-charts/SKILL.md` with the V1 workflow.
3. Expand `skills/imf-ra-charts/references/chart-tool-usage.md` with the PNG,
   Python-script reproducibility, and optional Excel contract.
4. Add chart behavior test cases to `tests/auto_test_cases.yaml` after V1 is
   implemented.
5. Mirror reviewer-facing test descriptions in `tests/auto_test_instructions.md`
   when chart cases are added.
6. Run `python scripts/sync_skills.py` after updating the actual skill.

## Success Criteria

V1 is successful when a user can ask for a chart and receive:

- a PNG chart they can immediately inspect or use;
- a Python generation script containing data loading, cleaning, transformation,
  QA checks, chart metadata, and plotting code;
- an offer to create an optional Excel workbook containing `raw_data`,
  `clean_data`, `chart_ready`, and an embedded chart;
- a clear record of source, units, and transformations;
- sensible chart choices when the user does not specify a chart type;
- safe clarification behavior when the data are ambiguous or misleading.

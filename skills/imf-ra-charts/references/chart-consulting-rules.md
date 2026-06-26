# Chart Consulting Rules

Use these rules to act like a visualization consultant, not just a chart
generator. The goal is a chart that makes the right economic comparison easy to
see without hiding assumptions.

## Consulting Brief

Before choosing a chart, infer the brief from the user's request and available
data:

- analytical task: trend, ranking, comparison, relationship, distribution,
  composition, contribution, or before/after;
- intended takeaway, if the user states one;
- audience or use, if stated, such as memo draft, quick inspection, or
  presentation;
- main entities, periods, units, and source;
- required caveats, such as forecast, vintage, missing data, or transformation.

Do not over-ask. Ask only when missing brief details would make the chart wrong
or misleading.

## Clarification Policy

Ask before charting when:

- there is no clear value column;
- there is no clear time, category, or geography axis;
- multiple plausible indicators or series could answer the request;
- units or frequencies are incompatible;
- the requested chart requires a Tier 2 or Tier 3 transformation;
- the requested chart type would be unreadable for the number of series;
- no usable data are available and the user has not asked the agent to fetch
  data.

Otherwise, create the best reasonable default chart and briefly explain the
choice.

## Transformation Policy

### Tier 1: Safe To Infer Automatically

These are data-preparation transformations. Apply them without separate
confirmation when needed to make the data chartable:

- parse dates and periods, such as `2020`, `2020Q1`, or `Jan-2020`;
- convert numeric strings to numbers;
- sort time or category axes;
- rename columns into standard fields such as `country`, `time`, `value`, and
  `series`;
- drop fully empty rows or columns;
- trim labels and standardize obvious whitespace;
- reshape long data to wide plotting-ready data when useful;
- reshape wide data to long clean data when useful;
- create a forecast or estimate flag when source status labels are clear;
- filter to requested countries, indicators, dates, or series;
- select the latest available observation when the user asks for a latest-period
  comparison.

### Tier 2: Suggest Or Ask First

These change analytical meaning. Suggest them if useful, but ask for
confirmation before applying:

- percent change, growth rate, year-over-year, or quarter-over-quarter change;
- index to 100;
- difference from benchmark or previous period;
- share of GDP;
- per-capita transformation;
- rolling average;
- real versus nominal adjustment;
- currency or unit scaling, such as millions to billions;
- aggregating countries into groups;
- ranking or top-N selection when the user did not specify `N`;
- normalizing countries or series to a common start year;
- combining multiple indicators into one derived metric.

### Tier 3: Explicit Request Only

Only do these when the user explicitly requests them and the needed assumptions
or input data are available:

- forecasting or extrapolation;
- seasonal adjustment;
- deflation or inflation adjustment using another series;
- rebaselining with a non-obvious base period;
- outlier removal or winsorization;
- imputation or interpolation of missing values;
- weighting and weighted aggregates;
- contribution calculations;
- decomposition charts;
- regression or fitted lines;
- smoothing beyond a simple rolling average;
- currency conversion using exchange rates;
- any transformation requiring another dataset.

Record every Tier 2 or Tier 3 transformation in the generated Python script.

## Chart Recommendation Rules

First infer the analytical task, then match it to the simplest chart that
answers the question accurately. Use the user's chart type when provided and
safe. If it would be misleading, unreadable, or unnecessarily complex, briefly
explain the issue and recommend a simpler alternative.

Selection order:

1. Identify the analytical task.
2. Confirm the data shape can support that task.
3. Choose the lowest-cognitive-load chart that answers the task accurately.
4. Check whether the chart requires a Tier 2 or Tier 3 transformation.
5. Ask before applying transformations that change analytical meaning.

| User wants to see | Default chart |
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

| Data shape | Recommended chart |
|---|---|
| `time` + `value` | Line chart |
| `time` + `series/country` + `value` | Multi-line chart or small multiples |
| `country/category` + `value` | Sorted bar chart |
| `country/category` + `x_value` + `y_value` | Scatter plot |
| `time` + `component` + `value` | Stacked bar or stacked area, only if additive |
| `period` + `country/category` + `value` for two periods | Slope chart or grouped bar chart |

## Cognitive Load And Anti-Patterns

Prefer:

- fewer series per chart;
- sorted categories when order helps interpretation;
- direct labels when practical;
- clear units in axis labels;
- titles that state the subject and comparison;
- notes only when they prevent misunderstanding;
- the IMF house style palette with sufficient contrast.

Avoid:

- excessive color variation;
- too many categories in one chart;
- crowded legends or too many lines;
- unjustified truncated axes or inconsistent scales across related charts;
- decorative elements, including 3D effects, shadows, gradients, heavy borders,
  background images, unnecessary icons, or ornamental shapes;
- dual-axis charts by default;
- pie charts for many categories or precise comparisons;
- stacked area or stacked bar charts when components are not additive;
- unsorted bar charts when ranking or comparison is the goal;
- inconsistent colors for the same country, group, or series across related
  charts;
- transformations such as growth rates, index-to-100, smoothing, shares, or
  aggregations without user request or confirmation;
- chart types that force comparison by areas, angles, or subtle color
  differences when position or length would be clearer.

When in doubt, choose the simplest chart that preserves accuracy: line for time,
sorted bar for category comparison, scatter for two numeric variables, and small
multiples when one chart becomes crowded.

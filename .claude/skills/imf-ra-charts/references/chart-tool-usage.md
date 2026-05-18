# Internal charting tool - usage

The charting tool API is not yet fully specified. Until it is finalized, use this file as the minimum contract between `imf-ra-data` output and chart construction.

## Installation and Import

Use the charting environment already available in the active project. Do not install new visualization dependencies unless the user asks for a new charting stack or the existing project clearly requires it.

## Invocation

Follow the active charting tool or project convention once identified. If no charting tool is available, produce the cleaned chart-ready data and explain what chart specification should be passed to the charting layer.

## Input data shape

Expect tidy data from `imf-ra-data`: one observation per row with at least `geo`, `time`, and `value`, plus identifying columns such as `database`, `series`, `indicator`, `freq`, `unit`, and `vintage` when available.

Before charting, verify:

- `time` is consistently typed or formatted.
- `value` is numeric.
- country/group labels are human-readable.
- units and scale are known enough to label the axis.

## Chart-type selection

Use the user's requested chart type when provided. Otherwise choose a simple default:

- single time series: line chart
- multiple time series across countries/groups: multi-line chart or small multiples
- latest-period country/group comparison: bar chart
- two numeric measures by country/group: scatter plot
- composition over time: stacked bar or stacked area chart when additive units are valid

## Captions, sources, footnotes

Include a source line when known, for example `Source: IMF, World Economic Outlook`. Add footnotes for WEO vintage, forecast periods, unit transformations, or non-obvious country-group definitions.

## Output

Save or return the chart according to the active project convention. If no convention exists, prefer a clearly named output file and provide the path plus any remaining caveats.

---
name: imf-ra-charts
description: Use when the user wants to make a chart, plot, or visualization of IMF data using the internal charting tool. Covers chart-tool input formats, chart-type selection from data shape and intent, and source/footnote conventions. If data is not yet in scope, follow imf-ra-data to fetch it first.
---

# IMF RA - Charts

Handing tidy data to the internal charting tool.

## Before you chart

See the umbrella `imf-ra` for shared conventions.

## When data isn't in scope yet

Load `imf-ra-data` in the same turn and follow it to fetch. Do not duplicate SDK call patterns here. See [`imf-ra-data/references/imf_datatools_agent_api_reference.md`](../imf-ra-data/references/imf_datatools_agent_api_reference.md). If the user only described what they want in plain English, also load `imf-ra-catalog` to resolve the identifier.

## How to chart

See [references/chart-tool-usage.md](references/chart-tool-usage.md) for the internal charting tool's invocation, input shape, chart-type selection, and captioning conventions.

## Chart-type heuristics

Use the user's stated chart type when provided. Otherwise use the data shape as a guide: single time series -> line; multiple countries over time -> multi-line or small multiples; latest country comparison -> bar; two numeric series by country -> scatter; contribution or composition over time -> stacked bar/area when appropriate.

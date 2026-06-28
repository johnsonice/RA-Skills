---
name: imf-ra-charts
description: Use when the user wants to turn IMF RA data or user-provided CSV/Excel data into a static or interactive economics chart. Produces a PNG plus a complete reproducible Python script; optionally produces a self-contained interactive HTML chart (Plotly) and an editable Excel workbook after user confirmation.
---

# IMF RA - Charts

Chart-production worker for the RA Skills family. Use this skill when the user
asks to chart, plot, visualize, or prepare a figure from available data.

Keep the interaction practical: make a reasonable chart when the data and
intent are clear, and ask only when ambiguity would make the chart wrong or
misleading.

## Load The Right References

- For workflow, output files, routing, failure behavior, and optional Excel:
  see [references/chart-tool-usage.md](references/chart-tool-usage.md).
- For chart choice, consulting brief, transformation tiers, accessibility, and
  anti-patterns: see
  [references/chart-consulting-rules.md](references/chart-consulting-rules.md).
- For IMF house styling, fonts, borders, and colors: see
  [references/chart-formatting-rules.md](references/chart-formatting-rules.md).

## Core Rules

- Use existing `imf-ra-data` output or user-provided CSV/Excel before attempting
  a new pull.
- Pull data only when no usable data are available and the user explicitly asks
  the agent to pull data.
- Confirm before creating or writing to `chart-temp/` in the current working
  directory. In that confirmation, tell the user `chart-temp/` will be deleted
  after the charting session ends and that they should save anything they need
  to keep.
- Required outputs are the PNG and the complete Python script that generated it.
- Interactive HTML output (Plotly) is a parallel optional output — produce it when the user asks for an interactive chart or says "interactive". It is always paired with the PNG; never replaces it.
- Do not use or invent an internal charting tool; V1 chart production is done
  with generated Python scripts.
- Create the optional Excel workbook only after the user confirms, after the
  PNG is ready.
- Do not handle mimicry, PPT deck generation, interactive dashboards, or new
  data retrieval logic in this skill.

## Implementation Stack

Use Python `pandas` for cleaning and reshaping, `matplotlib` for PNG output,
`plotly` (with `plotly.graph_objects`) for the optional interactive HTML chart,
and `xlsxwriter` for the optional Excel workbook with an embedded editable chart.
If a chart dependency is missing, tell the user which package is missing and
what was already prepared.

## Before Delivery

Run chart QA before showing the PNG. At minimum, verify the image is nonblank,
the data are chartable, the labels are readable, and source/unit/transform notes
are present when available.

If chart generation fails, tell the user what failed, whether data cleaning
succeeded, what outputs were saved, and what is needed next. Do not claim a
chart was created when it was not.

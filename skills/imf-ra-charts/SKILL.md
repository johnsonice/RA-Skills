---
name: imf-ra-charts
description: Use when the user wants to turn IMF RA data or user-provided CSV/Excel data into a static economics chart. Produces a PNG plus a complete reproducible Python script containing data cleaning, transformation, and plotting code, with an optional editable Excel workbook only after user confirmation.
---

# IMF RA - Charts
Chart-production worker for the RA Skills family. Use this skill to turn available data into a static economics chart, with optional interactive HTML output when the user asks for it.

## Load The Right References

- Workflow, output files, routing, QA, failure behavior, and optional Excel:
  see [references/chart-tool-usage.md](references/chart-tool-usage.md).
- Chart choice, transformation tiers, cognitive load, and anti-patterns: see
  [references/chart-consulting-rules.md](references/chart-consulting-rules.md).
- Default static chart formatting, report placement, fonts, borders, and colors:
  see
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
- Required outputs are a PNG and the complete Python script that generated it.
- Create the optional Excel workbook only after the user confirms, after the
  PNG is ready.
- If the user gives no specific formatting requirement, apply the IMF-style
  defaults in `chart-formatting-rules.md`.
- Ask only when ambiguity would make the chart wrong or misleading; otherwise
  make a reasonable default chart.
- Do not handle mimicry, PPT decks, dashboards, or new data retrieval logic in
  this skill.

## Implementation Stack

Use Python `pandas` for cleaning and reshaping, `matplotlib` for PNG output, and
`xlsxwriter` for the optional Excel workbook with an embedded editable chart.
If a chart dependency is missing, tell the user which package is missing and
what was already prepared.

## Before Delivery

Run the QA checklist in `chart-tool-usage.md` before showing the PNG.

If chart generation fails, tell the user what failed, whether data cleaning
succeeded, what outputs were saved, and what is needed next. Do not claim a
chart was created when it was not.

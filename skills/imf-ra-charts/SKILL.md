---
name: imf-ra-charts
description: Use when the user wants to turn IMF RA data or user-provided CSV/Excel data into a static economics chart. Produces a PNG plus a complete reproducible Python script containing data cleaning, transformation, and plotting code, with an optional editable Excel workbook only after user confirmation.
---

# IMF RA - Charts
Chart-production worker for the RA Skills family. Use this skill to turn available data into a static economics chart, with optional interactive HTML output when the user asks for it.

## Load The Right References

- For workflow, output files, routing, failure behavior, and optional Excel:
  see [references/chart-tool-usage.md](references/chart-tool-usage.md).
- For chart choice, consulting brief, transformation tiers, accessibility, and
  anti-patterns: see
  [references/chart-consulting-rules.md](references/chart-consulting-rules.md).

## Core Rules

- Use existing `imf-ra-data` output or user-provided CSV/Excel before attempting
  a new pull.
- Pull data only when no usable data are available and the user explicitly asks
  the agent to pull data.
- Required outputs are the PNG and the complete Python script that generated it.
- Create the optional Excel workbook only after the user confirms.

## Implementation Stack

Use Python `pandas` for cleaning and reshaping, `matplotlib` for PNG output, and
`xlsxwriter` for the optional Excel workbook with an embedded editable chart.

## Before Delivery

Run chart QA before showing the PNG. At minimum, verify the image is nonblank,
the data are chartable, the labels are readable, and source/unit/transform notes
are present when available.

If chart generation fails, tell the user what failed, whether data cleaning
succeeded, what outputs were saved, and what is needed next. Do not claim a
chart was created when it was not.

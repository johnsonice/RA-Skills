---
name: imf-ra-charts
description: Use when the user asks to create, plot, chart, or visualize economic data, including requests that first require data discovery or retrieval and requests using existing IMF RA data or user-provided CSV/Excel files. Produces a PNG plus a complete reproducible Python script, with optional interactive HTML and editable Excel outputs.
---

# IMF RA - Charts

Chart-production worker for the RA Skills family. Owns chart preparation,
generation, and QA whether data are supplied up front or fetched during the
request. Follow the input routing in the workflow reference below when data
are not yet available.

## Runtime

Use the company Python on IMF Windows; do not create or use virtual/Conda
environments. Before executing helpers, read the shared
[runtime contract](../imf-ra/references/runtime.md) for installed-skill paths, interpreter
selection, SDK setup authorization, and user output locations. Resolve scripts
from the loaded skill directory, not the user's working directory.


## Load The Right References

Before writing plotting code, read these references:

- Workflow, output files, routing, QA, failure behavior, and optional outputs:
  see [references/chart-tool-usage.md](references/chart-tool-usage.md).
- Chart choice, transformation tiers, cognitive load, and anti-patterns: see
  [references/chart-consulting-rules.md](references/chart-consulting-rules.md).
- Default static chart formatting, report placement, fonts, borders, and colors:
  see
  [references/chart-formatting-rules.md](references/chart-formatting-rules.md).

## Core Rules

- Use existing `imf-ra-data` output or user-provided CSV/Excel before attempting
  a new pull.
- When usable data are unavailable, a chart request authorizes the retrieval
  needed for that chart through `imf-ra-catalog` and `imf-ra-data`. Follow the
  workflow reference's input routing and honor user restrictions on retrieval.
- Save final outputs in the user's requested location, or a persistent
  `charts/` directory in their workspace. No routine folder confirmation is
  needed. Never delete final PNGs, scripts, or their required input data.
- Required outputs are a PNG and the complete Python script that generated it.
- Interactive HTML and editable Excel are optional outputs. Create either one
  only when the user asks for it or confirms the post-PNG offer.
- If the user gives no specific formatting requirement, apply the IMF-style
  defaults in `chart-formatting-rules.md`.
- Ask only when ambiguity would make the chart wrong or misleading; otherwise
  make a reasonable default chart.
- Do not handle mimicry, PPT decks, dashboards, or new data retrieval logic in
  this skill.

## Implementation Stack

Implement this skill by writing and running a complete Python script that
follows the workflow, formatting, and QA requirements above. Use
`pandas` for cleaning and reshaping, `matplotlib` for PNG output,
`plotly` (with `plotly.graph_objects`) for the optional interactive HTML chart,
and `xlsxwriter` for the optional Excel workbook with an embedded editable chart.
If a chart dependency is missing, tell the user which package is missing and
what was already prepared.

## Before Delivery

Run the QA checklist in `chart-tool-usage.md` before showing the PNG.

If chart generation fails, tell the user what failed, whether data cleaning
succeeded, what outputs were saved, and what is needed next. Do not claim a
chart was created when it was not.

# Chart Workflow And Output Contract

This file is the operating contract for `imf-ra-charts`. The skill produces
static PNG charts through Python. Interactive
HTML and editable Excel outputs are optional add-ons.

## Scope

- Use data from `imf-ra-data` output or user-provided CSV/Excel files.
- Clean and reshape data inside the generated script.
- Choose a reasonable chart when the user does not specify one.
- Always produce a PNG plus the complete Python script that reproduces it.
- Offer optional self-contained interactive HTML and editable Excel outputs
  after the PNG is ready, unless the user already requested one of them.

## Input Order

Use available data before attempting any pull:

1. data already produced by `imf-ra-data`;
2. user-provided Excel or CSV data;
3. a new data pull through `imf-ra-catalog` and `imf-ra-data` when no usable
   data are available and retrieval is needed to fulfill the chart request.

A request to chart specified economic series authorizes the retrieval needed
for that chart; no separate permission to fetch is required. Honor any
user-imposed source or retrieval restrictions. If the user limits the task to
supplied files and those files are missing or unusable, ask for the required
input. Resolve ambiguous series or missing specifications through the catalog
and data skills' normal clarification rules. Use their supported fetch helpers;
do not create new retrieval scripts. This authorization does not extend to
environment creation or package installation; follow the shared runtime contract.

## Output Folder

Save final files in the user's requested location, or a persistent `charts/`
folder in the user's workspace. Create it as part of the chart request without
a separate confirmation. If the workspace is unknown or unwritable, ask for a
destination. Do not save outputs under the installed skill directory.

Use stable, readable topic-based names, for example:

```text
charts/
  real_gdp_growth_selected_economies.png
  real_gdp_growth_selected_economies_generate.py
  real_gdp_growth_selected_economies_interactive.html   # optional
  real_gdp_growth_selected_economies.xlsx               # optional
```

Avoid overwriting existing files by adding `_v2`, unless replacement was
requested. Final deliverables persist after the session. A generated script
must read persistent input files: use paths resolved relative to the script or
explicit configurable paths, not ephemeral files or an assumed launch directory.
If intermediate files are necessary, create a unique temporary directory and
clean up only those intermediates after success. Never delete user inputs or
pre-existing directories. Preserve required cleaned data alongside the script
if reproducing the chart depends on them.

## Required Outputs

Every successful chart session must save:

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

## Optional Outputs

Create optional outputs only when the user asks for them up front or confirms
the post-PNG offer. Generate only the requested optional output(s), preserving
the PNG chart's meaning and styling. Use this short prompt when neither optional output has
already been requested:

```text
Would you also want an HTML interactive chart or an editable Excel workbook with data and chart included?
```

### Interactive HTML

Produce a self-contained interactive HTML chart using `plotly.graph_objects`
when the user asks for an interactive chart, uses the word `interactive`, or
confirms the optional HTML offer.

Rules:

- Use `fig.write_html(path, include_plotlyjs=True)` by default so the HTML is
  fully self-contained and works offline.
- Use `include_plotlyjs="cdn"` only if the user explicitly asks for a smaller
  internet-dependent file.
- Apply the same chart (including chart type, title, axis labels, units, source note, and series colors as)
  the PNG.
- Add hover templates showing year and value with unit label.
- Save as `<topic>_interactive.html` beside the PNG in the persistent output directory.
- Include the HTML generation code in the same Python script as the PNG, gated
  by an `INTERACTIVE = True` flag at the top so the script is self-documenting.
- If the local host supports browser opening, open the HTML after saving so the
  user sees it immediately. If the environment is headless, remote, or
  browser-opening fails, provide the saved HTML path instead.

### Excel Workbook

Produce an editable Excel workbook when the user requests it or confirms the offer.

The workbook does not replace the required PNG or Python script.

Required sheets:

| Sheet | Purpose |
|---|---|
| `raw_data` | Original pulled or uploaded data, preserved as much as practical. |
| `clean_data` | Normalized and cleaned data with consistent field names and types. |
| `chart_ready` | Exact table used by the chart, easy to inspect and edit. |
| `chart_spec` | Chart type, title, axes, units, source, filters, caveats, and transformations. |
| `chart` | Embedded Excel chart same as in PNG linked to `chart_ready`. |

Recommended sheets:

| Sheet | Purpose |
|---|---|
| `QA_checks` | Checks for duplicates, missing values, numeric conversion, dates, units, and source notes. |

## Execution Flow

1. Resolve the user's output folder, or use persistent `charts/` in the workspace; ask only when the destination is unknown or unusable.
2. Load data from `imf-ra-data` output or user-provided Excel/CSV.
3. If no usable data are available, follow [Input Order](#input-order) to
   retrieve the required series or resolve missing input, then resume charting.
4. Inspect columns, data types, grain, units, source, frequency, and date range.
5. Ask clarification only if the chart would otherwise be wrong or misleading.
6. Clean and transform data according to the transformation rules.
7. Choose a chart type from user instruction or the consulting rules.
8. Write and run the complete Python script to generate the PNG and any
   already-requested optional outputs.
9. Run QA before delivery.
10. Keep the exact Python script beside the PNG.
11. Show or link the PNG to the user.
12. Offer optional outputs not already requested.
13. If the user requests changes, update the chart and version or overwrite
    outputs according to the file naming rule.
14. Before ending the turn, clean up agent-created temporary intermediates
    according to [Output Folder](#output-folder); keep all final deliverables.

## Data Preparation

Use Tier 1 preparation from `chart-consulting-rules.md` for routine cleanup:
date parsing, numeric conversion, label trimming, reshaping, sorting, filtering,
and empty-row handling. Preserve missing values intentionally rather than hiding
them silently.

Record transformations and important cleaning choices in the generated Python
script.

## QA Before Delivery

Check and record whether the:

- PNG exists and is not blank;
- plotting-ready data has rows, required fields, numeric values, and no
  unexpected duplicate observations;
- missing values and transformations are handled intentionally;
- title, unit, source, caveats, labels, and legend are readable when present;
- axes and chart type are not misleading;
- chart avoids crowding, clutter, and unsupported transformations;
- generated Python script records the data source, cleaning, transformations,
  metadata, QA checks, plotting code, and PNG path.

For optional outputs, also check that:

- HTML exists, is non-empty, and is self-contained unless the user requested CDN
  mode;
- Excel opens and contains the required sheets when requested.

## Failure Behavior

Follow the shared [recovery contract](../../imf-ra/references/recovery.md) for
script execution limits, corrections, and reporting after exhausted recovery.

If chart generation fails, tell the user:

- what failed;
- whether the data were cleaned successfully;
- what output, if any, was saved;
- what input, confirmation, or environment fix is needed next.

If the failure happens after data cleaning, offer the partially generated Python
script or an optional diagnostic workbook, but only create optional files if the
user confirms.

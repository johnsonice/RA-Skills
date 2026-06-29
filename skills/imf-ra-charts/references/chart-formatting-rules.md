# Chart Formatting Rules

Use these rules as the default static-chart formatting layer for
`imf-ra-charts`. They define clean IMF-style defaults, not mimicry of
user-provided examples, PPT deck production, or a separate charting scope. They
do not override the analytical safety and chart-selection rules in
`chart-consulting-rules.md`.

## Formatting Priority

If the user gives no specific formatting requirement, use the IMF-style defaults
in this file as the first-priority formatting rule. Apply formatting in this
order:

1. Start from the IMF-style canvas, typography, color, and spacing rules below.
2. Apply any specific user-requested formatting that does not make the chart
   misleading or unreadable.
3. Adjust only when the data shape or chart type requires it.
4. Preserve analytical clarity, readability, and non-misleading encodings.

## Default PNG Layout

Default PNG export:

- Size: `2000 x 1125` pixels.
- Aspect ratio: `16:9`.
- Matplotlib equivalent: `figsize=(13.333, 7.5)`, `dpi=150`.
- Plot-area margins: left `8%`, right `4%`, top `16%`, bottom `14%`.
- Use extra bottom margin when source notes, footnotes, or long x-axis labels
  need more room.

Placement:

- Align title, subtitle, plot area, and source note to the same left edge.
- Place title at the top-center above the plot area.
- Place subtitle directly below the title.
- Place source and notes at the bottom-left below the plot area.
- Keep source and notes outside the plotting area whenever practical.

## Word And Report Placement

When preparing figures for Word reports:

- Place each figure as close as possible to the first reference to it in the
  text.
- Small in-text figures may appear within a paragraph when they help illustrate
  a key point. They do not need figure numbers unless the report requires them.
- For in-text figures, use Square or Tight text wrapping so the figure is
  separated from surrounding text.
- Large or full-page figures may appear on a separate page or within the text,
  depending on size and readability.
- After copying a figure from Excel to Word, resize it only if labels remain
  readable. If text becomes too small, enlarge the font in the source Excel file
  and recopy the figure as an image, preferably Enhanced Metafile.

## Typography

Use Segoe UI as the default chart font.

For chart-sheet style outputs:

| Element | Font | Size | Color |
|---|---|---:|---|
| Basic chart text | Segoe UI | 10 pt | Black/auto |
| Figure title | Segoe UI | 24 pt | Black/auto |
| Chart subtitle | Segoe UI | 18 pt | Black/auto |
| Axis labels | Segoe UI | 10 pt | Black/auto |
| Legend | Segoe UI | 10 pt | Black/auto |
| Source box | Segoe UI | 10 pt | Black/auto |

For panel-sheet style outputs:

- Default font size: 10.
- Do not use font sizes below 8 because they may become unreadable.

is intended only for screen review, larger fonts may be used, but the generated
script should record that output-specific choice.

## Titles, Captions, And Units

For formal report figures that require numbered captions, place the figure title
as a caption to the graphic box or frame that contains the chart. Center that
caption above the figure and keep it inside the surrounding frame when a frame
is used. This report caption convention can differ from the default standalone
PNG title placement above.

Use Arabic numerals for numbered report figures:

```text
Figure 7. Jamaica: Monetary Growth, 2014-20
```

For single-panel figures, use:

```text
Figure #. Country: Concise Figure Subject, Time Period
(unit of measurement)
```

Omit the country or time period when not applicable. For multipanel figures, use
the same convention for the overall figure and add concise panel titles.

Center units of measurement below the panel title, not in bold, and enclose the
units in parentheses:

```text
(in percent of GDP)
```

## Plot Area And Axes

Plot area:

- Border line: light solid line.
- Border color: RGB `179,179,179` (`#B3B3B3`).
- Border dash style: solid line.
- Plot-area background: white. Use Background `#F3F4F5` only for page or
  background bands outside the plot area, unless the user requests another
  template.

X-axis:

- Tick marks: inside.
- Axis line: solid.
- Axis line color: RGB `179,179,179` (`#B3B3B3`).
- Axis dash style: solid line.

Use light gridlines only when they help the reader compare values. Use the
light solid border above, and avoid heavy axis frames or decorative effects.

## Frames And Borders

- For large or full-page figures in the main body of a report, place a black
  single-line frame around the entire figure, including title, source, notes,
  and footnotes.
- Borders are optional for small in-text charts.
- For figures in annexes, appendices, and attachments, use a black single-line
  frame for full-page figures.
- Keep the internal plot-area border light, as specified above, unless the user
  or report template requires otherwise.

## Legend And Labels

- Legend background fill: no fill.
- When using a legend, place it to the right of the chart or below the chart.
- Prefer direct labels when they reduce legend-reading.
- Do not let the legend cover data.
- Use consistent colors for the same country, group, or series across related
  charts.

## Source Notes And Footnotes

- Place source text where it is visible but does not compete with the main chart
  message.
- Use notes for caveats, source details, vintages, forecast flags, and
  transformations.

## Colors

### Core Brand Colors

| Name | Hex | RGB |
|---|---:|---:|
| Fund Blue | `#004C97` | `0,76,151` |
| Black | `#231F20` | `35,31,32` |
| Pantone 424 | `#707372` | `112,115,114` |
| White | `#FFFFFF` | `255,255,255` |
| Background | `#F3F4F5` | `243,244,245` |

Use Background `#F3F4F5` for surrounding canvas or page bands only. Keep the
plot area white by default.

### Categorical Color Order

Use this order when multiple categorical colors are needed:

1. Fund Blue `#004C97`
2. Pantone 2925 `#009CDE`
3. Pantone 130 `#F2A900`
4. Cool Gray 5 `#B1B3B3`
5. Pantone 2757 `#001E60`
6. Pantone 485 `#DA291C`

Avoid using many saturated colors when a highlight-plus-neutral design would
make the message clearer.

### Sequential Color Scales

When many ordered categories or value bands require color, use a sequential
scale instead of unrelated categorical colors.

- Prefer a single-hue or closely related scale anchored in Fund Blue.
- Use darker shades for larger or more important values and lighter shades for
  smaller values.
- Keep the scale monotonic and easy to explain.
- Include a legend or colorbar when color encodes values.
- Do not use a sequential scale for unrelated categorical series.

## Matplotlib Defaults

Generated Python scripts should encode the formatting choices explicitly:

- Set `font.family` to `Segoe UI`.
- Set `figsize=(13.333, 7.5)` and `dpi=150`.
- Set subplot margins to approximately left `0.08`, right `0.96`, top `0.84`,
  bottom `0.14`, adjusting bottom margin as needed for notes or long labels.
- Define brand color constants in the script.
- Set title, subtitle, axis label, tick label, source, and legend font sizes
  explicitly. For report figures, use 24 pt for figure titles and 10 pt for
  other chart text unless the output is only for screen review.
- Use light borders and gridlines.
- Save PNG output at the standard size unless the user requests another format.

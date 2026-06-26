# Chart Formatting Rules

Use these rules as the IMF house styling layer for standard static charts.
They define the default visual appearance for `imf-ra-charts`; they do not
override the analytical safety and chart-selection rules in
`chart-consulting-rules.md`.

## Formatting Priority

Apply formatting in this order:

1. Preserve analytical clarity and avoid misleading encodings.
2. Make the chart readable without relying on notes.
3. Apply the IMF house style canvas, typography, color, and spacing rules below.
4. Adjust only when the data shape, chart type, or user request requires it.

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
- Place title at the top-left above the plot area.
- Place subtitle directly below the title.
- Place source and notes at the bottom-left below the plot area.
- Keep source and notes outside the plotting area whenever practical.

## Typography

Use Segoe UI as the default chart font.

For chart-sheet style outputs:

| Element | Font | Size | Color |
|---|---|---:|---|
| All chart text | Segoe UI | 18 | Black/auto |
| Chart title | Segoe UI bold | 24 | RGB `75,130,173` (`#4B82AD`) |
| Chart subtitle | Segoe UI | 18 | RGB `75,130,173` (`#4B82AD`) |
| Axis labels | Segoe UI | 18 | Black/auto |
| Legend | Segoe UI | 18 | Black/auto |
| Source box | Segoe UI | 18 | Black/auto |

For panel-sheet style outputs:

- Default font size: 8.
- Do not use font sizes below 8 because they may become unreadable.

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

## Legend And Labels

- Legend background fill: no fill.
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
  explicitly.
- Use light borders and gridlines.
- Save PNG output at the standard size unless the user requests another format.

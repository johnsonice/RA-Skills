# <Database name> (e.g., World Economic Outlook — WEO)

> Template for a per-database catalog file. Copy to `<dbname>.md` and fill in.

## Dataflow identity

- **Dataflow ID:** `<e.g., WEO>`
- **Source:** `<URL or "internal Python SDK">`
- **Updated:** `<release cadence — e.g., biannual, October and April>`

## Primary dimensions

List the dataflow's dimensions and brief descriptions.

- `<dim 1>` — `<description>`
- `<dim 2>` — `<description>`

## Frequencies available

`<A | Q | M | …>` with notes on which series are available at which frequency.

## Common indicators

| Indicator | Code | Frequency | Unit | Notes |
|---|---|---|---|---|
| `<e.g., Real GDP growth>` | `NGDP_RPCH` | A | percent | |
| `<e.g., CPI inflation, period average>` | `PCPIPCH` | A | percent | |

## Country / geo conventions

How this database identifies geographies. Group codes that exist (e.g., `AE`, `EM`, `LIC`).

## Gotchas

- `<e.g., WEO is a forecast database — most-recent observations are projections, not realized data.>`
- `<e.g., Pre-2000 vintages used different country code conventions.>`

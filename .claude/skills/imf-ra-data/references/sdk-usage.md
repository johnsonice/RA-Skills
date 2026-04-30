# Internal Python SDK — usage

> _Placeholder._ Fill in once the SDK identity and API are confirmed.

## Installation and import

> Document the install command (pip / internal index) and the canonical import alias.

## Single-series fetch

> Document the function signature, required arguments, and a worked example:
> "Fetch WEO real GDP growth for the United States, annual, 2010–present."

## Multi-country panel

> Document how to fetch the same series across a list of geographies (e.g., G20, advanced economies)
> and return a tidy panel.

## Ratio of two series

> Document the canonical pattern for "series A divided by series B" — fetch each, align on
> `(geo, time)`, compute the ratio, return the tidy result.

## Frequency conversion

> Document how to convert between A/Q/M, including which aggregation method (mean, sum, last)
> the SDK uses and how to override.

## Gotchas

> Document rate limits, retry conventions, and large-pull patterns (chunking, async).

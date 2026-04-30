# Internal charting tool — usage

> _Placeholder._ Fill in once the charting tool's identity and API are confirmed.

## Installation and import

> Document install and import conventions.

## Invocation

> Document the tool's primary entry point, required arguments, and return shape.

## Input data shape

> Specify the tidy DataFrame shape the tool expects (column names, index, types). This must align with the output of `imf-ra-data`.

## Chart-type selection

> Document the chart types the tool supports and the heuristic for picking one from `(data shape, user intent)`.

## Captions, sources, footnotes

> Document the IMF source-line conventions the tool needs (e.g., "Source: IMF, World Economic Outlook").

## Output

> Document where the tool writes its output (file path, in-memory object) and how to surface it back to the RA.

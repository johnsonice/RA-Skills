#!/usr/bin/env python3
"""
Pre-built iData fetch utility for the imf-ra-data skill.
The agent calls this via Bash — never write a new retrieval script.

Modes (use this script for all SDK interactions — never write a new Python script):

  1. List dimension names for a confirmed database:
     --db DB --explore
       Prints dimension names in key order. Use this to understand the key structure.

  2. List valid codes for a specific dimension:
     --db DB --dimension-values DIM [--keyword KEYWORD]
       Prints all valid codes and labels as "Label (CODE)". Use --keyword to filter.
       --keyword matches against both codes and labels, so "USA" and "United States"
       both work depending on how the database encodes values.

  3. Fetch data:
     --db DB --key KEY --start START --end END --format {refreshable,wide,long}
     [--indicator-dim DIM] [--excel] [--output FILE]

Output formats (--format required for fetch):
  refreshable  RA enriched Excel (.xlsx). Layout auto-selected by number of indicators:
               - Single indicator → wide layout: one row per series, dates as columns.
                 Columns: DATASET | Series_Code | [CountryName | ISO3 | IFSCODE] |
                 [other dimension cols] | <indicator label col> | 2019 | 2020 | ...
               - Multiple indicators → long layout: one row per observation.
                 Columns: DATASET | Series_Code | [CountryName | ISO3 | IFSCODE] |
                 [dimension cols — indicator dim shows label] | Date | Value
               Country columns included only when a country dimension is detected.
               Always .xlsx.
  wide         Raw API wide format (dates as rows, series as columns).
               Use --excel for .xlsx; omit for .csv.
  long         Raw API long format (one row per observation).
               Use --excel for .xlsx; omit for .csv.

Examples:
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py --db "IMF.RES.WEO:WEO_LIVE" --explore

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.RES.WEO:WEO_LIVE" --dimension-values FREQUENCY

  # WEO uses ISO3 codes for COUNTRY; WDI uses REF_AREA with region labels — use the
  # appropriate dimension name and keyword style for the database.
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.RES.WEO:WEO_LIVE" --dimension-values COUNTRY --keyword "USA"

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "WB:WDI" --dimension-values REF_AREA --keyword "Africa"

  # Single indicator, multi-country → refreshable produces wide layout (dates as columns)
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE" --key "USA+GBR.NGDP_RPCH..A" \\
      --start 2000 --end 2026 --format refreshable

  # Bloomberg (no country dim, single series)
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.CSF:BBGDL" --key "JPAYIELD_INDEX.PX_LAST.D" \\
      --start 2015 --end 2026 --format refreshable --indicator-dim TICKER

  # WDI — indicator dim is SERIES
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "WB:WDI" --key "A.AG_CON_FERT_PT_ZS.AFE" \\
      --start 2000 --end 2023 --format refreshable --indicator-dim SERIES

  # Multi-indicator → refreshable produces long layout (one row per observation)
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.RES.WEO:WEO_LIVE" --key "USA.NGDP_RPCH+NGDP_D..A" \\
      --start 2000 --end 2026 --format refreshable

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \\
      --db "IMF.STA:CPI" --key "USA+JPN.CPI._T.IX.M" --start 2010 --end 2026 --format long

Key format notes:
  Dot-separated dimension values in the order shown by --explore.
  Omit a value to select all (blank between dots).
  Separate multiple values within a dimension with + (e.g. USA+GBR+DEU).
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import pandas as pd
from imf_datatools import idata_utilities

# LIVE databases (WEO_LIVE, GAS_LIVE, GEE_LIVE, etc.) are private IMF datasets.
# Safe to leave on for public databases as well.
idata_utilities.PRIVATE = True

# Country lookup: lives in the imf-ra skill, two levels up from here
COUNTRIES_CSV = (
    Path(__file__).parents[2] / "imf-ra" / "references" / "Country Group" / "csv" / "1. countries.csv"
)

# Candidate column names for the COUNTRY dimension (tried in order)
_COUNTRY_DIMS = ("COUNTRY", "country", "GEO", "geo", "REF_AREA", "COUNTERPART_AREA")

# Fallback candidate names for the indicator dimension when --indicator-dim is not specified.
# Prefer explicit --indicator-dim (from catalog handoff) over this list.
_INDICATOR_DIMS = (
    "INDICATOR", "indicator",
    "SERIES", "series",
    "TICKER", "ticker",
    "SUBJECT", "subject",
)


def load_country_lookup():
    """Return {iso3: {name, ifs}} from the RA catalog 1. countries.csv."""
    try:
        df = pd.read_csv(COUNTRIES_CSV, dtype=str)
        return {
            row["countrycode"]: {"name": row["countryname"], "ifs": row["countrycode_s"]}
            for _, row in df.iterrows()
            if pd.notna(row.get("countrycode"))
        }
    except Exception as exc:
        print(f"Warning: could not load country lookup ({exc})", file=sys.stderr)
        return {}


def format_date_label(ts, freq_code):
    """Format a period-start Timestamp as a date label.

    Annual  -> '2019'
    Quarter -> '2019Q1'
    Monthly -> '2019M1'
    Daily   -> '2019-01-31'
    """
    f = (freq_code or "").upper()
    if f == "A":
        return str(ts.year)
    if f == "Q":
        return f"{ts.year}Q{ts.quarter}"
    if f == "M":
        return f"{ts.year}M{ts.month}"
    if f == "D":
        return str(ts.date())
    return str(ts.date())


def detect_freq(df):
    """Detect frequency string from a FREQUENCY/FREQ dimension column, if present."""
    for col in ("FREQUENCY", "FREQ", "frequency", "freq"):
        if col in df.columns:
            vals = df[col].dropna().unique()
            if len(vals) == 1:
                return str(vals[0])
    return None


def build_refreshable_output(df_long, db, country_lookup, indicator_dim=None):
    """Build the RA refreshable enriched format. Layout is auto-selected:

    - Single indicator → wide layout (dates as columns, one row per series):
        DATASET | Series_Code | [CountryName | ISO3 | IFSCODE] |
        [other dim cols] | <indicator label col> | 2019 | 2020 | ...

    - Multiple indicators → long layout (one row per observation):
        DATASET | Series_Code | [CountryName | ISO3 | IFSCODE] |
        [dim cols — indicator dim shows label] | Date | Value

    Country columns (CountryName, ISO3, IFSCODE) are included only when a country
    dimension is detected. The indicator column always shows the human-readable label.

    Args:
        indicator_dim: explicit indicator dimension name from catalog handoff
                       (e.g. TICKER for BBG, SERIES for WDI). Overrides auto-detection.
    """
    # ── 1. Normalize: bring DatetimeIndex into a regular column ───────────────
    if isinstance(df_long.index, pd.DatetimeIndex):
        df_long = df_long.reset_index()
        date_col = df_long.columns[0]
    else:
        candidates = [c for c in df_long.columns
                      if any(k in str(c).lower() for k in ("date", "time", "period"))]
        date_col = candidates[0] if candidates else df_long.columns[0]

    df_long[date_col] = pd.to_datetime(df_long[date_col])

    # ── 2. Find value column ──────────────────────────────────────────────────
    val_col = next(
        (c for c in ("value", "values", "OBS_VALUE", "obs_value") if c in df_long.columns),
        None,
    )
    if val_col is None:
        numeric = df_long.select_dtypes(include="number").columns.tolist()
        val_col = numeric[-1] if numeric else df_long.columns[-1]

    # ── 3. Identify dimension columns ─────────────────────────────────────────
    id_cols = [c for c in df_long.columns if c not in (date_col, val_col)]
    country_col = next((c for c in _COUNTRY_DIMS if c in id_cols), None)
    if indicator_dim and indicator_dim in id_cols:
        indicator_col = indicator_dim
    else:
        indicator_col = next((c for c in _INDICATOR_DIMS if c in id_cols), None)

    # ── 4. Detect frequency and decide layout ─────────────────────────────────
    freq_code = detect_freq(df_long)
    n_indicators = df_long[indicator_col].nunique() if indicator_col else 0
    use_wide = n_indicators <= 1  # single indicator → wide; multiple → long

    # ── 5. Look up indicator labels once ─────────────────────────────────────
    ind_map = {}
    if indicator_col:
        try:
            ind_meta = idata_utilities.get_dimension_values(db, indicator_col)
            ind_map = ind_meta.set_index("Code")["Name"].to_dict()
        except Exception:
            pass

    # ── 6. Build shared metadata columns ─────────────────────────────────────
    # These are the same regardless of wide/long layout.
    out = pd.DataFrame()
    out["DATASET"] = db

    # Series_Code: all dimension values joined with "." in key order
    if id_cols:
        out["Series_Code"] = df_long[id_cols].apply(
            lambda row: ".".join(str(v) for v in row if pd.notna(v) and str(v) != ""),
            axis=1,
        )
    else:
        out["Series_Code"] = ""

    # Country enrichment — only when a country dimension is present.
    # ISO3 is the raw country code; CountryName and IFSCODE are best-effort enrichments.
    if country_col:
        iso3 = df_long[country_col].astype(str)
        out["CountryName"] = iso3.map(lambda x: country_lookup.get(x, {}).get("name", ""))
        out["ISO3"]        = iso3
        out["IFSCODE"]     = iso3.map(lambda x: country_lookup.get(x, {}).get("ifs",  ""))

    # Non-country, non-indicator dimension columns retain their actual names and codes.
    other_dims = [c for c in id_cols if c != country_col and c != indicator_col]
    for col in other_dims:
        out[col] = df_long[col].values

    # Indicator column always shows the human-readable label.
    if indicator_col:
        out[indicator_col] = df_long[indicator_col].astype(str).map(lambda x: ind_map.get(x, x))

    # ── 7a. Wide layout (single indicator) — pivot dates to columns ───────────
    if use_wide:
        df_long["_label"] = df_long[date_col].apply(lambda t: format_date_label(t, freq_code))

        # Build a mapping from label → date for chronological sort
        label_to_date = (
            df_long[["_label", date_col]].drop_duplicates()
            .sort_values(date_col)
            .set_index("_label")[date_col].to_dict()
        )
        date_labels_sorted = sorted(label_to_date, key=lambda x: label_to_date[x])

        # Add value and date label columns, then pivot
        out = out.reset_index(drop=True)
        out["_date_label"] = df_long["_label"].values
        out["_value"] = df_long[val_col].values
        pivot = out.pivot_table(
            index=[c for c in out.columns if c not in ("_date_label", "_value")],
            columns="_date_label",
            values="_value",
            aggfunc="first",
        ).reset_index()
        pivot.columns.name = None

        # Reorder date columns chronologically
        non_date = [c for c in pivot.columns if c not in date_labels_sorted]
        date_present = [c for c in date_labels_sorted if c in pivot.columns]
        return pivot[non_date + date_present]

    # ── 7b. Card layout (multiple indicators) ────────────────────────────────
    # Structure: Label column + one column per series (named by Series_Code).
    # Rows: metadata labels (DATASET, Series_Code, dim names) followed by date rows.
    # Each series column holds the metadata values and then the time-series values.

    # Collect per-series data: {series_code: {label → value}}
    series_data = {}
    for series_key, grp in df_long.groupby(id_cols, sort=False):
        if not isinstance(series_key, tuple):
            series_key = (series_key,)

        series_code = ".".join(
            str(v) for v in series_key if pd.notna(v) and str(v) != ""
        )

        row_data: dict = {}
        row_data["DATASET"] = db
        row_data["Series_Code"] = series_code

        if country_col:
            idx = id_cols.index(country_col)
            cv = str(series_key[idx])
            row_data["CountryName"] = country_lookup.get(cv, {}).get("name", "")
            row_data["ISO3"]        = cv
            row_data["IFSCODE"]     = country_lookup.get(cv, {}).get("ifs", "")

        for i, col in enumerate(id_cols):
            if col == country_col:
                continue
            val = str(series_key[i])
            row_data[col] = ind_map.get(val, val) if col == indicator_col else val

        for _, r in grp.sort_values(date_col).iterrows():
            lbl = format_date_label(pd.Timestamp(r[date_col]), freq_code)
            row_data[lbl] = r[val_col]

        series_data[series_code] = row_data

    # Determine label order: fixed metadata rows first, then dates chronologically
    meta_labels = ["DATASET", "Series_Code"]
    if country_col:
        meta_labels += ["CountryName", "ISO3", "IFSCODE"]
    for col in id_cols:
        if col != country_col:
            meta_labels.append(col)

    date_ts: dict = {}
    for _, r in df_long.iterrows():
        ts  = pd.Timestamp(r[date_col])
        lbl = format_date_label(ts, freq_code)
        date_ts[lbl] = ts
    sorted_date_labels = sorted(date_ts, key=lambda x: date_ts[x])

    all_labels = meta_labels + sorted_date_labels

    # Build result: first column = Label, one column per series
    result = pd.DataFrame({"Label": all_labels})
    for sc, data in series_data.items():
        result[sc] = [data.get(lbl, "") for lbl in all_labels]
    return result.reset_index(drop=True)


# Required columns that must always be present in refreshable output.
_REFRESHABLE_REQUIRED_COLS = {"DATASET", "Series_Code"}
_DATE_LABEL_RE = re.compile(
    r"^\d{4}$"               # annual:    2019
    r"|^\d{4}Q[1-4]$"       # quarterly: 2019Q1
    r"|^\d{4}M\d{1,2}$"     # monthly:   2019M1
    r"|^\d{4}-\d{2}-\d{2}$" # daily:     2019-01-31
)


def validate_refreshable_output(df, db):
    """Validate the refreshable output against the RA standard format.
    Returns (is_valid, list_of_error_strings).
    """
    errors = []

    # 1. Core columns always present
    missing = _REFRESHABLE_REQUIRED_COLS - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
        return False, errors

    if df.empty:
        errors.append("Output is empty.")
        return False, errors

    # 2. DATASET — must match --db argument
    if not (df["DATASET"] == db).all():
        errors.append(f"DATASET column does not match database '{db}'.")

    # 3. Series_Code — must be dot-separated
    no_dot = df["Series_Code"].dropna().astype(str)
    no_dot = no_dot[~no_dot.str.contains(r"\.", regex=True)]
    if not no_dot.empty:
        errors.append("Series_Code has values without dots — key construction may be incorrect.")

    # 4. Country columns — validate only when present
    if "ISO3" in df.columns:
        bad_iso = df["ISO3"].dropna().astype(str)
        bad_iso = bad_iso[~bad_iso.str.match(r"^[A-Z]{2,4}$|^G\w+$")]
        if not bad_iso.empty:
            errors.append(f"ISO3 has unexpected values: {bad_iso.unique()[:3].tolist()}")

    if "IFSCODE" in df.columns:
        bad_ifs = df["IFSCODE"].dropna().astype(str)
        bad_ifs = bad_ifs[~bad_ifs.str.match(r"^\d+$|^$")]
        if not bad_ifs.empty:
            errors.append(f"IFSCODE has non-numeric values: {bad_ifs.unique()[:3].tolist()}")

    if "CountryName" in df.columns:
        if (df["CountryName"].isna() | (df["CountryName"].astype(str).str.strip() == "")).all():
            errors.append("CountryName is empty — country lookup may have failed.")

    # 5. Layout-specific checks
    if "Label" in df.columns:
        # Card layout (multi-indicator): Label column + series columns
        label_vals = df["Label"].astype(str).tolist()
        if "DATASET" not in label_vals:
            errors.append("Card layout is missing a DATASET label row.")
        if "Series_Code" not in label_vals:
            errors.append("Card layout is missing a Series_Code label row.")
        date_rows = [v for v in label_vals if _DATE_LABEL_RE.match(v)]
        if not date_rows:
            errors.append("Card layout has no date rows — data may be empty.")
        series_cols = [c for c in df.columns if c != "Label"]
        if not series_cols:
            errors.append("Card layout has no series columns.")
    elif "Date" in df.columns:
        # Tabular long (not currently used but guard against regression)
        bad_dates = df["Date"].dropna().astype(str)
        bad_dates = bad_dates[~bad_dates.str.match(_DATE_LABEL_RE.pattern)]
        if not bad_dates.empty:
            errors.append(f"Date column has unexpected format: {bad_dates.unique()[:3].tolist()}")
        if "Value" not in df.columns:
            errors.append("Long layout is missing the Value column.")
    else:
        # Wide layout (single indicator) — check that at least one date column exists
        date_cols = [c for c in df.columns
                     if c not in _REFRESHABLE_REQUIRED_COLS
                     and c not in ("CountryName", "ISO3", "IFSCODE")
                     and _DATE_LABEL_RE.match(str(c))]
        if not date_cols:
            errors.append("Wide layout has no date columns — pivot may have failed.")

    return len(errors) == 0, errors


def validate_output_format(fmt, excel, output_path):
    """Validate that the output file extension matches the requested format and flags.
    Returns (is_valid, list_of_error_strings).
    """
    errors = []
    if fmt == "refreshable" and not output_path.endswith(".xlsx"):
        errors.append("Refreshable format must be saved as .xlsx.")
    if fmt in ("wide", "long") and excel and not output_path.endswith(".xlsx"):
        errors.append("--excel flag is set but output path is not .xlsx.")
    if fmt in ("wide", "long") and not excel and not output_path.endswith(".csv"):
        errors.append("Output should be .csv when --excel is not set.")
    return len(errors) == 0, errors


def save_output(df, path):
    """Save DataFrame to Excel or CSV depending on file extension."""
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    else:
        try:
            df.to_excel(path, index=False)
        except ImportError:
            fallback = path.replace(".xlsx", ".csv")
            print("Warning: no Excel writer engine available — saving as CSV instead.", file=sys.stderr)
            df.to_csv(fallback, index=False)
            return fallback
    return path


def main():
    parser = argparse.ArgumentParser(
        description="Fetch iData time series. Use --format to select output format."
    )
    parser.add_argument("--db", required=True,
                        help="iData database identifier (e.g. IMF.RES.WEO:WEO_LIVE)")
    # Explore / metadata modes (no fetch)
    parser.add_argument("--explore", action="store_true",
                        help="List all dimension names for the database in key order (no fetch).")
    parser.add_argument("--dimension-values", default=None, metavar="DIM", dest="dim_values",
                        help="List all valid codes and labels for a specific dimension.")
    parser.add_argument("--keyword", default=None,
                        help="Filter codes by keyword (used with --dimension-values).")
    # Fetch mode args
    parser.add_argument("--key", default=None,
                        help="iData dot-separated dimension key (e.g. USA+GBR.NGDP_RPCH..A)")
    parser.add_argument("--start", default=None,
                        help="Start period (e.g. 2015 or 2015-01)")
    parser.add_argument("--end",   default=None,
                        help="End period (e.g. 2026 or 2026-12)")
    parser.add_argument("--format", default=None, choices=["refreshable", "wide", "long"],
                        dest="fmt",
                        help="Output format: refreshable (RA enriched auto-layout), "
                             "wide (API wide), long (API long)")
    parser.add_argument("--indicator-dim", default=None, dest="indicator_dim",
                        help="Indicator dimension name for the database (e.g. TICKER for BBG, "
                             "SERIES for WDI). From the catalog handoff dimension_name field. "
                             "Overrides automatic detection.")
    parser.add_argument("--excel", action="store_true",
                        help="Save wide/long output as .xlsx instead of .csv (ignored for refreshable)")
    parser.add_argument("--output", default=None,
                        help="Output file path (auto-named if omitted)")
    args = parser.parse_args()

    # ── Explore mode ──────────────────────────────────────────────────────────
    if args.explore:
        try:
            dims = idata_utilities.get_dimensions(args.db)
        except Exception as exc:
            print(f"ERROR fetching dimensions: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"Dimensions for {args.db} (in key order):")
        print("-" * 60)
        for _, row in dims.iterrows():
            dim_name = row.get("Dimension", row.iloc[0])
            print(f"  {dim_name}")
        print("\nUse --dimension-values <DIM> to see valid codes for a specific dimension.")
        return

    # ── Dimension-values mode ─────────────────────────────────────────────────
    if args.dim_values:
        try:
            vals = idata_utilities.get_dimension_values(
                args.db, args.dim_values,
                keyword=args.keyword if args.keyword else None,
            )
        except Exception as exc:
            print(f"ERROR fetching dimension values: {exc}", file=sys.stderr)
            sys.exit(1)
        print(f"{args.dim_values} values for {args.db}:")
        print("-" * 60)
        for _, row in vals.iterrows():
            print(f"  {row['Name']} ({row['Code']})")
        return

    # ── Fetch mode ────────────────────────────────────────────────────────────
    if args.fmt is None:
        parser.error("--format is required when fetching data")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output is None:
        ext = "xlsx" if (args.fmt == "refreshable" or args.excel) else "csv"
        args.output = f"idata_{ts}.{ext}"

    # Validate output format/extension match
    fmt_valid, fmt_errors = validate_output_format(args.fmt, args.excel, args.output)
    if not fmt_valid:
        for e in fmt_errors:
            print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Database : {args.db}")
    print(f"Key      : {args.key}")
    if args.start or args.end:
        print(f"Period   : {args.start or 'earliest'} -> {args.end or 'latest'}")
    print(f"Format   : {args.fmt}")
    print(f"Output   : {args.output}")
    print("-" * 60)

    # wide format uses the API's native wide output; long and refreshable use long internally
    use_long = args.fmt != "wide"

    try:
        df = idata_utilities.get_idata_data(
            args.db, args.key,
            start=args.start,
            end=args.end,
            longformat=use_long,
            debug=False,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if df is None or df.empty:
        print("No data returned. Check the key, database identifier, and period.")
        sys.exit(1)

    if args.fmt == "long":
        out_df = df.reset_index() if isinstance(df.index, pd.DatetimeIndex) else df
        saved = save_output(out_df, args.output)
        print(f"\nSaved to: {saved}")
        return

    if args.fmt == "wide":
        out_df = df.reset_index() if isinstance(df.index, pd.DatetimeIndex) else df
        saved = save_output(out_df, args.output)
        print(f"\nSaved to: {saved}")
        return

    # refreshable
    country_lookup = load_country_lookup()
    out = build_refreshable_output(df, args.db, country_lookup, indicator_dim=args.indicator_dim)

    # Validate refreshable output before saving
    rf_valid, rf_errors = validate_refreshable_output(out, args.db)
    if not rf_valid:
        print("WARNING: Refreshable output failed validation:", file=sys.stderr)
        for e in rf_errors:
            print(f"  - {e}", file=sys.stderr)

    layout = "card" if "Label" in out.columns else "wide"
    print(f"Layout   : refreshable ({layout})")
    print(f"Output shape: {out.shape[0]} rows x {out.shape[1]} columns")
    print()
    print(out.head().to_string())

    saved = save_output(out, args.output)
    print(f"\nSaved to: {saved}")


if __name__ == "__main__":
    main()

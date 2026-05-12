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

  3. Fetch data:
     --db DB --key KEY --start START --end END --format {refreshable,wide,long} [--excel] [--output FILE]

Output formats (--format required for fetch):
  refreshable  RA structured Excel (.xlsx): CountryName | ISO3 | IFSCODE | DATASET |
               Series_Code | INDICATOR | 2019 | 2019Q1 | ... Always .xlsx.
  wide         Raw API wide format (dates as rows, series as columns).
               Use --excel for .xlsx; omit for .csv.
  long         Raw API long format (one row per observation).
               Use --excel for .xlsx; omit for .csv.

Examples:
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py --db "IMF.RES.WEO:WEO_LIVE" --explore

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.RES.WEO:WEO_LIVE" --dimension-values FREQUENCY

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.RES.WEO:WEO_LIVE" --dimension-values COUNTRY --keyword "United States"

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE" --key "USA+GBR.NGDP_RPCH..A" \
      --start 2000 --end 2026 --format refreshable

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
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

# Country lookup: countries.csv lives in the imf-ra skill, two levels up from here
COUNTRIES_CSV = (
    Path(__file__).parents[2] / "imf-ra" / "references" / "Country Group" / "csv" / "countries.csv"
)

# Candidate column names for the COUNTRY and INDICATOR dimensions (tried in order)
_COUNTRY_DIMS  = ("COUNTRY", "country", "GEO", "geo", "REF_AREA", "COUNTERPART_AREA")
_INDICATOR_DIMS = ("INDICATOR", "indicator", "SERIES", "series", "SUBJECT", "subject")


def load_country_lookup():
    """Return {iso3: {name, ifs}} from the RA catalog countries.csv."""
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
    """Format a period-start Timestamp as a date column header.

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


def build_wide_output(df_long, db, country_lookup):
    """Reshape long-format iData output to the RA standard wide Excel format."""
    # ── 1. Normalise: bring DatetimeIndex into a regular column ──────────────
    if isinstance(df_long.index, pd.DatetimeIndex):
        df_long = df_long.reset_index()
        date_col = df_long.columns[0]
    else:
        candidates = [c for c in df_long.columns
                      if any(k in str(c).lower() for k in ("date", "time", "period"))]
        date_col = candidates[0] if candidates else df_long.columns[0]

    df_long[date_col] = pd.to_datetime(df_long[date_col])

    # ── 2. Find value column ─────────────────────────────────────────────────
    val_col = next(
        (c for c in ("value", "values", "OBS_VALUE", "obs_value") if c in df_long.columns),
        None,
    )
    if val_col is None:
        numeric = df_long.select_dtypes(include="number").columns.tolist()
        val_col = numeric[-1] if numeric else df_long.columns[-1]

    # ── 3. Build date labels ─────────────────────────────────────────────────
    freq_code = detect_freq(df_long)
    df_long["_label"] = df_long[date_col].apply(lambda t: format_date_label(t, freq_code))

    # ── 4. Identify dimension columns ────────────────────────────────────────
    id_cols = [c for c in df_long.columns if c not in (date_col, val_col, "_label")]
    country_col   = next((c for c in _COUNTRY_DIMS   if c in id_cols), None)
    indicator_col = next((c for c in _INDICATOR_DIMS if c in id_cols), None)

    # ── 5. Pivot to wide ─────────────────────────────────────────────────────
    wide = df_long.pivot_table(
        index=id_cols, columns="_label", values=val_col, aggfunc="first"
    ).reset_index()

    # Sort date columns chronologically
    label_to_date = (
        df_long[["_label", date_col]].drop_duplicates()
        .sort_values(date_col)
        .set_index("_label")[date_col].to_dict()
    )
    date_cols_sorted = sorted(
        [c for c in wide.columns if c in label_to_date],
        key=lambda x: label_to_date[x],
    )
    meta_cols = [c for c in wide.columns if c not in date_cols_sorted]
    wide = wide[meta_cols + date_cols_sorted]

    # ── 6. Build RA standard output ──────────────────────────────────────────
    out = pd.DataFrame()

    # Country enrichment from RA catalog
    if country_col and country_col in wide.columns:
        iso3 = wide[country_col].astype(str)
        out["CountryName"] = iso3.map(lambda x: country_lookup.get(x, {}).get("name", ""))
        out["ISO3"]        = iso3
        out["IFSCODE"]     = iso3.map(lambda x: country_lookup.get(x, {}).get("ifs",  ""))
    else:
        out["CountryName"] = ""
        out["ISO3"]        = ""
        out["IFSCODE"]     = ""

    out["DATASET"] = db

    # Series_Code: all dimension columns joined with "." in key order
    if id_cols:
        out["Series_Code"] = wide[id_cols].apply(
            lambda row: ".".join(str(v) for v in row if pd.notna(v) and str(v) != ""),
            axis=1,
        )
    else:
        out["Series_Code"] = ""

    # INDICATOR: use the human-readable name/label, not the code (code is in Series_Code)
    if indicator_col and indicator_col in wide.columns:
        try:
            ind_meta = idata_utilities.get_dimension_values(db, indicator_col)
            ind_map = ind_meta.set_index("Code")["Name"].to_dict()
            out["INDICATOR"] = wide[indicator_col].astype(str).map(lambda x: ind_map.get(x, x))
        except Exception:
            out["INDICATOR"] = wide[indicator_col].astype(str)
    else:
        out["INDICATOR"] = ""

    for dc in date_cols_sorted:
        out[dc] = wide[dc].values

    return out


_REFRESHABLE_REQUIRED_COLS = {"CountryName", "ISO3", "IFSCODE", "DATASET", "Series_Code", "INDICATOR"}
_DATE_COL_RE = re.compile(
    r"^\d{4}$"               # annual:    2019
    r"|^\d{4}Q[1-4]$"       # quarterly: 2019Q1
    r"|^\d{4}M\d{1,2}$"     # monthly:   2019M1
    r"|^\d{4}-\d{2}-\d{2}$" # daily:     2019-01-31
)


def validate_refreshable_output(df, db):
    """Validate that the refreshable output conforms to the RA standard format.
    Returns (is_valid, list_of_error_strings).
    """
    errors = []

    # 1. Required columns
    missing = _REFRESHABLE_REQUIRED_COLS - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
        return False, errors

    if df.empty:
        errors.append("Output is empty.")
        return False, errors

    # 2. CountryName — should be non-empty text
    if (df["CountryName"].isna() | (df["CountryName"].astype(str).str.strip() == "")).all():
        errors.append("CountryName is empty — country lookup may have failed.")

    # 3. ISO3 — 2-4 uppercase letters or group code (G...)
    bad_iso = df["ISO3"].dropna().astype(str)
    bad_iso = bad_iso[~bad_iso.str.match(r"^[A-Z]{2,4}$|^G\w+$")]
    if not bad_iso.empty:
        errors.append(f"ISO3 has unexpected values: {bad_iso.unique()[:3].tolist()}")

    # 4. IFSCODE — should be numeric strings
    bad_ifs = df["IFSCODE"].dropna().astype(str)
    bad_ifs = bad_ifs[~bad_ifs.str.match(r"^\d+$|^$")]
    if not bad_ifs.empty:
        errors.append(f"IFSCODE has non-numeric values: {bad_ifs.unique()[:3].tolist()}")

    # 5. DATASET — should match the --db argument
    if not (df["DATASET"] == db).all():
        errors.append(f"DATASET column does not match database '{db}'.")

    # 6. Series_Code — should be dot-separated
    no_dot = df["Series_Code"].dropna().astype(str)
    no_dot = no_dot[~no_dot.str.contains(r"\.", regex=True)]
    if not no_dot.empty:
        errors.append("Series_Code has values without dots — key construction may be incorrect.")

    # 7. INDICATOR — should be non-empty text
    if (df["INDICATOR"].isna() | (df["INDICATOR"].astype(str).str.strip() == "")).all():
        errors.append("INDICATOR column is empty.")

    # 8. Date columns — at least one, correctly formatted
    date_cols = [c for c in df.columns if c not in _REFRESHABLE_REQUIRED_COLS]
    if not date_cols:
        errors.append("No date columns found — data pivot may have failed.")
    else:
        bad_dates = [c for c in date_cols if not _DATE_COL_RE.match(str(c))]
        if bad_dates:
            errors.append(f"Date columns with unexpected format: {bad_dates[:5]}")

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
                        help="Output format: refreshable (RA Excel), wide (API wide), long (API long)")
    parser.add_argument("--excel", action="store_true",
                        help="Save wide/long output as .xlsx instead of .csv (ignored for refreshable)")
    parser.add_argument("--output", default=None,
                        help="Output file path (auto-named if omitted)")
    args = parser.parse_args()

    # ── Explore mode ─────────────────────────────────────────────────────────
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

    # ── Dimension-values mode ────────────────────────────────────────────────
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

    # ── Fetch mode ───────────────────────────────────────────────────────────
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
    out = build_wide_output(df, args.db, country_lookup)

    # Validate refreshable output before saving
    rf_valid, rf_errors = validate_refreshable_output(out, args.db)
    if not rf_valid:
        print("WARNING: Refreshable output failed validation:", file=sys.stderr)
        for e in rf_errors:
            print(f"  - {e}", file=sys.stderr)

    print(f"Output shape: {out.shape[0]} rows x {out.shape[1]} columns")
    print()
    print(out.head().to_string())

    saved = save_output(out, args.output)
    print(f"\nSaved to: {saved}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Pre-built iData fetch utility for the imf-ra-data skill.
The agent calls this via Bash — never write a new retrieval script.

Usage:
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db DB --key KEY [--start START] [--end END] [--longformat] [--output FILE]

Default output: wide RA Excel (.xlsx) with headers:
  CountryName | ISO3 | IFSCODE | DATASET | Series_Code | INDICATOR | 2019 | 2020 | ...
  Date column format: 2019 (annual), 2019Q1 (quarterly), 2019M1 (monthly).
  CountryName and IFSCODE are looked up from the RA catalog countries.csv using ISO3.

Examples:
  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE" --key "USA+GBR.NGDP_RPCH..A" --start 2000

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.STA:CPI" --key "USA+JPN.CPI._T.IX.M" --start 2010 --output cpi.xlsx

  python .claude/skills/imf-ra-data/scripts/fetch_idata.py \
      --db "IMF.STA:CPI" --key "USA+JPN.CPI._T.IX.M" --start 2010 --longformat

Key format notes:
  Dot-separated dimension values in the order returned by get_dimensions().
  Omit a value to select all (blank between dots selects everything for that dimension).
  Separate multiple values within a dimension with + (e.g. USA+GBR+DEU).
  See dimension-resolution-guide.md for key construction rules.
"""

import argparse
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
    """
    f = (freq_code or "").upper()
    if f in ("A", "AN", "ANNUAL", "Y"):
        return str(ts.year)
    if f in ("Q", "QT", "QUARTERLY"):
        return f"{ts.year}Q{ts.quarter}"
    if f in ("M", "MO", "MONTHLY"):
        return f"{ts.year}M{ts.month}"
    # Infer from month: period-start for Q is Jan/Apr/Jul/Oct; annual is Jan
    m = ts.month
    if m == 1 and ts.day == 1:
        return str(ts.year)          # could be annual or Q1 — annual takes priority
    if m in (1, 4, 7, 10):
        return f"{ts.year}Q{ts.quarter}"
    return f"{ts.year}M{m}"


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
    other_dims    = [c for c in id_cols if c not in (country_col, indicator_col)]

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

    # Series_Code: all non-country, non-indicator dimensions joined with "."
    if other_dims:
        out["Series_Code"] = wide[other_dims].apply(
            lambda row: ".".join(str(v) for v in row if pd.notna(v) and str(v) != ""),
            axis=1,
        )
    elif indicator_col and indicator_col in wide.columns:
        out["Series_Code"] = wide[indicator_col].astype(str)
    else:
        out["Series_Code"] = ""

    out["INDICATOR"] = wide[indicator_col].astype(str) if (indicator_col and indicator_col in wide.columns) else ""

    for dc in date_cols_sorted:
        out[dc] = wide[dc].values

    return out


def save_output(df, path):
    """Save DataFrame to Excel or CSV depending on file extension."""
    if path.endswith(".csv"):
        df.to_csv(path, index=False)
    else:
        try:
            df.to_excel(path, index=False, engine="openpyxl")
        except ImportError:
            fallback = path.replace(".xlsx", ".csv")
            print("Warning: openpyxl not installed — saving as CSV instead.", file=sys.stderr)
            df.to_csv(fallback, index=False)
            return fallback
    return path


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Fetch iData time series and save in RA standard wide Excel format.\n"
            "Default: wide .xlsx with CountryName/ISO3/IFSCODE headers and formatted date columns."
        )
    )
    parser.add_argument("--db",  required=True,
                        help="iData database identifier (e.g. IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE)")
    parser.add_argument("--key", required=True,
                        help="iData dot-separated dimension key (e.g. USA+GBR.NGDP_RPCH..A)")
    parser.add_argument("--start", default=None,
                        help="Start period (e.g. 2015 or 2015-01)")
    parser.add_argument("--end",   default=None,
                        help="End period (e.g. 2026 or 2026-12)")
    parser.add_argument("--longformat", action="store_true",
                        help="Save raw long/tidy format as CSV instead of the RA wide Excel format")
    parser.add_argument("--output", default=None,
                        help="Output path (default: idata_YYYYMMDD_HHMMSS.xlsx or .csv with --longformat). "
                             "Force CSV with a .csv extension.")
    args = parser.parse_args()

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    if args.output is None:
        args.output = f"idata_{ts}.{'csv' if args.longformat else 'xlsx'}"

    print(f"Database : {args.db}")
    print(f"Key      : {args.key}")
    if args.start or args.end:
        print(f"Period   : {args.start or 'earliest'} -> {args.end or 'latest'}")
    print(f"Format   : {'long/tidy CSV' if args.longformat else 'wide RA Excel'}")
    print(f"Output   : {args.output}")
    print("-" * 60)

    try:
        df = idata_utilities.get_idata_data(
            args.db, args.key,
            start=args.start,
            end=args.end,
            longformat=True,   # always fetch long; we reshape ourselves
            debug=False,
        )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)

    if df is None or df.empty:
        print("No data returned. Check the key, database identifier, and period.")
        sys.exit(1)

    print(f"Raw rows fetched: {df.shape[0]}")

    if args.longformat:
        saved = save_output(df.reset_index() if isinstance(df.index, pd.DatetimeIndex) else df,
                            args.output)
        print(f"\nSaved to: {saved}")
        return

    country_lookup = load_country_lookup()
    out = build_wide_output(df, args.db, country_lookup)

    print(f"Output shape: {out.shape[0]} rows x {out.shape[1]} columns")
    print()
    print(out.to_string())

    saved = save_output(out, args.output)
    print(f"\nSaved to: {saved}")


if __name__ == "__main__":
    main()

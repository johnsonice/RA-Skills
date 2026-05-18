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
      --db "IMF.RES.WEO:WEO_LIVE" --key "USA.NGDP_RPCH+NGDP_D.A" \\
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


def _build_card_sheet(grp, db, country_lookup, id_cols, country_col,
                      indicator_col, ind_map, freq_code, date_col, val_col):
    """Build card format for one indicator: Label column + one column per series.

    Rows: metadata labels (DATASET, Series_Code, CountryName, ISO3, IFSCODE,
    other dims, indicator label) followed by date rows.
    Columns: one per unique series (named by Series_Code).
    """
    series_data: dict = {}
    for series_key, sg in grp.groupby(id_cols, sort=False):
        if not isinstance(series_key, tuple):
            series_key = (series_key,)
        series_code = ".".join(str(v) for v in series_key if pd.notna(v) and str(v) != "")

        row_data: dict = {"DATASET": db, "Series_Code": series_code}
        if country_col:
            idx = id_cols.index(country_col)
            cv  = str(series_key[idx])
            row_data["CountryName"] = country_lookup.get(cv, {}).get("name", "")
            row_data["ISO3"]        = cv
            row_data["IFSCODE"]     = country_lookup.get(cv, {}).get("ifs",  "")
        for i, col in enumerate(id_cols):
            if col == country_col:
                continue
            val = str(series_key[i])
            row_data[col] = ind_map.get(val, val) if col == indicator_col else val
        for _, r in sg.sort_values(date_col).iterrows():
            lbl = format_date_label(pd.Timestamp(r[date_col]), freq_code)
            row_data[lbl] = r[val_col]
        series_data[series_code] = row_data

    meta_labels = ["DATASET", "Series_Code"]
    if country_col:
        meta_labels += ["CountryName", "ISO3", "IFSCODE"]
    for col in id_cols:
        if col != country_col:
            meta_labels.append(col)

    date_ts: dict = {}
    for _, r in grp.iterrows():
        ts  = pd.Timestamp(r[date_col])
        lbl = format_date_label(ts, freq_code)
        date_ts[lbl] = ts
    sorted_dates = sorted(date_ts, key=lambda x: date_ts[x])

    all_labels = meta_labels + sorted_dates
    result = pd.DataFrame({"Label": all_labels})
    for sc, data in series_data.items():
        result[sc] = [data.get(lbl, "") for lbl in all_labels]
    return result.reset_index(drop=True)


def _build_wide_sheet(grp, db, country_lookup, id_cols, country_col,
                      indicator_col, ind_map, freq_code, date_col, val_col):
    """Build one wide DataFrame (dates as columns) for a single-indicator group."""
    grp = grp.reset_index(drop=True).copy()
    out = pd.DataFrame(index=grp.index)
    out["DATASET"] = db

    if id_cols:
        out["Series_Code"] = grp[id_cols].apply(
            lambda row: ".".join(str(v) for v in row if pd.notna(v) and str(v) != ""),
            axis=1,
        )
    else:
        out["Series_Code"] = ""

    if country_col:
        iso3 = grp[country_col].astype(str)
        out["CountryName"] = iso3.map(lambda x: country_lookup.get(x, {}).get("name", ""))
        out["ISO3"]        = iso3
        out["IFSCODE"]     = iso3.map(lambda x: country_lookup.get(x, {}).get("ifs",  ""))

    for col in id_cols:
        if col == country_col:
            continue
        if col == indicator_col:
            out[col] = grp[col].astype(str).map(lambda x: ind_map.get(x, x)).values
        else:
            out[col] = grp[col].values

    grp["_label"] = grp[date_col].apply(lambda t: format_date_label(t, freq_code))
    label_to_date = (
        grp[["_label", date_col]].drop_duplicates()
        .sort_values(date_col)
        .set_index("_label")[date_col].to_dict()
    )
    date_labels_sorted = sorted(label_to_date, key=lambda x: label_to_date[x])

    out = out.reset_index(drop=True)
    out["_date_label"] = grp["_label"].values
    out["_value"]      = grp[val_col].values
    pivot = out.pivot_table(
        index=[c for c in out.columns if c not in ("_date_label", "_value")],
        columns="_date_label",
        values="_value",
        aggfunc="first",
    ).reset_index()
    pivot.columns.name = None

    non_date   = [c for c in pivot.columns if c not in date_labels_sorted]
    date_present = [c for c in date_labels_sorted if c in pivot.columns]
    return pivot[non_date + date_present]


def build_refreshable_output(df_long, db, country_lookup, indicator_dim=None):
    """Build the RA refreshable enriched format. Layout is auto-selected by data shape:

    1. Wide (n_indicators == 1):
       Single sheet, dates as columns, one row per series.

    2. Multi-sheet card (n_indicators > 1 AND n_countries > 1 AND n_dates > 1):
       dict[sheet_name → DataFrame]. One card sheet per indicator (sheet name =
       indicator label, max 31 chars). Each sheet: Label col + one col per series.

    3. Single card (n_indicators > 1, but not all three dimensions plural):
       Single card DataFrame. Label col + one col per series (all indicators together).

    Country columns (CountryName, ISO3, IFSCODE) are included only when a country
    dimension is detected. The indicator column always shows the human-readable label.

    Returns:
        DataFrame (cases 1 and 3) or dict[str, DataFrame] (case 2).

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

    # ── 4. Detect frequency ───────────────────────────────────────────────────
    freq_code = detect_freq(df_long)
    n_indicators = df_long[indicator_col].nunique() if indicator_col else 0

    # ── 5. Look up indicator labels once ──────────────────────────────────────
    ind_map = {}
    if indicator_col:
        try:
            ind_meta = idata_utilities.get_dimension_values(db, indicator_col)
            ind_map = ind_meta.set_index("Code")["Name"].to_dict()
        except Exception:
            pass

    shared = dict(
        db=db, country_lookup=country_lookup, id_cols=id_cols,
        country_col=country_col, indicator_col=indicator_col,
        ind_map=ind_map, freq_code=freq_code, date_col=date_col, val_col=val_col,
    )

    # ── 6. Decide layout ──────────────────────────────────────────────────────
    n_countries = df_long[country_col].nunique() if country_col else 0
    n_dates     = df_long[date_col].nunique()

    # Multi-sheet card: only when all three dimensions are plural
    if n_indicators > 1 and n_countries > 1 and n_dates > 1:
        sheets: dict = {}
        used_names: dict = {}
        for ind_code, grp in df_long.groupby(indicator_col, sort=False):
            label = ind_map.get(str(ind_code), str(ind_code))
            base  = label[:31]
            if base in used_names:
                used_names[base] += 1
                sheet_name = base[:28] + f"_{used_names[base]}"
            else:
                used_names[base] = 1
                sheet_name = base
            sheets[sheet_name] = _build_card_sheet(grp.reset_index(drop=True), **shared)
        return sheets

    # n_indicators > 1 but not all three dimensions plural:
    # single card sheet with all series together
    if n_indicators > 1:
        return _build_card_sheet(df_long, **shared)

    # n_indicators <= 1: single wide sheet
    return _build_wide_sheet(df_long, **shared)


# Required columns that must always be present in refreshable output.
_REFRESHABLE_REQUIRED_COLS = {"DATASET", "Series_Code"}
_DATE_LABEL_RE = re.compile(
    r"^\d{4}$"               # annual:    2019
    r"|^\d{4}Q[1-4]$"       # quarterly: 2019Q1
    r"|^\d{4}M\d{1,2}$"     # monthly:   2019M1
    r"|^\d{4}-\d{2}-\d{2}$" # daily:     2019-01-31
)


def _validate_wide_sheet(df, db):
    """Validate one wide refreshable sheet. Returns list of error strings."""
    errors = []
    missing = _REFRESHABLE_REQUIRED_COLS - set(df.columns)
    if missing:
        errors.append(f"Missing required columns: {', '.join(sorted(missing))}")
        return errors
    if df.empty:
        errors.append("Sheet is empty.")
        return errors
    if not (df["DATASET"] == db).all():
        errors.append(f"DATASET column does not match database '{db}'.")
    no_dot = df["Series_Code"].dropna().astype(str)
    no_dot = no_dot[~no_dot.str.contains(r"\.", regex=True)]
    if not no_dot.empty:
        errors.append("Series_Code has values without dots.")
    if "ISO3" in df.columns:
        bad = df["ISO3"].dropna().astype(str)
        bad = bad[~bad.str.match(r"^[A-Z]{2,4}$|^G\w+$")]
        if not bad.empty:
            errors.append(f"ISO3 has unexpected values: {bad.unique()[:3].tolist()}")
    if "IFSCODE" in df.columns:
        bad = df["IFSCODE"].dropna().astype(str)
        bad = bad[~bad.str.match(r"^\d+$|^$")]
        if not bad.empty:
            errors.append(f"IFSCODE has non-numeric values: {bad.unique()[:3].tolist()}")
    if "CountryName" in df.columns:
        if (df["CountryName"].isna() | (df["CountryName"].astype(str).str.strip() == "")).all():
            errors.append("CountryName is empty — country lookup may have failed.")
    date_cols = [c for c in df.columns
                 if c not in _REFRESHABLE_REQUIRED_COLS
                 and c not in ("CountryName", "ISO3", "IFSCODE")
                 and _DATE_LABEL_RE.match(str(c))]
    if not date_cols:
        errors.append("No date columns found — pivot may have failed.")
    return errors


def _validate_card_sheet(df, db):
    """Validate one card-format sheet. Returns list of error strings."""
    errors = []
    if "Label" not in df.columns:
        errors.append("Missing 'Label' column.")
        return errors
    if df.empty:
        errors.append("Sheet is empty.")
        return errors
    label_vals = df["Label"].astype(str).tolist()
    if "DATASET" not in label_vals:
        errors.append("Missing DATASET label row.")
    if "Series_Code" not in label_vals:
        errors.append("Missing Series_Code label row.")
    date_rows = [v for v in label_vals if _DATE_LABEL_RE.match(v)]
    if not date_rows:
        errors.append("No date rows found — data may be empty.")
    if len(df.columns) < 2:
        errors.append("No series columns — expected one column per series.")
    # Check DATASET value in each series column
    if "DATASET" in label_vals:
        ds_idx = label_vals.index("DATASET")
        for col in df.columns[1:]:
            if str(df.at[ds_idx, col]) != db:
                errors.append(f"Column '{col}': DATASET row does not match '{db}'.")
                break
    return errors


def validate_refreshable_output(out, db):
    """Validate refreshable output (DataFrame or dict of DataFrames).
    Returns (is_valid, list_of_error_strings).
    """
    if isinstance(out, dict):
        # Multi-sheet card
        all_errors = []
        for sheet_name, df in out.items():
            for e in _validate_card_sheet(df, db):
                all_errors.append(f"[{sheet_name}] {e}")
        return len(all_errors) == 0, all_errors
    elif "Label" in out.columns:
        # Single card sheet
        errors = _validate_card_sheet(out, db)
        return len(errors) == 0, errors
    else:
        # Wide sheet
        errors = _validate_wide_sheet(out, db)
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
            dim_name = row.get("Dimension", row.iloc[0]).upper() ## get_dimension_values only take upper case dimension names
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
            #print(f"  {row['Name']} ({row['Code']})")
            print(f" {row})")
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

    # Validate refreshable output — hard fail so no misleading file is saved
    rf_valid, rf_errors = validate_refreshable_output(out, args.db)
    if not rf_valid:
        print("ERROR: Refreshable output failed validation — file not saved:", file=sys.stderr)
        for e in rf_errors:
            print(f"  - {e}", file=sys.stderr)
        sys.exit(1)

    if isinstance(out, dict):
        print(f"Layout   : refreshable (multi-sheet card, {len(out)} indicators)")
        try:
            with pd.ExcelWriter(args.output) as writer:
                for sheet_name, df_sheet in out.items():
                    df_sheet.to_excel(writer, sheet_name=sheet_name, index=False)
                    print(f"  Sheet '{sheet_name}': {df_sheet.shape[0]} rows x {df_sheet.shape[1]} cols")
        except ImportError:
            fallback = args.output.replace(".xlsx", ".csv")
            print("Warning: no Excel writer engine — saving first sheet as CSV.", file=sys.stderr)
            next(iter(out.values())).to_csv(fallback, index=False)
            args.output = fallback
        print(f"\nSaved to: {args.output}")
    else:
        layout = "card" if "Label" in out.columns else "wide"
        print(f"Layout   : refreshable ({layout})")
        print(f"Output shape: {out.shape[0]} rows x {out.shape[1]} columns")
        print()
        print(out.head().to_string())
        saved = save_output(out, args.output)
        print(f"\nSaved to: {saved}")


if __name__ == "__main__":
    main()

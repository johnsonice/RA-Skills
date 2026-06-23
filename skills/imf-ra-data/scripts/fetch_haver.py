#!/usr/bin/env python3
"""
Fetch Haver series via imf_datatools.haver_utilities.

Usage:
  python fetch_haver.py --codes "GDP@USECON" "UNRATE@USECON" --start 2000 --end 2024 --format refreshable

CODE@DB format: use the short Haver database code without the HAVER: prefix
(e.g. EMERGECW, INTDAILY, USECON — not HAVER:EMERGECW).
haver_catalog_search.py output shows database_name as HAVER:EMERGECW; strip the
prefix when building the @DB part of each code.

Output formats:
  refreshable  Card-format .xlsx: Label column + one column per series.
               Metadata rows (.DESC, .T1, .TN, .LSOURCE, .AGG, .FRQ, .DATA_TYPE, .MAG) then date rows.
               Always .xlsx.
  wide         Dates as rows, one column per series. CSV or .xlsx.
  long         One row per observation: Date, Ticker, Value. CSV or .xlsx.
"""

from __future__ import annotations

import argparse
import os
import sqlite3
import sys
from pathlib import Path

import pandas as pd


def _resolve_haver_db() -> Path:
    """Locate haver.db across environments (Windows/macOS/Linux/cloud).

    Resolution order:
      1. HAVER_DB_PATH environment variable (the only reliable option when the
         skill is installed into a global dir, e.g. ~/.copilot/skills).
      2. An upward search from this script: haver.db beside any ancestor
         directory. Covers the conventional "one level above the repo root"
         placement and works when scripts run from a mirrored skills dir.
      3. Fallback to a sensible path so the .exists() check downstream can emit
         a clear error if haver.db is found nowhere.

    Common locations:  macOS  ~/haver.db   Windows  Q:\\DATA\\SPRAI\\...\\haver.db
    """
    env = os.environ.get("HAVER_DB_PATH")
    if env:
        return Path(env).expanduser()
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "haver.db"
        if candidate.exists():
            return candidate
    return here.parents[2] / "haver.db"


_DB_PATH = _resolve_haver_db()

_FREQ_LABELS = {"A": "Annual", "Q": "Quarterly", "M": "Monthly", "W": "Weekly", "D": "Daily"}
_AGG_LABELS = {"AVG": "Average", "EOP": "End of Period", "SUM": "Sum", "NST": "Not Specified", "NDF": "Non-Disaggregated Flow"}


def _load_metadata(codes: list[str]) -> dict[str, dict]:
    """Look up indicator metadata from haver.db for each CODE@DATABASE string."""
    if not _DB_PATH.exists():
        return {}
    meta: dict[str, dict] = {}
    with sqlite3.connect(_DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        for code_at_db in codes:
            parts = code_at_db.upper().split("@", 1)
            if len(parts) != 2:
                continue
            code, database = parts
            # Tolerate HAVER:EMERGECW or EMERGECW — DB stores bare lowercase codes.
            if database.startswith("HAVER:"):
                database = database[6:]
            row = conn.execute(
                "SELECT descriptor, frequency, shortsource, longsource, startdate, enddate, "
                "datatype, aggtype, magnitude "
                "FROM indicators WHERE lower(code)=lower(?) AND lower(database)=lower(?)",
                (code, database),
            ).fetchone()
            if row:
                meta[code_at_db.upper()] = dict(row)
    return meta


def _fetch(codes: list[str]) -> pd.DataFrame:
    """Fetch from Haver. Returns wide DataFrame: DatetimeIndex, one column per CODE@DB."""
    from imf_datatools import haver_utilities
    df = haver_utilities.get_haver_data(codes)
    if df is None or df.empty:
        raise ValueError("No data returned from haver_utilities.get_haver_data().")
    df.index = pd.to_datetime(df.index)
    df.columns = [c.upper() for c in df.columns]
    return df


def _filter_dates(df: pd.DataFrame, start: str | None, end: str | None) -> pd.DataFrame:
    if start:
        df = df[df.index >= pd.to_datetime(start)]
    if end:
        df = df[df.index <= pd.to_datetime(end + "-12-31" if len(end) == 4 else end)]
    return df


def _format_date_label(ts: pd.Timestamp, freq: str) -> str:
    f = freq.upper()
    if f == "A":
        return str(ts.year)
    if f == "Q":
        return f"{ts.year}Q{ts.quarter}"
    if f == "M":
        return f"{ts.year}{ts.month:02d}"
    return ts.strftime("%Y-%m-%d")


def _detect_freq(df: pd.DataFrame) -> str:
    """Infer dominant frequency from the DatetimeIndex."""
    if len(df) < 2:
        return "D"
    delta = (df.index[1] - df.index[0]).days
    if delta >= 300:
        return "A"
    if delta >= 80:
        return "Q"
    if delta >= 25:
        return "M"
    if delta >= 5:
        return "W"
    return "D"


def _build_refreshable(df: pd.DataFrame, meta: dict[str, dict]) -> pd.DataFrame:
    """
    Card format: Label column + one column per series (CODE@DATABASE).
    Metadata row order matches Haver DLX convention:
    .DESC, .T1, .TN, .LSOURCE, .AGG, .FRQ, .DATA_TYPE, .MAG, then date rows.
    """
    codes = list(df.columns)
    freq = _detect_freq(df)

    def _m(c: str, key: str) -> str:
        return meta.get(c, {}).get(key) or ""

    meta_rows: dict[str, dict[str, str]] = {
        ".DESC":      {c: _m(c, "descriptor") for c in codes},
        ".T1":        {c: _m(c, "startdate")[:10] for c in codes},
        ".TN":        {c: _m(c, "enddate")[:10] for c in codes},
        ".LSOURCE":   {c: _m(c, "longsource") for c in codes},
        ".AGG":       {c: _AGG_LABELS.get(_m(c, "aggtype").upper(), _m(c, "aggtype")) for c in codes},
        ".FRQ":       {c: _FREQ_LABELS.get(_m(c, "frequency").upper(), _m(c, "frequency")) for c in codes},
        ".DATA_TYPE": {c: _m(c, "datatype") for c in codes},
        ".MAG":       {c: str(meta.get(c, {}).get("magnitude", "")) for c in codes},
    }

    all_labels = list(meta_rows.keys()) + [_format_date_label(ts, freq) for ts in df.index]
    result = pd.DataFrame({"Label": all_labels})
    for code in codes:
        meta_vals = [meta_rows[m][code] for m in meta_rows]
        data_vals = [df.at[ts, code] for ts in df.index]
        result[code] = meta_vals + data_vals
    return result.reset_index(drop=True)


def _build_wide(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out.index.name = "Date"
    return out.reset_index()


def _build_long(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.index.name = "Date"
    long = df.reset_index().melt(id_vars="Date", var_name="Ticker", value_name="Value")
    return long.sort_values(["Ticker", "Date"]).reset_index(drop=True)


def _save(df: pd.DataFrame, path: str, as_excel: bool) -> None:
    if as_excel or path.endswith(".xlsx"):
        df.to_excel(path, index=False)
    else:
        df.to_csv(path, index=False)
    print(f"Saved to {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--codes", nargs="+", required=True, metavar="CODE@DB",
                        help="One or more Haver codes, e.g. GDP@USECON UNRATE@USECON")
    parser.add_argument("--start", metavar="YYYY", help="Start year or date (YYYY or YYYY-MM-DD)")
    parser.add_argument("--end",   metavar="YYYY", help="End year or date (YYYY or YYYY-MM-DD)")
    parser.add_argument("--format", dest="fmt", required=True,
                        choices=["refreshable", "wide", "long"],
                        help="Output format")
    parser.add_argument("--excel", action="store_true",
                        help="Save wide/long as .xlsx instead of .csv")
    parser.add_argument("--output", metavar="FILE", help="Output file path")
    args = parser.parse_args()

    codes = [c.upper() for c in args.codes]

    try:
        df = _fetch(codes)
    except Exception as exc:
        print(f"[error] fetch failed: {exc}", file=sys.stderr)
        return 1

    df = _filter_dates(df, args.start, args.end)
    if df.empty:
        print("[error] No data in the requested date range.", file=sys.stderr)
        return 1

    meta = _load_metadata(codes)

    # If the API returned columns without the @DB suffix, remap meta keys to match.
    # Build a fallback index: code-only (before @) → full meta key.
    _code_only_index = {k.split("@")[0]: k for k in meta}
    for col in df.columns:
        if col not in meta and col.split("@")[0] in _code_only_index:
            meta[col] = meta[_code_only_index[col.split("@")[0]]]

    if args.fmt == "refreshable":
        out = _build_refreshable(df, meta)
        path = args.output or "haver_refreshable.xlsx"
        out.to_excel(path, index=False)
        print(f"Saved refreshable to {path}")

    elif args.fmt == "wide":
        out = _build_wide(df)
        path = args.output or ("haver_wide.xlsx" if args.excel else "haver_wide.csv")
        _save(out, path, args.excel)

    elif args.fmt == "long":
        out = _build_long(df)
        path = args.output or ("haver_long.xlsx" if args.excel else "haver_long.csv")
        _save(out, path, args.excel)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

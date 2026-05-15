#!/usr/bin/env python3
"""Search IMF variable and dataset reference CSVs for catalog lookups."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_DIR / "references"
DATABASES_DIR = SKILL_DIR / "databases"
VARIABLES_DIR = SKILL_DIR / "indicators"
VARIABLES_CSV = VARIABLES_DIR / "1. non_vintage_variable_list.csv"
NON_VINTAGE_DATASETS_CSV = DATABASES_DIR / "non_vintage_databases.csv"
VINTAGE_DATASETS_CSV = DATABASES_DIR / "vintage_databased.csv"
WEO_LIVE_DB = "IMF.RES.WEO:WEO_LIVE"
LEGACY_WEO_DB = "IMF.RES:WEO"
MONTHS = {
    "JAN": 1,
    "FEB": 2,
    "MAR": 3,
    "APR": 4,
    "MAY": 5,
    "JUN": 6,
    "JUL": 7,
    "AUG": 8,
    "SEP": 9,
    "OCT": 10,
    "NOV": 11,
    "DEC": 12,
}
QUERY_SYNONYMS = {
    "real": ["constant", "prices"],
    "growth": ["percent", "change"],
    "nominal": ["current", "prices"],
    "cpi": ["consumer", "prices"],
    "inflation": ["consumer", "prices", "percent", "change"],
    "ca": ["current", "account"],
    "cab": ["current", "account", "balance"],
    "fiscal": ["government"],
    "exports": ["export"],
    "imports": ["import"],
    "gdp": ["gross", "domestic", "product"],
    "usd": ["us", "dollar", "dollars"],
}


def norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").casefold()).strip()


def tokens(text: str) -> list[str]:
    base = [t for t in norm(text).split() if t]
    expanded = list(base)
    for token in base:
        expanded.extend(QUERY_SYNONYMS.get(token, []))
    return expanded


def parse_weo_sort_key(resource_id: str) -> tuple[int, int, int]:
    match = re.search(r"WEO_LIVE_(\d{4})_([A-Z]{3})(?:_([A-Z0-9]+))?_VINTAGE", resource_id or "")
    if not match:
        return (0, 0, 0)
    year = int(match.group(1))
    month = MONTHS.get(match.group(2), 0)
    is_standard = 1 if not match.group(3) else 0
    return (year, month, is_standard)


def is_vintage_database(database_name: str) -> bool:
    return "_VINTAGE" in (database_name or "")


def database_sort_key(database_name: str, latest_weo_db: str | None = None) -> tuple[int, int, int, int, str]:
    if database_name == WEO_LIVE_DB:
        return (0, 0, 0, 0, database_name)
    if database_name == LEGACY_WEO_DB:
        return (1, 0, 0, 0, database_name)
    if latest_weo_db and database_name == latest_weo_db:
        return (2, 9999, 99, 1, database_name)
    if is_vintage_database(database_name):
        resource_id = database_name.split(":", 1)[1]
        year, month, is_standard = parse_weo_sort_key(resource_id)
        return (3, -year, -month, -is_standard, database_name)
    return (4, 0, 0, 0, database_name)


def load_datasets(include_vintage: bool = False, vintage_only: bool = False) -> list[dict[str, str]]:
    paths = [VINTAGE_DATASETS_CSV] if vintage_only else [NON_VINTAGE_DATASETS_CSV]
    if include_vintage and not vintage_only:
        paths.append(VINTAGE_DATASETS_CSV)
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8-sig") as f:
            rows.extend(csv.DictReader(f))
    return rows


def load_variables() -> list[dict[str, str]]:
    with VARIABLES_CSV.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_catalog_variables() -> list[dict[str, str]]:
    return load_variables()


def latest_weo_dataset() -> dict[str, str]:
    for row in load_datasets(include_vintage=False):
        if row.get("database") == WEO_LIVE_DB:
            return row
    raise RuntimeError("No non-vintage WEO Live dataset found")


def is_weo_live_database(database_name: str) -> bool:
    return database_name == WEO_LIVE_DB


def explicitly_requested_legacy_weo(query: str | None) -> bool:
    return norm(query or "") in {norm(LEGACY_WEO_DB), "imf res weo", "res weo"}


def include_dataset_row(row: dict[str, str], query: str | None) -> bool:
    return row.get("database") != LEGACY_WEO_DB or explicitly_requested_legacy_weo(query)


def include_variable_row(row: dict[str, str]) -> bool:
    return row.get("database_name") != LEGACY_WEO_DB


def score_variable(row: dict[str, str], query: str) -> int:
    q = norm(query)
    q_tokens = tokens(query)
    exact_tokens = set(norm(query).split())
    code = norm(row.get("Code", "") or row.get("indicator_code", ""))
    name = norm(row.get("Name", "") or row.get("indicator_name", ""))
    score = 0
    if q == code:
        score += 120
    if q == name:
        score += 100
    if code and q in code:
        score += 70
    if q and q in name:
        score += 60
    score += sum(12 for token in q_tokens if token == code)
    score += sum(10 for token in exact_tokens if token in name)
    score += sum(6 for token in q_tokens if token in name)
    if "growth" in exact_tokens and "percent change" in name:
        score += 24
    if "real" in exact_tokens and "constant prices" in name:
        score += 24
    if "nominal" in exact_tokens and "current prices" in name:
        score += 24
    if "gdp" in exact_tokens and "gross domestic product" in name:
        score += 18
    if "nominal" in exact_tokens and "gdp" in exact_tokens and "gross domestic product" in name and "current prices" in name:
        score += 30
    wants_usd = "usd" in exact_tokens or {"us", "dollar"}.issubset(exact_tokens) or {"us", "dollars"}.issubset(exact_tokens)
    if wants_usd and ("us dollar" in name or "us dollars" in name):
        score += 45
    if wants_usd and "international dollar" in name:
        score -= 35
    if "current" in exact_tokens and "account" in exact_tokens and "current account" in name:
        score += 35
        if "balance" in exact_tokens and "balance" in name:
            score += 15
    if "gdp" in exact_tokens and "percent of gdp" in name:
        score += 25
    if "percent of gdp" in name and not {"percent", "gdp"}.issubset(exact_tokens):
        score -= 35
    if "inflation" in exact_tokens and "consumer prices" in name and "percent change" in name:
        score += 50
        if code in {"pcpi pch", "pcpie pch"}:
            score += 15
    score -= max(0, len(name.split()) - 8)
    return score


def cmd_latest_weo(_args: argparse.Namespace) -> None:
    row = latest_weo_dataset()
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["database", "name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerow(row)


def cmd_datasets(args: argparse.Namespace) -> None:
    rows = load_datasets(include_vintage=args.include_vintage, vintage_only=args.vintage_only)
    if args.query:
        q = norm(args.query)
        if explicitly_requested_legacy_weo(args.query):
            rows = [row for row in rows if row.get("database") == LEGACY_WEO_DB]
        else:
            rows = [
                row
                for row in rows
                if q in norm(row.get("name", ""))
                or q in norm(row.get("Agency ID", ""))
                or q in norm(row.get("Resource ID", ""))
                or q in norm(row.get("Unique ID", ""))
            ]
    rows = [row for row in rows if include_dataset_row(row, args.query)]
    rows.sort(
        key=lambda row: (
            database_sort_key(row.get("database", "")),
            row.get("Agency ID", ""),
            row.get("name", ""),
        )
    )
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["database", "name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows[: args.limit])


def cmd_search(args: argparse.Namespace) -> None:
    variables = load_catalog_variables()

    if args.database:
        candidates = [row for row in variables if row.get("database_name") == args.database]
    elif args.all_databases:
        candidates = [row for row in variables if include_variable_row(row)]
    else:
        candidates = [row for row in variables if is_weo_live_database(row.get("database_name", ""))]

    scored = [(score_variable(row, args.query), row) for row in candidates]
    scored = [(score, row) for score, row in scored if score > 0]
    scored.sort(
        key=lambda item: (
            -item[0],
            database_sort_key(item[1].get("database_name", "")),
            item[1].get("dimension_name", ""),
            item[1].get("Code", "") or item[1].get("indicator_code", ""),
            item[1].get("Name", "") or item[1].get("indicator_name", ""),
        )
    )

    if (not scored or scored[0][0] < 25) and not args.all_databases and not args.database:
        fallback = [(score_variable(row, args.query), row) for row in variables if include_variable_row(row)]
        scored = [(score, row) for score, row in fallback if score > 0]
        scored.sort(
            key=lambda item: (
                -item[0],
                database_sort_key(item[1].get("database_name", "")),
                item[1].get("dimension_name", ""),
                item[1].get("Code", "") or item[1].get("indicator_code", ""),
            )
        )

    fieldnames = ["score", "database_name", "dimension_name", "code", "name"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for score, row in scored[: args.limit]:
        writer.writerow(
            {
                "score": score,
                "database_name": row.get("database_name", ""),
                "dimension_name": row.get("dimension_name", ""),
                "code": row.get("Code", "") or row.get("indicator_code", ""),
                "name": row.get("Name", "") or row.get("indicator_name", ""),
            }
        )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("latest-weo")
    p.set_defaults(func=cmd_latest_weo)

    p = sub.add_parser("datasets")
    p.add_argument("query", nargs="?")
    p.add_argument("--limit", type=int, default=20)
    vintage_group = p.add_mutually_exclusive_group()
    vintage_group.add_argument("--include-vintage", action="store_true")
    vintage_group.add_argument("--vintage-only", action="store_true")
    p.set_defaults(func=cmd_datasets)

    p = sub.add_parser("search")
    p.add_argument("query")
    p.add_argument("--database")
    p.add_argument("--all-databases", action="store_true")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_search)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Search IMF indicator and dataset reference CSVs for catalog lookups."""

from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
REFERENCES_DIR = SKILL_DIR / "references"
INDICATORS_CSV = REFERENCES_DIR / "Full_indicators_List.csv"
DATASETS_CSV = REFERENCES_DIR / "internal_full_datasets.csv"
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


def database_sort_key(database_name: str, latest_weo_db: str) -> tuple[int, int, int, int, str]:
    if database_name == latest_weo_db:
        return (0, 9999, 99, 1, database_name)
    if database_name.startswith("IMF.RES.WEO:"):
        resource_id = database_name.split(":", 1)[1]
        year, month, is_standard = parse_weo_sort_key(resource_id)
        return (1, -year, -month, -is_standard, database_name)
    return (2, 0, 0, 0, database_name)


def load_datasets() -> list[dict[str, str]]:
    with DATASETS_CSV.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_indicators() -> list[dict[str, str]]:
    with INDICATORS_CSV.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def latest_weo_dataset() -> dict[str, str]:
    datasets = [
        row
        for row in load_datasets()
        if row.get("Agency ID") == "IMF.RES.WEO" and row.get("Resource ID", "").startswith("WEO_LIVE_")
    ]
    if not datasets:
        raise RuntimeError("No WEO Live datasets found")
    return max(datasets, key=lambda row: parse_weo_sort_key(row.get("Resource ID", "")))


def score_indicator(row: dict[str, str], query: str) -> int:
    q = norm(query)
    q_tokens = tokens(query)
    exact_tokens = set(norm(query).split())
    code = norm(row.get("indicator_code", ""))
    name = norm(row.get("indicator_name", ""))
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
    if {"us", "dollars"}.issubset(exact_tokens) and ("us dollar" in name or "us dollars" in name):
        score += 20
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
    writer = csv.DictWriter(sys.stdout, fieldnames=["name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"])
    writer.writeheader()
    writer.writerow(row)


def cmd_datasets(args: argparse.Namespace) -> None:
    rows = load_datasets()
    if args.query:
        q = norm(args.query)
        rows = [
            row
            for row in rows
            if q in norm(row.get("name", ""))
            or q in norm(row.get("Agency ID", ""))
            or q in norm(row.get("Resource ID", ""))
            or q in norm(row.get("Unique ID", ""))
        ]
    rows.sort(key=lambda row: (row.get("Agency ID", ""), row.get("name", "")))
    writer = csv.DictWriter(sys.stdout, fieldnames=["name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"])
    writer.writeheader()
    writer.writerows(rows[: args.limit])


def cmd_search(args: argparse.Namespace) -> None:
    latest_weo = latest_weo_dataset()
    latest_weo_db = f"{latest_weo['Agency ID']}:{latest_weo['Resource ID']}"
    indicators = load_indicators()

    if args.database:
        candidates = [row for row in indicators if row.get("database_name") == args.database]
    elif args.all_databases:
        candidates = indicators
    else:
        candidates = [row for row in indicators if row.get("database_name") == latest_weo_db]

    scored = [(score_indicator(row, args.query), row) for row in candidates]
    scored = [(score, row) for score, row in scored if score > 0]
    scored.sort(key=lambda item: (-item[0], item[1].get("indicator_code", ""), item[1].get("indicator_name", "")))

    if (not scored or scored[0][0] < 25) and not args.all_databases and not args.database:
        fallback = [(score_indicator(row, args.query), row) for row in indicators]
        scored = [(score, row) for score, row in fallback if score > 0]
        scored.sort(
            key=lambda item: (
                -item[0],
                database_sort_key(item[1].get("database_name", ""), latest_weo_db),
                item[1].get("indicator_code", ""),
            )
        )

    fieldnames = ["score", "database_name", "indicator_code", "indicator_name"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for score, row in scored[: args.limit]:
        writer.writerow(
            {
                "score": score,
                "database_name": row.get("database_name", ""),
                "indicator_code": row.get("indicator_code", ""),
                "indicator_name": row.get("indicator_name", ""),
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

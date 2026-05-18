#!/usr/bin/env python3
"""Small helper for ambiguous WEO country-group CSV lookups."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import unicodedata
from pathlib import Path
from typing import Iterable


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSV_DIR = SKILL_DIR / "references" / "Country Group" / "csv"
CSV_FILES = {
    "countries": "1. countries.csv",
    "groups": "2. country_groups.csv",
    "composition": "3. country_group_composition.csv",
}
GROUP_ALIASES = {
    "ae": "G110",
    "advanced economies": "G110",
    "emdes": "G200",
    "emde": "G200",
    "emerging market and developing economies": "G200",
    "lac": "G205",
    "latin america and the caribbean": "G205",
    "meca": "G400",
    "middle east and central asia": "G400",
    "ssa": "G603",
    "sub saharan africa": "G603",
    "sub sahara africa": "G603",
    "world": "G001",
    "asean 5": "G510",
    "asean-5": "G510",
    "eu": "G998",
    "european union": "G998",
    "ea": "G995",
    "euro area": "G995",
    "hipc": "G711",
    "lic": "G201",
    "lidc": "G201",
    "low income countries": "G201",
    "low income developing countries": "G201",
    "cca": "G940",
    "mena": "G406",
}
COUNTRY_ALIASES = {
    "america": "USA",
    "united states of america": "USA",
    "us": "USA",
    "u s": "USA",
    "mainland": "CHN",
    "mainland china": "CHN",
    "china mainland": "CHN",
    "cote d ivoire": "CIV",
    "ivory coast": "CIV",
}


def _norm(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()


def _compact(value: str) -> str:
    return _norm(value).replace(" ", "")


def group_alias_code(query: str) -> str | None:
    return GROUP_ALIASES.get(_norm(query))


def country_alias_code(query: str) -> str | None:
    return COUNTRY_ALIASES.get(_norm(query))


class CsvTables:
    def __init__(self, csv_dir: Path) -> None:
        self.csv_dir = csv_dir

    def rows(self, table_name: str) -> list[dict[str, str]]:
        csv_path = self.csv_dir / CSV_FILES[table_name]
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing WEO country-group CSV: {csv_path}")
        for encoding in ("utf-8-sig", "cp1252"):
            try:
                with csv_path.open(newline="", encoding=encoding) as f:
                    return list(csv.DictReader(f))
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("utf-8-sig", b"", 0, 1, f"Could not decode {csv_path}")


def matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    q = _norm(query)
    compact_q = _compact(query)
    for field in fields:
        v = _norm(row.get(field, ""))
        if q in v or compact_q == v.replace(" ", ""):
            return True
    return False


def exact_matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    q = _compact(query)
    return any(_compact(row.get(field, "")) == q for field in fields)


def write_rows(rows: list[dict[str, str]], fields: list[str]) -> None:
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


def cmd_groups(tables: CsvTables, args: argparse.Namespace) -> None:
    rows = tables.rows("groups")
    if args.query:
        alias_code = group_alias_code(args.query)
        if alias_code:
            rows = [r for r in rows if r.get("groupcode") == alias_code]
        else:
            rows = [
                r
                for r in rows
                if matches(r, args.query, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])
            ]
    write_rows(rows, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def cmd_countries(tables: CsvTables, args: argparse.Namespace) -> None:
    rows = tables.rows("countries")
    if args.query:
        alias_code = country_alias_code(args.query)
        if alias_code:
            rows = [r for r in rows if r.get("countrycode") == alias_code]
        else:
            rows = [
                r
                for r in rows
                if matches(r, args.query, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
            ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])


def cmd_members(tables: CsvTables, args: argparse.Namespace) -> None:
    groups = tables.rows("groups")
    alias_code = group_alias_code(args.group)
    exact_groups = [
        r
        for r in groups
        if (alias_code and r.get("groupcode") == alias_code)
        or exact_matches(r, args.group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]
    group_codes = {r["groupcode"] for r in exact_groups}
    composition = tables.rows("composition")
    if group_codes:
        rows = [r for r in composition if r["groupcode"] in group_codes]
    else:
        rows = [
            r
            for r in composition
            if matches(r, args.group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
        ]
    write_rows(rows, ["groupcode", "groupname", "groupcode_s", "groupname_s", "countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_memberships(tables: CsvTables, args: argparse.Namespace) -> None:
    countries = tables.rows("countries")
    alias_code = country_alias_code(args.country)
    exact_countries = [
        r
        for r in countries
        if (alias_code and r.get("countrycode") == alias_code)
        or exact_matches(r, args.country, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
    ]
    country_codes = {r["countrycode"] for r in exact_countries}
    composition = tables.rows("composition")
    if country_codes:
        rows = [r for r in composition if r["countrycode"] in country_codes]
    else:
        rows = [
            r
            for r in composition
            if matches(r, args.country, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
        ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-dir", type=Path, default=DEFAULT_CSV_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("groups")
    p.add_argument("query", nargs="?")
    p.set_defaults(func=cmd_groups)

    p = sub.add_parser("countries")
    p.add_argument("query", nargs="?")
    p.set_defaults(func=cmd_countries)

    p = sub.add_parser("members")
    p.add_argument("group")
    p.set_defaults(func=cmd_members)

    p = sub.add_parser("memberships")
    p.add_argument("country")
    p.set_defaults(func=cmd_memberships)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tables = CsvTables(args.csv_dir)
    args.func(tables, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

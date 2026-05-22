#!/usr/bin/env python3
"""Helper for common WEO country, group, and framework lookups."""

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
    "em": "G1201",
    "emerging market": "G1201",
    "emerging markets": "G1201",
    "emerging market economies": "G1201",
    "emerging market and middle income economies": "G1201",
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
    "prgt em": "G-PRGT-EM",
    "prgt-em": "G-PRGT-EM",
    "g prgt em": "G-PRGT-EM",
    "g-prgt-em": "G-PRGT-EM",
    "prgt lic": "G-PRGT-LIC",
    "prgt-lic": "G-PRGT-LIC",
    "g prgt lic": "G-PRGT-LIC",
    "g-prgt-lic": "G-PRGT-LIC",
    "cca": "G940",
    "mena": "G406",
}
COUNTRY_ALIASES = {
    "america": "USA",
    "usa": "USA",
    "u s a": "USA",
    "united states of america": "USA",
    "us": "USA",
    "u s": "USA",
    "uk": "GBR",
    "u k": "GBR",
    "great britain": "GBR",
    "britain": "GBR",
    "england": "GBR",
    "uae": "ARE",
    "u a e": "ARE",
    "emirates": "ARE",
    "south korea": "KOR",
    "republic of korea": "KOR",
    "korea republic": "KOR",
    "russia": "RUS",
    "russian federation": "RUS",
    "iran": "IRN",
    "islamic republic of iran": "IRN",
    "venezuela": "VEN",
    "bolivarian republic of venezuela": "VEN",
    "bolivia": "BOL",
    "plurinational state of bolivia": "BOL",
    "moldova": "MDA",
    "republic of moldova": "MDA",
    "laos": "LAO",
    "lao": "LAO",
    "lao pdr": "LAO",
    "lao p d r": "LAO",
    "vietnam": "VNM",
    "viet nam": "VNM",
    "brunei": "BRN",
    "hong kong": "HKG",
    "hong kong sar": "HKG",
    "macao": "MAC",
    "macau": "MAC",
    "macao sar": "MAC",
    "taiwan": "TWN",
    "taiwan province of china": "TWN",
    "mainland": "CHN",
    "mainland china": "CHN",
    "china mainland": "CHN",
    "prc": "CHN",
    "people s republic of china": "CHN",
    "czechia": "CZE",
    "czech republic": "CZE",
    "slovakia": "SVK",
    "slovak republic": "SVK",
    "turkey": "TUR",
    "turkiye": "TUR",
    "tuerkiye": "TUR",
    "egypt": "EGY",
    "arab republic of egypt": "EGY",
    "syria": "SYR",
    "syrian arab republic": "SYR",
    "yemen": "YEM",
    "west bank gaza": "WBG",
    "west bank and gaza": "WBG",
    "palestine": "WBG",
    "palestinian territories": "WBG",
    "kyrgyzstan": "KGZ",
    "kyrgyz republic": "KGZ",
    "cape verde": "CPV",
    "cabo verde": "CPV",
    "gambia": "GMB",
    "the gambia": "GMB",
    "swaziland": "SWZ",
    "eswatini": "SWZ",
    "tanzania": "TZA",
    "united republic of tanzania": "TZA",
    "micronesia": "FSM",
    "federated states of micronesia": "FSM",
    "marshall islands": "MHL",
    "republic of the marshall islands": "MHL",
    "kosovo": "KOS",
    "republic of kosovo": "KOS",
    "bahamas": "BHS",
    "the bahamas": "BHS",
    "north macedonia": "MKD",
    "macedonia": "MKD",
    "myanmar": "MMR",
    "burma": "MMR",
    "timor leste": "TLS",
    "east timor": "TLS",
    "sao tome and principe": "STP",
    "cote d ivoire": "CIV",
    "cote divoire": "CIV",
    "ivory coast": "CIV",
    "democratic republic of the congo": "COD",
    "drc": "COD",
    "congo kinshasa": "COD",
    "republic of congo": "COG",
    "republic of the congo": "COG",
    "congo brazzaville": "COG",
}
TERM_EXPLANATIONS = {
    "ae": {
        "title": "Advanced Economies",
        "note": "WEO and SPR/PRGT use the same advanced-economies group code in this reference.",
        "groups": [("WEO", "G110"), ("SPR/PRGT", "G110")],
    },
    "advanced economies": {
        "title": "Advanced Economies",
        "note": "WEO and SPR/PRGT use the same advanced-economies group code in this reference.",
        "groups": [("WEO", "G110"), ("SPR/PRGT", "G110")],
    },
    "em": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G1201"), ("SPR/PRGT", "G-PRGT-EM")],
    },
    "emerging markets": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G1201"), ("SPR/PRGT", "G-PRGT-EM")],
    },
    "lic": {
        "title": "Low-Income Countries",
        "note": "LIC coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G201"), ("SPR/PRGT", "G-PRGT-LIC")],
    },
    "lidc": {
        "title": "Low-Income Developing Countries",
        "note": "LIDC usually maps to WEO G201 in this reference. PRGT LIC uses G-PRGT-LIC and has different coverage.",
        "groups": [("WEO", "G201"), ("SPR/PRGT", "G-PRGT-LIC")],
    },
    "emde": {
        "title": "Emerging Market and Developing Economies",
        "note": "WEO EMDE maps to G200. In this reference EMDE is broader than WEO EM alone.",
        "groups": [("WEO", "G200")],
    },
    "emdes": {
        "title": "Emerging Market and Developing Economies",
        "note": "WEO EMDE maps to G200. In this reference EMDE is broader than WEO EM alone.",
        "groups": [("WEO", "G200")],
    },
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


def unique_rows(rows: Iterable[dict[str, str]], key_fields: list[str]) -> list[dict[str, str]]:
    seen: set[tuple[str, ...]] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def group_rows_from_composition(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    return unique_rows(
        [
            {
                "grouptype": "",
                "groupcode": row.get("groupcode", ""),
                "groupname": row.get("groupname", ""),
                "groupcode_s": row.get("groupcode_s", ""),
                "groupname_s": row.get("groupname_s", ""),
            }
            for row in rows
        ],
        ["groupcode"],
    )


def group_members(tables: CsvTables, group: str) -> list[dict[str, str]]:
    group_rows = resolve_group_rows(tables, group, exact_only=True)
    group_codes = {row["groupcode"] for row in group_rows}
    composition = tables.rows("composition")
    if group_codes:
        return [row for row in composition if row["groupcode"] in group_codes]
    return [
        row
        for row in composition
        if matches(row, group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]


def group_summary(rows: list[dict[str, str]], fallback: str) -> tuple[str, str]:
    if not rows:
        return fallback, ""
    row = rows[0]
    return row.get("groupcode", fallback), row.get("groupname_s") or row.get("groupname", "")


def resolve_group_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    groups = tables.rows("groups")
    composition_groups = group_rows_from_composition(tables.rows("composition"))
    all_groups = unique_rows([*composition_groups, *groups], ["groupcode"])
    alias_code = group_alias_code(query)
    if alias_code:
        exact = [row for row in all_groups if row.get("groupcode") == alias_code]
        if exact:
            return exact
    exact_code = [row for row in all_groups if row.get("groupcode") == query or row.get("groupcode_s") == query]
    if exact_code:
        return exact_code
    exact = [
        row
        for row in all_groups
        if exact_matches(row, query, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]
    if exact or exact_only:
        return exact
    return [
        row
        for row in all_groups
        if matches(row, query, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]


def resolve_country_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    countries = tables.rows("countries")
    alias_code = country_alias_code(query)
    if alias_code:
        exact = [row for row in countries if row.get("countrycode") == alias_code]
        if exact:
            return exact
    exact = [
        row
        for row in countries
        if exact_matches(row, query, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
    ]
    if exact or exact_only:
        return exact
    return [
        row
        for row in countries
        if matches(row, query, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
    ]


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
    rows = group_members(tables, args.group)
    write_rows(rows, ["groupcode", "groupname", "groupcode_s", "groupname_s", "countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_memberships(tables: CsvTables, args: argparse.Namespace) -> None:
    exact_countries = resolve_country_rows(tables, args.country, exact_only=True)
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


def cmd_resolve(tables: CsvTables, args: argparse.Namespace) -> None:
    rows: list[dict[str, str]] = []
    for row in resolve_group_rows(tables, args.query):
        rows.append(
            {
                "kind": "group",
                "code": row.get("groupcode", ""),
                "name": row.get("groupname", ""),
                "code_s": row.get("groupcode_s", ""),
                "name_s": row.get("groupname_s", ""),
                "note": row.get("grouptype", ""),
            }
        )
    for row in resolve_country_rows(tables, args.query):
        rows.append(
            {
                "kind": "country",
                "code": row.get("countrycode", ""),
                "name": row.get("countryname", ""),
                "code_s": row.get("countrycode_s", ""),
                "name_s": row.get("countryname_s", ""),
                "note": row.get("department", ""),
            }
        )
    write_rows(rows, ["kind", "code", "name", "code_s", "name_s", "note"])


def cmd_expand_for_idata(tables: CsvTables, args: argparse.Namespace) -> None:
    rows = group_members(tables, args.group)
    if args.codes_only:
        print(",".join(row["countrycode"] for row in rows))
        return
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_compare(tables: CsvTables, args: argparse.Namespace) -> None:
    rows_a = group_members(tables, args.group_a)
    rows_b = group_members(tables, args.group_b)
    if not rows_a:
        raise SystemExit(f"No members found for group_a: {args.group_a}")
    if not rows_b:
        raise SystemExit(f"No members found for group_b: {args.group_b}")

    map_a = {row["countrycode"]: row for row in rows_a}
    map_b = {row["countrycode"]: row for row in rows_b}
    code_a, name_a = group_summary(rows_a, args.group_a)
    code_b, name_b = group_summary(rows_b, args.group_b)
    only_a = [map_a[code] for code in sorted(set(map_a) - set(map_b), key=lambda c: map_a[c]["countryname_s"])]
    only_b = [map_b[code] for code in sorted(set(map_b) - set(map_a), key=lambda c: map_b[c]["countryname_s"])]

    print(f"group_a: {code_a} | {name_a} | members={len(map_a)}")
    print(f"group_b: {code_b} | {name_b} | members={len(map_b)}")
    print(f"overlap: {len(set(map_a) & set(map_b))}")
    print()
    print(f"only_in_group_a: {len(only_a)}")
    write_rows(only_a, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
    print()
    print(f"only_in_group_b: {len(only_b)}")
    write_rows(only_b, ["countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_explain(tables: CsvTables, args: argparse.Namespace) -> None:
    explanation = TERM_EXPLANATIONS.get(_norm(args.term))
    if not explanation:
        cmd_resolve(tables, argparse.Namespace(query=args.term))
        return
    print(f"term: {args.term}")
    print(f"meaning: {explanation['title']}")
    print(f"note: {explanation['note']}")
    print("groups:")
    for framework, code in explanation["groups"]:
        rows = resolve_group_rows(tables, code, exact_only=True)
        group_code, group_name = group_summary(rows, code)
        print(f"- {framework}: {group_code} | {group_name}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv-dir", type=Path, default=DEFAULT_CSV_DIR)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "groups",
        help="Find group rows by code, name, alias, or group type.",
        epilog='Example: weo_country_groups.py groups "advanced economies"',
    )
    p.add_argument("query", nargs="?")
    p.set_defaults(func=cmd_groups)

    p = sub.add_parser(
        "countries",
        help="Find country rows by code, name, alias, or department.",
        epilog='Example: weo_country_groups.py countries "South Korea"',
    )
    p.add_argument("query", nargs="?")
    p.set_defaults(func=cmd_countries)

    p = sub.add_parser(
        "members",
        help="List member countries for a WEO or SPR/PRGT group.",
        epilog="Example: weo_country_groups.py members G110",
    )
    p.add_argument("group")
    p.set_defaults(func=cmd_members)

    p = sub.add_parser(
        "memberships",
        help="List groups that include a country.",
        epilog="Example: weo_country_groups.py memberships USA",
    )
    p.add_argument("country")
    p.set_defaults(func=cmd_memberships)

    p = sub.add_parser(
        "resolve",
        help="Resolve an ambiguous term to matching countries and groups.",
        description="Resolve a user term to country and group candidates before committing to a code.",
        epilog="Example: weo_country_groups.py resolve Congo",
    )
    p.add_argument("query")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser(
        "expand-for-idata",
        help="Expand a group to member country codes for iData handoff.",
        description="Expand a WEO or SPR/PRGT group to member countrycode values. Use this instead of passing groupcode as an iData country selector.",
        epilog="Example: weo_country_groups.py expand-for-idata G200 --codes-only",
    )
    p.add_argument("group")
    p.add_argument("--codes-only", action="store_true", help="Print only comma-separated countrycode values.")
    p.set_defaults(func=cmd_expand_for_idata)

    p = sub.add_parser(
        "compare",
        help="Compare membership of two WEO or SPR/PRGT groups.",
        description="Return answer-ready membership counts, overlap, and only-in-each-group country rows.",
        epilog="Examples: weo_country_groups.py compare G201 G-PRGT-LIC; weo_country_groups.py compare G1201 G-PRGT-EM",
    )
    p.add_argument("group_a")
    p.add_argument("group_b")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser(
        "explain",
        help="Explain common RA shorthand such as AE, EM, EMDE, LIC, or LIDC.",
        description="Explain common RA shorthand and show the relevant WEO and SPR/PRGT group codes when applicable.",
        epilog="Examples: weo_country_groups.py explain EM; weo_country_groups.py explain LIC",
    )
    p.add_argument("term")
    p.set_defaults(func=cmd_explain)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    tables = CsvTables(args.csv_dir)
    args.func(tables, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

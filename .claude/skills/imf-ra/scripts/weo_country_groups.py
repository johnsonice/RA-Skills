#!/usr/bin/env python3
"""Helper for common WEO country, group, and framework lookups."""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

from weo_country_groups_data import (
    COUNTRY_ALIASES,
    CSV_FILES,
    DEFAULT_CSV_DIR,
    GROUP_ALIASES,
    SKILL_DIR,
    TERM_EXPLANATIONS,
    CsvTables,
)
from weo_country_groups_lookup import (
    _group_summary,
    _matches,
    _norm,
    country_alias_code,
    group_alias_code,
    group_members,
    resolve_country_rows,
    resolve_group_rows,
)


def write_rows(rows: list[dict[str, str]], fields: list[str]) -> None:
    """Write selected row fields to stdout as CSV.

    [When to Use]
    Use at CLI boundaries after lookup logic has already produced rows.
    """
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


def cmd_groups(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for listing or searching group reference rows."""
    rows = tables.rows("groups")
    if args.query:
        alias_code = group_alias_code(args.query)
        if alias_code:
            rows = [r for r in rows if r.get("groupcode") == alias_code]
        else:
            rows = [
                r
                for r in rows
                if _matches(r, args.query, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])
            ]
    write_rows(rows, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def cmd_countries(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for listing or searching country reference rows."""
    rows = tables.rows("countries")
    if args.query:
        alias_code = country_alias_code(args.query)
        if alias_code:
            rows = [r for r in rows if r.get("countrycode") == alias_code]
        else:
            rows = [
                r
                for r in rows
                if _matches(r, args.query, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
            ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])


def cmd_members(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for listing countries in one group."""
    rows = group_members(tables, args.group)
    write_rows(rows, ["groupcode", "groupname", "groupcode_s", "groupname_s", "countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_memberships(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for listing groups that include one country."""
    exact_countries = resolve_country_rows(tables, args.country, exact_only=True)
    country_codes = {r["countrycode"] for r in exact_countries}
    composition = tables.rows("composition")
    if country_codes:
        rows = [r for r in composition if r["countrycode"] in country_codes]
    else:
        rows = [
            r
            for r in composition
            if _matches(r, args.country, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
        ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def cmd_resolve(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for resolving an ambiguous term to countries and groups."""
    rows: list[dict[str, str]] = []
    if country_alias_code(args.query):
        for row in resolve_country_rows(tables, args.query, exact_only=True):
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
        return
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
    """CLI handler for expanding a group into iData-ready country rows/codes."""
    rows = group_members(tables, args.group)
    if args.codes_only:
        print(",".join(row["countrycode"] for row in rows))
        return
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_compare(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for comparing two groups' memberships."""
    rows_a = group_members(tables, args.group_a)
    rows_b = group_members(tables, args.group_b)
    if not rows_a:
        raise SystemExit(f"No members found for group_a: {args.group_a}")
    if not rows_b:
        raise SystemExit(f"No members found for group_b: {args.group_b}")

    map_a = {row["countrycode"]: row for row in rows_a}
    map_b = {row["countrycode"]: row for row in rows_b}
    code_a, name_a = _group_summary(rows_a, args.group_a)
    code_b, name_b = _group_summary(rows_b, args.group_b)
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
    """CLI handler for explaining common RA shorthand and framework differences."""
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
        group_code, group_name = _group_summary(rows, code)
        print(f"- {framework}: {group_code} | {group_name}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser and register subcommands."""
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
    """Run the CLI using parsed arguments and CSV-backed reference tables."""
    args = build_parser().parse_args()
    tables = CsvTables(args.csv_dir)
    args.func(tables, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

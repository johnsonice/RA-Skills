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


COUNTRY_GROUP_DIR = Path(__file__).resolve().parent
DEFAULT_COUNTRY_GROUP_CSV = COUNTRY_GROUP_DIR / "Country Group.csv"
DEFAULT_CSV_DIR = DEFAULT_COUNTRY_GROUP_CSV
COUNTRY_COLUMNS = ("countrycode", "countryname", "countrycode_s", "countryname_s", "department")

GROUP_ALIASES = {
    "ae": "Advanced Economies(AE)",
    "advanced economies": "Advanced Economies(AE)",
    "em": "Emerging Market and Middle-Income Economies(EM)",
    "emerging market": "Emerging Market and Middle-Income Economies(EM)",
    "emerging markets": "Emerging Market and Middle-Income Economies(EM)",
    "emerging market economies": "Emerging Market and Middle-Income Economies(EM)",
    "emerging market and middle income economies": "Emerging Market and Middle-Income Economies(EM)",
    "emdes": "Emerging Market and Developing Economies(EMDE)",
    "emde": "Emerging Market and Developing Economies(EMDE)",
    "emerging market and developing economies": "Emerging Market and Developing Economies(EMDE)",
    "lac": "Latin America and the Caribbean (LAC)",
    "latin america and the caribbean": "Latin America and the Caribbean (LAC)",
    "meca": "Middle East and Central Asia",
    "middle east and central asia": "Middle East and Central Asia",
    "ssa": "Sub-Saharan Africa (SSA)",
    "sub saharan africa": "Sub-Saharan Africa (SSA)",
    "sub sahara africa": "Sub-Saharan Africa (SSA)",
    "world": "World",
    "asean 5": "ASEAN-5",
    "asean-5": "ASEAN-5",
    "eu": "European Union (EU)",
    "european union": "European Union (EU)",
    "ea": "Euro Area (EA) – aggregate of member states",
    "euro area": "Euro Area (EA) – aggregate of member states",
    "hipc": "Heavily Indebted Poor Countries (HIPC)",
    "lic": "Low-Income Developing Countries (LIDC)",
    "lidc": "Low-Income Developing Countries (LIDC)",
    "low income countries": "Low-Income Developing Countries (LIDC)",
    "low income developing countries": "Low-Income Developing Countries (LIDC)",
    "spr em": "SPR-Emerging Market and Middle-Income Economies(EM)",
    "spr emerging market": "SPR-Emerging Market and Middle-Income Economies(EM)",
    "spr emerging market and middle income economies": "SPR-Emerging Market and Middle-Income Economies(EM)",
    "prgt em": "SPR-Emerging Market and Middle-Income Economies(EM)",
    "prgt emerging market": "SPR-Emerging Market and Middle-Income Economies(EM)",
    "spr lic": "SPR-Low-Income Developing Countries (LIC)",
    "spr low income countries": "SPR-Low-Income Developing Countries (LIC)",
    "prgt lic": "SPR-Low-Income Developing Countries (LIC)",
    "prgt low income countries": "SPR-Low-Income Developing Countries (LIC)",
    "cca": "Caucasus and Central Asia (CCA)",
    "mena": "Middle East and North Africa (MENA)",
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
        "note": "This reference uses the same Advanced Economies(AE) membership column for WEO and SPR context.",
        "groups": [("WEO", "Advanced Economies(AE)"), ("SPR/PRGT", "Advanced Economies(AE)")],
    },
    "advanced economies": {
        "title": "Advanced Economies",
        "note": "This reference uses the same Advanced Economies(AE) membership column for WEO and SPR context.",
        "groups": [("WEO", "Advanced Economies(AE)"), ("SPR/PRGT", "Advanced Economies(AE)")],
    },
    "em": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [
            ("WEO", "Emerging Market and Middle-Income Economies(EM)"),
            ("SPR/PRGT", "SPR-Emerging Market and Middle-Income Economies(EM)"),
        ],
    },
    "emerging markets": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [
            ("WEO", "Emerging Market and Middle-Income Economies(EM)"),
            ("SPR/PRGT", "SPR-Emerging Market and Middle-Income Economies(EM)"),
        ],
    },
    "lic": {
        "title": "Low-Income Countries",
        "note": "LIC coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [
            ("WEO", "Low-Income Developing Countries (LIDC)"),
            ("SPR/PRGT", "SPR-Low-Income Developing Countries (LIC)"),
        ],
    },
    "lidc": {
        "title": "Low-Income Developing Countries",
        "note": "LIDC maps to the WEO Low-Income Developing Countries (LIDC) column. SPR/PRGT LIC uses a separate column and has different coverage.",
        "groups": [
            ("WEO", "Low-Income Developing Countries (LIDC)"),
            ("SPR/PRGT", "SPR-Low-Income Developing Countries (LIC)"),
        ],
    },
    "emde": {
        "title": "Emerging Market and Developing Economies",
        "note": "EMDE is framework-sensitive. WEO EMDE is its own column; SPR/PRGT EMDE is represented by the SPR EM and SPR LIC columns. Clarify WEO vs SPR/PRGT before committing to a group.",
        "groups": [
            ("WEO", "Emerging Market and Developing Economies(EMDE)"),
            ("SPR/PRGT", "SPR-Emerging Market and Middle-Income Economies(EM)"),
            ("SPR/PRGT", "SPR-Low-Income Developing Countries (LIC)"),
        ],
    },
    "emdes": {
        "title": "Emerging Market and Developing Economies",
        "note": "EMDE is framework-sensitive. WEO EMDE is its own column; SPR/PRGT EMDE is represented by the SPR EM and SPR LIC columns. Clarify WEO vs SPR/PRGT before committing to a group.",
        "groups": [
            ("WEO", "Emerging Market and Developing Economies(EMDE)"),
            ("SPR/PRGT", "SPR-Emerging Market and Middle-Income Economies(EM)"),
            ("SPR/PRGT", "SPR-Low-Income Developing Countries (LIC)"),
        ],
    },
}


class CsvTables:
    """Read the single Country Group.csv and expose logical lookup views."""

    def __init__(self, country_group_csv: Path) -> None:
        self.country_group_csv = self._resolve_path(country_group_csv)
        self._country_group_rows: list[dict[str, str]] | None = None

    @staticmethod
    def _resolve_path(path: Path) -> Path:
        """Return the consolidated Country Group.csv path."""
        if path.is_dir():
            candidates = [path / "Country Group.csv", path.parent / "Country Group.csv"]
            for candidate in candidates:
                if candidate.exists():
                    return candidate
        if path.exists():
            return path
        raise FileNotFoundError(f"Missing WEO country-group CSV: {path}")

    def _read_country_group_csv(self) -> list[dict[str, str]]:
        """Read the consolidated country-group CSV once with supported encodings."""
        if self._country_group_rows is not None:
            return self._country_group_rows
        for encoding in ("utf-8-sig", "cp1252"):
            try:
                with self.country_group_csv.open(newline="", encoding=encoding) as f:
                    self._country_group_rows = list(csv.DictReader(f))
                    return self._country_group_rows
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("utf-8-sig", b"", 0, 1, f"Could not decode {self.country_group_csv}")

    def _group_columns(self) -> list[str]:
        rows = self._read_country_group_csv()
        if not rows:
            return []
        return [field for field in rows[0] if field not in COUNTRY_COLUMNS]

    def _country_rows(self) -> list[dict[str, str]]:
        return [
            {field: row.get(field, "") for field in COUNTRY_COLUMNS}
            for row in self._read_country_group_csv()
            if row.get("countrycode")
        ]

    def _group_rows(self) -> list[dict[str, str]]:
        return [{"group": column, "groupname": column} for column in self._group_columns()]

    def _composition_rows(self) -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        source_rows = self._read_country_group_csv()
        for column in self._group_columns():
            for row in source_rows:
                if str(row.get(column, "")).strip() != "1":
                    continue
                rows.append(
                    {
                        "group": column,
                        "groupname": column,
                        "countrycode": row.get("countrycode", ""),
                        "countryname": row.get("countryname", ""),
                        "countrycode_s": row.get("countrycode_s", ""),
                        "countryname_s": row.get("countryname_s", ""),
                    }
                )
        return rows

    def rows(self, table_name: str) -> list[dict[str, str]]:
        """Return one logical WEO reference table as dictionaries."""
        if table_name == "countries":
            return self._country_rows()
        if table_name == "groups":
            return self._group_rows()
        if table_name == "composition":
            return self._composition_rows()
        raise ValueError(f"Unknown WEO country-group table: {table_name}")


def _norm(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()


def _compact(value: str) -> str:
    return _norm(value).replace(" ", "")


def group_alias(query: str) -> str | None:
    """Map common WEO/SPR group shorthand to a consolidated CSV group column."""
    return GROUP_ALIASES.get(_norm(query))


def country_alias_code(query: str) -> str | None:
    """Map common country aliases to WEO country codes."""
    return COUNTRY_ALIASES.get(_norm(query))


def _matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    """Return whether a row loosely matches a query across selected fields."""
    q = _norm(query)
    compact_q = _compact(query)
    for field in fields:
        v = _norm(row.get(field, ""))
        if q in v or compact_q == v.replace(" ", ""):
            return True
    return False


def _exact_matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    """Return whether a row exactly matches a query after normalization."""
    q = _compact(query)
    return any(_compact(row.get(field, "")) == q for field in fields)


def _unique_rows(rows: Iterable[dict[str, str]], key_fields: list[str]) -> list[dict[str, str]]:
    """Deduplicate rows by selected key fields while preserving order."""
    seen: set[tuple[str, ...]] = set()
    out: list[dict[str, str]] = []
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        if key in seen:
            continue
        seen.add(key)
        out.append(row)
    return out


def _group_rows_from_composition(rows: Iterable[dict[str, str]]) -> list[dict[str, str]]:
    """Extract unique group descriptors from composition rows."""
    return _unique_rows(
        [{"group": row.get("group", ""), "groupname": row.get("groupname", "")} for row in rows],
        ["group"],
    )


def group_members(tables: CsvTables, group: str) -> list[dict[str, str]]:
    """Return member countries for a WEO or SPR/PRGT group column."""
    group_rows = resolve_group_rows(tables, group, exact_only=True)
    group_names = {row["group"] for row in group_rows}
    composition = tables.rows("composition")
    if group_names:
        return [row for row in composition if row["group"] in group_names]
    return [row for row in composition if _matches(row, group, ["group", "groupname"])]


def _group_summary(rows: list[dict[str, str]], fallback: str) -> str:
    """Return a display-ready group column name from member rows."""
    if not rows:
        return fallback
    return rows[0].get("groupname") or rows[0].get("group", fallback)


def resolve_group_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    """Resolve a user group term to candidate consolidated CSV group rows."""
    groups = tables.rows("groups")
    composition_groups = _group_rows_from_composition(tables.rows("composition"))
    all_groups = _unique_rows([*groups, *composition_groups], ["group"])
    alias = group_alias(query)
    if alias:
        exact = [row for row in all_groups if row.get("group") == alias]
        if exact:
            return exact
    exact = [row for row in all_groups if _exact_matches(row, query, ["group", "groupname"])]
    if exact or exact_only:
        return exact
    return [row for row in all_groups if _matches(row, query, ["group", "groupname"])]


def resolve_country_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    """Resolve a user country term to candidate WEO country rows."""
    countries = tables.rows("countries")
    alias_code = country_alias_code(query)
    if alias_code:
        exact = [row for row in countries if row.get("countrycode") == alias_code]
        if exact:
            return exact
    exact = [
        row
        for row in countries
        if _exact_matches(row, query, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
    ]
    if exact or exact_only:
        return exact
    return [
        row
        for row in countries
        if _matches(row, query, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
    ]


def write_rows(rows: list[dict[str, str]], fields: list[str]) -> None:
    """Write selected row fields to stdout as CSV."""
    writer = csv.DictWriter(sys.stdout, fieldnames=fields, extrasaction="ignore")
    writer.writeheader()
    writer.writerows(rows)


def cmd_groups(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for listing or searching group reference rows."""
    rows = tables.rows("groups")
    if args.query:
        alias = group_alias(args.query)
        if alias:
            rows = [r for r in rows if r.get("group") == alias]
        else:
            rows = [r for r in rows if _matches(r, args.query, ["group", "groupname"])]
    write_rows(rows, ["group", "groupname"])


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
    write_rows(rows, ["group", "groupname", "countrycode", "countryname", "countrycode_s", "countryname_s"])


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
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "group", "groupname"])


def cmd_resolve(tables: CsvTables, args: argparse.Namespace) -> None:
    """CLI handler for resolving an ambiguous term to countries and groups."""
    rows: list[dict[str, str]] = []
    if country_alias_code(args.query):
        for row in resolve_country_rows(tables, args.query, exact_only=True):
            rows.append(
                {
                    "kind": "country",
                    "identifier": row.get("countrycode", ""),
                    "name": row.get("countryname", ""),
                    "note": row.get("department", ""),
                }
            )
        write_rows(rows, ["kind", "identifier", "name", "note"])
        return
    for row in resolve_group_rows(tables, args.query):
        rows.append(
            {
                "kind": "group",
                "identifier": row.get("group", ""),
                "name": row.get("groupname", ""),
                "note": "Country Group.csv column",
            }
        )
    for row in resolve_country_rows(tables, args.query):
        rows.append(
            {
                "kind": "country",
                "identifier": row.get("countrycode", ""),
                "name": row.get("countryname", ""),
                "note": row.get("department", ""),
            }
        )
    write_rows(rows, ["kind", "identifier", "name", "note"])


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
    name_a = _group_summary(rows_a, args.group_a)
    name_b = _group_summary(rows_b, args.group_b)
    only_a = [map_a[code] for code in sorted(set(map_a) - set(map_b), key=lambda c: map_a[c]["countryname_s"])]
    only_b = [map_b[code] for code in sorted(set(map_b) - set(map_a), key=lambda c: map_b[c]["countryname_s"])]

    print(f"group_a: {name_a} | members={len(map_a)}")
    print(f"group_b: {name_b} | members={len(map_b)}")
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
    for framework, group in explanation["groups"]:
        rows = resolve_group_rows(tables, group, exact_only=True)
        group_name = rows[0]["groupname"] if rows else group
        print(f"- {framework}: {group_name}")


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser and register subcommands."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--csv-dir",
        type=Path,
        default=DEFAULT_CSV_DIR,
        help="Path to the consolidated Country Group.csv file, or a directory containing it.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser(
        "groups",
        help="Find group columns by name or alias.",
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
        help="List member countries for a WEO or SPR/PRGT group column.",
        epilog='Example: weo_country_groups.py members "Advanced Economies(AE)"',
    )
    p.add_argument("group")
    p.set_defaults(func=cmd_members)

    p = sub.add_parser(
        "memberships",
        help="List group columns that include a country.",
        epilog="Example: weo_country_groups.py memberships USA",
    )
    p.add_argument("country")
    p.set_defaults(func=cmd_memberships)

    p = sub.add_parser(
        "resolve",
        help="Resolve an ambiguous term to matching countries and group columns.",
        description="Resolve a user term to country and group candidates before committing to a reference row/column.",
        epilog="Example: weo_country_groups.py resolve Congo",
    )
    p.add_argument("query")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser(
        "expand-for-idata",
        help="Expand a group column to member country codes for iData handoff.",
        description="Expand a WEO or SPR/PRGT group column to member countrycode values.",
        epilog='Example: weo_country_groups.py expand-for-idata "Emerging Market and Developing Economies(EMDE)" --codes-only',
    )
    p.add_argument("group")
    p.add_argument("--codes-only", action="store_true", help="Print only comma-separated countrycode values.")
    p.set_defaults(func=cmd_expand_for_idata)

    p = sub.add_parser(
        "compare",
        help="Compare membership of two WEO or SPR/PRGT group columns.",
        description="Return answer-ready membership counts, overlap, and only-in-each-group country rows.",
        epilog='Example: weo_country_groups.py compare "Low-Income Developing Countries (LIDC)" "SPR-Low-Income Developing Countries (LIC)"',
    )
    p.add_argument("group_a")
    p.add_argument("group_b")
    p.set_defaults(func=cmd_compare)

    p = sub.add_parser(
        "explain",
        help="Explain common RA shorthand such as AE, EM, EMDE, LIC, or LIDC.",
        description="Explain common RA shorthand and show the relevant consolidated CSV group columns when applicable.",
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

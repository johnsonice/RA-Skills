#!/usr/bin/env python3
"""Query the WEO Countries and Country Groups workbook without third-party deps."""

from __future__ import annotations

import argparse
import csv
import re
import sys
import zipfile
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_WORKBOOK = SKILL_DIR / "references" / "Country Group" / "WEO Countries and Country Groups 2026.xlsx"
NS = {
    "a": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
}
RID = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
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


def _text(el: ET.Element) -> str:
    return "".join(t.text or "" for t in el.iter(f"{{{NS['a']}}}t"))


def _colnum(cell_ref: str) -> int:
    letters = re.match(r"([A-Z]+)", cell_ref).group(1)
    n = 0
    for ch in letters:
        n = n * 26 + ord(ch) - 64
    return n


def _norm(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _compact(value: str) -> str:
    return _norm(value).replace(" ", "")


def group_alias_code(query: str) -> str | None:
    return GROUP_ALIASES.get(_norm(query))


class Workbook:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.zf = zipfile.ZipFile(path)
        self.shared = self._load_shared_strings()
        self.sheet_paths = self._load_sheet_paths()

    def _load_shared_strings(self) -> list[str]:
        root = ET.fromstring(self.zf.read("xl/sharedStrings.xml"))
        return [_text(si) for si in root.findall("a:si", NS)]

    def _load_sheet_paths(self) -> dict[str, str]:
        wb = ET.fromstring(self.zf.read("xl/workbook.xml"))
        rels = ET.fromstring(self.zf.read("xl/_rels/workbook.xml.rels"))
        relmap = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels}
        out = {}
        for sheet in wb.find("a:sheets", NS):
            out[sheet.attrib["name"]] = relmap[sheet.attrib[RID]]
        return out

    def rows(self, sheet_name: str) -> list[dict[str, str]]:
        path = self.sheet_paths[sheet_name]
        root = ET.fromstring(self.zf.read("xl/" + path))
        raw_rows: list[list[str]] = []
        for row in root.findall(".//a:sheetData/a:row", NS):
            vals: dict[int, str] = {}
            for cell in row.findall("a:c", NS):
                idx = _colnum(cell.attrib.get("r", "A1")) - 1
                typ = cell.attrib.get("t")
                v = cell.find("a:v", NS)
                inline = cell.find("a:is", NS)
                if typ == "s" and v is not None:
                    val = self.shared[int(v.text)]
                elif typ == "inlineStr" and inline is not None:
                    val = _text(inline)
                elif v is not None:
                    val = v.text or ""
                else:
                    val = ""
                vals[idx] = val
            if vals:
                raw_rows.append([vals.get(i, "") for i in range(max(vals) + 1)])

        header = raw_rows[0]
        return [dict(zip(header, row + [""] * (len(header) - len(row)))) for row in raw_rows[1:]]


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


def cmd_summary(wb: Workbook, _args: argparse.Namespace) -> None:
    countries = wb.rows("1. Countries")
    groups = wb.rows("2. Country Groups")
    composition = wb.rows("3. Country Group Composition")
    group_a = wb.rows("4. Group A and A+")
    print(f"workbook,{wb.path}")
    print(f"countries,{len(countries)}")
    print(f"groups,{len(groups)}")
    print(f"group_memberships,{len(composition)}")
    print(f"group_a_rows,{len(group_a)}")
    print("group_types")
    counts: dict[str, int] = {}
    for row in groups:
        counts[row["grouptype"]] = counts.get(row["grouptype"], 0) + 1
    for key in sorted(counts):
        print(f"{key},{counts[key]}")


def cmd_groups(wb: Workbook, args: argparse.Namespace) -> None:
    rows = wb.rows("2. Country Groups")
    if args.query:
        alias_code = group_alias_code(args.query)
        rows = [
            r
            for r in rows
            if (alias_code and r.get("groupcode") == alias_code)
            or matches(r, args.query, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])
        ]
    write_rows(rows, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def cmd_countries(wb: Workbook, args: argparse.Namespace) -> None:
    rows = wb.rows("1. Countries")
    if args.query:
        rows = [
            r
            for r in rows
            if matches(r, args.query, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
        ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "department"])


def cmd_members(wb: Workbook, args: argparse.Namespace) -> None:
    groups = wb.rows("2. Country Groups")
    alias_code = group_alias_code(args.group)
    exact_groups = [
        r
        for r in groups
        if (alias_code and r.get("groupcode") == alias_code)
        or exact_matches(r, args.group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]
    group_codes = {r["groupcode"] for r in exact_groups}
    composition = wb.rows("3. Country Group Composition")
    if group_codes:
        rows = [r for r in composition if r["groupcode"] in group_codes]
    else:
        rows = [
            r
            for r in composition
            if matches(r, args.group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
        ]
    write_rows(rows, ["groupcode", "groupname", "groupcode_s", "groupname_s", "countrycode", "countryname", "countrycode_s", "countryname_s"])


def cmd_memberships(wb: Workbook, args: argparse.Namespace) -> None:
    countries = wb.rows("1. Countries")
    exact_countries = [r for r in countries if exact_matches(r, args.country, ["countrycode", "countryname", "countrycode_s", "countryname_s"])]
    country_codes = {r["countrycode"] for r in exact_countries}
    composition = wb.rows("3. Country Group Composition")
    if country_codes:
        rows = [r for r in composition if r["countrycode"] in country_codes]
    else:
        rows = [
            r
            for r in composition
            if matches(r, args.country, ["countrycode", "countryname", "countrycode_s", "countryname_s"])
        ]
    write_rows(rows, ["countrycode", "countryname", "countrycode_s", "countryname_s", "groupcode", "groupname", "groupcode_s", "groupname_s"])


def cmd_group_a(wb: Workbook, args: argparse.Namespace) -> None:
    rows = wb.rows("4. Group A and A+")
    if args.query:
        exact_group_rows = [r for r in rows if r.get("groupname", "").casefold() == args.query.casefold()]
        rows = exact_group_rows or [
            r
            for r in rows
            if matches(r, args.query, ["groupname", "countrycode", "countryname", "countrycode_s", "countryname_s", "department"])
        ]
    write_rows(rows, ["groupname", "countrycode", "countryname", "countrycode_s", "countryname_s", "department"])


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workbook", type=Path, default=DEFAULT_WORKBOOK)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("summary")
    p.set_defaults(func=cmd_summary)

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

    p = sub.add_parser("group-a")
    p.add_argument("query", nargs="?")
    p.set_defaults(func=cmd_group_a)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    wb = Workbook(args.workbook)
    args.func(wb, args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

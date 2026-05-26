"""Lookup and resolution logic for WEO country, group, and framework terms."""

from __future__ import annotations

import re
import unicodedata
from typing import Iterable

from weo_country_groups_data import COUNTRY_ALIASES, GROUP_ALIASES, CsvTables


def _norm(value: str) -> str:
    ascii_value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", " ", ascii_value.lower()).strip()


def _compact(value: str) -> str:
    return _norm(value).replace(" ", "")


def group_alias_code(query: str) -> str | None:
    """Map common WEO/SPR group shorthand to a canonical group code.

    [When to Use]
    Call before fuzzy group search when the user says "AE", "EMDE", "LIC",
    "euro area", or similar shorthand.
    """
    return GROUP_ALIASES.get(_norm(query))


def country_alias_code(query: str) -> str | None:
    """Map common country aliases to WEO country codes.

    [When to Use]
    Call before country search when the user says "US", "UK", "South Korea",
    "DRC", or another colloquial country name.
    """
    return COUNTRY_ALIASES.get(_norm(query))


def _matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    """Return whether a row loosely matches a query across selected fields.

    [When to Use]
    Use for fallback search after alias and exact matching fail.
    """
    q = _norm(query)
    compact_q = _compact(query)
    for field in fields:
        v = _norm(row.get(field, ""))
        if q in v or compact_q == v.replace(" ", ""):
            return True
    return False


def _exact_matches(row: dict[str, str], query: str, fields: Iterable[str]) -> bool:
    """Return whether a row exactly matches a query after normalization.

    [When to Use]
    Use when a query should resolve only to an exact code or official name.
    """
    q = _compact(query)
    return any(_compact(row.get(field, "")) == q for field in fields)


def _unique_rows(rows: Iterable[dict[str, str]], key_fields: list[str]) -> list[dict[str, str]]:
    """Deduplicate rows by selected key fields while preserving order.

    [When to Use]
    Use when combining group rows from multiple reference tables.
    """
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
    """Extract unique group descriptors from composition rows.

    [When to Use]
    Use when group metadata may exist in the membership table even if it is not
    enough to rely only on the standalone groups table.
    """
    return _unique_rows(
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
    """Return member countries for a WEO or SPR/PRGT group.

    [When to Use]
    Use when the user asks which countries are in a group, or before expanding a
    group into country codes for data retrieval.

    Args:
        tables: CSV reference reader.
        group: Group code, alias, or group name.

    Returns:
        Composition rows for matching group members.
    """
    group_rows = resolve_group_rows(tables, group, exact_only=True)
    group_codes = {row["groupcode"] for row in group_rows}
    composition = tables.rows("composition")
    if group_codes:
        return [row for row in composition if row["groupcode"] in group_codes]
    return [
        row
        for row in composition
        if _matches(row, group, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]


def _group_summary(rows: list[dict[str, str]], fallback: str) -> tuple[str, str]:
    """Return a display-ready group code and group name from member rows.

    [When to Use]
    Use when reporting counts or comparisons for an already-resolved group.
    """
    if not rows:
        return fallback, ""
    row = rows[0]
    return row.get("groupcode", fallback), row.get("groupname_s") or row.get("groupname", "")


def resolve_group_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    """Resolve a user group term to candidate WEO/SPR group rows.

    [Intent]
    Maps shorthand, codes, or natural-language group names to official group
    metadata without guessing.

    [When to Use]
    Call before committing to any group code such as G110, G200, G201,
    G-PRGT-EM, or G-PRGT-LIC.

    Args:
        tables: CSV reference reader.
        query: User-provided group code, alias, or name.
        exact_only: If True, skip fuzzy fallback matches.

    Returns:
        Matching group rows, possibly empty.
    """
    groups = tables.rows("groups")
    composition_groups = _group_rows_from_composition(tables.rows("composition"))
    all_groups = _unique_rows([*composition_groups, *groups], ["groupcode"])
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
        if _exact_matches(row, query, ["groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]
    if exact or exact_only:
        return exact
    return [
        row
        for row in all_groups
        if _matches(row, query, ["grouptype", "groupcode", "groupname", "groupcode_s", "groupname_s"])
    ]


def resolve_country_rows(tables: CsvTables, query: str, exact_only: bool = False) -> list[dict[str, str]]:
    """Resolve a user country term to candidate WEO country rows.

    [Intent]
    Maps aliases, codes, or country names to official WEO country metadata.

    [When to Use]
    Call before using a country code in membership checks or data retrieval.

    Args:
        tables: CSV reference reader.
        query: User-provided country code, alias, or name.
        exact_only: If True, skip fuzzy fallback matches.

    Returns:
        Matching country rows, possibly empty.
    """
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

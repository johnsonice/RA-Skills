#!/usr/bin/env python3
"""Search IMF variable and dataset reference CSVs for catalog lookups."""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter

from catalog_data import (
    BBG_VARIABLES_CSV,
    COMMON_TOPIC_ROUTES,
    DATABASES_DIR,
    INDICATOR_CSVS,
    IFS_TOPIC_ROUTES,
    LEGACY_WEO_DB,
    MONTH_ALIASES,
    MONTHS,
    NON_VINTAGE_DATABASES_CSV,
    QUERY_SYNONYMS,
    SKILL_DIR,
    SPECIALIZED_INDICATOR_CSVS,
    VARIABLES_CSV,
    VARIABLES_DIR,
    VARIANT_TERMS,
    VINTAGE_DATABASES_CSV,
    WDI_VARIABLES_CSV,
    WEO_LIVE_DB,
    WTO_VARIABLES_CSV,
    all_datasets,
    dataset_record,
    load_catalog_variables,
    load_datasets,
    load_variable_file,
    norm,
    row_code,
    row_name,
    tokens,
)
from catalog_lookup import (
    build_clarification,
    candidate_variable_paths,
    candidate_variables,
    compare_records,
    distinction_note,
    exact_code_matches,
    fallback_variables,
    handoff_record,
    has_variant_marker,
    indicator_paths_for_database,
    resolve_catalog_request,
    resolve_status,
    result_record,
    score_variable,
    scored_sort_key,
    scored_variables,
    search_summary,
    variable_record,
)
from catalog_routing import (
    classify_database,
    common_topic_route,
    database_sort_key,
    exact_database_matches,
    explicitly_requested_legacy_weo,
    include_dataset_row,
    include_variable_row,
    indicator_lookup_database,
    is_vintage_database,
    is_weo_live_database,
    is_weo_vintage_database,
    latest_weo_dataset,
    latest_weo_vintage_dataset,
    legacy_ifs_route,
    materialize_database,
    parse_weo_sort_key,
    phrase_match,
    preferred_database_for_query,
    preferred_specialized_database,
    requested_weo_vintage_database,
    route_explanation,
    route_query,
)


def write_search_rows(scored: list[tuple[int, dict[str, str]]], limit: int) -> None:
    fieldnames = ["score", "database_name", "dimension_name", "code", "name"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for score, row in scored[:limit]:
        writer.writerow(result_record(score, row))


def write_json(payload: object) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def cmd_latest_weo(_args: argparse.Namespace) -> None:
    """
    [Intent]
    Prints the default non-vintage WEO Live dataset row.

    [When to Use]
    Use when the user asks for the current/latest WEO Live database.
    """
    row = latest_weo_dataset()
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["database", "name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerow(row)


def cmd_datasets(args: argparse.Namespace) -> None:
    """
    [Intent]
    Lists dataset catalog rows, optionally filtered to WEO vintages.

    [When to Use]
    Use when the user asks what datasets or WEO vintages are available.
    """
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
    """
    [Intent]
    Prints ranked indicator candidates for a natural-language metric query.

    [When to Use]
    Use for exploratory lookup when candidates should be inspected before commitment.
    """
    scored = scored_variables(args)
    records = [result_record(score, row) for score, row in scored[: args.limit]]
    if args.json:
        write_json(
            {
                "query": args.query,
                "route": route_explanation(args.query, args.database),
                "summary": search_summary(records),
                "results": records,
            }
        )
        return
    write_search_rows(scored, args.limit)


def cmd_resolve(args: argparse.Namespace) -> int:
    """
    [Intent]
    Resolves a metric query to a single handoff when safe, otherwise returns candidates.

    [When to Use]
    Use before handing a catalog identifier to data retrieval.
    """
    payload = resolve_catalog_request(args)
    if args.json:
        write_json(payload)
    else:
        print(f"status: {payload['status']}")
        print(f"note: {payload['note']}")
        if payload["handoff"]:
            handoff = payload["handoff"]
            print(f"database: {handoff['database']}")
            print(f"dimension_name: {handoff['dimension_name']}")
            print(f"code: {handoff['code']}")
            print(f"name: {handoff['name']}")
            print(f"notes: {handoff['notes']}")
            if handoff.get("legacy_source_note"):
                print(f"legacy_source_note: {handoff['legacy_source_note']}")
        else:
            candidates = payload.get("candidates", [])
            fieldnames = ["score", "database_name", "dimension_name", "code", "name"]
            writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            writer.writerows(candidates)
            clarification = payload.get("clarification")
            if clarification:
                print(f"clarification: {clarification['question']}")
    return 0


def cmd_explain_source(args: argparse.Namespace) -> None:
    """
    [Intent]
    Explains which source/database family a request should route to.

    [When to Use]
    Use before indicator search when IFS, WDI, Bloomberg, WTO, WEO vintage, or
    source-family ambiguity appears.
    """
    payload = route_explanation(args.query, args.database)
    if args.json:
        write_json(payload)
        return
    print(f"status: {payload['status']}")
    print(f"database: {payload['database'] or ''}")
    print(f"reason: {payload['reason']}")
    print(f"next_step: {payload['next_step']}")


def cmd_code(args: argparse.Namespace) -> None:
    """
    [Intent]
    Looks up exact indicator code metadata.

    [When to Use]
    Use when the user already supplied a known code and needs validation or meaning.
    """
    matches = exact_code_matches(args.code, args.database)
    records = [variable_record(row) for row in matches]
    payload = {
        "status": "found" if records else "not_found",
        "code": args.code,
        "database": args.database,
        "matches": records,
        "summary": search_summary([dict(record, score=0) for record in records]),
    }
    if args.json:
        write_json(payload)
        return
    fieldnames = ["database_name", "dimension_name", "code", "name"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(records)


def cmd_dimensions(args: argparse.Namespace) -> None:
    """
    [Intent]
    Lists indicator dimensions represented in a database's local catalog registry.

    [When to Use]
    Use before data handoff when the code dimension might not be `INDICATOR`.
    """
    rows = load_catalog_variables(indicator_paths_for_database(args.database))
    lookup_database = indicator_lookup_database(args.database)
    rows = [
        materialize_database(row, args.database)
        for row in rows
        if row.get("database_name") == lookup_database
    ]
    counts = Counter(row.get("dimension_name", "") for row in rows)
    examples: dict[str, list[str]] = {}
    for row in rows:
        dimension = row.get("dimension_name", "")
        examples.setdefault(dimension, [])
        if len(examples[dimension]) < 3:
            examples[dimension].append(row_code(row))
    records = [
        {"database_name": args.database, "dimension_name": dimension, "count": count, "example_codes": examples[dimension]}
        for dimension, count in counts.most_common()
    ]
    payload = {
        "status": "found" if records else "not_found",
        "database": args.database,
        "dimensions": records,
    }
    if args.json:
        write_json(payload)
        return
    writer = csv.DictWriter(sys.stdout, fieldnames=["database_name", "dimension_name", "count", "example_codes"])
    writer.writeheader()
    for record in records:
        writer.writerow({**record, "example_codes": ";".join(record["example_codes"])})


def cmd_classify_database(args: argparse.Namespace) -> None:
    """
    [Intent]
    Classifies an exact database as live, vintage, legacy, non-vintage, or missing.

    [When to Use]
    Use when LIVE vs vintage or legacy status is unclear.
    """
    payload = classify_database(args.database)
    if args.json:
        write_json(payload)
        return
    print(f"status: {payload['status']}")
    print(f"database: {payload['database']}")
    print(f"classification: {payload['classification'] or ''}")
    print(f"notes: {payload['notes']}")


def cmd_compare_codes(args: argparse.Namespace) -> None:
    """
    [Intent]
    Compares exact indicator codes by database, dimension, and official name.

    [When to Use]
    Use when the user asks which variant/code is appropriate.
    """
    records_by_code = {code: exact_code_matches(code, args.database) for code in args.codes}
    payload = {
        "status": "complete" if all(records_by_code.values()) else "partial",
        "database": args.database,
        "codes": {code: [variable_record(row) for row in rows] for code, rows in records_by_code.items()},
        "comparison": compare_records(records_by_code),
    }
    if args.json:
        write_json(payload)
        return
    print(f"status: {payload['status']}")
    comparison = payload["comparison"]
    print(f"same_database: {comparison['same_database']}")
    print(f"same_dimension: {comparison['same_dimension']}")
    print(f"note: {comparison['note']}")
    for code, rows in payload["codes"].items():
        if not rows:
            print(f"{code}: NOT FOUND")
            continue
        row = rows[0]
        print(f"{code}: {row['database_name']} | {row['dimension_name']} | {row['name']}")


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
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("resolve")
    p.add_argument("query")
    p.add_argument("--database")
    p.add_argument("--all-databases", action="store_true")
    p.add_argument("--limit", type=int, default=5)
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_resolve)

    p = sub.add_parser("explain-source")
    p.add_argument("query")
    p.add_argument("--database")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_explain_source)

    p = sub.add_parser("code")
    p.add_argument("code")
    p.add_argument("--database")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_code)

    p = sub.add_parser("dimensions")
    p.add_argument("database")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_dimensions)

    p = sub.add_parser("classify-database")
    p.add_argument("database")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_classify_database)

    p = sub.add_parser("compare-codes")
    p.add_argument("codes", nargs="+")
    p.add_argument("--database")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cmd_compare_codes)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    result = args.func(args)
    return int(result or 0)


if __name__ == "__main__":
    raise SystemExit(main())

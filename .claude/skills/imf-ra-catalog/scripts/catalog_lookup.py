"""Indicator scoring, exact lookup, ambiguity handling, and handoff records."""

from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from catalog_data import (
    INDICATOR_CSVS,
    SPECIALIZED_INDICATOR_CSVS,
    VARIABLES_CSV,
    VARIANT_TERMS,
    WEO_LIVE_DB,
    load_catalog_variables,
    norm,
    row_code,
    row_name,
    tokens,
)
from catalog_routing import (
    database_sort_key,
    indicator_lookup_database,
    include_variable_row,
    is_weo_live_database,
    materialize_database,
    preferred_database_for_query,
    route_explanation,
)


def indicator_paths_for_database(database_name: str) -> list[Path]:
    """
    [Intent]
    Chooses the indicator registry CSV for a requested database.

    [When to Use]
    Use before loading variables for WEO, WDI, Bloomberg, WTO, or WEO vintage lookup.

    Args:
        database_name: Requested database name.

    Returns:
        List of CSV paths to search.
    """
    lookup_database = indicator_lookup_database(database_name)
    return [SPECIALIZED_INDICATOR_CSVS.get(lookup_database, VARIABLES_CSV)]


def candidate_variable_paths(args: argparse.Namespace) -> list[Path]:
    if args.database:
        return indicator_paths_for_database(args.database)
    if args.all_databases:
        return INDICATOR_CSVS
    preferred_db = preferred_database_for_query(args.query)
    if preferred_db:
        return indicator_paths_for_database(preferred_db)
    return [VARIABLES_CSV]


def candidate_variables(args: argparse.Namespace) -> list[dict[str, str]]:
    """
    [Intent]
    Loads and filters indicator candidates according to query routing options.

    [When to Use]
    Use before scoring a fuzzy indicator request.

    Args:
        args: CLI-like namespace containing query, database, and all_databases.

    Returns:
        Candidate indicator rows ready for scoring.
    """
    variables = load_catalog_variables(candidate_variable_paths(args))
    if args.database:
        lookup_database = indicator_lookup_database(args.database)
        return [
            materialize_database(row, args.database)
            for row in variables
            if row.get("database_name") == lookup_database
        ]
    if args.all_databases:
        return [row for row in variables if include_variable_row(row)]
    preferred_db = preferred_database_for_query(args.query)
    if preferred_db:
        lookup_database = indicator_lookup_database(preferred_db)
        return [
            materialize_database(row, preferred_db)
            for row in variables
            if row.get("database_name") == lookup_database
        ]
    return [row for row in variables if is_weo_live_database(row.get("database_name", ""))]


def fallback_variables(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.database or args.all_databases or preferred_database_for_query(args.query):
        return []
    variables = load_catalog_variables()
    return [row for row in variables if include_variable_row(row)]


def score_variable(row: dict[str, str], query: str) -> int:
    """
    [Intent]
    Scores how well one indicator row matches a natural-language metric query.

    [When to Use]
    Use during fuzzy indicator search; do not hand-pick codes from memory when this
    scoring helper can rank candidates.

    Args:
        row: Indicator catalog row.
        query: User metric request.

    Returns:
        Integer relevance score. Non-positive scores are discarded.
    """
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
    if "exchange" in exact_tokens and "rate" in exact_tokens and "exchange rate" in name:
        score += 30
    if row.get("database_name") == "IMF.STA:ER" and "exchange" in exact_tokens and "rate" in exact_tokens:
        score += 35
    if "monthly" in exact_tokens and "monthly" in name:
        score += 20
    if "financial" in exact_tokens and "soundness" in exact_tokens and "capital" in name:
        score += 25
    score -= max(0, len(name.split()) - 8)
    return score


def scored_variables(args: argparse.Namespace) -> list[tuple[int, dict[str, str]]]:
    """
    [Intent]
    Produces ranked indicator candidates for a catalog query.

    [When to Use]
    Use for `search` and as the first step of `resolve`.

    Args:
        args: CLI-like namespace containing query, database, all_databases, and limit.

    Returns:
        Sorted `(score, row)` tuples, highest relevance first.
    """
    candidates = candidate_variables(args)
    scored = [(score_variable(row, args.query), row) for row in candidates]
    scored = [(score, row) for score, row in scored if score > 0]
    scored.sort(key=scored_sort_key)

    fallback_candidates = fallback_variables(args)
    if (not scored or scored[0][0] < 25) and fallback_candidates:
        fallback = [(score_variable(row, args.query), row) for row in fallback_candidates]
        scored = [(score, row) for score, row in fallback if score > 0]
        scored.sort(key=scored_sort_key)
    return scored


def scored_sort_key(item: tuple[int, dict[str, str]]) -> tuple[int, tuple[int, int, int, int, str], str, str, str]:
    score, row = item
    return (
        -score,
        database_sort_key(row.get("database_name", "")),
        row.get("dimension_name", ""),
        row_code(row),
        row_name(row),
    )


def result_record(score: int, row: dict[str, str]) -> dict[str, object]:
    """
    [Intent]
    Converts a scored catalog row into the standard result shape.

    [When to Use]
    Use before returning search, resolve, or JSON payload results.

    Args:
        score: Relevance score.
        row: Indicator catalog row.

    Returns:
        Result dictionary with database_name, dimension_name, code, name, and score.
    """
    record: dict[str, object] = {
        "score": score,
        "database_name": row.get("database_name", ""),
        "dimension_name": row.get("dimension_name", ""),
        "code": row_code(row),
        "name": row_name(row),
    }
    if row.get("indicator_source_database") and row.get("indicator_source_database") != row.get("database_name"):
        record["indicator_source_database"] = row.get("indicator_source_database", "")
    return record


def variable_record(row: dict[str, str]) -> dict[str, str]:
    """
    [Intent]
    Converts an exact indicator row into a compact metadata record.

    [When to Use]
    Use for exact code lookup, dimension examples, and code comparison outputs.

    Args:
        row: Indicator catalog row.

    Returns:
        Dictionary with database_name, dimension_name, code, and name.
    """
    record = {
        "database_name": row.get("database_name", ""),
        "dimension_name": row.get("dimension_name", ""),
        "code": row_code(row),
        "name": row_name(row),
    }
    if row.get("indicator_source_database") and row.get("indicator_source_database") != row.get("database_name"):
        record["indicator_source_database"] = row.get("indicator_source_database", "")
    return record


def exact_code_matches(code: str, database: str | None = None) -> list[dict[str, str]]:
    """
    [Intent]
    Finds exact indicator/code matches without fuzzy inference.

    [When to Use]
    Use when the user already supplied a code, or before comparing known code variants.

    Args:
        code: Exact code to find.
        database: Optional database filter.

    Returns:
        Matching indicator rows, possibly empty.
    """
    wanted = code.casefold()
    lookup_database = indicator_lookup_database(database)
    rows = load_catalog_variables(indicator_paths_for_database(database)) if database else load_catalog_variables()
    matches = [row for row in rows if row_code(row).casefold() == wanted]
    if lookup_database:
        matches = [row for row in matches if row.get("database_name") == lookup_database]
    if database:
        matches = [materialize_database(row, database) for row in matches]
    return matches


def search_summary(records: list[dict[str, object]], status: str | None = None, note: str | None = None) -> dict[str, object]:
    """
    [Intent]
    Summarizes search or resolve results for agent decision-making.

    [When to Use]
    Use whenever returning ranked candidates or a resolution payload.

    Args:
        records: Result records.
        status: Optional resolve status.
        note: Optional status explanation.

    Returns:
        Summary with result counts, database/dimension counts, and recommended_next_step.
    """
    db_counts = Counter(str(record.get("database_name", "")) for record in records)
    dim_counts = Counter(str(record.get("dimension_name", "")) for record in records)
    summary: dict[str, object] = {
        "result_count": len(records),
        "database_counts": dict(db_counts.most_common()),
        "dimension_counts": dict(dim_counts.most_common()),
    }
    if status:
        summary["status"] = status
    if note:
        summary["note"] = note
    if status == "resolved":
        summary["recommended_next_step"] = "Use result.database_name, result.dimension_name, and result.code for handoff; do not run a data fetch from catalog context."
    elif not records:
        summary["recommended_next_step"] = "Ask for one additional source, unit, or terminology hint before writing temporary code."
    elif len(db_counts) > 1:
        summary["recommended_next_step"] = "Treat this as cross-database ambiguity; ask the user to choose the intended source or use resolve with a database."
    elif len(dim_counts) > 1:
        summary["recommended_next_step"] = "Treat this as dimension ambiguity; preserve dimension_name and ask which dimension/code family is intended."
    else:
        summary["recommended_next_step"] = "Inspect the top candidates; use resolve when a single handoff identifier is needed."
    return summary


def distinction_note(record: dict[str, object]) -> str:
    name = str(record.get("name", ""))
    parts = [part.strip() for part in name.split(",")]
    if len(parts) > 1:
        return ", ".join(parts[1:4])
    return name


def build_clarification(records: list[dict[str, object]]) -> dict[str, object] | None:
    """
    [Intent]
    Builds a user-facing clarification prompt from ambiguous catalog candidates.

    [When to Use]
    Use when `resolve` cannot safely commit to one identifier.

    Args:
        records: Ranked result records.

    Returns:
        Clarification question and options, or None when no records exist.
    """
    if not records:
        return None
    options = [
        {
            "database_name": record.get("database_name", ""),
            "dimension_name": record.get("dimension_name", ""),
            "code": record.get("code", ""),
            "name": record.get("name", ""),
            "distinction": distinction_note(record),
        }
        for record in records[:5]
    ]
    labels = [f"{option['code']} ({option['distinction']})" for option in options]
    return {
        "question": "Which catalog candidate should I use: " + "; ".join(labels) + "?",
        "options": options,
    }


def handoff_record(record: dict[str, object], route: dict[str, object], note: str) -> dict[str, object]:
    """
    [Intent]
    Creates the machine-readable catalog handoff for data retrieval.

    [When to Use]
    Use only after `resolve` determines that one candidate is safe to commit.

    Args:
        record: Resolved result record.
        route: Source-routing metadata.
        note: Resolution explanation.

    Returns:
        Handoff dictionary with database, dimension_name, code, name, and notes.
    """
    handoff = {
        "database": record.get("database_name", ""),
        "dimension_name": record.get("dimension_name", ""),
        "code": record.get("code", ""),
        "name": record.get("name", ""),
        "notes": note,
    }
    if record.get("indicator_source_database"):
        handoff["indicator_source_database"] = record["indicator_source_database"]
        handoff["notes"] = (
            f"{note} Indicator metadata were matched from {record['indicator_source_database']} "
            f"and the requested database remains {record.get('database_name', '')}."
        )
    if route.get("status") == "routed" and "IFS is a legacy" in str(route.get("reason", "")):
        handoff["legacy_source_note"] = (
            "IFS is a legacy EcOS source, not a single iData dataset; this result is from the replacement iData topic database."
        )
    return handoff


def compare_records(records_by_code: dict[str, list[dict[str, str]]]) -> dict[str, object]:
    """
    [Intent]
    Compares metadata for multiple exact indicator codes.

    [When to Use]
    Use when the user asks how two or more known codes differ.

    Args:
        records_by_code: Mapping from requested code to exact-match rows.

    Returns:
        Comparison payload covering database, dimension, names, and completeness.
    """
    found = {code: rows for code, rows in records_by_code.items() if rows}
    first_rows = {code: rows[0] for code, rows in found.items()}
    databases = {row.get("database_name", "") for row in first_rows.values()}
    dimensions = {row.get("dimension_name", "") for row in first_rows.values()}
    names = {code: row_name(row) for code, row in first_rows.items()}
    return {
        "all_codes_found": len(found) == len(records_by_code),
        "same_database": len(databases) == 1,
        "same_dimension": len(dimensions) == 1,
        "databases": sorted(databases),
        "dimensions": sorted(dimensions),
        "names": names,
        "note": "Compare the names for unit, timing, basis, and transformation differences before committing."
        if len(found) > 1
        else "At least one requested code was not found; do not infer missing metadata.",
    }


def has_variant_marker(record: dict[str, object]) -> bool:
    name = norm(str(record.get("name", "")))
    return any(term in name for term in VARIANT_TERMS)


def resolve_status(scored: list[tuple[int, dict[str, str]]], query: str) -> tuple[str, str]:
    """
    [Intent]
    Decides whether ranked candidates are resolved, ambiguous, or no_match.

    [When to Use]
    Use after scoring before creating a handoff or asking for clarification.

    Args:
        scored: Ranked `(score, row)` tuples.
        query: Original user query.

    Returns:
        `(status, note)` where status is resolved, ambiguous, or no_match.
    """
    if not scored:
        return ("no_match", "No catalog rows received a positive score.")
    top = result_record(*scored[0])
    if int(top["score"]) < 25:
        return ("no_match", "Top score is below the helper confidence threshold.")
    if len(scored) == 1:
        return ("resolved", "Only one plausible catalog row matched.")
    second = result_record(*scored[1])
    score_gap = int(top["score"]) - int(second["score"])
    if int(top["score"]) >= 100 and score_gap > 0 and not has_variant_marker(top):
        return ("resolved", "Top candidate is a high-scoring base concept and outranks close variants.")
    if score_gap >= 25:
        return ("resolved", "Top candidate is clearly separated from the next candidate.")
    if top["database_name"] != second["database_name"] or top["dimension_name"] != second["dimension_name"]:
        return ("ambiguous", "Multiple databases or dimensions remain plausible.")
    return ("ambiguous", "Several close variants differ by transformation, unit, basis, or frequency.")


def resolve_catalog_request(args: argparse.Namespace) -> dict[str, object]:
    """
    [Intent]
    Resolves a natural-language metric request into a safe catalog handoff when possible.

    [When to Use]
    Use as the default path before data retrieval when the user asks for a metric,
    source route, or find-and-download workflow.

    Args:
        args: CLI-like namespace containing query, database, all_databases, and limit.

    Returns:
        Payload with status, route, summary, result, handoff, candidates, and clarification.
    """
    original_database = args.database
    route = route_explanation(args.query, args.database)
    routed_database = route.get("database")
    if not args.database and routed_database and routed_database != WEO_LIVE_DB:
        args.database = str(routed_database)
    scored = scored_variables(args)
    status, note = resolve_status(scored, args.query)
    records = [result_record(score, row) for score, row in scored[: args.limit]]
    route = route_explanation(args.query, args.database) if original_database else route
    payload: dict[str, object] = {
        "status": status,
        "query": args.query,
        "route": route,
        "note": note,
        "summary": search_summary(records, status=status, note=note),
        "result": records[0] if status == "resolved" and records else None,
        "handoff": handoff_record(records[0], route, note) if status == "resolved" and records else None,
        "candidates": records if status != "resolved" else records[: min(3, len(records))],
    }
    if status != "resolved":
        payload["clarification"] = build_clarification(records)
    return payload

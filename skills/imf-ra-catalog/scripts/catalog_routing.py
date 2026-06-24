"""Source routing, database classification, and WEO vintage handling."""

from __future__ import annotations

import re

from catalog_data import (
    COMMON_TOPIC_ROUTES,
    IFS_TOPIC_ROUTES,
    LEGACY_WEO_DB,
    MONTH_ALIASES,
    MONTHS,
    WEO_LIVE_DB,
    all_datasets,
    dataset_record,
    load_datasets,
    norm,
)


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


def is_weo_vintage_database(database_name: str) -> bool:
    return (database_name or "").startswith("IMF.RES.WEO:WEO_LIVE_") and is_vintage_database(database_name)


def indicator_lookup_database(database_name: str | None) -> str | None:
    """
    [Intent]
    Maps a requested database to the database whose indicator metadata should be searched.

    [When to Use]
    Use when the request names a WEO vintage; indicator metadata come from WEO Live while
    the requested vintage database is preserved in outputs.

    Args:
        database_name: Requested database name, or None.

    Returns:
        Metadata lookup database name, or None.
    """
    if database_name and is_weo_vintage_database(database_name):
        return WEO_LIVE_DB
    return database_name


def materialize_database(row: dict[str, str], database_name: str | None) -> dict[str, str]:
    """
    [Intent]
    Rewrites a matched indicator row to preserve the user's requested database.

    [When to Use]
    Use after matching WEO Live metadata for a WEO vintage request.

    Args:
        row: Indicator catalog row.
        database_name: Requested database to report.

    Returns:
        Original or materialized row with `indicator_source_database` when needed.
    """
    if not database_name or row.get("database_name") == database_name:
        return row
    materialized = dict(row)
    materialized["indicator_source_database"] = row.get("database_name", "")
    materialized["database_name"] = database_name
    return materialized


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


def latest_weo_dataset() -> dict[str, str]:
    """
    [Intent]
    Returns the default non-vintage WEO Live dataset row.

    [When to Use]
    Use when the user asks for latest/current WEO data without specifying a vintage.

    Returns:
        Dataset catalog row for `IMF.RES.WEO:WEO_LIVE`.
    """
    for row in load_datasets(include_vintage=False):
        if row.get("database") == WEO_LIVE_DB:
            return row
    raise RuntimeError("No non-vintage WEO Live dataset found")


def latest_weo_vintage_dataset() -> dict[str, str]:
    """
    [Intent]
    Returns the newest dated WEO Live vintage dataset row.

    [When to Use]
    Use when the user explicitly asks for the latest WEO vintage release.

    Returns:
        Dataset catalog row for the newest WEO vintage.
    """
    rows = load_datasets(vintage_only=True)
    rows = [row for row in rows if is_weo_vintage_database(row.get("database", ""))]
    if not rows:
        raise RuntimeError("No WEO Live vintage dataset found")
    rows.sort(key=lambda row: database_sort_key(row.get("database", "")))
    return rows[0]


def is_weo_live_database(database_name: str) -> bool:
    return database_name == WEO_LIVE_DB


def explicitly_requested_legacy_weo(query: str | None) -> bool:
    return norm(query or "") in {norm(LEGACY_WEO_DB), "imf res weo", "res weo"}


def requested_weo_vintage_database(query: str | None) -> str | None:
    """
    [Intent]
    Extracts an explicit WEO vintage database from user wording.

    [When to Use]
    Use during source routing before defaulting to WEO Live.

    Args:
        query: User request text.

    Returns:
        Matching WEO vintage database name, or None.
    """
    query_norm = norm(query or "")
    query_tokens = set(query_norm.split())
    if "weo" not in query_tokens or "vintage" not in query_tokens:
        return None

    for row in load_datasets(vintage_only=True):
        database = row.get("database", "")
        if database and database.casefold() in (query or "").casefold():
            return database

    if "latest" in query_tokens:
        return latest_weo_vintage_dataset().get("database")

    years = re.findall(r"\b(20\d{2})\b", query_norm)
    month = next((abbr for token, abbr in MONTH_ALIASES.items() if token in query_tokens), None)
    if years and month:
        wanted_resource = f"WEO_LIVE_{years[0]}_{month}_VINTAGE"
        for row in load_datasets(vintage_only=True):
            if row.get("Resource ID") == wanted_resource:
                return row.get("database")
    return None


def include_dataset_row(row: dict[str, str], query: str | None) -> bool:
    return row.get("database") != LEGACY_WEO_DB or explicitly_requested_legacy_weo(query)


def include_variable_row(row: dict[str, str]) -> bool:
    return row.get("database_name") != LEGACY_WEO_DB


def phrase_match(query: str, phrase: str) -> bool:
    return norm(phrase) in norm(query)


def legacy_ifs_route(query: str) -> str | None:
    """
    [Intent]
    Routes legacy IFS wording to the replacement iData topic database.

    [When to Use]
    Use when the user mentions IFS plus a topic such as CPI, exchange rates, BOP,
    reserves, labor, or fiscal data.

    Args:
        query: User request text.

    Returns:
        Replacement iData database name, or None if the topic is unclear.
    """
    query_norm = norm(query)
    if "ifs" not in set(query_norm.split()) and "international financial statistics" not in query_norm:
        return None
    for phrases, database in IFS_TOPIC_ROUTES:
        if any(phrase_match(query, phrase) for phrase in phrases):
            return database
    return None


def common_topic_route(query: str) -> str | None:
    for phrases, database in COMMON_TOPIC_ROUTES:
        if any(phrase_match(query, phrase) for phrase in phrases):
            return database
    return None


def preferred_specialized_database(query: str) -> str | None:
    """
    [Intent]
    Routes obvious specialized-source requests to WDI, Bloomberg, or WTO catalogs.

    [When to Use]
    Use before WEO-default search when the user names World Bank/WDI, Bloomberg/BBG,
    WTO, tariff, commodity, or HS concepts.

    Args:
        query: User request text.

    Returns:
        Specialized database name, or None.
    """
    query_norm = norm(query)
    query_tokens = set(query_norm.split())
    if "world bank" in query_norm or "wdi" in query_tokens:
        return "WB:WDI"
    if "bloomberg" in query_tokens or "bbg" in query_tokens or "ticker" in query_tokens:
        return "IMF.CSF:BBGDL"
    if (
        "wto" in query_tokens
        or "tariff" in query_tokens
        or "commodity" in query_tokens
        or "hs" in query_tokens
    ):
        return "WTO:WTOIMFTT"
    return None


def route_query(query: str, database: str | None = None) -> dict[str, object]:
    """
    [Intent]
    Classifies a user request into the correct catalog source route.

    [When to Use]
    Run before indicator search or resolution whenever source family, WEO vintage,
    legacy IFS routing, or specialized catalog coverage may matter.

    Args:
        query: User request text.
        database: Optional caller-supplied database override.

    Returns:
        Routing metadata with status, database, reason, and next_step.
    """
    query_norm = norm(query)
    query_tokens = set(query_norm.split())
    is_ifs = "ifs" in query_tokens or "international financial statistics" in query_norm

    if is_ifs:
        routed_database = database or legacy_ifs_route(query)
        return {
            "status": "routed" if routed_database else "needs_more_context",
            "query": query,
            "database": routed_database,
            "reason": "IFS is a legacy EcOS source, not a single iData dataset; route by topic to the replacement iData database.",
            "next_step": "Run search with --database after the topic route is identified."
            if routed_database
            else "Ask for the IFS topic, such as CPI, exchange rates, current account, or reserves.",
        }

    if database and is_weo_vintage_database(database):
        return {
            "status": "routed",
            "query": query,
            "database": database,
            "reason": "The request targets a dated WEO Live vintage; indicator metadata are resolved from WEO Live and returned with the vintage database.",
            "next_step": f'Run resolve "{query}" --database {database}.',
        }

    if database:
        return {
            "status": "explicit_database",
            "query": query,
            "database": database,
            "reason": "The database was supplied explicitly by the caller.",
            "next_step": f'Run search "{query}" --database {database}.',
        }

    requested_vintage = requested_weo_vintage_database(query)
    if requested_vintage:
        return {
            "status": "routed",
            "query": query,
            "database": requested_vintage,
            "reason": "The request targets a dated WEO Live vintage; indicator metadata are resolved from WEO Live and returned with the vintage database.",
            "next_step": f'Run resolve "{query}" --database {requested_vintage}.',
        }

    specialized_database = preferred_specialized_database(query)
    if specialized_database:
        return {
            "status": "routed",
            "query": query,
            "database": specialized_database,
            "reason": "Query matched a specialized source covered by catalog_search.py.",
            "next_step": f'Run search "{query}" --database {specialized_database}.',
        }

    topic_route = common_topic_route(query)
    if topic_route:
        return {
            "status": "routed",
            "query": query,
            "database": topic_route,
            "reason": "Query matched a common topic route covered by catalog_search.py.",
            "next_step": f'Run search "{query}" --database {topic_route}.',
        }

    if "vintage" in query_tokens or "historical release" in query_norm:
        return {
            "status": "needs_more_context",
            "query": query,
            "database": None,
            "reason": "Vintage requests need an explicit release or a latest-vintage confirmation.",
            "next_step": "Run datasets WEO --vintage-only, then ask the user to confirm the intended vintage if needed.",
        }

    return {
        "status": "default",
        "query": query,
        "database": WEO_LIVE_DB,
        "reason": "No specialized source or topic route matched; WEO Live remains the default for common macro concepts.",
        "next_step": f'Run search "{query}" first; use --all-databases only if WEO Live is not plausible.',
    }


def preferred_database_for_query(query: str) -> str | None:
    route = route_query(query)
    if route.get("status") == "routed":
        return str(route.get("database") or "") or None
    return None


def exact_database_matches(database: str) -> list[dict[str, str]]:
    wanted = database.casefold()
    return [row for row in all_datasets() if row.get("database", "").casefold() == wanted]


def classify_database(database: str) -> dict[str, object]:
    """
    [Intent]
    Validates and classifies an exact database identifier.

    [When to Use]
    Use when checking whether a database is WEO Live, WEO vintage, legacy WEO,
    another non-vintage dataset, or missing.

    Args:
        database: Exact database identifier.

    Returns:
        Classification payload with status, notes, and matching dataset rows.
    """
    matches = exact_database_matches(database)
    if not matches:
        return {
            "status": "not_found",
            "database": database,
            "classification": None,
            "notes": "No exact database match found in non-vintage or vintage dataset catalogs.",
            "matches": [],
        }
    row = matches[0]
    db = row.get("database", "")
    if db == WEO_LIVE_DB:
        classification = "weo_live_non_vintage"
        notes = "This is the default non-vintage WEO Live database."
    elif db == LEGACY_WEO_DB:
        classification = "legacy_weo"
        notes = "This legacy WEO resource should be used only when explicitly requested."
    elif is_vintage_database(db):
        classification = "vintage"
        notes = "This is a dated WEO Live vintage, not the default live database."
    else:
        classification = "non_vintage"
        notes = "This is a non-vintage dataset catalog entry."
    return {
        "status": "found",
        "database": db,
        "classification": classification,
        "notes": notes,
        "matches": [dataset_record(row) for row in matches],
    }


def route_explanation(query: str, database: str | None = None) -> dict[str, object]:
    return route_query(query, database)

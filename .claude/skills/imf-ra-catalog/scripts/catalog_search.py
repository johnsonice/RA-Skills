#!/usr/bin/env python3
"""Search IMF variable and dataset reference CSVs for catalog lookups."""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DATABASES_DIR = SKILL_DIR / "databases"
VARIABLES_DIR = SKILL_DIR / "indicators"
VARIABLES_CSV = VARIABLES_DIR / "1. non_vintage_variable_list.csv"
BBG_VARIABLES_CSV = VARIABLES_DIR / "2. bbg_variable_list.csv"
WDI_VARIABLES_CSV = VARIABLES_DIR / "3. wdi_variable_list.csv"
WTO_VARIABLES_CSV = VARIABLES_DIR / "4. wto_variable_List.csv"
NON_VINTAGE_DATABASES_CSV = DATABASES_DIR / "non_vintage_datasets.csv"
VINTAGE_DATABASES_CSV = DATABASES_DIR / "vintage_datasets.csv"
WEO_LIVE_DB = "IMF.RES.WEO:WEO_LIVE"
LEGACY_WEO_DB = "IMF.RES:WEO"
SPECIALIZED_INDICATOR_CSVS = {
    "IMF.CSF:BBGDL": BBG_VARIABLES_CSV,
    "WB:WDI": WDI_VARIABLES_CSV,
    "WTO:WTOIMFTT": WTO_VARIABLES_CSV,
}
INDICATOR_CSVS = [VARIABLES_CSV, *SPECIALIZED_INDICATOR_CSVS.values()]
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
    "usd": ["us", "dollar", "dollars"],
    "exchange": ["rate"],
    "fx": ["exchange", "rate"],
    "reer": ["real", "effective", "exchange", "rate"],
    "neer": ["nominal", "effective", "exchange", "rate"],
    "reserves": ["reserve", "assets"],
    "bank": ["banking"],
    "capital": ["adequacy"],
}
IFS_TOPIC_ROUTES = [
    (("cpi", "consumer price", "consumer prices", "inflation index"), "IMF.STA:CPI"),
    (("exchange rate", "exchange rates", "fx"), "IMF.STA:ER"),
    (("effective exchange", "reer", "neer"), "IMF.STA:EER"),
    (("interest rate", "interest rates"), "IMF.STA:MFS_IR"),
    (("money", "monetary aggregate", "monetary aggregates"), "IMF.STA:MFS_MA"),
    (("national account", "national accounts", "gdp", "expenditure"), "IMF.STA:ANEA"),
    (("quarterly national", "quarterly gdp"), "IMF.STA:QNEA"),
    (("balance of payments", "current account"), "IMF.STA:BOP"),
    (("international investment", "iip"), "IMF.STA:IIP"),
    (("liquidity", "reserves", "reserve assets"), "IMF.STA:IL"),
    (("goods trade", "trade in goods"), "IMF.STA:ITG"),
    (("producer price", "producer prices", "ppi"), "IMF.STA:PPI"),
    (("production index", "industrial production", "ipi"), "IMF.STA:PI"),
    (("government finance", "fiscal", "qgfs"), "IMF.STA:QGFS"),
    (("labor", "labour", "employment", "unemployment"), "IMF.STA:LS"),
    (("fund accounts",), "IMF.STA:FA"),
    (("special purpose", "spe"), "IMF.STA:SPE"),
]
COMMON_TOPIC_ROUTES = [
    (("financial soundness", "capital adequacy", "risk weighted assets", "fsi"), "IMF.STA:FSIC"),
    (("consumer price index", "cpi"), "IMF.STA:CPI"),
    (("monthly exchange rate", "exchange rate", "exchange rates", "fx"), "IMF.STA:ER"),
    (("effective exchange", "reer", "neer"), "IMF.STA:EER"),
    (("current account", "balance of payments", "bop"), "IMF.STA:BOP"),
    (("international investment position", "iip"), "IMF.STA:IIP"),
    (("reserves", "reserve assets", "international liquidity"), "IMF.STA:IL"),
]
VARIANT_TERMS = (
    "median",
    "per capita",
    "quarter-over-quarter",
    "year-over-year",
    "seasonally adjusted",
    "purchasing power parity",
    "aggregate",
    "weighted",
)
MONTH_ALIASES = {
    "january": "JAN",
    "jan": "JAN",
    "february": "FEB",
    "feb": "FEB",
    "march": "MAR",
    "mar": "MAR",
    "april": "APR",
    "apr": "APR",
    "may": "MAY",
    "june": "JUN",
    "jun": "JUN",
    "july": "JUL",
    "jul": "JUL",
    "august": "AUG",
    "aug": "AUG",
    "september": "SEP",
    "sep": "SEP",
    "october": "OCT",
    "oct": "OCT",
    "november": "NOV",
    "nov": "NOV",
    "december": "DEC",
    "dec": "DEC",
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


def is_vintage_database(database_name: str) -> bool:
    return "_VINTAGE" in (database_name or "")


def is_weo_vintage_database(database_name: str) -> bool:
    return (database_name or "").startswith("IMF.RES.WEO:WEO_LIVE_") and is_vintage_database(database_name)


def indicator_lookup_database(database_name: str | None) -> str | None:
    if database_name and is_weo_vintage_database(database_name):
        return WEO_LIVE_DB
    return database_name


def materialize_database(row: dict[str, str], database_name: str | None) -> dict[str, str]:
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


def load_datasets(include_vintage: bool = False, vintage_only: bool = False) -> list[dict[str, str]]:
    paths = [VINTAGE_DATABASES_CSV] if vintage_only else [NON_VINTAGE_DATABASES_CSV]
    if include_vintage and not vintage_only:
        paths.append(VINTAGE_DATABASES_CSV)
    rows: list[dict[str, str]] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8-sig") as f:
            rows.extend(csv.DictReader(f))
    return rows


def load_variable_file(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def load_catalog_variables(paths: list[Path] | None = None) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for path in paths or INDICATOR_CSVS:
        rows.extend(load_variable_file(path))
    return rows


def all_datasets() -> list[dict[str, str]]:
    return load_datasets(include_vintage=True)


def route_query(query: str, database: str | None = None) -> dict[str, object]:
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


def phrase_match(query: str, phrase: str) -> bool:
    return norm(phrase) in norm(query)


def legacy_ifs_route(query: str) -> str | None:
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


def indicator_paths_for_database(database_name: str) -> list[Path]:
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


def latest_weo_dataset() -> dict[str, str]:
    for row in load_datasets(include_vintage=False):
        if row.get("database") == WEO_LIVE_DB:
            return row
    raise RuntimeError("No non-vintage WEO Live dataset found")


def latest_weo_vintage_dataset() -> dict[str, str]:
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


def score_variable(row: dict[str, str], query: str) -> int:
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


def row_code(row: dict[str, str]) -> str:
    return row.get("Code", "") or row.get("indicator_code", "")


def row_name(row: dict[str, str]) -> str:
    return row.get("Name", "") or row.get("indicator_name", "")


def result_record(score: int, row: dict[str, str]) -> dict[str, object]:
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
    record = {
        "database_name": row.get("database_name", ""),
        "dimension_name": row.get("dimension_name", ""),
        "code": row_code(row),
        "name": row_name(row),
    }
    if row.get("indicator_source_database") and row.get("indicator_source_database") != row.get("database_name"):
        record["indicator_source_database"] = row.get("indicator_source_database", "")
    return record


def dataset_record(row: dict[str, str]) -> dict[str, str]:
    return {
        "database": row.get("database", ""),
        "name": row.get("name", ""),
        "agency_id": row.get("Agency ID", ""),
        "resource_id": row.get("Resource ID", ""),
        "latest_version": row.get("Latest Version", ""),
        "unique_id": row.get("Unique ID", ""),
    }


def write_search_rows(scored: list[tuple[int, dict[str, str]]], limit: int) -> None:
    fieldnames = ["score", "database_name", "dimension_name", "code", "name"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    for score, row in scored[:limit]:
        writer.writerow(result_record(score, row))


def write_json(payload: object) -> None:
    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


def exact_code_matches(code: str, database: str | None = None) -> list[dict[str, str]]:
    wanted = code.casefold()
    lookup_database = indicator_lookup_database(database)
    rows = load_catalog_variables(indicator_paths_for_database(database)) if database else load_catalog_variables()
    matches = [row for row in rows if row_code(row).casefold() == wanted]
    if lookup_database:
        matches = [row for row in matches if row.get("database_name") == lookup_database]
    if database:
        matches = [materialize_database(row, database) for row in matches]
    return matches


def exact_database_matches(database: str) -> list[dict[str, str]]:
    wanted = database.casefold()
    return [row for row in all_datasets() if row.get("database", "").casefold() == wanted]


def classify_database(database: str) -> dict[str, object]:
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


def search_summary(records: list[dict[str, object]], status: str | None = None, note: str | None = None) -> dict[str, object]:
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


def route_explanation(query: str, database: str | None = None) -> dict[str, object]:
    return route_query(query, database)


def has_variant_marker(record: dict[str, object]) -> bool:
    name = norm(str(record.get("name", "")))
    return any(term in name for term in VARIANT_TERMS)


def resolve_status(scored: list[tuple[int, dict[str, str]]], query: str) -> tuple[str, str]:
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


def cmd_latest_weo(_args: argparse.Namespace) -> None:
    row = latest_weo_dataset()
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["database", "name", "Agency ID", "Resource ID", "Latest Version", "Unique ID"],
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerow(row)


def cmd_datasets(args: argparse.Namespace) -> None:
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
    payload = route_explanation(args.query, args.database)
    if args.json:
        write_json(payload)
        return
    print(f"status: {payload['status']}")
    print(f"database: {payload['database'] or ''}")
    print(f"reason: {payload['reason']}")
    print(f"next_step: {payload['next_step']}")


def cmd_code(args: argparse.Namespace) -> None:
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
    payload = classify_database(args.database)
    if args.json:
        write_json(payload)
        return
    print(f"status: {payload['status']}")
    print(f"database: {payload['database']}")
    print(f"classification: {payload['classification'] or ''}")
    print(f"notes: {payload['notes']}")


def cmd_compare_codes(args: argparse.Namespace) -> None:
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

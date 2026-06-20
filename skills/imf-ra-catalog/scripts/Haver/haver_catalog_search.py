#!/usr/bin/env python3
"""Search packaged Haver indicator metadata from haver.db."""

from __future__ import annotations

import argparse
import csv
import os
import re
import sqlite3
import sys
from pathlib import Path
from typing import Iterable


def _resolve_haver_db() -> Path:
    """Locate haver.db across environments (Windows/macOS/Linux/cloud).

    Resolution order: HAVER_DB_PATH env var, then an upward search for haver.db
    beside any ancestor directory (covers the conventional placement one level
    above the repo root and mirrored skills dirs), then a fallback path so a
    clear error can surface if it is found nowhere.

    Common locations:  macOS  ~/haver.db   Windows  Q:\\DATA\\SPRAI\\...\\haver.db
    """
    env = os.environ.get("HAVER_DB_PATH")
    if env:
        return Path(env).expanduser()
    here = Path(__file__).resolve()
    for parent in here.parents:
        candidate = parent / "haver.db"
        if candidate.exists():
            return candidate
    return here.parents[2] / "haver.db"


DEFAULT_DB_PATH = _resolve_haver_db()

QUERY_SYNONYMS = {
    "ca": ["current", "account"],
    "cab": ["current", "account", "balance"],
    "claims": ["claim", "jobless", "unemployment"],
    "cpi": ["consumer", "price", "prices"],
    "exports": ["export"],
    "fed": ["federal", "reserve"],
    "gdp": ["gross", "domestic", "product"],
    "imports": ["import"],
    "inflation": ["consumer", "prices"],
    "jobless": ["unemployment", "claims"],
    "m2": ["money", "supply"],
    "pce": ["personal", "consumption", "expenditures"],
    "ppi": ["producer", "price", "prices"],
    "rate": ["rates"],
    "rates": ["rate"],
    "treasury": ["government", "bond", "yield"],
    "unemployment": ["jobless"],
    "us": ["united", "states"],
    "usa": ["united", "states", "us"],
    "yield": ["yields", "rate"],
    "yields": ["yield", "rates"],
}

FREQUENCY_TERMS = {
    "a": {"annual", "yearly", "year"},
    "q": {"quarterly", "quarter"},
    "m": {"monthly", "month"},
    "w": {"weekly", "week"},
    "d": {"daily", "day"},
}

HAVER_DATABASE_NOTES = {
    "EMERGE": "Emerging Markets Country Summary",
    "USECON": "United States broad macro summary",
    "WEEKLY": "United States weekly macro and financial indicators",
}

SEARCH_STOP_TERMS = {
    "annual",
    "daily",
    "database",
    "db",
    "haver",
    "month",
    "monthly",
    "quarter",
    "quarterly",
    "states",
    "united",
    "us",
    "usa",
    "week",
    "weekly",
    "year",
    "yearly",
    "emerge",
    "emerging",
    "usecon",
}


def db_path() -> Path:
    return DEFAULT_DB_PATH


def norm(text: str | None) -> str:
    return re.sub(r"[^a-z0-9]+", " ", (text or "").casefold()).strip()


def tokens(text: str | None) -> list[str]:
    base = [token for token in norm(text).split() if token]
    expanded = list(base)
    for token in base:
        expanded.extend(QUERY_SYNONYMS.get(token, []))
    return expanded


def search_terms(text: str | None) -> list[str]:
    return [token for token in norm(text).split() if token and token not in SEARCH_STOP_TERMS]


def csv_safe(value: object) -> str:
    return "" if value is None else str(value)


def haver_database_name(database: str | None) -> str:
    return f"HAVER:{(database or '').upper()}"


def coverage(startdate: str | None, enddate: str | None) -> str:
    return f"{csv_safe(startdate)[:10]} - {csv_safe(enddate)[:10]}"


def open_db(path: Path | None = None) -> sqlite3.Connection:
    path = path or db_path()
    if not path.exists():
        raise FileNotFoundError(f"Haver SQLite database not found: {path}")
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn


def fts_query(user_query: str) -> str:
    """
    Convert a plain-English query to a conservative FTS5 MATCH expression.

    Keeps quoted phrases intact and adds prefix matching for ordinary tokens.
    """
    raw_tokens: list[str] = []
    buf: list[str] = []
    in_quote = False
    for ch in user_query.strip():
        if ch == '"':
            in_quote = not in_quote
            buf.append(ch)
        elif ch.isspace() and not in_quote:
            if buf:
                raw_tokens.append("".join(buf))
                buf = []
        else:
            buf.append(ch)
    if buf:
        raw_tokens.append("".join(buf))

    parts: list[str] = []
    for token in raw_tokens:
        if token.startswith('"') and token.endswith('"') and len(token) > 2:
            parts.append(token)
            continue
        clean = "".join(ch for ch in token if ch.isalnum() or ch == "_")
        if clean and clean.casefold() not in SEARCH_STOP_TERMS:
            # Pure numbers (e.g. "2", "10") must not use prefix matching:
            # "2*" would match "20", "25", etc. and confuse tenor lookups.
            parts.append(clean if clean.isdigit() else f"{clean}*")
    return " AND ".join(parts) if parts else user_query


def fts_or_query(user_query: str) -> str:
    parts = []
    for token in tokens(" ".join(search_terms(user_query))):
        clean = "".join(ch for ch in token if ch.isalnum() or ch == "_")
        if clean and clean.casefold() not in SEARCH_STOP_TERMS:
            parts.append(f"{clean}*")
    return " OR ".join(dict.fromkeys(parts))


def requested_frequency(query: str) -> set[str]:
    query_tokens = set(norm(query).split())
    requested: set[str] = set()
    for freq, aliases in FREQUENCY_TERMS.items():
        if query_tokens & aliases:
            requested.add(freq)
    return requested


def database_hint_score(database: str, query: str) -> int:
    q_tokens = set(norm(query).split())
    database = database.upper()
    score = 0
    if database.lower() in q_tokens or database in q_tokens:
        score += 30
    if database == "WEEKLY" and ({"weekly", "week", "claims", "mortgage", "money", "m2"} & q_tokens):
        score += 18
    if database == "USECON" and ({"us", "usa", "united", "states", "gdp", "cpi", "pce", "payroll"} & q_tokens):
        score += 14
    if database == "EMERGE" and (
        {"emerging", "emerge", "brazil", "china", "india", "turkey", "turkiye", "mexico"} & q_tokens
    ):
        score += 18
    return score


def score_indicator(row: sqlite3.Row, query: str) -> int:
    q = norm(query)
    exact_tokens = set(norm(query).split())
    q_tokens = tokens(query)
    code = norm(row["code"])
    descriptor = norm(row["descriptor"])
    database = csv_safe(row["database"]).upper()
    frequency = norm(row["frequency"])

    score = database_hint_score(database, query)
    if q == code:
        score += 150
    if q == descriptor:
        score += 110
    if code and q in code:
        score += 80
    if q and q in descriptor:
        score += 70
    score += sum(16 for token in q_tokens if token == code)
    score += sum(12 for token in exact_tokens if token in descriptor)
    score += sum(7 for token in q_tokens if token in descriptor)
    if q_tokens and all(token in descriptor or token in code for token in set(q_tokens[:8])):
        score += 25

    requested_freqs = requested_frequency(query)
    if requested_freqs and frequency in requested_freqs:
        score += 18
    elif requested_freqs and frequency:
        score -= 10

    if {"current", "account"}.issubset(exact_tokens) and "current account" in descriptor:
        score += 30
    if "gdp" in exact_tokens and "gross domestic product" in descriptor:
        score += 25
    if "inflation" in exact_tokens and ("consumer price" in descriptor or "cpi" in code):
        score += 28
    if {"unemployment", "rate"}.issubset(exact_tokens) and "unemployment rate" in descriptor:
        score += 35
        if descriptor.startswith("civilian unemployment rate") and ("16 yr" in descriptor or "16 years" in descriptor):
            score += 40
    if "claims" in exact_tokens and "claim" in descriptor:
        score += 30
    if "yield" in exact_tokens and ("yield" in descriptor or "treasury" in descriptor):
        score += 22

    # Tenor-aware scoring: boost exact tenor match, penalise mismatches.
    tenor_m = re.search(r"\b(\d+)\b", q)
    if tenor_m and re.search(r"\b\d+\b", descriptor):
        queried = tenor_m.group(1)
        if re.search(rf"\b{queried}\b", descriptor):
            score += 35
        else:
            score -= 25
    if len(code) <= 3 and q_tokens:
        score += 8
    if "(sa" in descriptor:
        score += 4

    score -= max(0, len(descriptor.split()) - 18) // 2
    return score


def like_where_clause(columns: Iterable[str], query: str, require_all: bool = True) -> tuple[str, list[str]]:
    query_tokens = [token for token in tokens(" ".join(search_terms(query))) if len(token) > 1]
    if not query_tokens:
        return "1 = 1", []
    clauses: list[str] = []
    params: list[str] = []
    cols = list(columns)
    for token in query_tokens[:8]:
        per_token = " OR ".join(f"lower({col}) LIKE ?" for col in cols)
        clauses.append(f"({per_token})")
        params.extend([f"%{token}%"] * len(cols))
    return (" AND " if require_all else " OR ").join(clauses), params


def fetch_candidates(conn: sqlite3.Connection, query: str, database: str | None, limit: int) -> list[sqlite3.Row]:
    def run_fts(match_expr: str) -> list[sqlite3.Row]:
        params: list[object] = [match_expr]
        sql = """
        SELECT i.rowid, i.database, i.code, i.descriptor, i.frequency,
               i.startdate, i.enddate, i.shortsource, i.longsource,
               i.aggtype, i.datatype
        FROM indicators_fts
        JOIN indicators i ON i.rowid = indicators_fts.rowid
        WHERE indicators_fts MATCH ?
        """
        if database:
            db_filter = database.upper()
            if db_filter.startswith("HAVER:"):
                db_filter = db_filter[6:]
            sql += " AND upper(i.database) = ?"
            params.append(db_filter)
        sql += " ORDER BY bm25(indicators_fts) LIMIT ?"
        params.append(max(limit * 100, 1000))
        return list(conn.execute(sql, params))

    def run_like(require_all: bool) -> list[sqlite3.Row]:
        where, like_params = like_where_clause(("code", "descriptor", "database"), query, require_all=require_all)
        sql = f"""
                SELECT rowid, database, code, descriptor, frequency,
                       startdate, enddate, shortsource, longsource,
                       aggtype, datatype
                FROM indicators
                WHERE {where}
            """
        params = list(like_params)
        if database:
            db_filter = database.upper()
            if db_filter.startswith("HAVER:"):
                db_filter = db_filter[6:]
            sql += " AND upper(database) = ?"
            params.append(db_filter)
        sql += " LIMIT ?"
        params.append(max(limit * 100, 1000))
        return list(conn.execute(sql, params))

    def dedupe(rows: list[sqlite3.Row]) -> list[sqlite3.Row]:
        seen: set[int] = set()
        unique: list[sqlite3.Row] = []
        for row in rows:
            rowid = int(row["rowid"])
            if rowid not in seen:
                seen.add(rowid)
                unique.append(row)
        return unique

    try:
        rows = run_fts(fts_query(query))
        if rows:
            return dedupe(rows)
        or_query = fts_or_query(query)
        if or_query:
            rows = run_fts(or_query)
            if rows:
                return dedupe(rows)
    except sqlite3.OperationalError:
        pass

    for require_all in (True, False):
        rows = run_like(require_all=require_all)
        if rows:
            return rows
    return []


def search_indicators(query: str, database: str | None = None, limit: int = 20) -> list[dict[str, object]]:
    with open_db() as conn:
        rows = fetch_candidates(conn, query, database, limit)

    scored = [(score_indicator(row, query), row) for row in rows]
    scored = [(score, row) for score, row in scored if score > 0]
    scored.sort(
        key=lambda item: (
            -item[0],
            csv_safe(item[1]["database"]).upper(),
            csv_safe(item[1]["frequency"]),
            csv_safe(item[1]["code"]),
        )
    )
    return [format_result(score, row) for score, row in scored[:limit]]


def format_result(score: int, row: sqlite3.Row) -> dict[str, object]:
    return {
        "score": score,
        "database_name": haver_database_name(row["database"]),
        "dimension_name": "N/A",
        "code": csv_safe(row["code"]),
        "name": csv_safe(row["descriptor"]),
        "frequency": csv_safe(row["frequency"]),
        "aggtype": csv_safe(row["aggtype"]),
        "datatype": csv_safe(row["datatype"]),
        "coverage": coverage(row["startdate"], row["enddate"]),
        "source": csv_safe(row["shortsource"]),
    }


def write_rows(rows: list[dict[str, object]]) -> None:
    fieldnames = ["score", "database_name", "dimension_name", "code", "name", "frequency", "aggtype", "datatype", "coverage", "source"]
    writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)


def cmd_search(args: argparse.Namespace) -> None:
    databases = args.databases if args.databases else ([args.database] if args.database else [None])
    for db in databases:
        write_rows(search_indicators(args.query, database=db, limit=args.limit))


def cmd_code(args: argparse.Namespace) -> None:
    sql = """
        SELECT database, code, descriptor, frequency, startdate, enddate, shortsource, longsource,
               aggtype, datatype
        FROM indicators
        WHERE lower(code) = lower(?)
    """
    params: list[object] = [args.code]
    if args.database:
        db_filter = args.database.upper()
        if db_filter.startswith("HAVER:"):
            db_filter = db_filter[6:]
        sql += " AND upper(database) = ?"
        params.append(db_filter)
    sql += " ORDER BY database, code"

    with open_db() as conn:
        rows = list(conn.execute(sql, params))
    write_rows([format_result(999, row) for row in rows])


def cmd_databases(_args: argparse.Namespace) -> None:
    with open_db() as conn:
        rows = list(
            conn.execute(
                """
                SELECT database, series_count, earliest_start, latest_end, distinct_frequencies
                FROM database_summary
                ORDER BY upper(database)
                """
            )
        )
    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["database_name", "description", "series_count", "earliest_start", "latest_end", "frequencies"],
    )
    writer.writeheader()
    for row in rows:
        db = csv_safe(row["database"]).upper()
        writer.writerow(
            {
                "database_name": haver_database_name(db),
                "description": HAVER_DATABASE_NOTES.get(db, ""),
                "series_count": row["series_count"],
                "earliest_start": row["earliest_start"],
                "latest_end": row["latest_end"],
                "frequencies": row["distinct_frequencies"],
            }
        )


def cmd_info(_args: argparse.Namespace) -> None:
    with open_db() as conn:
        rows = list(conn.execute("SELECT key, value FROM meta ORDER BY key"))
    writer = csv.DictWriter(sys.stdout, fieldnames=["key", "value"])
    writer.writeheader()
    writer.writerows(dict(row) for row in rows)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("search", help="Search Haver indicators by plain-English keywords")
    p.add_argument("query")
    p.add_argument("--database", "--db", dest="database", help="Filter to a single Haver DB code, e.g. USECON")
    p.add_argument("--databases", "--dbs", dest="databases", nargs="+", metavar="DB",
                   help="Filter to multiple Haver DB codes in one call, e.g. --databases EMERGE EMERGELA EMERGEPR")
    p.add_argument("--limit", type=int, default=20)
    p.set_defaults(func=cmd_search)

    p = sub.add_parser("code", help="Look up an exact Haver indicator code")
    p.add_argument("code")
    p.add_argument("--database", "--db", dest="database", help="Filter to a Haver DB code, e.g. WEEKLY")
    p.set_defaults(func=cmd_code)

    p = sub.add_parser("databases", help="List packaged Haver databases")
    p.set_defaults(func=cmd_databases)

    p = sub.add_parser("info", help="Show SQLite build metadata")
    p.set_defaults(func=cmd_info)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        args.func(args)
    except FileNotFoundError as exc:
        print(f"[error] {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

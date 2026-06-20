"""Data paths, constants, and CSV loading for IMF catalog lookups."""

from __future__ import annotations

import csv
import re
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


def load_datasets(include_vintage: bool = False, vintage_only: bool = False) -> list[dict[str, str]]:
    """
    [Intent]
    Loads the IMF dataset catalog rows used to identify valid database names.

    [When to Use]
    Use before listing datasets, finding WEO vintages, or classifying a database.

    Args:
        include_vintage: Include dated vintage datasets in addition to non-vintage datasets.
        vintage_only: Load only vintage dataset rows.

    Returns:
        Dataset catalog rows as dictionaries.
    """
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
    """
    [Intent]
    Loads indicator/code registry rows from one or more catalog CSVs.

    [When to Use]
    Use before fuzzy indicator search, exact code lookup, dimension discovery, or comparison.

    Args:
        paths: Optional CSV paths. Defaults to all supported indicator registries.

    Returns:
        Indicator catalog rows as dictionaries.
    """
    rows: list[dict[str, str]] = []
    for path in paths or INDICATOR_CSVS:
        rows.extend(load_variable_file(path))
    return rows


def all_datasets() -> list[dict[str, str]]:
    """
    [Intent]
    Loads the complete dataset catalog, including non-vintage and vintage rows.

    [When to Use]
    Use for exact database validation across all known catalog sources.

    Returns:
        All dataset catalog rows.
    """
    return load_datasets(include_vintage=True)


def row_code(row: dict[str, str]) -> str:
    return row.get("Code", "") or row.get("indicator_code", "")


def row_name(row: dict[str, str]) -> str:
    return row.get("Name", "") or row.get("indicator_name", "")


def dataset_record(row: dict[str, str]) -> dict[str, str]:
    return {
        "database": row.get("database", ""),
        "name": row.get("name", ""),
        "agency_id": row.get("Agency ID", ""),
        "resource_id": row.get("Resource ID", ""),
        "latest_version": row.get("Latest Version", ""),
        "unique_id": row.get("Unique ID", ""),
    }

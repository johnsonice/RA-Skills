"""Data sources and reference constants for WEO country-group lookups."""

from __future__ import annotations

import csv
from pathlib import Path


SKILL_DIR = Path(__file__).resolve().parents[1]
DEFAULT_CSV_DIR = SKILL_DIR / "references" / "Country Group" / "csv"
CSV_FILES = {
    "countries": "1. countries.csv",
    "groups": "2. country_groups.csv",
    "composition": "3. country_group_composition.csv",
}

GROUP_ALIASES = {
    "ae": "G110",
    "advanced economies": "G110",
    "em": "G1201",
    "emerging market": "G1201",
    "emerging markets": "G1201",
    "emerging market economies": "G1201",
    "emerging market and middle income economies": "G1201",
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
    "prgt em": "G-PRGT-EM",
    "prgt-em": "G-PRGT-EM",
    "g prgt em": "G-PRGT-EM",
    "g-prgt-em": "G-PRGT-EM",
    "prgt lic": "G-PRGT-LIC",
    "prgt-lic": "G-PRGT-LIC",
    "g prgt lic": "G-PRGT-LIC",
    "g-prgt-lic": "G-PRGT-LIC",
    "cca": "G940",
    "mena": "G406",
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
        "note": "WEO and SPR/PRGT use the same advanced-economies group code in this reference.",
        "groups": [("WEO", "G110"), ("SPR/PRGT", "G110")],
    },
    "advanced economies": {
        "title": "Advanced Economies",
        "note": "WEO and SPR/PRGT use the same advanced-economies group code in this reference.",
        "groups": [("WEO", "G110"), ("SPR/PRGT", "G110")],
    },
    "em": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G1201"), ("SPR/PRGT", "G-PRGT-EM")],
    },
    "emerging markets": {
        "title": "Emerging Market / Middle-Income Economies",
        "note": "EM coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G1201"), ("SPR/PRGT", "G-PRGT-EM")],
    },
    "lic": {
        "title": "Low-Income Countries",
        "note": "LIC coverage differs between WEO and SPR/PRGT. Clarify the framework before committing to a group.",
        "groups": [("WEO", "G201"), ("SPR/PRGT", "G-PRGT-LIC")],
    },
    "lidc": {
        "title": "Low-Income Developing Countries",
        "note": "LIDC usually maps to WEO G201 in this reference. PRGT LIC uses G-PRGT-LIC and has different coverage.",
        "groups": [("WEO", "G201"), ("SPR/PRGT", "G-PRGT-LIC")],
    },
    "emde": {
        "title": "Emerging Market and Developing Economies",
        "note": "WEO EMDE maps to G200. In this reference EMDE is broader than WEO EM alone.",
        "groups": [("WEO", "G200")],
    },
    "emdes": {
        "title": "Emerging Market and Developing Economies",
        "note": "WEO EMDE maps to G200. In this reference EMDE is broader than WEO EM alone.",
        "groups": [("WEO", "G200")],
    },
}


class CsvTables:
    """CSV-backed table reader for WEO country, group, and composition references.

    [Intent]
    Centralizes access to the three source-of-truth CSV files used by the lookup
    helpers.

    [When to Use]
    Use this before resolving countries, groups, memberships, or group expansion.
    """

    def __init__(self, csv_dir: Path) -> None:
        self.csv_dir = csv_dir

    def rows(self, table_name: str) -> list[dict[str, str]]:
        """Read one registered WEO reference table as dictionaries.

        Args:
            table_name: One of "countries", "groups", or "composition".

        Returns:
            CSV rows keyed by header name.

        Raises:
            FileNotFoundError: If the expected CSV file is missing.
            UnicodeDecodeError: If no supported encoding can read the file.
        """
        csv_path = self.csv_dir / CSV_FILES[table_name]
        if not csv_path.exists():
            raise FileNotFoundError(f"Missing WEO country-group CSV: {csv_path}")
        for encoding in ("utf-8-sig", "cp1252"):
            try:
                with csv_path.open(newline="", encoding=encoding) as f:
                    return list(csv.DictReader(f))
            except UnicodeDecodeError:
                continue
        raise UnicodeDecodeError("utf-8-sig", b"", 0, 1, f"Could not decode {csv_path}")

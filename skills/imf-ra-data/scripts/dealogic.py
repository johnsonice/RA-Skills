#!/usr/bin/env python3
"""Build, search, and safely verify Dealogic SQL metadata and preview queries.

The canonical metadata is extracted from the Dealogic feed data dictionary.
Runtime database access is read-only and limited to explicit metadata inspection
or user-confirmed SELECT/CTE preview queries capped at TOP (20).
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import zipfile
from collections import Counter, deque
from pathlib import Path
from xml.etree import ElementTree as ET


SCRIPT_DIR = Path(__file__).resolve().parent
REFERENCE_DIR = SCRIPT_DIR.parent / "references" / "Dealogic"
SCHEMA_PATH = REFERENCE_DIR / "dealogic_schema.csv"
RELATIONSHIPS_PATH = REFERENCE_DIR / "dealogic_relationships.csv"
MANIFEST_PATH = REFERENCE_DIR / "dealogic_source_manifest.json"

XML_MAIN = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
XML_REL = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS = {"m": XML_MAIN, "r": XML_REL}

NON_SCHEMA_SHEETS = {"Table Content", "FEED CONTENT", "DATA TYPES"}
PREVIEW_LIMIT = 20
DEFAULT_QUERY_TIMEOUT = 20

# Live SQL metadata can differ from the supplied feed dictionary's loader
# mapping. Keep verified exceptions here so catalog rebuilds preserve the
# deployed schema rather than reintroducing known-invalid column names.
LIVE_SCHEMA_FIELD_OVERRIDES: dict[tuple[str, str, str], dict[str, str]] = {
    ("DCM", "ISIN", "ISIN"): {
        "physical_columns": "ISIN",
        "confidence": "database_verified",
        "notes": (
            "Live SQL metadata verified in July 2026: "
            "DCMDealTranchesISINs stores the identifier in ISIN, not "
            "SecurityNumber."
        ),
    },
}

# Explicit targets cover naming differences that cannot be resolved reliably
# from the workbook text alone. Values are loader table names.
REFERENCE_TARGET_TABLES = {
    ("COMPANY", "SIGId"): "CompanySIG",
    ("COMPANY", "Code", "CompanyNAICSCodes"): "CompanyNAICSCode",
    ("COMPANY", "Code", "CompanySICCodes"): "CompanySICCode",
    ("DCM", "LocalIssueTypeId"): "DCMLocalIssueType",
    ("DCM", "MTNProgrammeTypeId"): "DCMMTNProgramType",
    ("DCM", "BasisId"): "DCMBasis",
    ("DCM", "BearerRegisteredId"): "BearerType",
    ("DCM", "CollateralTypeId"): "DCMCollateralType",
    ("DCM", "IssueTypeId"): "DCMIssueType",
    ("DCM", "MarketSubTypeId"): "DCMMarketSubType",
    ("DCM", "SecurityTypeId"): "DCMSecurityType",
    ("DCM", "NationalityISOCode"): "Country",
    ("ECM", "CanadianIncomeTrustId"): "ECMCIT",
    ("ECM", "RevisionDirectionId"): "ECMRevisionDirection",
    ("ECM", "ShelfTypeId"): "ECMShelfType",
    ("ECM", "TypeId"): "ECMDealType",
    ("ECM", "WithdrawnPostponedId"): "ECMWithdrawn",
    ("ECM", "ATMBasisId"): "ECMATMBasis",
    ("ECM", "BearerRegisteredId"): "BearerType",
    ("ECM", "ConvertibleRankId"): "ECMConvertibleRank",
    ("ECM", "MarketSubTypeId"): "ECMMarketSubType",
    ("ECM", "OfferTypeId"): "ECMOfferType",
    ("ECM", "PriceRangeId"): "ECMPriceRange",
    ("ECM", "SecurityTypeId"): "ECMSecurityType",
    ("ECM", "SubTypeId"): "ECMSubType",
    ("ECM", "AttorneyRoleId"): "ECMAttorneyRole",
    ("ECMSHARE", "PricePeriodId"): "ECMPricePeriod",
    ("LOAN", "TypeId"): "LoanDealType",
    ("LOAN", "MarketTypeId"): "LoanMarketType",
    ("LOAN", "PrimaryInstrumentTypeId"): "LoanInstrumentType",
    ("LOAN", "InstrumentTypeId"): "LoanInstrumentType",
    ("LOAN", "RoleId"): "LoanCompanyRole",
    ("LOAN", "StatusId"): "DealStatus",
    ("MNA", "AcquirorPublicStatusId"): "CompanyPublicStatus",
    ("MNA", "FinalBoardAttitudeId"): "MNABoardAttitude",
    ("MNA", "InitialBoardAttitudeId"): "MNABoardAttitude",
    ("MNA", "TypeId"): "MNADealType",
    ("MNA", "AcquisitionMethodId"): "MNAAcquisitionMethod",
    ("MNA", "AdvisorRoleId"): "MNAAdvisorRole",
    ("MNA", "CompanyRoleId"): "MNACompanyRole",
    ("MNA", "SIGId"): "CompanySIG",
    ("MNA", "ConsiderationId"): "MNADealConisderationType",
    ("MNA", "DefenseTechiqueId"): "MNADefenseTechniques",
    ("MNA", "Code", "MNADealCompaniesPreDealSICCodes"): "CompanySICCode",
    ("REFERENCE_FILES", "IndustrySectorId"): "CompanyIndustrySector",
    ("REFERENCE_FILES", "CountryISOCode"): "Country",
    ("REFERENCE_FILES", "ExchangeCountryId"): "Country",
}

COMPANY_REFERENCE_ELEMENTS = {
    "BankParentId",
    "CompanyParentId",
    "FinancialSponsorParentId",
    "ImmediateParentId",
    "SuccessorCompanyId",
    "IssuerId",
    "OriginatorId",
    "PrincipalPayingAgentId",
    "TrusteeId",
    "FinancialSponsorId",
    "GuarantorId",
    "BankId",
    "UnderlyingAssetId",
    "AttorneyId",
    "VendorId",
    "CompanyId",
    "SponsorId",
    "AdvisorId",
}


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.strip().lower()).strip("_")


def _column_number(cell_ref: str) -> int:
    letters = re.match(r"[A-Z]+", cell_ref)
    if not letters:
        return 0
    value = 0
    for letter in letters.group():
        value = value * 26 + ord(letter) - 64
    return value


def _cell_text(cell: ET.Element, shared: list[str]) -> str:
    kind = cell.attrib.get("t")
    value = cell.find(f"{{{XML_MAIN}}}v")
    inline = cell.find(f"{{{XML_MAIN}}}is")
    if kind == "s" and value is not None:
        return shared[int(value.text or "0")]
    if kind == "inlineStr" and inline is not None:
        return "".join(node.text or "" for node in inline.iter(f"{{{XML_MAIN}}}t"))
    return value.text if value is not None and value.text is not None else ""


def _read_xlsx_rows(path: Path) -> tuple[list[tuple[str, dict[int, dict[int, str]]]], dict[str, str]]:
    with zipfile.ZipFile(path) as archive:
        shared_root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
        shared = [
            "".join(node.text or "" for node in item.iter(f"{{{XML_MAIN}}}t"))
            for item in shared_root.findall(f"{{{XML_MAIN}}}si")
        ]
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rel_root = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        relationships = {item.attrib["Id"]: item.attrib["Target"] for item in rel_root}

        sheets: list[tuple[str, dict[int, dict[int, str]]]] = []
        sheet_nodes = workbook.find(f"{{{XML_MAIN}}}sheets")
        for sheet in sheet_nodes if sheet_nodes is not None else []:
            name = sheet.attrib["name"]
            rel_id = sheet.attrib[f"{{{XML_REL}}}id"]
            target = relationships[rel_id].lstrip("/")
            if not target.startswith("xl/"):
                target = f"xl/{target}"
            root = ET.fromstring(archive.read(target))
            rows: dict[int, dict[int, str]] = {}
            for cell in root.findall(f".//{{{XML_MAIN}}}c"):
                ref = cell.attrib.get("r", "")
                row_match = re.search(r"\d+", ref)
                if not row_match:
                    continue
                row_number = int(row_match.group())
                rows.setdefault(row_number, {})[_column_number(ref)] = _cell_text(cell, shared)
            sheets.append((name, rows))

        properties: dict[str, str] = {}
        if "docProps/core.xml" in archive.namelist():
            core = ET.fromstring(archive.read("docProps/core.xml"))
            for node in core:
                properties[node.tag.split("}")[-1]] = node.text or ""
        return sheets, properties


def _normalize_type(raw: str) -> tuple[str, str, str]:
    compact = re.sub(r"\s+", "", raw or "")
    upper = compact.upper()
    length = ""
    scale = ""
    match = re.fullmatch(r"STRING\((\d+|MAX)\)", upper)
    if match:
        length = match.group(1)
        return ("string" if length != "MAX" else "text", length, scale)
    match = re.fullmatch(r"DECIMAL\((\d+)\)", upper)
    if match:
        scale = match.group(1)
        return "decimal", length, scale
    if upper.startswith("MONEY"):
        match = re.search(r"\(([^)]+)\)", upper)
        scale = match.group(1) if match else ""
        return "money", length, scale
    return {
        "INT": "integer",
        "ID": "identifier",
        "BOOL": "boolean",
        "DATETIME": "datetime",
        "DATE": "date",
        "DECIMAL": "decimal",
        "FLOAT": "float",
        "TEXT": "text",
        "EXCHANGERATE": "exchange_rate",
        "COLLECTION": "collection",
        "COMPLEX": "complex",
        "STRING": "string",
    }.get(upper, "unknown"), length, scale


def _clean_columns(value: str) -> str:
    cleaned = value.replace("_x000D_", "\n").replace("\r", "\n")
    parts = [part.strip() for part in cleaned.splitlines() if part.strip()]
    return ";".join(dict.fromkeys(parts))


def _record_name(value: str) -> str:
    match = re.search(r"Record:\s*(?:Record:\s*)?([^\[]+)", value, re.IGNORECASE)
    return match.group(1).strip() if match else value.strip()


def _record_path(value: str) -> str:
    paths = re.findall(r"\[\s*([^\]]+?)\s*\]", value)
    return paths[-1].strip() if paths else ""


def _domain_from_sheet(sheet_name: str) -> str:
    return sheet_name.replace("_nn.xml", "").replace(".xml", "").upper()


def _primary_table(fields: list[dict[str, str]]) -> str:
    candidates = [
        field["physical_table"]
        for field in fields
        if field["physical_table"] and field["logical_type"] != "collection"
    ]
    return Counter(candidates).most_common(1)[0][0] if candidates else ""


def _make_grain(record_name: str, keys: list[str], domain: str) -> str:
    key_text = " and ".join(keys) if keys else "an undocumented key"
    return f"One row per {domain} {record_name}, identified by {key_text}."


def _reference_target_columns(field: dict[str, str], target: dict[str, str]) -> str:
    element = field["element_name"].lower()
    available = {
        item["element_name"].lower(): item["physical_columns"]
        for item in target["fields"]  # type: ignore[index]
    }
    if element.endswith("isocode") and "isocode" in available:
        return available["isocode"]
    if element == "code" and "code" in available:
        return available["code"]
    keys = target["primary_key"]  # type: ignore[assignment]
    return ";".join(keys)


def _reference_match(
    field: dict[str, str], candidate_entities: list[dict[str, str]]
) -> tuple[str, str]:
    if field["is_reference"] != "true":
        return "", ""
    explicit_table = REFERENCE_TARGET_TABLES.get(
        (field["domain"], field["element_name"], field["physical_table"])
    ) or REFERENCE_TARGET_TABLES.get((field["domain"], field["element_name"]))
    if not explicit_table and field["element_name"] in COMPANY_REFERENCE_ELEMENTS:
        explicit_table = "Company"
    if field["domain"] == "COMPANYSHARE" and field["element_name"] == "Id":
        explicit_table = "Company"
    if field["domain"] == "ECMSHARE" and field["element_name"] == "DealId":
        explicit_table = "ECMDeal"
    if field["element_name"] in {"LBOMNADealId", "MNADealNo"}:
        explicit_table = "MNADeal"
    if explicit_table:
        matches = [
            entity
            for entity in candidate_entities
            if str(entity.get("physical_table", "")).lower() == explicit_table.lower()
        ]
        if len(matches) == 1:
            target = matches[0]
            return str(target["entity_id"]), _reference_target_columns(field, target)

    reference_entities = [
        entity for entity in candidate_entities if entity["domain"] == "REFERENCE_FILES"
    ]
    element_base = re.sub(r"(?:id|no|code)$", "", field["element_name"], flags=re.IGNORECASE)
    haystack = " ".join(
        [field["element_name"], field["business_name"], field["description"]]
    ).lower()
    scored: list[tuple[int, str]] = []
    for entity in reference_entities:
        record = entity["record_name"]
        physical_table = str(entity.get("physical_table", ""))
        normalized_haystack = re.sub(r"[^a-z0-9]", "", haystack)
        score = 0
        for candidate_name, weight in ((physical_table, 7), (record, 5)):
            normalized = re.sub(r"[^a-z0-9]", "", candidate_name.lower())
            if normalized and normalized in normalized_haystack:
                score += weight
        if _slug(record) == _slug(element_base):
            score += 4
        for token in re.findall(r"[a-z0-9]+", record.lower()):
            if len(token) > 3 and token in haystack:
                score += 1
        if score:
            scored.append((score, entity["entity_id"]))
    if not scored:
        return "", ""
    scored.sort(reverse=True)
    if len(scored) > 1 and scored[0][0] == scored[1][0]:
        return "", ""
    target_id = scored[0][1]
    target = next(entity for entity in reference_entities if entity["entity_id"] == target_id)
    return target_id, _reference_target_columns(field, target)


def build_catalog(source: Path, output_dir: Path) -> dict[str, int]:
    sheets, properties = _read_xlsx_rows(source)
    entities: list[dict[str, str]] = []
    fields: list[dict[str, str]] = []

    for sheet_name, rows in sheets:
        if sheet_name in NON_SCHEMA_SHEETS:
            continue
        domain = _domain_from_sheet(sheet_name)
        current: dict[str, object] | None = None
        for row_number, cells in sorted(rows.items()):
            column_b = cells.get(2, "").strip()
            column_c = cells.get(3, "").strip()
            if column_b.lower().startswith("record:"):
                record_name = _record_name(column_b)
                entity_id = f"{domain.lower()}.{_slug(record_name)}"
                current = {
                    "domain": domain,
                    "entity_id": entity_id,
                    "record_name": record_name,
                    "xml_record_path": _record_path(column_b),
                    "primary_key": [],
                    "source_sheet": sheet_name,
                    "source_row": str(row_number),
                    "annotations": [],
                    "fields": [],
                }
                entities.append(current)  # type: ignore[arg-type]
                continue
            if current is None:
                continue
            if column_b.lower().startswith("key(s):"):
                keys = [item.strip() for item in column_b.split(":", 1)[1].split(",") if item.strip()]
                current["primary_key"] = keys
                continue
            annotation = cells.get(8, "")
            if "ParentKeyReference" in annotation:
                current["annotations"].append(annotation)  # type: ignore[union-attr]
            if not column_b or not column_c or column_c == "Type":
                continue
            if not cells.get(7, "") and not cells.get(8, ""):
                continue
            logical_type, max_length, scale = _normalize_type(column_c)
            keys = current["primary_key"]  # type: ignore[assignment]
            is_reference_sheet = domain == "REFERENCE_FILES"
            field = {
                "domain": domain,
                "entity_id": str(current["entity_id"]),
                "record_name": str(current["record_name"]),
                "entity_grain": "",
                "entity_primary_key": ";".join(keys),
                "parent_entity_id": "",
                "element_name": column_b,
                "business_name": cells.get(4, "").strip(),
                "description": cells.get(5, "").strip(),
                "source_type_raw": column_c,
                "logical_type": logical_type,
                "max_length": max_length,
                "scale": scale,
                "xml_path": "" if is_reference_sheet else cells.get(7, "").strip(),
                "physical_table": cells.get(7 if is_reference_sheet else 8, "").strip(),
                "physical_columns": _clean_columns(cells.get(8 if is_reference_sheet else 9, "")),
                "is_key": str(column_b in keys).lower(),
                "is_reference": str(cells.get(6, "").strip().lower() == "reference").lower(),
                "reference_entity_id": "",
                "reference_target_columns": "",
                "is_collection": str(
                    cells.get(6, "").strip().lower() == "collection" or logical_type == "collection"
                ).lower(),
                "confidence": (
                    "database_verified"
                    if (
                        (domain == "DCM" and column_b == "DealId")
                        or (domain == "DCM" and column_b in {"IssuerId", "CommonStatusId"})
                        or (
                            domain == "ECMSHARE"
                            and str(current["record_name"]).strip() == "Tranche"
                            and column_b == "TrancheId"
                        )
                        or (
                            domain == "LOAN"
                            and str(current["record_name"]).strip() == "Tranche"
                            and column_b == "StatusId"
                        )
                    )
                    else "documented"
                ),
                "source_sheet": sheet_name,
                "source_row": str(row_number),
                "search_terms": " | ".join(
                    item for item in [column_b, cells.get(4, "").strip(), cells.get(5, "").strip()] if item
                ),
                "notes": (
                    "Live SQL metadata verified in July 2026: DealId is int NOT NULL; "
                    "DealNo is nullable and observed as NULL. Live index metadata returned "
                    "no index involving either column. Treat DealId as the feed-documented "
                    "logical key, not as a database-enforced unique key."
                    if domain == "DCM" and column_b == "DealId"
                    else (
                        "Live TOP (20) verification in July 2026 confirmed IssuerId "
                        "joins to Company.Id. BrandName was populated for 8 of 20 "
                        "sampled deals; use LEFT JOIN and preserve IssuerId when the "
                        "name is missing."
                        if domain == "DCM" and column_b == "IssuerId"
                        else (
                            "Live TOP (20) verification in July 2026 confirmed "
                            "CommonStatusId joins to DealStatus.Id; all 20 sampled "
                            "rows decoded as Priced."
                            if domain == "DCM" and column_b == "CommonStatusId"
                            else (
                        "Live verification in July 2026 confirmed the composite join "
                        "(ShareECMDealDealId, TrancheId) to "
                        "ECMDealTranches(ECMDealDealId, TrancheId)."
                        if (
                            domain == "ECMSHARE"
                            and str(current["record_name"]).strip() == "Tranche"
                            and column_b == "TrancheId"
                        )
                        else (
                            "Live verification in July 2026 confirmed StatusId values "
                            "2, 3, and 12 decode through DealStatus.Id as Announced, "
                            "Close, and Mandated; they do not join to LoanDealStatus."
                            if (
                                domain == "LOAN"
                                and str(current["record_name"]).strip() == "Tranche"
                                and column_b == "StatusId"
                            )
                            else ""
                        )
                            )
                        )
                    )
                ),
            }
            field.update(
                LIVE_SCHEMA_FIELD_OVERRIDES.get(
                    (domain, str(current["record_name"]).strip(), column_b),
                    {},
                )
            )
            fields.append(field)
            current["fields"].append(field)  # type: ignore[union-attr]

    for entity in entities:
        entity["physical_table"] = _primary_table(entity["fields"])  # type: ignore[arg-type]

    duplicate_ids = Counter(str(entity["entity_id"]) for entity in entities)
    for entity in entities:
        entity_id = str(entity["entity_id"])
        if duplicate_ids[entity_id] > 1:
            suffix = _slug(str(entity["physical_table"])) or str(entity["source_row"])
            entity["entity_id"] = f"{entity_id}.{suffix}"
            for field in entity["fields"]:  # type: ignore[union-attr]
                field["entity_id"] = str(entity["entity_id"])

    for entity in entities:
        path = str(entity["xml_record_path"]).rstrip("/")
        parent_candidates = [
            other
            for other in entities
            if other is not entity
            and other["domain"] == entity["domain"]
            and path.startswith(str(other["xml_record_path"]).rstrip("/") + "/")
        ]
        parent = max(parent_candidates, key=lambda item: len(str(item["xml_record_path"])), default=None)
        entity["parent_entity_id"] = str(parent["entity_id"]) if parent else ""
        entity["grain"] = _make_grain(
            str(entity["record_name"]),
            entity["primary_key"],  # type: ignore[arg-type]
            str(entity["domain"]),
        )
        for field in entity["fields"]:  # type: ignore[union-attr]
            field["parent_entity_id"] = str(entity["parent_entity_id"])
            field["entity_grain"] = str(entity["grain"])

    for field in fields:
        target_id, target_columns = _reference_match(field, entities)
        field["reference_entity_id"] = target_id
        field["reference_target_columns"] = target_columns

    relationships: list[dict[str, str]] = []
    entities_by_id = {str(entity["entity_id"]): entity for entity in entities}
    for entity in entities:
        parent_id = str(entity["parent_entity_id"])
        if not parent_id:
            continue
        parent = entities_by_id[parent_id]
        annotations = "\n".join(entity["annotations"])  # type: ignore[arg-type]
        pairs = re.findall(
            r'ParentKeyReference\s+ColumnName="([^"]+)"\s+ParentColumnName="([^"]+)"',
            annotations,
        )
        if pairs:
            from_columns = ";".join(pair[0] for pair in pairs)
            to_columns = ";".join(pair[1] for pair in pairs)
            confidence = "documented"
        else:
            parent_keys = parent["primary_key"]  # type: ignore[assignment]
            child_keys = entity["primary_key"]  # type: ignore[assignment]
            common = [key for key in parent_keys if key in child_keys]
            from_columns = ";".join(common)
            to_columns = ";".join(common)
            confidence = "derived"
        relationships.append(
            {
                "relationship_id": f"parent.{entity['entity_id']}.{parent_id}",
                "from_entity_id": str(entity["entity_id"]),
                "from_table": str(entity["physical_table"]),
                "from_columns": from_columns,
                "to_entity_id": parent_id,
                "to_table": str(parent["physical_table"]),
                "to_columns": to_columns,
                "relationship_type": "parent",
                "cardinality": "many-to-one",
                "confidence": confidence,
                "source": str(entity["source_sheet"]),
                "notes": "Derived from XML hierarchy and documented parent-key annotations.",
            }
        )

    seen_reference_relationships: set[tuple[str, str, str]] = set()
    for field in fields:
        target_id = field["reference_entity_id"]
        columns = field["physical_columns"]
        if not target_id or not columns or ";" in columns:
            continue
        key = (field["physical_table"], columns, target_id)
        if key in seen_reference_relationships:
            continue
        seen_reference_relationships.add(key)
        target = entities_by_id[target_id]
        relationships.append(
            {
                "relationship_id": f"reference.{field['entity_id']}.{_slug(field['element_name'])}",
                "from_entity_id": field["entity_id"],
                "from_table": field["physical_table"],
                "from_columns": columns,
                "to_entity_id": target_id,
                "to_table": str(target["physical_table"]),
                "to_columns": field["reference_target_columns"],
                "relationship_type": "reference",
                "cardinality": "many-to-one",
                "confidence": (
                    "database_verified"
                    if field["confidence"] == "database_verified"
                    else "derived"
                ),
                "source": f"{field['source_sheet']}:{field['source_row']}",
                "notes": (
                    field["notes"]
                    if field["confidence"] == "database_verified"
                    else "Reference target inferred from the field name and business description; verify against the live database."
                ),
            }
        )

    relationships.append(
        {
            "relationship_id": "live.ecmshare.tranche.ecm.tranche",
            "from_entity_id": "ecmshare.tranche",
            "from_table": "ShareECMDealTranches",
            "from_columns": "ShareECMDealDealId;TrancheId",
            "to_entity_id": "ecm.tranche",
            "to_table": "ECMDealTranches",
            "to_columns": "ECMDealDealId;TrancheId",
            "relationship_type": "association",
            "cardinality": "one-to-one logical",
            "confidence": "database_verified",
            "source": "Live TOP (20) verification, July 2026",
            "notes": "All 20 sampled composite keys matched exactly; uniqueness is logical rather than database-enforced.",
        }
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    schema_fields = list(fields[0]) if fields else []
    with (output_dir / SCHEMA_PATH.name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=schema_fields)
        writer.writeheader()
        writer.writerows(fields)
    relationship_fields = list(relationships[0]) if relationships else []
    with (output_dir / RELATIONSHIPS_PATH.name).open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=relationship_fields)
        writer.writeheader()
        writer.writerows(relationships)

    digest = hashlib.sha256(source.read_bytes()).hexdigest()
    manifest = {
        "source_filename": source.name,
        "source_sha256": digest,
        "source_created": properties.get("created", ""),
        "source_modified": properties.get("modified", ""),
        "generator": "skills/imf-ra-data/scripts/dealogic.py build",
        "schema_rows": len(fields),
        "relationship_rows": len(relationships),
        "domains": sorted({field["domain"] for field in fields}),
    }
    (output_dir / MANIFEST_PATH.name).write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )
    return {"schema_rows": len(fields), "relationship_rows": len(relationships)}


def _read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Catalog file not found: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def _tokens(query: str) -> list[str]:
    return [token for token in re.findall(r"[a-z0-9]+", query.lower()) if len(token) > 1]


def search_catalog(query: str, domain: str | None, limit: int) -> list[dict[str, object]]:
    query_tokens = _tokens(query)
    results: list[tuple[int, dict[str, str]]] = []
    for row in _read_csv(SCHEMA_PATH):
        if domain and row["domain"].lower() != domain.lower():
            continue
        searchable = " ".join(
            [
                row["element_name"],
                row["business_name"],
                row["description"],
                row["physical_table"],
                row["physical_columns"],
                row["record_name"],
                row["search_terms"],
            ]
        ).lower()
        score = sum(3 if token in row["business_name"].lower() else 1 for token in query_tokens if token in searchable)
        if query.lower() in searchable:
            score += 5
        if score:
            results.append((score, row))
    results.sort(key=lambda item: (-item[0], item[1]["domain"], item[1]["physical_table"], item[1]["element_name"]))
    output: list[dict[str, object]] = []
    for score, row in results[:limit]:
        output.append(
            {
                "score": score,
                "domain": row["domain"],
                "entity_id": row["entity_id"],
                "grain": row["entity_grain"],
                "element": row["element_name"],
                "business_name": row["business_name"],
                "description": row["description"],
                "table": row["physical_table"],
                "columns": row["physical_columns"].split(";") if row["physical_columns"] else [],
                "type": row["logical_type"],
                "reference_entity_id": row["reference_entity_id"] or None,
                "source": f"{row['source_sheet']}:{row['source_row']}",
            }
        )
    return output


def _entity_aliases(schema: list[dict[str, str]]) -> dict[str, dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in schema:
        grouped.setdefault(row["entity_id"], []).append(row)
    aliases: dict[str, dict[str, str]] = {}
    for entity_id, rows in grouped.items():
        table_counts = Counter(
            row["physical_table"]
            for row in rows
            if row["physical_table"] and row["logical_type"] != "collection"
        )
        primary_table = table_counts.most_common(1)[0][0] if table_counts else ""
        aliases[entity_id] = {
            "entity_id": entity_id.lower(),
            "record_name": rows[0]["record_name"].lower(),
            "physical_table": primary_table.lower(),
        }
    return aliases


def _resolve_entity(value: str, aliases: dict[str, dict[str, str]]) -> str:
    lowered = value.lower()
    for field in ("entity_id", "physical_table", "record_name"):
        matches = [
            entity_id for entity_id, names in aliases.items() if names[field] == lowered
        ]
        if len(matches) == 1:
            return matches[0]
        if len(matches) > 1 and field != "record_name":
            break
    normalized = _slug(value)
    matches = [entity_id for entity_id in aliases if entity_id.endswith(f".{normalized}")]
    if len(matches) == 1:
        return matches[0]
    if len(matches) != 1:
        raise ValueError(f"Entity/table {value!r} resolved to {len(matches)} matches: {matches}")
    return matches[0]


def find_joins(
    from_value: str, to_value: str, from_column: str | None = None
) -> dict[str, object]:
    schema = _read_csv(SCHEMA_PATH)
    relationships = _read_csv(RELATIONSHIPS_PATH)
    aliases = _entity_aliases(schema)
    start = _resolve_entity(from_value, aliases)
    target = _resolve_entity(to_value, aliases)
    direct: list[tuple[dict[str, str], bool]] = []
    for relationship in relationships:
        if relationship["from_entity_id"] == start and relationship["to_entity_id"] == target:
            direct.append((relationship, True))
        elif relationship["to_entity_id"] == start and relationship["from_entity_id"] == target:
            direct.append((relationship, False))
    if from_column:
        direct = [
            (relationship, forward)
            for relationship, forward in direct
            if from_column.lower()
            in (
                relationship["from_columns"] if forward else relationship["to_columns"]
            ).lower().split(";")
        ]
    if len(direct) == 1:
        relationship, forward = direct[0]
        return {
            "status": "found",
            "from_entity_id": start,
            "to_entity_id": target,
            "relationships": [
                {
                    **relationship,
                    "direction": "forward" if forward else "reverse",
                }
            ],
        }
    if len(direct) > 1:
        return {
            "status": "ambiguous",
            "from_entity_id": start,
            "to_entity_id": target,
            "clarification": "Specify --from-column to select one direct relationship.",
            "relationships": [
                {
                    **relationship,
                    "direction": "forward" if forward else "reverse",
                }
                for relationship, forward in direct
            ],
        }
    if from_column:
        return {
            "status": "not_found",
            "from_entity_id": start,
            "to_entity_id": target,
            "from_column": from_column,
        }
    graph: dict[str, list[tuple[str, dict[str, str], bool]]] = {}
    for relationship in relationships:
        left = relationship["from_entity_id"]
        right = relationship["to_entity_id"]
        graph.setdefault(left, []).append((right, relationship, True))
        graph.setdefault(right, []).append((left, relationship, False))
    queue: deque[tuple[str, list[tuple[dict[str, str], bool]]]] = deque([(start, [])])
    visited = {start}
    while queue:
        node, path = queue.popleft()
        if node == target:
            return {
                "status": "found",
                "from_entity_id": start,
                "to_entity_id": target,
                "relationships": [
                    {
                        **relationship,
                        "direction": "forward" if forward else "reverse",
                    }
                    for relationship, forward in path
                ],
            }
        if len(path) >= 4:
            continue
        for neighbor, relationship, forward in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [(relationship, forward)]))
    return {"status": "not_found", "from_entity_id": start, "to_entity_id": target}


def _connection_string() -> str:
    driver = os.environ.get("DEALOGIC_ODBC_DRIVER", "{SQL Server Native Client 11.0}")
    server = os.environ.get("DEALOGIC_SERVER", "PrdBigDataSql,5876")
    database = os.environ.get("DEALOGIC_DATABASE", "Dealogic")
    trusted = os.environ.get("DEALOGIC_TRUSTED_CONNECTION", "yes")
    return f"DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection={trusted};"


def _connect(timeout: int):
    try:
        import pyodbc
    except ImportError as exc:
        raise RuntimeError("pyodbc is required for Dealogic verification.") from exc
    return pyodbc.connect(_connection_string(), timeout=timeout, autocommit=True)


def inspect_table(table: str, timeout: int) -> dict[str, object]:
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", table):
        raise ValueError("Table names may contain only letters, numbers, and underscores.")
    schema = os.environ.get("DEALOGIC_SCHEMA", "dbo")
    sql = """
SELECT
    c.ORDINAL_POSITION,
    c.COLUMN_NAME,
    c.DATA_TYPE,
    c.CHARACTER_MAXIMUM_LENGTH,
    c.NUMERIC_PRECISION,
    c.NUMERIC_SCALE,
    c.IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS AS c
WHERE c.TABLE_CATALOG = ?
  AND c.TABLE_SCHEMA = ?
  AND c.TABLE_NAME = ?
ORDER BY c.ORDINAL_POSITION
"""
    database = os.environ.get("DEALOGIC_DATABASE", "Dealogic")
    started = time.monotonic()
    with _connect(timeout) as connection:
        cursor = connection.cursor()
        cursor.timeout = timeout
        rows = cursor.execute(sql, database, schema, table).fetchall()
        columns = [item[0] for item in cursor.description]
    return {
        "database": database,
        "schema": schema,
        "table": table,
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "columns": [dict(zip(columns, row)) for row in rows],
    }


def _scrub_sql(sql: str) -> str:
    without_block_comments = re.sub(r"/\*.*?\*/", " ", sql, flags=re.DOTALL)
    without_line_comments = re.sub(r"--[^\n]*", " ", without_block_comments)
    return re.sub(r"'(?:''|[^'])*'", "''", without_line_comments)


def validate_preview_sql(sql: str) -> None:
    scrubbed = _scrub_sql(sql).strip()
    if scrubbed.endswith(";"):
        scrubbed = scrubbed[:-1].rstrip()
    if ";" in scrubbed:
        raise ValueError("Only one SQL statement is allowed.")
    first = re.match(r"([A-Za-z]+)", scrubbed)
    if not first or first.group(1).upper() not in {"SELECT", "WITH"}:
        raise ValueError("Only SELECT or WITH ... SELECT queries are allowed.")
    prohibited = re.compile(
        r"\b(INSERT|UPDATE|DELETE|MERGE|DROP|ALTER|CREATE|TRUNCATE|EXEC(?:UTE)?|CALL|GRANT|REVOKE|BACKUP|RESTORE|DBCC|WAITFOR|OPENROWSET|OPENQUERY|OPENDATASOURCE|BULK)\b",
        re.IGNORECASE,
    )
    match = prohibited.search(scrubbed)
    if match:
        raise ValueError(f"Unsafe SQL keyword is not allowed: {match.group(1).upper()}")
    if re.search(r"\bSELECT\s+INTO\b", scrubbed, re.IGNORECASE):
        raise ValueError("SELECT INTO is not allowed.")
    if re.search(r"\bSELECT\s+\*", scrubbed, re.IGNORECASE) or re.search(
        r"\bSELECT\s+(?:TOP\s*(?:\(\s*)?\d+\s*\)?\s+)?(?:\[[^\]]+\]|[A-Za-z_][A-Za-z0-9_]*)\.\*",
        scrubbed,
        re.IGNORECASE,
    ):
        raise ValueError("SELECT * is not allowed; name the preview columns explicitly.")
    if "[dealogic].[dbo]." not in scrubbed.lower():
        raise ValueError("Preview SQL must reference fully qualified [Dealogic].[dbo] tables.")
    top_values = [int(value) for value in re.findall(r"\bTOP\s*(?:\(\s*)?(\d+)", scrubbed, re.IGNORECASE)]
    if not top_values:
        raise ValueError("Preview SQL must include TOP (20) or a smaller TOP limit.")
    if max(top_values) > PREVIEW_LIMIT:
        raise ValueError(f"Preview SQL may return at most TOP ({PREVIEW_LIMIT}) rows.")


def verify_sql(sql: str, timeout: int) -> dict[str, object]:
    validate_preview_sql(sql)
    started = time.monotonic()
    with _connect(timeout) as connection:
        cursor = connection.cursor()
        cursor.timeout = timeout
        rows = cursor.execute(sql).fetchmany(PREVIEW_LIMIT)
        columns = [item[0] for item in cursor.description] if cursor.description else []
    return {
        "status": "verified",
        "row_limit": PREVIEW_LIMIT,
        "rows_returned": len(rows),
        "elapsed_seconds": round(time.monotonic() - started, 3),
        "columns": columns,
        "rows": [list(row) for row in rows],
    }


def _print_json(value: object) -> None:
    print(json.dumps(value, indent=2, default=str))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    build_parser = subparsers.add_parser("build", help="Build canonical CSV metadata from the Dealogic XLSX dictionary.")
    build_parser.add_argument("--source", required=True, type=Path)
    build_parser.add_argument("--output-dir", type=Path, default=REFERENCE_DIR)

    search_parser = subparsers.add_parser("search", help="Search Dealogic fields and tables.")
    search_parser.add_argument("query")
    search_parser.add_argument("--domain")
    search_parser.add_argument("--limit", type=int, default=10)

    joins_parser = subparsers.add_parser("joins", help="Find an approved join path between two entities or tables.")
    joins_parser.add_argument("from_entity")
    joins_parser.add_argument("to_entity")
    joins_parser.add_argument(
        "--from-column",
        help="Disambiguate multiple direct relationships by the source-side column.",
    )

    inspect_parser = subparsers.add_parser("inspect", help="Inspect live SQL Server column metadata for one table.")
    inspect_parser.add_argument("--table", required=True)
    inspect_parser.add_argument("--timeout", type=int, default=DEFAULT_QUERY_TIMEOUT)

    validate_parser = subparsers.add_parser("validate-sql", help="Validate SQL without connecting to Dealogic.")
    validate_parser.add_argument("--sql")
    validate_parser.add_argument("--sql-file", type=Path)

    verify_parser = subparsers.add_parser("verify", help="Execute a user-confirmed, read-only TOP (20) preview.")
    verify_parser.add_argument("--sql")
    verify_parser.add_argument("--sql-file", type=Path)
    verify_parser.add_argument("--confirmed", action="store_true", help="Required acknowledgement that the user approved execution.")
    verify_parser.add_argument("--timeout", type=int, default=DEFAULT_QUERY_TIMEOUT)

    args = parser.parse_args()
    try:
        if args.command == "build":
            _print_json(build_catalog(args.source, args.output_dir))
        elif args.command == "search":
            _print_json(search_catalog(args.query, args.domain, args.limit))
        elif args.command == "joins":
            _print_json(find_joins(args.from_entity, args.to_entity, args.from_column))
        elif args.command == "inspect":
            _print_json(inspect_table(args.table, args.timeout))
        elif args.command in {"validate-sql", "verify"}:
            sql = args.sql or (args.sql_file.read_text(encoding="utf-8") if args.sql_file else "")
            if not sql.strip():
                raise ValueError("Provide --sql or --sql-file.")
            if args.command == "validate-sql":
                validate_preview_sql(sql)
                _print_json({"status": "valid", "row_limit": PREVIEW_LIMIT})
            else:
                if not args.confirmed:
                    raise ValueError("Verification requires --confirmed after explicit user approval.")
                _print_json(verify_sql(sql, args.timeout))
        return 0
    except Exception as exc:
        _print_json({"status": "error", "error": str(exc)})
        return 1


if __name__ == "__main__":
    raise SystemExit(main())

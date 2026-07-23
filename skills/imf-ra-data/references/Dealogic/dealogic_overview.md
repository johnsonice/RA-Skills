# Dealogic Source Overview

## Contents

- [Service scope](#service-scope)
- [Data model](#data-model)
- [Source-selection boundary](#source-selection-boundary)
- [Official IMF guidance](#official-imf-guidance)
- [Technical profile](#technical-profile)
- [Reference map](#reference-map)

## Service scope

Dealogic provides detailed primary-market transaction data for:

- Debt Capital Markets (DCM), including bond issuance
- Syndicated loans
- Equity Capital Markets (ECM), including IPOs and rights issues
- Mergers and Acquisitions (M&A)

Dealogic is particularly useful for bond and loan issuance arranged by
syndicates of investment banks, including foreign-currency borrowing by
sovereign and corporate issuers.

## Data model

The database is transaction-oriented:

- A **deal** represents the overall transaction.
- DCM, ECM, and Loan deals may contain **tranches**, which represent individual
  securities or facilities with distinct terms.
- M&A transactions are deal-level and do not have formal tranche records.
- Company and reference tables decode issuers, borrowers, banks, advisors,
  statuses, countries, currencies, roles, and other identifiers.

The feed dictionary documents more than 140 DCM tranche attributes, including
ISIN, issue yield, coupon, maturity, issuer nationality, face value, and
syndicate information.

## Source-selection boundary

Use Dealogic for primary-market questions about issuance, deal structure,
tranches, syndicates, participants, proceeds, terms, and transaction status.

Do not use Dealogic for secondary-market bid, ask, traded-price, or comparable
market time-series requests. Route those requests to an available secondary
market source such as Bloomberg, Refinitiv Eikon/Datastream, or another
appropriately licensed provider.

Dealogic is not an iData time-series source. Dealogic requests follow the
schema-aware SQL path in `imf-ra-data` and do not use the iData/Haver catalog
handoff or output-format workflow.

## Official IMF guidance

At the start of a Dealogic conversation, provide the user with the official IMF
[Economic and Financial Data at the IMF (EconFinData) guidance](https://apps.powerapps.com/play/e/e56a91a7-5e7c-ed89-bcf7-ca68bdf12f1c/a/b1e30305-b5d9-464d-9ee2-c4b878a86cd5?tenantId=8085fa43-302e-45bd-b171-a6648c3b6be7&hint=859df194-14d0-4956-8376-e4a21185f4a1&ItemId=2693).
This is user-facing usage guidance; the schema CSVs and SQL patterns in this
skill remain the technical sources for query construction.

## Technical profile

```text
engine:       Microsoft SQL Server
database:     Dealogic
schema:       dbo
server:       PrdBigDataSql,5876
authentication: Trusted_Connection=yes
production driver: {SQL Server Native Client 11.0}
```

The helper reads environment overrides from:

```text
DEALOGIC_ODBC_DRIVER
DEALOGIC_SERVER
DEALOGIC_DATABASE
DEALOGIC_SCHEMA
DEALOGIC_TRUSTED_CONNECTION
```

Never store usernames or passwords in the skill. Database inspection and
preview execution require the IMF work environment.

## Reference map

- `dealogic_schema.csv` — canonical field and entity metadata extracted from
  the feed dictionary, plus recorded live-verification notes.
- `dealogic_relationships.csv` — join paths, cardinality, confidence, and
  provenance.
- `dealogic_sql_patterns.md` — SQL Server patterns, performance safeguards,
  aggregation rules, and detailed live-validation findings.
- `../../scripts/dealogic.py` — deterministic schema build/search, join lookup,
  SQL validation, metadata inspection, and confirmed preview execution.

Source-description basis: Dealogic service summary supplied by the user in
July 2026. Technical field definitions remain grounded in the supplied Dealogic
feed data dictionary and recorded live-schema checks.

# Dealogic SQL Generation

Use this reference only for Dealogic requests. The canonical field and join
metadata live in `dealogic_schema.csv` and `dealogic_relationships.csv`.

## Workflow

1. Search the canonical schema with `dealogic.py search`.
2. Resolve the output grain before selecting columns.
3. Use `dealogic.py joins` for every multi-table query.
4. Do not use a relationship marked `unverified`. Disclose `derived`
   relationships and prefer `database_verified` or `documented` relationships.
5. Generate Microsoft SQL Server syntax against `[Dealogic].[dbo]`.
6. Show the SQL, grain, filters, joins, and assumptions to the user.
7. Run `validate-sql`.
8. Execute `verify --confirmed` only after the user explicitly approves the
   displayed query.

## Preview and performance rules

- Return at most `TOP (20)` rows during verification.
- Select explicit columns; never use `SELECT *`.
- Ask for a date range when a request would otherwise scan a large transaction
  table.
- Prefer selective equality, identifier, date, and status filters.
- Do not wrap filtered key or date columns in functions.
- Avoid leading-wildcard searches on large tables.
- Avoid `DISTINCT` as a substitute for understanding the output grain.
- Join collection tables only when the requested output requires them.
- Warn when a one-to-many join changes deal-level output to tranche, bank,
  company, or reference-value grain.
- Use `EXISTS` when the user only needs to test whether a related record exists.
- Order previews only when the ordering is meaningful to the request.

`TOP (20)` limits returned rows, but it does not guarantee a cheap execution
plan. Require a selective filter when joins, sorting, or broad text predicates
could still scan a large table.

## Deal-level preview

```sql
SELECT TOP (20)
    d.[DealId],
    d.[AnnouncementDate],
    d.[BookrunnerCount]
FROM [Dealogic].[dbo].[DCMDeal] AS d
WHERE d.[AnnouncementDate] >= '<START_DATE>'
  AND d.[AnnouncementDate] < '<END_DATE_EXCLUSIVE>'
ORDER BY d.[AnnouncementDate] DESC;
```

Live SQL metadata confirmed that `DealId` is `int NOT NULL`, while `DealNo` is
nullable and can be `NULL`. Use `DealId` for DCM deal templates. Neither column
is declared as a SQL primary key, and live index metadata returned no index
involving either column. Treat `DealId` as the feed-documented logical key, not
as a database-enforced unique key. Avoid a full duplicate scan unless the user
explicitly accepts the potential cost.
Replace date placeholders with validated ISO `YYYY-MM-DD` literals before
validation or verification.

## Parent-child join

Use only the columns returned by `dealogic.py joins`. A documented DCM
deal-to-tranche relationship from the feed dictionary is:

```sql
SELECT TOP (20)
    d.[DealId],
    d.[AnnouncementDate],
    t.[TrancheId]
FROM [Dealogic].[dbo].[DCMDeal] AS d
INNER JOIN [Dealogic].[dbo].[DCMDealTranches] AS t
    ON t.[DCMDealDealId] = d.[DealId]
WHERE d.[AnnouncementDate] >= '<START_DATE>'
  AND d.[AnnouncementDate] < '<END_DATE_EXCLUSIVE>';
```

This changes the output from one row per deal to one row per tranche. Confirm
the live column names before verification.

## Membership without row multiplication

```sql
SELECT TOP (20)
    d.[DealId],
    d.[AnnouncementDate]
FROM [Dealogic].[dbo].[DCMDeal] AS d
WHERE d.[AnnouncementDate] >= '<START_DATE>'
  AND d.[AnnouncementDate] < '<END_DATE_EXCLUSIVE>'
  AND EXISTS (
      SELECT 1
      FROM [Dealogic].[dbo].[DCMDealTranches] AS t
      WHERE t.[DCMDealDealId] = d.[DealId]
  );
```

## Verified ECM-share tranche join

Live verification confirmed this composite relationship:

```sql
SELECT TOP (20)
    s.[ShareECMDealDealId],
    s.[TrancheId],
    e.[ECMDealDealId],
    e.[TrancheId] AS [ECMTrancheId]
FROM [Dealogic].[dbo].[ShareECMDealTranches] AS s
INNER JOIN [Dealogic].[dbo].[ECMDealTranches] AS e
    ON e.[ECMDealDealId] = s.[ShareECMDealDealId]
   AND e.[TrancheId] = s.[TrancheId];
```

Treat this as a logical one-to-one relationship. The 20-row verification sample
matched exactly, but no database uniqueness constraint has been established.

Decode `LoanDealTranches.StatusId` through the shared `DealStatus` table, not
`LoanDealStatus`. Live values 2, 3, and 12 resolved as Announced, Close, and
Mandated:

```sql
LEFT JOIN [Dealogic].[dbo].[DealStatus] AS tranche_status
    ON tranche_status.[Id] = t.[StatusId]
```

## Verified DCM issuer and status joins

Live verification confirmed:

```sql
LEFT JOIN [Dealogic].[dbo].[Company] AS issuer
    ON issuer.[Id] = d.[IssuerId]
LEFT JOIN [Dealogic].[dbo].[DealStatus] AS deal_status
    ON deal_status.[Id] = d.[CommonStatusId]
```

`CommonStatusId` decoded successfully for all 20 sampled deals. Only 8 of the
20 sampled `IssuerId` values had a populated `Company.BrandName`, so issuer
enrichment must use `LEFT JOIN` and retain the numeric `IssuerId` when the name
is missing.

## Verified DCM ISIN column

Live SQL metadata confirmed that `DCMDealTranchesISINs` stores the identifier
in `ISIN`. The feed dictionary's loader mapping named `SecurityNumber`, but
that column does not exist in the deployed table. Use:

```sql
SELECT TOP (20)
    i.[DCMDealTrancheDealId],
    i.[DCMDealTrancheTrancheId],
    i.[ISIN],
    i.[SortNumber]
FROM [Dealogic].[dbo].[DCMDealTranchesISINs] AS i
ORDER BY i.[DCMDealTrancheDealId], i.[DCMDealTrancheTrancheId], i.[SortNumber];
```

Do not substitute `DCMDealTranchesSecurityNumbers.SecurityNumber`; that is a
different child collection containing non-US domestic and foreign security
numbers rather than the ISIN field.

## Aggregation guardrail

State the aggregation grain explicitly. When aggregating a deal-level measure,
do not sum it after joining to a one-to-many tranche or syndicate table unless
the query first restores one row per deal.

```sql
WITH qualifying_deals AS (
    SELECT
        d.[DealId],
        d.[AnnouncementDate]
    FROM [Dealogic].[dbo].[DCMDeal] AS d
    WHERE d.[AnnouncementDate] >= '<START_DATE>'
      AND d.[AnnouncementDate] < '<END_DATE_EXCLUSIVE>'
)
SELECT TOP (20)
    YEAR(q.[AnnouncementDate]) AS [AnnouncementYear],
    COUNT(*) AS [DealCount]
FROM qualifying_deals AS q
GROUP BY YEAR(q.[AnnouncementDate])
ORDER BY [AnnouncementYear] DESC;
```

## Query explanation contract

Return these items with every generated query:

```text
Domain:
Output grain:
Tables:
Join path:
Filters and parameters:
Preview limit:
Relationship confidence:
Assumptions or unresolved ambiguities:
```

SELECT TOP (20)
    d.[DealId],
    t.[TrancheId],
    d.[AnnouncementDate],
    d.[PricingDate],
    d.[SettlementDate],
    d.[IssuerId],
    COALESCE(issuer.[BrandName], issuer.[Name]) AS [IssuerName],
    d.[NationalityISOCode] AS [IssuerNationalityISOCode],
    deal_status.[Name] AS [DealStatus],
    d.[SectorId],
    d.[TypeId] AS [DealTypeId],
    t.[SecurityTypeId],
    t.[IssueTypeId],
    t.[Class] AS [TrancheClass],
    t.[CurrencyISOCode] AS [IssueCurrencyISOCode],
    face_value.[Value] AS [FaceValue],
    primary_isin.[ISIN] AS [PrimaryISIN],
    t.[CouponPercent],
    t.[CouponDetails],
    t.[YieldToMaturityAnnualPercent],
    t.[MaturityDate],
    t.[YearsToMaturity],
    t.[EffectiveRatingLaunch],
    t.[EffectiveRatingCurrent],
    d.[IsInvestmentGrade],
    t.[IsHighYield],
    t.[IsSubordinated],
    t.[TierCapitalId],
    t.[IsInternational],
    t.[IsCancelled],
    d.[IsEmergingMarket],
    d.[IsHybridCapital],
    d.[BookrunnerCount],
    d.[BankCount]
FROM [Dealogic].[dbo].[DCMDeal] AS d
INNER JOIN [Dealogic].[dbo].[DCMDealTranches] AS t
    ON t.[DCMDealDealId] = d.[DealId]
LEFT JOIN [Dealogic].[dbo].[Company] AS issuer
    ON issuer.[Id] = d.[IssuerId]
LEFT JOIN [Dealogic].[dbo].[DealStatus] AS deal_status
    ON deal_status.[Id] = d.[CommonStatusId]
OUTER APPLY (
    SELECT TOP (1)
        v.[Value]
    FROM [Dealogic].[dbo].[DCMDealTranchesValue] AS v
    WHERE v.[DCMDealTrancheDealId] = t.[DCMDealDealId]
      AND v.[DCMDealTrancheTrancheId] = t.[TrancheId]
      AND v.[CurrencyISOCode] = t.[CurrencyISOCode]
) AS face_value
OUTER APPLY (
    SELECT TOP (1)
        i.[ISIN]
    FROM [Dealogic].[dbo].[DCMDealTranchesISINs] AS i
    WHERE i.[DCMDealTrancheDealId] = t.[DCMDealDealId]
      AND i.[DCMDealTrancheTrancheId] = t.[TrancheId]
    ORDER BY i.[SortNumber]
) AS primary_isin
WHERE d.[AnnouncementDate] >= '2026-07-01'
  AND d.[AnnouncementDate] <= GETDATE()
ORDER BY d.[AnnouncementDate] DESC, d.[DealId], t.[TrancheId];

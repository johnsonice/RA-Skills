# Haver Analytics — Database Directory

Haver provides economic, financial, industry, and forecast data from 200+ databases covering 750+ government and private sources. Coverage spans 1945–present at annual, quarterly, monthly, weekly, and daily frequencies.

Use this file to identify which Haver database is the most likely source for a given indicator request **before** looking up metadata. Match the concept and geography to the appropriate group below.

---

## U.S. Macroeconomic — Core

Use for standard U.S. macro and national accounts data.

| Code | Description |
|---|---|
| `USECON` | United States — broad macro summary (GDP, prices, employment, trade, finance) |
| `USNA` | U.S. National Accounts — GDP components, income, saving |
| `CAPSTOCK` | U.S. Capital Stock |
| `LABOR` | U.S. Payroll Employment Detail (CES) |
| `EMPL` | U.S. Household Employment Detail (CPS) |
| `CEW` | U.S. Covered Employment & Wages (ES-202 / QCEW) |
| `OES` | U.S. Occupational Employment Statistics |
| `IP` | U.S. Industrial Production Detail |
| `CPIDATA` | U.S. Consumer Prices Detail |
| `PPI` | U.S. Producer Prices by Commodity |
| `PPIR` | U.S. Producer Prices by Industry |
| `USINT` | U.S. International Transactions (BOP) |
| `USTRADE` | U.S. Trade Details (goods by partner/commodity) |
| `SURVEYS` | U.S. Economic Surveys (consumer sentiment, ISM, PMI, etc.) |
| `FFUNDS` | U.S. Flow of Funds (Financial Accounts of the U.S.) |
| `GOVFIN` | U.S. Government Finance |

---

## High-Frequency & Financial — U.S. and Global

Use for daily, weekly, or high-frequency financial and market data.

| Code | Description |
|---|---|
| `DAILY` | U.S. Daily+ — interest rates, FX, equities, commodities |
| `INTDAILY` | Global Daily — cross-country daily financial indicators |
| `WEEKLY` | U.S. Weekly+ — money supply, jobless claims, mortgage rates |
| `INTWKLY` | Global Weekly — cross-country weekly indicators |
| `CRYPTO` | Cryptocurrency Statistics |
| `BONDINDX` | Bond Indexes (third-party) |

---

## EPFR Global — Fund Flows and Allocations

Use for fund flow data by asset class, region, country, or sector.

| Code | Description |
|---|---|
| `EPFREIN` | Equity Fund Flows — Industrialized Countries |
| `EPFREEM` | Equity Fund Flows — Emerging Markets |
| `EPFRBIN` | Bond Fund Flows — Industrialized Countries |
| `EPFRBEM` | Bond Fund Flows — Emerging Markets |
| `EPFRBMM` | Bond Fund Flows — Money Market |
| `EPFRESA` | Equity Fund Sector and Industry Allocations |
| `EPFRESF` | Equity Fund Sector and Industry Flows |
| `EPFRECA` | Equity Fund Country Allocations |
| `EPFRBCA` | Bond Fund Country Allocations |
| `EPFRECF` | Equity Fund Country Flows |
| `EPFRBCF` | Bond Fund Country Flows |
| `EPRDEFF` | Equity Fund Flows (daily) |
| `EPFRDECF` | Equity Country Flows (daily) |
| `EPFRDBFF` | Bond Fund Flows (daily) |
| `EPFRDBCF` | Bond Country Flows (daily) |
| `EPFRDESF` | Sector Flows (daily) |

---

## Industry & Sector Detail

Use for industry-level, transportation, energy, or sector-specific data.

| Code | Description |
|---|---|
| `QFR` | Quarterly Financial Report (U.S. manufacturing, mining, trade) |
| `ASM` | Annual Survey of Manufactures |
| `BALTIC` | Baltic Freight Indexes (shipping) |
| `GLSECTOR` | Global Sector Statistics |
| `TRANSPRT` | Global Transportation Statistics |
| `TOURISM` | Global Tourism Statistics |

---

## Energy

Use for energy production, consumption, and pricing data.

| Code | Description |
|---|---|
| `ENERGY` | Global Energy Statistics (production, consumption, trade by fuel type) |
| `EEI` | U.S. Electric Output, Weekly |
| `JODI` | JODI Oil World Database (oil supply and demand) |

---

## Advanced Economies — Country Summary

Use for broad country-level macro data for individual advanced economies or groups.

| Code | Description |
|---|---|
| `G10` | G10 Country Summary Statistics |
| `ANZ` | Australia & New Zealand |
| `CANADA` | Canada |
| `EUDATA` | Euro Area & European Union |
| `FRANCE` | France |
| `GERMANY` | Germany |
| `IRELAND` | Ireland |
| `ITALY` | Italy |
| `JAPAN` | Japan |
| `SPAIN` | Spain |
| `UK` | United Kingdom |
| `BENELUX` | Belgium, Netherlands, Luxembourg |
| `NORDIC` | Denmark, Finland, Iceland, Norway, Sweden |
| `ALPMED` | Andorra, Austria, Cyprus, Greece, Malta, Portugal, Switzerland |

---

## Europe — Detailed Thematic

Use for detailed European/Euro Area data by theme (accounts, finance, labor, trade).

| Code | Description |
|---|---|
| `EUNA` | European National Accounts |
| `EUSURVYS` | European Surveys (sentiment, PMI, etc.) |
| `EUFIN` | European Financial Accounts |
| `EUSEC` | European Debt Securities |
| `EUGOV` | European Government Finance |
| `EULABOR` | European Regional Labor Markets |
| `AMECO` | European Commission AMECO Macro Forecasts |
| `EUINT` | European International Transactions |
| `EUPOP` | European Demographics |
| `EUTRADE` | European Trade Detail |

---

## Emerging Markets — Country Summary

Use for broad macro data across emerging market economies.

| Code | Description |
|---|---|
| `EMERGE` | Emerging Markets Country Summary (broad panel) |
| `EMERGELA` | Latin America |
| `EMERGEPR` | Asia Pacific |
| `EMERGECW` | Central & Eastern Europe and Western Asia |
| `EMERGEMA` | Middle East & Africa |

---

## Other Country Surveys & ESG

| Code | Description |
|---|---|
| `INTSURVYS` | Country-level Surveys (business and consumer) |
| `ESG` | Environment, Social and Governance Indicators |

---

## Advanced Economy Regional Detail

Use when country-level regional breakdown within an advanced economy is needed.

| Code | Description |
|---|---|
| `ANZR` | Australia & New Zealand Regional |
| `CANADAR` | Canada Regional |
| `FRANCER` | France Regional |
| `GERMANYR` | Germany Regional |
| `ITALYR` | Italy Regional |
| `JAPANR` | Japan Regional |
| `SPAINR` | Spain Regional |
| `UKR` | United Kingdom Regional |
| `ALPMEDR` | Cyprus, Portugal, Switzerland Regional |

---

## Emerging Market Regional Detail

| Code | Description |
|---|---|
| `MENAR` | Middle East & North Africa Regional |
| `SUBAFR` | Sub-Saharan Africa Regional |

---

## Forecasts & Consensus

Use for economic forecasts, consensus surveys, or model-based projections.

| Code | Description |
|---|---|
| `MA4CAST` | U.S. Short-Term Quarterly Forecasts (S&P Global Market Intelligence / Macroeconomic Advisers) |
| `IIFDATA` | IIF (Institute of International Finance) Forecasts |
| `ASREPGDP` | U.S. GDP Headline Tables (as-reported and forecast survey medians) |
| `BLUECHIP` | Blue Chip Consensus Forecasts — current and historical |

---

## PMI / Purchasing Managers Surveys

| Code | Description |
|---|---|
| `MKTPMI` | Markit/S&P Global PMI Surveys — manufacturing and services PMI globally |

---

## International Organizations (within Haver)

These are Haver-hosted mirrors of IMF and BIS statistical releases. Prefer native iData sources for IMF databases unless the user specifically requests the Haver version.

| Code | Description |
|---|---|
| `BIS` | Bank for International Settlements — includes QEDS and JEDH |
| `IFS` | IMF International Financial Statistics, Monthly/Quarterly |
| `IFSANN` | IMF International Financial Statistics, Annual |
| `IMFDOTM` | IMF Direction of Trade, Monthly |
| `IMFDOT` | IMF Direction of Trade, Annual |
| `IMFBOP` | IMF Balance of Payments, Quarterly |
| `IMFBOPA` | IMF Balance of Payments, Annual |
| `CPIS` | IMF Coordinated Portfolio Investment Survey |
| `CDIS` | IMF Coordinated Direct Investment Survey |
| `IMFWEO` | IMF World Economic Outlook, Annual |
| `IMFREO` | IMF Regional Economic Outlook |

---

## U.S. Regional

Use for U.S. state- or county-level economic data.

| Code | Description |
|---|---|
| `REGIONAL` | Selected Regional Indicators (states) |
| `REGIONW` | Selected Regional Indicators, Weekly |
| `USPOP` | U.S. Regional Demographics |
| `GSP` | Gross State Product |
| `MBAMTG` | Mortgage Delinquencies by State |
| `GOVFINR` | State Government Finance |
| `EMPLR` | Household Employment by State |
| `EMPLC` | Household Employment by County |
| `CEWR` | Covered Employment and Wages by State |

---

## FX Rates

| Code | Description |
|---|---|
| `FXRATES` | Foreign Exchange Rates, Monthly — for currency conversion |

---

## Routing Guidance for Agents

When a user describes a data request, use the following decision tree to narrow down the likely Haver database before fetching metadata:

1. **U.S. macro aggregate (GDP, CPI, employment, trade, government finance)?** → `USECON`, `USNA`, `CPIDATA`, `LABOR`, `GOVFIN`, `USINT`
2. **Daily or weekly financial/market data (rates, FX, equities)?** → `DAILY`, `INTDAILY`, `WEEKLY`, `INTWKLY`
3. **Fund flows (equity or bond, by country or sector)?** → `EPFR*` family; check frequency (daily vs. aggregate)
4. **Energy data?** → `ENERGY`, `JODI`, `EEI`
5. **Single advanced economy country detail?** → country-specific code (`GERMANY`, `JAPAN`, `UK`, etc.)
6. **Euro Area or EU aggregate?** → `EUDATA`; thematic detail → `EUNA`, `EUGOV`, `EULABOR`, etc.
7. **Emerging markets panel?** → `EMERGE`; by region → `EMERGELA`, `EMERGEPR`, `EMERGECW`, `EMERGEMA`
8. **Forecast or consensus?** → `BLUECHIP`, `IIFDATA`, `MA4CAST`
9. **PMI?** → `MKTPMI`
10. **IMF statistics via Haver?** → prefer native iData source; fall back to `IFS`, `IMFWEO`, `IMFBOP`, etc. if user requests Haver specifically
11. **U.S. regional or state-level?** → `REGIONAL`, `GSP`, `CEWR`, `EMPLR`
12. **ESG or governance?** → `ESG`

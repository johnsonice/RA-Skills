# Database Overview

## Purpose

This file is a source-selection guide for commonly used catalog database families. It helps agents understand broad coverage and plausible source choices before looking up exact identifiers.

This is not an operational routing policy. Use `../SKILL.md` and `../scripts/catalog_search.py` for routing decisions, helper commands, ambiguity handling, and handoff rules.

CSV catalogs remain the source of truth for identifiers. Metadata fields here are aligned with `non_vintage_datasets.csv`.

## How to Use

1. Use this overview to identify plausible database families.
2. Use `../scripts/catalog_search.py explain-source`, `search`, or `resolve` for operational lookup.
3. Use the dataset and indicator CSVs to confirm exact `database`, `dimension_name`, and `code` values.

## At a Glance

| Database | Status | Best for |
|---|---|---|
| `IMF.RES.WEO:WEO_LIVE` | Default non-vintage WEO source | WEO-style macro concepts, national accounts, prices, fiscal, external, and higher-frequency WEO variants. |
| `IMF.RES:WEO` | Legacy/explicit-use WEO source | Compact legacy WEO requests or explicit `IMF.RES:WEO` references. |
| `IMF.RES.GAS:GAS_LIVE` | Non-vintage source | Global assumptions, macro-financial variables, exchange rates, commodity assumptions, and financial conditions. |
| `IMF.RES.GEE:GEE_LIVE` | Non-vintage source | Trade-weighted partner demand, output, prices, costs, and competitiveness measures. |
| `IMF.STA:BOP` | Non-vintage source | BPM6 balance of payments indicators, current account, capital account, financial account, and reserve assets. |
| IFS legacy family | Legacy source hint | Old EcOS IFS requests that must be routed to replacement iData topic databases. |
| `IMF.CSF:BBGDL` | Specialized catalog | Bloomberg tickers and market-data fields. |
| `WB:WDI` | Specialized catalog | World Bank development indicators. |
| `WTO:WTOIMFTT` | Specialized catalog | WTO-IMF Tariff Tracker HS commodity codes and tariff/goods-trade classifications. |
| `HAVER:*` | External service (200+ databases) | US macro detail, global economies, high-frequency financial and daily data, industry statistics, fund flows, emerging markets, and international organization data. Accessed via `haver_utilities` — use `scripts/Haver/haver_catalog_search.py` for indicator lookup and `fetch_haver.py` for retrieval. |

## World Economic Outlook (WEO) Live
- **Database:** `IMF.RES.WEO:WEO_LIVE`
- **Status:** Default non-vintage WEO source.

**Overview:** WEO Live is the more granular World Economic Outlook dataset. It contains more than 350 indicators across national accounts, prices, labor markets, monetary variables, fiscal accounts, trade, balance of payments, international investment position, and external debt. It includes annual and higher-frequency series, with quarterly, seasonally adjusted, quarter-over-quarter annualized, and year-over-year percent-change variants where available.

**Key content:**

1. **National accounts, real:** GDP and demand components at constant prices, including `NGDP_R`, `NCP_R`, `NFI_R`, and `NTDD_R`.
2. **National accounts, nominal:** GDP and demand components at current prices, including `NGDP`, `NCP`, `NFI`, and `NGS`.
3. **Prices, labor, and monetary:** CPI, unemployment, broad money, interest rates, and bond yields, including `PCPI`, `LUR`, `FMB`, and `FIGB`.
4. **Fiscal indicators:** General government revenue, expenditure, net lending/borrowing, and gross debt, including `GGR`, `GGX`, `GGXCNL`, and `GGXWDG`.
5. **Trade:** Exports, imports, terms of trade, and goods trade, including `TX`, `TM`, `TT`, and `TXG`.
6. **Balance of payments:** Current account, goods and services balance, direct investment, and portfolio investment under BPM6, including `BCA_BP6`, `BGS_BP6`, `BFD_BP6`, and `BFP_BP6`.
7. **International investment position:** Net IIP, assets, liabilities, and reserve assets, including `I_BP6`, `IA_BP6`, `IL_BP6`, and `IAR_BP6`.
8. **External debt:** External debt and debt service measures, including `D`, `DS`, `DSP`, and `DSI`.

## World Economic Outlook (WEO)
- **Database:** `IMF.RES:WEO`
- **Status:** Legacy/explicit-use WEO resource. Do not use as the default WEO source; prefer `IMF.RES.WEO:WEO_LIVE` unless the user explicitly requests `IMF.RES:WEO`.

**Overview:** WEO provides a compact set of core macroeconomic indicators, typically at annual frequency, alongside extensive commodity price data. It is useful for country-level macro analysis, projections, and cross-country comparison.

**Key content:**

1. **Macroeconomic aggregates:** GDP at constant and current prices, inflation, unemployment, trade volumes, fiscal balances, public debt, and external debt.
2. **Commodity prices:** Unit prices and price indices for energy, metals, food, beverages, agricultural raw materials, and other commodities.
3. **Forecast-oriented series:** Historical and projected values for major macroeconomic variables used in WEO analysis.

## Global Assumptions (GAS) Live
- **Database:** `IMF.RES.GAS:GAS_LIVE`
- **Status:** Non-vintage source.

**Overview:** GAS Live is a broad macroeconomic, financial, external-sector, exchange-rate, and commodity statistics dataset used for global monitoring and analytical assumptions. Entries are indicator-level series under the `INDICATOR` dimension.

**Key content:**

1. **Macroeconomic activity:** GDP, real GDP growth, GDP deflators, and domestic demand indicators, including `NGDP_R`, `NGDP_USD`, `NGDP_D`, and `NTDD_R`.
2. **Prices and inflation:** Consumer price and price-level measures, including `PCPI`, `PCPI_PCH`, `NGDP_D`, and `NGDP_D_PCH`.
3. **External sector and trade:** Export, import, trade-volume, and trade-price indicators, including `TXG`, `TXG_D`, `TXGM_D`, `TM_R`, and `TOTXM_R`.
4. **Financial conditions:** Policy rates, SDR rates, risk-free rates, bond yields, and LIBOR-style indicators, including `FISDR`, `FPOLM`, `FIRF`, `FIST`, `FIGB`, `FIPIBOR`, and `FILIBOR`.
5. **Exchange rates and competitiveness:** Bilateral, SDR, end-of-period, nominal effective, and real effective exchange rates, including `ENDA`, `EDNA`, `ESDA`, `EDSA`, `ENDE`, `EDNE`, `ENEER_ULC`, and `EREER_ULC`.
6. **Commodity price aggregates:** Broad energy, non-fuel, agriculture, metals, and food commodity indexes, including `PZPIW`, `PZPINFW`, `PZPINRGW`, `PZPIAGRW`, `PZPIMETW`, and `PZPIFW`.
7. **Detailed commodity prices:** Energy, metals and minerals, agricultural and food products, and industrial inputs such as oil, natural gas, coal, copper, gold, wheat, coffee, sugar, fertilizers, rubber, wool, and timber.

## Global Economic Environment (GEE) Live
- **Database:** `IMF.RES.GEE:GEE_LIVE`
- **Status:** Non-vintage source.

**Overview:** GEE Live provides trade-weighted foreign output, demand, trade volume, price, cost, and commodity-price indicators. The composites are calculated for each country as weighted averages of trading-partner data, using bilateral trade shares as weights.

**Key content:**

1. **Trade-weighted demand and output:** Partner-country GDP and domestic demand weighted by trade shares.
2. **Trade volumes:** Export and import volume measures weighted by partner trade shares.
3. **Trade price deflators:** Price deflators for trade flows weighted by partner shares.
4. **Partner price pressures:** GDP deflators and CPI measures transmitted through trade exposure.
5. **Competitiveness:** Unit labor cost measures for manufacturing relative to trading partners.
6. **Commodity prices:** Non-fuel commodity price indices weighted by trade exposure.
7. **Component-based trade prices:** Three-component decomposition of non-fuel goods trade prices.

## Balance of Payments (BOP)
- **Database:** `IMF.STA:BOP`
- **Status:** Non-vintage source.

**Overview:** BOP is the IMF Balance of Payments Statistics database. It follows the BPM6 framework and provides a comprehensive catalog of balance of payments indicators covering the current account, capital account, financial account, aggregate balances, and exceptional financing items.

**Key content:**

1. **Current account:** Goods, services, primary income, secondary income, and current account balances.
2. **Capital account:** Capital transfers and nonproduced nonfinancial assets.
3. **Financial account:** Direct investment, portfolio investment, other investment, reserve assets, and financial derivatives.
4. **Sector and maturity detail:** Breakdowns by institutional sector, such as central bank, deposit-taking corporations, and general government, and by short-term or long-term maturity where available.
5. **Analytical balances:** Aggregate balances and financing items used in external-sector analysis.

## International Financial Statistics (IFS) Migration Note
- **Legacy source:** IFS in the old EcOS data system.
- **iData status:** Discontinued as a single iData dataset; data by topic remains.

**Overview:** After migration from EcOS to iData, IFS should be treated as a legacy source family rather than a single iData database. Current iData coverage is split across topic datasets; use `SKILL.md` for the operational routing policy.

**Topic datasets replacing legacy IFS coverage:**

1. **Labor Force Statistics (LS)**
2. **Consumer Price Index (CPI)**
3. **Fund Accounts (FA)**
4. **Effective Exchange Rate (EER)**
5. **Exchange Rate (ER)**
6. **National Economic Accounts (NEA), Quarterly Data**
7. **National Economic Accounts (NEA), Annual Data**
8. **Special Purpose Entities (SPE)**
9. **Balance of Payments (BOP)**
10. **International Investment Position (IIP)**
11. **Currency Composition of the International Investment Position (IIP)**
12. **Production Indexes (formerly IPI)**
13. **Producer Price Indexes (PPI)**
14. **International Liquidity (IL)**
15. **International Trade in Goods (ITG)**
16. **Quarterly Government Finance Statistics (GFS)**
17. **Monetary and Financial Statistics (MFS): Central Bank Data**
18. **Monetary and Financial Statistics (MFS): Depository Corporations**
19. **Monetary and Financial Statistics (MFS): Financial Corporations**
20. **Monetary and Financial Statistics (MFS): Other Financial Corporations**
21. **Monetary and Financial Statistics (MFS): Other Depository Corporations**

## Bloomberg Data License
- **Database:** `IMF.CSF:BBGDL`
- **Status:** Specialized catalog.

**Overview:** Bloomberg Data License is an internal Bloomberg market-data feed covering tickers across major asset classes and geographies. Entries are identified by Bloomberg ticker codes and descriptive names, with standard Bloomberg suffixes such as `_EQUITY`, `_GOVT`, `_CORP`, `_CURNCY`, `_INDEX`, and `_COMDTY`.

**Key content:**

1. **Equities:** Global listed stocks and equity market instruments.
2. **Fixed income:** Government bonds, sovereign yields, corporate bonds, and spread indices.
3. **Foreign exchange:** Spot rates, cross rates, forwards, NDFs, options, and implied volatility.
4. **Rates and derivatives:** Interest rate swaps, OIS, FRAs, basis swaps, inflation swaps, policy rates, and repo rates.
5. **Credit:** Sovereign and corporate CDS spreads.
6. **Commodities:** Energy, metals, and agricultural futures and spot prices.
7. **Indices and macro series:** Equity indices, macroeconomic indicators, economic sentiment, policy uncertainty, and selected tracking datasets.

## World Development Indicators
- **Database:** `WB:WDI`
- **Status:** Specialized catalog.

**Overview:** World Development Indicators is the World Bank's broad development statistics database. It covers countries worldwide and includes hundreds of indicators on economic conditions, public finance, finance, environment, health, education, labor markets, poverty, governance, and demographics.

**Key content:**

1. **Economy and national accounts:** GDP, GNI, inflation, exchange rates, savings, consumption, and capital formation.
2. **Trade and balance of payments:** Exports, imports, FDI, current account balances, remittances, tariffs, and terms of trade.
3. **Public finance and debt:** Government revenue, tax structure, expenditure, central government debt, external debt, and official development assistance.
4. **Financial sector and markets:** Banking indicators, domestic credit, interest rates, broad money, stock market capitalization, and financial inclusion.
5. **Energy, environment, and climate:** Electricity access, energy consumption, greenhouse gas emissions, air pollution, protected areas, freshwater resources, and threatened species.
6. **Health and population:** Life expectancy, mortality, disease prevalence, immunization, health expenditure, sanitation, fertility, population, and urbanization.
7. **Education and human capital:** Literacy, enrollment, educational attainment, pupil-teacher ratios, public education spending, and human capital measures.
8. **Labor, poverty, and governance:** Employment, unemployment, labor force participation, poverty, inequality, social protection, governance, gender equality, conflict, and migration.

## WTO-IMF Tariff Tracker
- **Database:** `WTO:WTOIMFTT`
- **Status:** Specialized catalog.

**Overview:** WTO-IMF Tariff Tracker contains detailed internationally traded goods classifications based on 6-digit Harmonized System commodity codes. It supports analysis of tariffs and goods trade across broad product groups.

**Key content:**

1. **Agriculture and food (HS 01-24):** Wheat, maize, beef, cane sugar, and other agricultural or food products.
2. **Minerals and fuels (HS 25-27):** Crude oil, natural gas, copper ores, electricity, and related products.
3. **Chemicals and pharmaceuticals (HS 28-38):** Medicaments, fertilizer, insecticides, titanium oxides, and other chemical products.
4. **Plastics, rubber, wood, and paper (HS 39-49):** Polyethylene, natural rubber, rough wood, newsprint, and related goods.
5. **Textiles and apparel (HS 50-67):** Raw cotton, T-shirts, footwear, jerseys, and related products.
6. **Metals and metal products (HS 68-83):** Hot-rolled steel, refined copper, unwrought aluminum, unwrought gold, and other metal goods.
7. **Machinery and electronics (HS 84-85):** Laptops, smartphones, processors, lithium-ion batteries, and other machinery or electronic goods.
8. **Transport, instruments, and miscellaneous goods (HS 86-97):** Passenger cars, aircraft, medical instruments, furniture, and other manufactured products.

## Haver Analytics
- **Database:** `HAVER:<database_code>` (200+ databases; specify by sub-database code, e.g. `HAVER:USECON`, `HAVER:EMERGE`)
- **Status:** External service. Access via `haver_utilities`; use `scripts/Haver/haver_catalog_search.py` for indicator lookup and `fetch_haver.py` for retrieval.
- **Coverage:** 1945–present. Annual, quarterly, monthly, weekly, and daily frequencies. Global.

**Overview:** Haver Analytics provides economic, financial, industry, and forecast data for advanced and emerging economies, drawing on 200+ databases from over 750 government and private sources. It covers US macro and regional detail, global country summaries, high-frequency financial and daily series, industry statistics, fund flows, third-party forecasts, and data from major international organizations including the IMF, BIS, and IIF.

**Sub-database catalog by category:**

1. **United States macro detail (`USECON` and related):** Core US national accounts (`USNA`), capital stock (`CAPSTOCK`), payroll employment (`LABOR`), household employment (`EMPL`), covered employment and wages (`CEW`), occupational employment (`OES`), industrial production (`IP`), consumer prices (`CPIDATA`), producer prices (`PPI`, `PPIR`), international transactions (`USINT`), trade detail (`USTRADE`), surveys (`SURVEYS`), flow of funds (`FFUNDS`), and government finance (`GOVFIN`).

2. **High-frequency and financial data:** US daily (`DAILY`), global daily (`INTDAILY`), US weekly (`WEEKLY`), global weekly (`INTWKLY`), and cryptocurrency statistics (`CRYPTO`). Third-party: bond indexes (`BONDINDX`).

3. **EPFR Global fund flows:** Equity fund sector/industry allocations and flows (`EPFRESA`, `EPFRESF`), equity fund flows by country group (`EPFREIN`, `EPFREEM`), bond fund flows (`EPFRBIN`, `EPFRBEM`, `EPFRBMM`), and country-level allocations and flows for equities and bonds (`EPFRECA`, `EPFRBCA`, `EPFRECF`, `EPFRBCF`). Daily variants: `EPRDEFF`, `EPFRDECF`, `EPFRDBFF`, `EPFRDBCF`, `EPFRDESF`.

4. **Industry and global sector detail:** Quarterly Financial Report (`QFR`), Annual Survey of Manufactures (`ASM`), Baltic freight indexes (`BALTIC`), global sector statistics (`GLSECTOR`), transportation (`TRANSPRT`), tourism (`TOURISM`).

5. **Energy detail:** Global energy statistics (`ENERGY`), weekly electric output (`EEI`), and JODI oil database (`JODI`).

6. **Advanced economies — country summaries and detail:** G10 summary (`G10`), and country-specific databases for Australia/New Zealand (`ANZ`), Belgium/Netherlands/Luxembourg (`BENELUX`), Canada (`CANADA`), Euro area/EU (`EUDATA`), France (`FRANCE`), Germany (`GERMANY`), Ireland (`IRELAND`), Italy (`ITALY`), Japan (`JAPAN`), Nordic countries (`NORDIC`), Spain (`SPAIN`), UK (`UK`), and Andorra/Austria/Cyprus/Greece/Malta/Portugal/Switzerland (`ALPMED`).

7. **Europe detail:** European national accounts (`EUNA`), surveys (`EUSURVYS`), financial accounts (`EUFIN`), debt securities (`EUSEC`), government finance (`EUGOV`), regional labor (`EULABOR`), European Commission macro forecasts (`AMECO`), international transactions (`EUINT`), demographics (`EUPOP`), and trade detail (`EUTRADE`).

8. **Emerging markets:** Country summaries (`EMERGE`), Latin America (`EMERGELA`), Asia Pacific (`EMERGEPR`), Central/Eastern Europe and Western Asia (`EMERGECW`), Middle East and Africa (`EMERGEMA`). Country surveys (`INTSURVYS`) and ESG indicators (`ESG`).

9. **Advanced and emerging market regional databases:** Country-level regional breakdowns for Australia/NZ, Canada, France, Germany, Italy, Japan, Spain, UK, Cyprus/Portugal/Switzerland, MENA (`MENAR`), and Sub-Saharan Africa (`SUBAFR`).

10. **Third-party forecasts and surveys:** Macroeconomic Advisers/S&P Global short-term quarterly forecasts (`MA4CAST`), IIF forecasts (`IIFDATA`), US GDP headline as-reported tables (`ASREPGDP`), Blue Chip consensus forecasts (`BLUECHIP`), and Markit/S&P Global Purchasing Managers surveys (`MKTPMI`).

11. **International organization data:** BIS statistics including QEDS and JEDH (`BIS`); IMF IFS monthly/quarterly (`IFS`) and annual (`IFSANN`), Direction of Trade monthly (`IMFDOTM`) and annual (`IMFDOT`), Balance of Payments quarterly (`IMFBOP`) and annual (`IMFBOPA`), CPIS (`CPIS`), CDIS (`CDIS`), WEO annual (`IMFWEO`), and Regional Economic Outlook (`IMFREO`).

12. **US regional:** Selected regional indicators (`REGIONAL`, `REGIONW`), regional demographics (`USPOP`), gross state product (`GSP`), mortgage delinquencies by state (`MBAMTG`), state government finance (`GOVFIN`), and regional employment by state and county (`EMPLR`, `EMPLC`, `CEWR`).

13. **FX rates:** Monthly FX rates for conversion (`FXRATES`).

14. **Archives:** Discontinued and pre-revision vintages for US national accounts, Euro area series, CANSIM (Canada), and annual US press release archives from 2004–2024 (`USARC04`–`USARC24`, `EUARC`, `EUARC18`, `CANSIM`, `CANSIMR`, `GLARC`, `USNA09`, `USNA92`, `USNA96`, `USNA13`).

# Database Overview

This file summarizes commonly used non-vintaged datasets. Metadata fields are aligned with `non_vintaged_datasets.csv`.

## World Economic Outlook (WEO) Live
- **Database:** `IMF.RES.WEO:WEO_LIVE`

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

**Overview:** WEO provides a compact set of core macroeconomic indicators, typically at annual frequency, alongside extensive commodity price data. It is useful for country-level macro analysis, projections, and cross-country comparison.

**Key content:**

1. **Macroeconomic aggregates:** GDP at constant and current prices, inflation, unemployment, trade volumes, fiscal balances, public debt, and external debt.
2. **Commodity prices:** Unit prices and price indices for energy, metals, food, beverages, agricultural raw materials, and other commodities.
3. **Forecast-oriented series:** Historical and projected values for major macroeconomic variables used in WEO analysis.

## Global Economic Environment (GEE) Live
- **Database:** `IMF.RES.GEE:GEE_LIVE`

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

**Overview:** BOP is the IMF Balance of Payments Statistics database. It follows the BPM6 framework and provides a comprehensive catalog of balance of payments indicators covering the current account, capital account, financial account, aggregate balances, and exceptional financing items.

**Key content:**

1. **Current account:** Goods, services, primary income, secondary income, and current account balances.
2. **Capital account:** Capital transfers and nonproduced nonfinancial assets.
3. **Financial account:** Direct investment, portfolio investment, other investment, reserve assets, and financial derivatives.
4. **Sector and maturity detail:** Breakdowns by institutional sector, such as central bank, deposit-taking corporations, and general government, and by short-term or long-term maturity where available.
5. **Analytical balances:** Aggregate balances and financing items used in external-sector analysis.

## Bloomberg Data License
- **Database:** `IMF.CSF:BBGDL`

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

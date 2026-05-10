---
title: "IMF datatools Agent API Reference"
source_pdf: "imf_datatools_doc.pdf"
source_doc_date: "2025-09-20"
refined_for: "local coding agents"
status: "agent-optimized reference distilled from the full IMF datatools documentation"
---

# IMF datatools Agent API Reference

This file is a cleaned, agent-oriented reference for the `imf_datatools` Python package. It is designed for local coding agents that need to select the right data source, call the right function, and produce reliable retrieval code with minimal ambiguity.

The package retrieves IMF and external time-series data and metadata from multiple sources, usually returning `pandas.DataFrame` objects. The original documentation also includes R and Stata usage; this reference prioritizes Python and keeps R/Stata notes where they matter for integration.

---

## 0. How an agent should use this file

### Default decision logic

1. **Prefer iData for new IMF data workflows** when the dataset has migrated or is available there.
2. **Use the EcOS-to-iData mapper** when maintaining old EcOS code or translating old country/series codes.
3. **Use EcOS only for legacy workflows** or when the target dataset has not yet migrated.
4. **Use EDI / data.imf.org / Data Mapper** for public-facing IMF APIs where appropriate.
5. **Use Haver, World Bank, Eurostat, BIS, SQL, DMX/DMXe** only when the requested source is explicit.
6. **Avoid broad `ALL` queries** unless the user explicitly needs full database extraction; loop over smaller requests to avoid limits and timeouts.
7. **Use metadata functions first** when database names, dimensions, countries, indicators, or valid codes are unknown.

### Common return convention

Most retrieval functions return a `pandas.DataFrame` with a `DatetimeIndex` named or representing `dates`. Monthly, quarterly, and annual dates are normally aligned to the **start of the period**:

- monthly February 2020 -> `2020-02-01`
- quarterly 2020Q2 -> `2020-04-01`
- annual 2019 -> `2019-01-01`

### Common options

| Option | Meaning |
|---|---|
| `debug=False` | Set `True` to print more detail and sometimes write intermediate files locally. |
| `longformat=False` | Set `True` to return long/tidy data instead of wide time-series columns. |
| `scale` | Apply numeric scale where supported. Common values include source/default scale options. |
| `scale_label` | Include scale labels in output column names or metadata where supported. |
| `freq` | Frequency. Common values: `A`, `Q`, `M`, `D`; some functions allow combined values such as `QA`. |

### Standard safe coding pattern

```python
import pandas as pd
from imf_datatools import idata_utilities

# 1. Discover available database / dimensions / valid codes first.
dbs = idata_utilities.get_databases(keyword="CPI")
dims = idata_utilities.get_dimensions("IMF.STA:CPI")
countries = idata_utilities.get_dimension_values("IMF.STA:CPI", "COUNTRY", keyword=["United States", "Japan"])

# 2. Build a valid iData key from dimension values.
key = "USA+JPN.CPI._T.IX.M"

# 3. Retrieve data.
df = idata_utilities.get_idata_data("IMF.STA:CPI", key=key, start="2000", end="2025")
```

---

# 1. Installation and environment

## 1.1 Workstation installation

Install or update the Python library from Command Prompt:

```powershell
python \\ecnswn12p\ems_shared\pub\datatools\installer.py
```

Test installation:

```python
import imf_datatools
```

## 1.2 R integration

R uses Python through `reticulate`. Set the Python path first:

```r
install.packages("reticulate")
library(reticulate)
use_python("C:/ProgramData/Python3", required = TRUE)
imf_datatools <- import("imf_datatools")
```

Example:

```r
df <- imf_datatools$get_haver_data("GDP@USECON")
tail(df)
```

If another R package masks `import()`, use:

```r
reticulate::import("imf_datatools")
```

## 1.3 Stata integration

Set Python path in Stata:

```stata
set python_exec C:\ProgramData\Python3\python.exe, perm
```

Install Stata command wrappers:

```stata
installdatatools
```

Useful Stata help commands:

```stata
help ediuse
help ecosuse
help dmxsuse
help dmxeuse
help sqlsuse
```

Test:

```stata
ediuse data, database(weo-published) country(111) indicator(NGDP) vintage(2023-10) clear
```

## 1.4 Econometric Support servers

Server environments may already include `imf_datatools`. Test in Command Prompt:

```python
import imf_datatools
```

Important limitation: **DMX file access is not available on Econometric Support servers** because required Microsoft Access drivers are unavailable.

---

# 2. Global coding conventions

## 2.1 Time index

All retrieved time-series data generally use period-start dates. This makes mixed-frequency merging easier but can surprise users expecting end-of-period dates.

## 2.2 Metadata-first approach

When a requested series fails, do not guess codes. Use metadata discovery:

```python
# iData
idata_utilities.get_databases(keyword="...")
idata_utilities.get_dimensions(db)
idata_utilities.get_dimension_values(db, dimension, keyword="...")

# EcOS
ecos_sdmx_utilities.get_databases(substr="...")
ecos_sdmx_utilities.get_countries(dbname)
ecos_sdmx_utilities.get_ecos_sdmx_metadata(dbname, substr="...")
```

## 2.3 Avoid excessive requests

EcOS has a 5,000-series response limit. Avoid `country='ALL'` and `var='ALL'` together unless absolutely necessary. Loop over countries, indicators, frequencies, or counterpart countries.

---

# 3. iData API

Use module:

```python
from imf_datatools import idata_utilities
```

iData is the newer Fund-wide data system and is planned to replace several legacy systems such as EcOS, EDI, data.imf.org, and Data Mapper.

## 3.1 Private / non-public iData access

All LIVE and vintage databases are private IMF datasets and **always** require this flag. Identify them by resource ID: LIVE databases do not contain `VINTAGE` (e.g. `IMF.RES.WEO:WEO_LIVE`); vintage snapshots contain `VINTAGE` (e.g. `IMF.RES.WEO:WEO_LIVE_2026_APR_VINTAGE`). Set the flag before any iData call in the session:

```python
from imf_datatools import idata_utilities
idata_utilities.PRIVATE = True
```

The pre-built fetch utility (`.claude/skills/imf-ra-data/scripts/fetch_idata.py`) sets this flag automatically. For any other non-public dataset, set the same flag. The flag is harmless for public datasets and can remain set throughout the session.

This triggers browser-based token acquisition when needed. Tokens expire and may need refresh. For R:

```r
datatools$idata_utilities$PRIVATE <- TRUE
```

For Stata:

```stata
idatause private
```

## 3.2 iData key format

`get_idata_data()` requires a dot-separated `key` built from dimension values in dimension order.

Example dataset: `IMF.STA:CPI` with dimensions:

1. `COUNTRY`
2. `INDEX_TYPE`
3. `COICOP_1999`
4. `TYPE_OF_TRANSFORMATION`
5. `FREQUENCY`

Example key:

```text
USA+JPN.CPI._T.IX.M
```

Rules:

- Use `.` to separate dimensions.
- Use `+` for multiple values within a dimension.
- Leave a dimension blank for an open query, e.g. `USA+JPN.CPI._T..M` opens `TYPE_OF_TRANSFORMATION`.
- Use metadata calls to discover dimension order and valid values.

## 3.3 Functions

### `idata_utilities.get_databases(keyword=None, searchmode='or', refresh=False, debug=False)`

Return available iData datasets as a `pandas.DataFrame`.

Parameters:

| Parameter | Use |
|---|---|
| `keyword` | `str` or iterable of strings used to filter dataset names/descriptions. |
| `searchmode` | `'or'` returns matches containing any keyword; `'and'` requires all keywords. |
| `refresh` | Force re-fetch instead of using in-memory cache. |
| `debug` | Print diagnostics. |

Example:

```python
from imf_datatools import idata_utilities

datasets = idata_utilities.get_databases(keyword=["sta", "cpi"])

idata_utilities.PRIVATE = True
datasets_all = idata_utilities.get_databases(refresh=True)
```

### `idata_utilities.get_dimensions(db: str, keyword=None, searchmode='or', refresh=False, debug=False)`

Return dimensions for an iData dataset, including dimension order.

Example:

```python
db = "IMF.STA:CPI"
dims = idata_utilities.get_dimensions(db)
```

### `idata_utilities.get_dimension_values(db, dimension, keyword=None, searchmode='or', refresh=False, debug=False)`

Return valid values for a given dimension.

Example:

```python
country_values = idata_utilities.get_dimension_values("IMF.STA:CPI", "COUNTRY")
republics = idata_utilities.get_dimension_values("IMF.STA:CPI", "COUNTRY", keyword="republic")
```

### `idata_utilities.get_idata_data(db: str, key, start=None, end=None, params=None, longformat=False, panel=None, debug=False)`

Retrieve iData observations.

Parameters:

| Parameter | Use |
|---|---|
| `db` | Dataset name, e.g. `'IMF.STA:CPI'`. |
| `key` | Dot-separated dimension key. |
| `start`, `end` | Optional period bounds. Formats: `'2020'`, `'2020-01'`, `'2020Q2'`. |
| `params` | Optional query parameters. |
| `longformat` | Return long/tidy data. |
| `panel` | Dimension name to use as panel identifier. Mutually exclusive with `longformat=True`. |
| `debug` | Diagnostics. |

Example: wide format

```python
db = "IMF.STA:CPI"
key = "USA+JPN.CPI._T.IX.M"
df = idata_utilities.get_idata_data(db, key=key, start="2000", end="2025")
```

Example: open one dimension

```python
key = "USA+JPN.CPI._T..M"  # TYPE_OF_TRANSFORMATION left open
df = idata_utilities.get_idata_data("IMF.STA:CPI", key=key)
```

Example: long format

```python
df_long = idata_utilities.get_idata_data("IMF.STA:CPI", key="USA+JPN.CPI._T.IX.M", longformat=True)
```

Example: panel format

```python
df_panel = idata_utilities.get_idata_data("IMF.STA:CPI", key="USA+JPN.CPI._T..M", panel="COUNTRY")
```

Date warning: for monthly or lower-frequency data, use period-level `end` values like `'2020-05'` or the final day of the month. `end='2020-05-30'` will not include May 2020 monthly data.

---

# 4. Mapping EcOS to iData

Use module:

```python
from imf_datatools.idata_mapper import *
```

Use this module when converting legacy EcOS calls to iData. Major changes in the migration include:

- Country codes are generally ISO3 in iData instead of IMF numeric codes such as `111` for the United States.
- Series codes may be split across several iData dimensions.
- Some databases, such as IFS, are split into multiple iData databases.
- Some legacy series are discontinued.

## 4.1 Functions

### `get_mapping_data(ecos_db: str, ecos_series: str, force_update=False, debug=False)`

Return mapping data between an EcOS database/series and iData equivalents. Mostly a diagnostic utility; agents should usually call `map_db_and_series()` directly.

Special case: `ecos_series='ALL'` retrieves all mappings for the database, which can be large.

```python
mapping = get_mapping_data("WEO_WEO_PUBLISHED", ecos_series="ALL")
```

### `get_mapping(ecos_db: str, ecos_series: str, force_update=False, debug=False)`

Return internal mapping objects:

```python
idata_db, series_mapping, dict_series_idata_db = get_mapping(ecos_db, ecos_series)
```

Mostly for diagnostics.

### `map_db_and_series(ecos_db, ecos_series)`

Map an EcOS database and series code to iData database and series key fragment.

```python
from imf_datatools.idata_mapper import map_db_and_series

idata_db, idata_series = map_db_and_series("WEO_WEO_PUBLISHED", "NGDP")
# Example result: ('IMF.RES.WEO:WEO_LIVE_2025_APR_VINTAGE', 'NGDP')
```

IFS example:

```python
idata_db, idata_series = map_db_and_series("ECDATA_IFS_Latest_Published", "PCPI_IX")
# Example result: ('IMF.STA:CPI', 'CPI._T.SPR_IX')
```

### `map_bloomberg_ticker(ecos_ticker)`

Map a Bloomberg ticker from EcOS to iData. Internally strips whitespace and converts to uppercase.

```python
idata_db, idata_ticker = map_bloomberg_ticker("VIX Index")
# Example result: ('IMF.CSF:BBGDL', 'VIX_INDEX')
```

### `get_countrylist(idata_db='IMF.RES:WEO')`

Return country dimension values for the specified iData database. Mostly diagnostic.

```python
countries = get_countrylist("IMF.RES:WEO")
```

### `translate_ecos_country(ecos_country, idata_db='IMF.RES:WEO')`

Translate an EcOS IMF country code into the iData country equivalent, typically ISO3.

```python
iso3 = translate_ecos_country("111")
# 'USA'
```

Country groups may fail if the group code cannot be matched through Enterprise Business Vocabularies.

### `get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=None)`

Testing helper that retrieves iData data using EcOS-like arguments. Not recommended for production code; prefer explicit mapping plus `idata_utilities.get_idata_data()`.

```python
df = get_idata_data_using_ecos(
    "ECDATA_DOT",
    ecos_country="111",
    ecos_series="TXG_FOB_USD",
    freq="A",
    ecos_counterpart="193",
)
```

## 4.2 Recommended migration pattern

```python
from imf_datatools import ecos_sdmx_utilities, idata_utilities
from imf_datatools.idata_mapper import map_db_and_series, translate_ecos_country

# Old EcOS identifiers
ecos_db = "ECDATA_CPI_LATEST_PUBLISHED"
ecos_series = "PCPI_IX"
ecos_country = "111"
freq = "Q"

# Translate
data_db, idata_series = map_db_and_series(ecos_db, ecos_series)
idata_country = translate_ecos_country(ecos_country)

# Build iData key and retrieve
data_key = f"{idata_country}.{idata_series}.{freq}"
df_idata = idata_utilities.get_idata_data(data_db, data_key)
```

---

# 5. EcOS API

Use module:

```python
from imf_datatools import ecos_sdmx_utilities
```

EcOS is a legacy IMF data system. It requires Fund authentication. Initial connection may take 10–20 seconds. EcOS database names often start with:

- `WEO_` for RES-owned WEO databases
- `ECDATA_` for many other departmental databases

Important constraint: EcOS web service returns up to **5,000 series** per request. If too broad a query returns exactly 5,000 series, `imf_datatools` warns instead of returning complete data.

## 5.1 EcOS discovery functions

### `ecos_sdmx_utilities.get_databases(substr=None, debug=False)`

Return sorted list of available EcOS database names. `substr` can be a string or list; list means all substrings must match.

```python
dbs = ecos_sdmx_utilities.get_databases(substr="WEO")
dbs_2018 = ecos_sdmx_utilities.get_databases(substr=["WEO", "2018"])
```

### `ecos_sdmx_utilities.get_weo_databases(debug=False)`

Return available WEO vintages as a `DataFrame`, sorted chronologically.

```python
weo_dbs = ecos_sdmx_utilities.get_weo_databases()
```

### `ecos_sdmx_utilities.get_data_structure(database, debug=False)`

Return raw structure for an EcOS database, including countries, indicators, and attributes. Usually used indirectly.

```python
structure = ecos_sdmx_utilities.get_data_structure("WEO_WEO_PUBLISHED")
```

### `ecos_sdmx_utilities.get_all_series(dbname, update=True, substr=None, debug=False)`

Return available series codes for a database.

```python
series = ecos_sdmx_utilities.get_all_series("WEO_WEO_PUBLISHED", substr="GDP")
```

### `ecos_sdmx_utilities.get_countries(dbname, debug=False)`

Return countries and country codes for a database.

```python
countries = ecos_sdmx_utilities.get_countries("WEO_WEO_PUBLISHED")
```

### `ecos_sdmx_utilities.get_ecos_sdmx_metadata(dbname, seriesname=None, substr=None, debug=False)`

Return metadata for EcOS series. Use `seriesname` for exact codes; `substr` for partial matching.

```python
metadata = ecos_sdmx_utilities.get_ecos_sdmx_metadata(
    "ECDATA_DOT_LATEST_PUBLISHED",
    seriesname=["TBG_USD", "TMG_CIF_USD"],
)

usd_series = ecos_sdmx_utilities.get_ecos_sdmx_metadata(
    "ECDATA_DOT_LATEST_PUBLISHED",
    substr="USD",
)
```

### `ecos_sdmx_utilities.get_ecos_gfs_metadata(sector, unit, classification, database='ECDATA_GFS_T2_EXPENSE', debug=False)`

Retrieve metadata for GFS databases, which use a different internal structure.

```python
metadata = ecos_sdmx_utilities.get_ecos_gfs_metadata(
    sector=["S13", "S1313", "S1311"],
    unit=["XDC", "XDC_R_B1GQ"],
    classification=["W0|S1|G2", "W0|S1|G21"],
)
```

## 5.2 EcOS retrieval functions

### `ecos_sdmx_utilities.get_ecos_sdmx_data(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None, longformat=False, scale=None, scale_label=None, use_original_indicator=False, get_data=True, debug=False)`

Main EcOS retrieval function.

Parameters:

| Parameter | Use |
|---|---|
| `database` | EcOS database name, e.g. `'WEO_WEO_PUBLISHED'`. |
| `country` | IMF country code, list of codes, or `'ALL'`. |
| `var` | Series code, list of codes, or `'ALL'`. |
| `counterpart` | Counterpart country for bilateral datasets such as DOT. |
| `freq` | Frequency. Default `'A'`; can use `'Q'`, `'M'`, or combined e.g. `'QA'`. |
| `sector`, `counterpart_sector` | For datasets needing sector/counterpart sector. |
| `longformat` | Return long/tidy format. |
| `scale`, `scale_label` | Apply/include scale details where supported. |
| `use_original_indicator` | Useful for special GAS behavior where returned indicator differs from requested code. |
| `get_data` | If `False`, returns attributes instead of observations. |
| `debug` | Diagnostics. |

Basic WEO example:

```python
df = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "WEO_WEO_PUBLISHED",
    country="111",
    var="NGDP",
)
```

Quarterly data:

```python
df_q = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "WEO_WEO_PUBLISHED",
    "111",
    "NGDP",
    freq="Q",
)
```

Multiple countries / variables:

```python
df = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "WEO_WEO_PUBLISHED",
    country=["111", "193"],
    var=["NGDP", "PPPPC"],
)
```

DOT bilateral example:

```python
df = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "ECDATA_DOT_LATEST_PUBLISHED",
    country="111",
    var="TBG_USD",
    counterpart="193",
)
```

Special GAS example:

```python
# Preserve requested indicator name in output
fuel = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "WEO_GAS_LIVE",
    "001",
    "POILAPSP",
    use_original_indicator=True,
)
```

### `ecos_sdmx_utilities.get_series_attributes(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None, longformat=False, debug=False)`

Return attributes for an EcOS series. Especially useful in WEO for scale, source, latest actual data, and forecast identification.

```python
attrs = ecos_sdmx_utilities.get_series_attributes("WEO_WEO_PUBLISHED", "111", "NGDP")
```

### `ecos_sdmx_utilities.get_ecos_gfs_data(country, sector=None, unit=None, classification=None, scale=None, scale_label=None, longformat=False, freq='A', database='ECDATA_GFS_T2_EXPENSE', debug=False)`

Retrieve GFS data. Use GFS metadata first to identify valid `sector`, `unit`, and `classification` values.

```python
df = ecos_sdmx_utilities.get_ecos_gfs_data(
    country="111",
    sector="S13",
    unit="XDC",
    classification="W0|S1|G2",
)
```

### `ecos_sdmx_utilities.get_ecos_commodity_data(database, commodity, datatype=None, freq='A', longformat=False, scale=None, scale_label=False, debug=False)`

Retrieve commodity data from EcOS commodity-style databases. These do not use country codes and therefore are not compatible with the EcOS-to-iData mapper.

```python
df = ecos_sdmx_utilities.get_ecos_commodity_data(
    database="...",
    commodity="...",
    datatype="...",
    freq="M",
)
```

### `ecos_sdmx_utilities.get_ecos_bloomberg_data(ticker, field, freq='D', debug=False)`

Retrieve Bloomberg data from EcOS.

```python
df = ecos_sdmx_utilities.get_ecos_bloomberg_data("VIX Index", "PX_LAST")
```

Ticker and field can be lists. Field can be `'ALL'`, but broad queries may be expensive.

Bloomberg daily data are business-day observations converted to daily frequency; weekends become `NaN`. To keep only business days:

```python
df_bday = df.resample("B").mean()
# or drop all NaN values
clean = df.dropna()
```

### `ecos_sdmx_utilities.get_weo_country_codes(save=False)`

Return WEO country and group codes, merged with World Bank country information where available.

```python
codes = ecos_sdmx_utilities.get_weo_country_codes(save=True)
```

### `ecos_sdmx_utilities.get_ebv_country_info(save=False)`

Return country information from Enterprise Business Vocabularies merged with World Bank information.

```python
ebv = ecos_sdmx_utilities.get_ebv_country_info(save=True)
```

### `ecos_sdmx_utilities._get_time_series_attributes(database, country, var, counterpart=None, sector=None, counterpart_sector=None, freq='A', debug=False)`

Internal/advanced function returning detailed time-series attributes. Use only when `get_series_attributes()` is insufficient.

---

# 6. DMX API

Use module:

```python
from imf_datatools import dmx_utilities
```

DMX files are Microsoft Access database files used by country desks. They require ODBC / Access drivers, usually installed through the Data Management for Excel add-in. DMX access does not work on Econometric Support servers.

### `dmx_utilities.get_all_series(dmxfilename, substr=None, debug=False)`

Return available series codes in a `.dmx` file.

```python
series = dmx_utilities.get_all_series(r"C:\ProgramData\IMF\DMX\Samples\sample.dmx")
series_be = dmx_utilities.get_all_series(r"C:\ProgramData\IMF\DMX\Samples\sample.dmx", substr=["911", "BE"])
```

### `dmx_utilities.get_dmx_data(dmxfilename, seriesname, freq=None, scale=None, scale_label=False, debug=False)`

Retrieve one or more series from a `.dmx` file.

```python
df = dmx_utilities.get_dmx_data(
    r"C:\ProgramData\IMF\DMX\Samples\sample.dmx",
    "911BF",
)

df_multi = dmx_utilities.get_dmx_data(
    r"C:\ProgramData\IMF\DMX\Samples\sample.dmx",
    ["911BF", "911BCA_GDP"],
)
```

### `dmx_utilities.get_dmx_metadata(dmxfilename, seriesname=None, substr=None, standard=False, debug=False)`

Retrieve metadata from a `.dmx` file. Use `seriesname`, `substr`, or a list of series.

```python
metadata = dmx_utilities.get_dmx_metadata(
    r"C:\ProgramData\IMF\DMX\Samples\sample.dmx",
    seriesname="911BF",
)
```

---

# 7. DMXe API

Use module:

```python
from imf_datatools import dmxe_utilities
```

DMXe is the sqlite-based successor to DMX.

### `dmxe_utilities.get_all_series(dmxfilename, substr=None, debug=False)`

Return available series codes in a `.dmxe` file.

```python
series = dmxe_utilities.get_all_series(r"\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe")
```

### `dmxe_utilities.get_dmxe_data(dmxfilename, seriesname, freq=None, scale=None, scale_label=False, debug=False)`

Retrieve one or more series from a `.dmxe` file.

```python
dmxefile = r"\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe"
df = dmxe_utilities.get_dmxe_data(dmxefile, "646BCA")
df_multi = dmxe_utilities.get_dmxe_data(dmxefile, ["646BCA", "646BCAXGT"])
```

### `dmxe_utilities.get_dmxe_metadata(dmxfilename, seriesname=None, substr=None, debug=False)`

Retrieve metadata from a `.dmxe` file.

```python
metadata = dmxe_utilities.get_dmxe_metadata(dmxefile, seriesname="646BCA")
```

---

# 8. SQL API

Use module:

```python
from imf_datatools import sql_utilities
```

SQL utilities retrieve series stored in SQL data tables such as DMX-style SQL databases.

### `sql_utilities.get_all_series(server, dbname, substr=None, debug=False)`

Return available series codes in a SQL database.

```python
series = sql_utilities.get_all_series("PRDDMXSQL", "DMX_WDI", substr=["111", "GDP"])
```

### `sql_utilities.get_sql_data(server, dbname, seriesname, freq=None, scale=None, scale_label=False, debug=False)`

Retrieve one or more SQL-backed time series.

```python
df = sql_utilities.get_sql_data("PRDDMXSQL", "DMX_WDI", "111.SP.POP.TOTL")
```

### `sql_utilities.get_sql_metadata(server, dbname, seriesname=None, substr=None, standard=False, debug=False)`

Retrieve SQL-backed metadata.

```python
metadata = sql_utilities.get_sql_metadata("PRDDMXSQL", "DMX_WDI", substr="POP")
```

---

# 9. Haver API

Use module:

```python
from imf_datatools import haver_utilities
```

Haver series are typically referenced as `SERIES@DATABASE`, e.g. `GDP@USECON`.

### `haver_utilities.get_databases()`

Return available Haver databases.

```python
dbs = haver_utilities.get_databases()
```

### `haver_utilities.get_haver_data(code, scale=None, eop=False, periods=False, debug=False)`

Retrieve Haver data.

Parameters:

| Parameter | Use |
|---|---|
| `code` | Haver code string or list, e.g. `'GDP@USECON'`. |
| `scale` | Optional scale handling. |
| `eop` | Align dates to end-of-period if supported. |
| `periods` | Return period labels rather than dates where supported. |

```python
df = haver_utilities.get_haver_data("GDP@USECON")
```

### `haver_utilities.get_haver_metadata(code, debug=False)`

Retrieve metadata for a Haver series.

```python
meta = haver_utilities.get_haver_metadata("GDP@USECON")
```

### `haver_utilities.get_all_haver_metadata(database)`

Retrieve metadata for all series in a Haver database.

```python
all_meta = haver_utilities.get_all_haver_metadata("USECON")
```

---

# 10. World Bank API

Use module:

```python
from imf_datatools import worldbank_utilities
```

### `worldbank_utilities.get_database_info()`

Return general World Bank database information.

```python
info = worldbank_utilities.get_database_info()
```

### `worldbank_utilities.get_all_worldbank_metadata(debug=False)`

Return metadata for all World Bank indicators.

```python
metadata = worldbank_utilities.get_all_worldbank_metadata()
```

### `worldbank_utilities.get_worldbank_countries(debug=False)`

Return World Bank country list.

```python
countries = worldbank_utilities.get_worldbank_countries()
```

### `worldbank_utilities.get_worldbank_data(seriesname, country, counterpart=None, freq='A', longformat=False, dataformat='json', debug=False)`

Retrieve World Bank indicator data.

```python
df = worldbank_utilities.get_worldbank_data(
    seriesname="SP.POP.TOTL",
    country="USA",
)
```

Country and series may support lists depending on source behavior.

### `worldbank_utilities.get_worldbank_metadata(seriesname)`

Retrieve metadata for one World Bank series.

```python
meta = worldbank_utilities.get_worldbank_metadata("SP.POP.TOTL")
```

### `worldbank_utilities.search_worldbank_metadata(search_str, debug=False)`

Search World Bank metadata.

```python
matches = worldbank_utilities.search_worldbank_metadata("population total")
```

### `worldbank_utilities.get_worldbank_topics(debug=False)`

Return World Bank topic list.

```python
topics = worldbank_utilities.get_worldbank_topics()
```

---

# 11. EDI API

Use module:

```python
from imf_datatools import edi_utilities
```

EDI provides access to public/standard IMF datasets through a consistent interface.

### `edi_utilities.get_databases(debug=False)`

Return available EDI databases.

```python
dbs = edi_utilities.get_databases()
```

### `edi_utilities.get_dimensions(database, input_only=True, debug=False)`

Return dimensions for an EDI database.

```python
dims = edi_utilities.get_dimensions("weo-published")
```

### `edi_utilities.get_dimension_values(database, dimension, substr=None, debug=False)`

Return valid values for an EDI dimension.

```python
values = edi_utilities.get_dimension_values("weo-published", "country", substr="United")
```

### `edi_utilities.get_edi_data_from_url(url, add_vintage=False, scale_factor=1, scale_label=False, longformat=False, debug=False)`

Retrieve data from an EDI URL. Useful when a fully formed EDI request URL already exists.

```python
df = edi_utilities.get_edi_data_from_url(url, longformat=True)
```

### `edi_utilities.get_edi_haver_data(havercode, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve Haver-style EDI data or return the URL.

```python
df = edi_utilities.get_edi_haver_data("GDP@USECON")
url = edi_utilities.get_edi_haver_data("GDP@USECON", get_url=True)
```

### `edi_utilities.get_edi_bloomberg_data(ticker, field, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve Bloomberg-style EDI data or URL.

```python
df = edi_utilities.get_edi_bloomberg_data("VIX Index", "PX_LAST")
```

### `edi_utilities.get_edi_weo_data(country, indicator, freq='A', vintage='current', add_vintage=False, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve WEO data via EDI.

```python
df = edi_utilities.get_edi_weo_data(
    country="111",
    indicator="NGDP",
    freq="A",
    vintage="current",
)
```

### `edi_utilities.get_edi_gfs_data(country, classification=None, sector=None, unit=None, freq='A', longformat=False, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve GFS data via EDI.

```python
df = edi_utilities.get_edi_gfs_data(
    country="111",
    classification="W0|S1|G2",
    sector="S13",
    unit="XDC",
)
```

### `edi_utilities.get_edi_wdi_data(country, indicator, freq='A', longformat=False, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve WDI data via EDI.

```python
df = edi_utilities.get_edi_wdi_data("111", "SP.POP.TOTL")
```

### `edi_utilities.get_edi_csd_desk_data(country, indicator, freq='A', vintage='current', vintagetimestamp=None, exercise=None, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve CSD desk data via EDI.

```python
df = edi_utilities.get_edi_csd_desk_data(
    country="111",
    indicator="...",
    vintage="current",
)
```

### `edi_utilities.get_edi_csd_ccx_data(country, indicator, freq='A', vintage='current', exercise=None, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve CSD CCX data via EDI.

```python
df = edi_utilities.get_edi_csd_ccx_data(country="111", indicator="...")
```

### `edi_utilities.get_edi_cf_data(country, indicator, longformat=False, freq=None, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieve CF data via EDI.

```python
df = edi_utilities.get_edi_cf_data(country="111", indicator="...")
```

### `edi_utilities.get_edi_metadata(database, country=None, indicator=None, freq=None, seriescode=None, vintage=None, debug=False)`

Retrieve EDI metadata.

```python
meta = edi_utilities.get_edi_metadata("weo-published", country="111", indicator="NGDP")
```

---

# 12. data.imf.org API

Use module:

```python
from imf_datatools import imf_ext_data_utilities
```

This covers external-facing IMF data APIs.

### `imf_ext_data_utilities.get_databases(debug=False)`

Return available data.imf.org databases.

```python
dbs = imf_ext_data_utilities.get_databases()
```

### `imf_ext_data_utilities.get_query_dimensions(database, debug=False)`

Return query dimensions for a database.

```python
dims = imf_ext_data_utilities.get_query_dimensions("IFS")
```

### `imf_ext_data_utilities.get_dimension_values(codelist, debug=False)`

Return values in a dimension codelist.

```python
values = imf_ext_data_utilities.get_dimension_values("CL_FREQ")
```

### `imf_ext_data_utilities.get_series_codes(database, debug=False)`

Return series codes for a data.imf.org database.

```python
series = imf_ext_data_utilities.get_series_codes("IFS")
```

### `imf_ext_data_utilities.get_country_codes(database, debug=False)`

Return country codes for a database.

```python
countries = imf_ext_data_utilities.get_country_codes("IFS")
```

### `imf_ext_data_utilities.get_imf_ext_data(database, *params, longformat=False, scale=None, scale_label=False, debug=False)`

Retrieve data from data.imf.org. The `*params` arguments follow the database-specific dimension order.

```python
df = imf_ext_data_utilities.get_imf_ext_data(
    "IFS",
    "M",       # frequency, example only
    "USA",     # area/country, example only
    "...",     # indicator, example only
)
```

Always discover dimensions first with `get_query_dimensions()` before constructing the call.

---

# 13. Data Mapper API

Use module:

```python
from imf_datatools import datamapper_utilities
```

### `datamapper_utilities.get_datamapper_data(indicators, country=None, longformat=False, debug=False)`

Retrieve Data Mapper data.

```python
df = datamapper_utilities.get_datamapper_data(
    indicators=["NGDP_RPCH"],
    country=["USA", "JPN"],
)
```

### `datamapper_utilities.get_datamapper_metadata(debug=False)`

Return indicator metadata.

```python
meta = datamapper_utilities.get_datamapper_metadata()
```

### Area code helpers

```python
countries = datamapper_utilities.get_country_codes()
regions = datamapper_utilities.get_region_codes()
groups = datamapper_utilities.get_group_codes()
areas = datamapper_utilities.get_all_areas()
valid_areas = datamapper_utilities.get_var_areas("NGDP_RPCH")
```

Functions:

- `get_country_codes(debug=False)`
- `get_region_codes(debug=False)`
- `get_group_codes(debug=False)`
- `get_all_areas(debug=False)`
- `get_var_areas(indicator, debug=False)`

---

# 14. Eurostat API

Use module:

```python
from imf_datatools import eurostat_utilities
```

### `eurostat_utilities.get_datasets(dataset='all', lang='en')`

Return available Eurostat datasets.

```python
datasets = eurostat_utilities.get_datasets()
```

### `eurostat_utilities.set_args(timeout=None, cert=None)`

Set global request options such as timeout or certificate.

```python
eurostat_utilities.set_args(timeout=60)
```

### `eurostat_utilities.get_dimensions(dataset)`

Return dimensions for a Eurostat dataset.

```python
dims = eurostat_utilities.get_dimensions("nama_10_gdp")
```

### `eurostat_utilities.get_dimension_values(dataset, dimension)`

Return valid values for a dataset dimension.

```python
geo = eurostat_utilities.get_dimension_values("nama_10_gdp", "geo")
```

### `eurostat_utilities.get_data_structure(dataset, dim=None, full=False)`

Return Eurostat data structure.

```python
structure = eurostat_utilities.get_data_structure("nama_10_gdp", full=True)
```

### `eurostat_utilities.get_eurostat_data(dataset, dims={}, longformat=False, flags=False)`

Retrieve Eurostat data.

```python
df = eurostat_utilities.get_eurostat_data(
    "nama_10_gdp",
    dims={"geo": ["DE", "FR"], "freq": "A"},
    longformat=True,
)
```

---

# 15. BIS API

Use module:

```python
from imf_datatools import bis_utilities
```

### `bis_utilities.get_databases()`

Return available BIS databases.

```python
dbs = bis_utilities.get_databases()
```

### `bis_utilities.get_dimensions(dataset, refresh=False, debug=False)`

Return dimensions for a BIS dataset.

```python
dims = bis_utilities.get_dimensions("...")
```

### `bis_utilities.get_dimension_values(dataset, dimension, refresh=False, debug=False)`

Return valid values for a BIS dimension.

```python
values = bis_utilities.get_dimension_values("...", "...")
```

### `bis_utilities.get_bis_sdmx_data(db, key={}, params={}, longformat=False, debug=False)`

Retrieve BIS SDMX data.

```python
df = bis_utilities.get_bis_sdmx_data(
    db="...",
    key={"FREQ": "Q", "...": "..."},
    params={"startPeriod": "2000-Q1"},
)
```

### `bis_utilities.get_bis_data(db, code, start=None, end=None, longformat=False)`

Retrieve BIS data by database and code.

```python
df = bis_utilities.get_bis_data("...", code="...", start="2000", end="2025")
```

---

# 16. Writing to DMXe files

Use module:

```python
from imf_datatools import dmxe_writer_utilities
```

These functions modify DMXe files. Use them carefully and prefer writing to a copy during development.

### `dmxe_writer_utilities.save_dmxe_data(outfilename, df, freq=None, datecol=None, debug=False)`

Save a DataFrame to a DMXe file.

```python
dmxe_writer_utilities.save_dmxe_data(
    outfilename="output.dmxe",
    df=df,
    freq="A",
)
```

### `dmxe_writer_utilities.save_dmxe_metadata(outfilename, seriescode, dict_metadata, debug=False)`

Save metadata for a series.

```python
dmxe_writer_utilities.save_dmxe_metadata(
    "output.dmxe",
    seriescode="111NGDP",
    dict_metadata={"Description": "Nominal GDP"},
)
```

### `dmxe_writer_utilities.delete_dmxe_data(filename, series, freq, debug=False)`

Delete a series/frequency from a DMXe file.

```python
dmxe_writer_utilities.delete_dmxe_data("output.dmxe", series="111NGDP", freq="A")
```

### `dmxe_writer_utilities.rename_dmxe_data(filename, series, newseries, debug=False)`

Rename a series in a DMXe file.

```python
dmxe_writer_utilities.rename_dmxe_data("output.dmxe", "OLD_CODE", "NEW_CODE")
```

### `dmxe_writer_utilities.check_logs(filename, debug=False)`

Read modification logs.

```python
logs = dmxe_writer_utilities.check_logs("output.dmxe")
```

### `dmxe_writer_utilities.delete_logs(filename)`

Delete logs.

```python
dmxe_writer_utilities.delete_logs("output.dmxe")
```

### `dmxe_writer_utilities.read_dmxe_data(infilename, series, freq=None, debug=False)`

Read data from DMXe writer interface.

```python
df = dmxe_writer_utilities.read_dmxe_data("output.dmxe", series="111NGDP", freq="A")
```

### `dmxe_writer_utilities.set_dmxe_libdir(corepath, mappingpath)`

Set library paths used by the DMXe writer utilities.

```python
dmxe_writer_utilities.set_dmxe_libdir(corepath="...", mappingpath="...")
```

---

# 17. DataFrame utilities

Use module:

```python
from imf_datatools import dataframe_utilities as idt_utils
```

### `dataframe_utilities.merge_dfs(iterable_dfs, how='outer')`

Merge multiple DataFrames by index.

```python
from imf_datatools import dataframe_utilities as idt_utils

df_all = idt_utils.merge_dfs([df_ecos, df_sql, df_dmx], how="outer")
```

---

# 18. Agent recipes

## 18.1 Retrieve CPI from iData

```python
from imf_datatools import idata_utilities

# Discover dimensions if unknown
print(idata_utilities.get_dimensions("IMF.STA:CPI"))

# Retrieve monthly CPI index for USA and Japan
df = idata_utilities.get_idata_data(
    "IMF.STA:CPI",
    key="USA+JPN.CPI._T.IX.M",
    start="2000",
    end="2025",
)
```

## 18.2 Convert old EcOS WEO retrieval to iData

```python
from imf_datatools import idata_utilities
from imf_datatools.idata_mapper import map_db_and_series, translate_ecos_country

ecos_db = "WEO_WEO_PUBLISHED"
ecos_country = "111"
ecos_series = "NGDP"
freq = "A"

idata_db, idata_series = map_db_and_series(ecos_db, ecos_series)
iso3 = translate_ecos_country(ecos_country)
key = f"{iso3}.{idata_series}.{freq}"

df = idata_utilities.get_idata_data(idata_db, key)
```

## 18.3 Retrieve legacy EcOS WEO data

```python
from imf_datatools import ecos_sdmx_utilities

df = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "WEO_WEO_PUBLISHED",
    country="111",
    var="NGDP",
    freq="A",
)
```

## 18.4 Retrieve DOT bilateral data from EcOS

```python
from imf_datatools import ecos_sdmx_utilities

df = ecos_sdmx_utilities.get_ecos_sdmx_data(
    "ECDATA_DOT_LATEST_PUBLISHED",
    country="111",          # United States in IMF numeric code
    var="TXG_FOB_USD",
    counterpart="193",      # Australia in IMF numeric code
    freq="A",
)
```

## 18.5 Search metadata before retrieval

```python
from imf_datatools import ecos_sdmx_utilities

# Find candidate database names
dbs = ecos_sdmx_utilities.get_databases(substr="DOT")

# Find candidate series containing USD
metadata = ecos_sdmx_utilities.get_ecos_sdmx_metadata(
    "ECDATA_DOT_LATEST_PUBLISHED",
    substr="USD",
)

# Find countries in that database
countries = ecos_sdmx_utilities.get_countries("ECDATA_DOT_LATEST_PUBLISHED")
```

## 18.6 Merge data from multiple sources

```python
from imf_datatools import dataframe_utilities as idt_utils

combined = idt_utils.merge_dfs([df_idata, df_ecos, df_haver], how="outer")
```

---

# 19. Troubleshooting checklist for agents

| Symptom | Likely issue | Action |
|---|---|---|
| Import error for `imf_datatools` | Package not installed or wrong Python path | Re-run installer and confirm `C:/ProgramData/Python3/python.exe`. |
| R cannot import package | `reticulate` using wrong Python or masked `import()` | Use `use_python(...)`; call `reticulate::import("imf_datatools")`. |
| Stata datatools commands fail | Stata Python path or old `installdatatools.ado` | Set Python path; remove old ado files; rerun installer. |
| iData non-public data fails | Token not acquired or expired | Set `idata_utilities.PRIVATE = True` and retry. |
| iData query returns unexpected columns | Open dimension in key | Check key; blank dimensions return multiple values. |
| iData period missing at end | End date not at period end | Use period strings like `'2020-05'` or final day of month. |
| EcOS returns warning around 5,000 series | Query too broad | Split request into loops. |
| DMX fails on server | Access/ODBC driver unavailable | Use workstation or DMXe/SQL alternative. |
| Bloomberg daily output has weekend NaNs | Business-day data expanded to daily dates | Use `df.resample('B').mean()` or `df.dropna()`. |

---

# 20. Compact API index

## iData

```python
idata_utilities.get_databases(keyword=None, searchmode='or', refresh=False, debug=False)
idata_utilities.get_dimensions(db: str, keyword=None, searchmode='or', refresh=False, debug=False)
idata_utilities.get_dimension_values(db, dimension, keyword=None, searchmode='or', refresh=False, debug=False)
idata_utilities.get_idata_data(db: str, key, start=None, end=None, params=None, longformat=False, panel=None, debug=False)
```

## EcOS to iData mapper

```python
get_mapping_data(ecos_db: str, ecos_series: str, force_update=False, debug=False)
get_mapping(ecos_db: str, ecos_series: str, force_update=False, debug=False)
map_db_and_series(ecos_db, ecos_series)
map_bloomberg_ticker(ecos_ticker)
get_countrylist(idata_db='IMF.RES:WEO')
translate_ecos_country(ecos_country, idata_db='IMF.RES:WEO')
get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=None)
```

## EcOS

```python
ecos_sdmx_utilities.get_databases(substr=None, debug=False)
ecos_sdmx_utilities.get_weo_databases(debug=False)
ecos_sdmx_utilities.get_data_structure(database, debug=False)
ecos_sdmx_utilities.get_all_series(dbname, update=True, substr=None, debug=False)
ecos_sdmx_utilities.get_countries(dbname, debug=False)
ecos_sdmx_utilities.get_ecos_sdmx_metadata(dbname, seriesname=None, substr=None, debug=False)
ecos_sdmx_utilities.get_ecos_gfs_metadata(sector, unit, classification, database='ECDATA_GFS_T2_EXPENSE', debug=False)
ecos_sdmx_utilities.get_series_attributes(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None, longformat=False, debug=False)
ecos_sdmx_utilities.get_ecos_sdmx_data(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None, longformat=False, scale=None, scale_label=None, use_original_indicator=False, get_data=True, debug=False)
ecos_sdmx_utilities.get_ecos_gfs_data(country, sector=None, unit=None, classification=None, scale=None, scale_label=None, longformat=False, freq='A', database='ECDATA_GFS_T2_EXPENSE', debug=False)
ecos_sdmx_utilities.get_ecos_commodity_data(database, commodity, datatype=None, freq='A', longformat=False, scale=None, scale_label=False, debug=False)
ecos_sdmx_utilities.get_ecos_bloomberg_data(ticker, field, freq='D', debug=False)
ecos_sdmx_utilities.get_weo_country_codes(save=False)
ecos_sdmx_utilities.get_ebv_country_info(save=False)
```

## DMX / DMXe / SQL / Haver

```python
dmx_utilities.get_all_series(dmxfilename, substr=None, debug=False)
dmx_utilities.get_dmx_data(dmxfilename, seriesname, freq=None, scale=None, scale_label=False, debug=False)
dmx_utilities.get_dmx_metadata(dmxfilename, seriesname=None, substr=None, standard=False, debug=False)

dmxe_utilities.get_all_series(dmxfilename, substr=None, debug=False)
dmxe_utilities.get_dmxe_data(dmxfilename, seriesname, freq=None, scale=None, scale_label=False, debug=False)
dmxe_utilities.get_dmxe_metadata(dmxfilename, seriesname=None, substr=None, debug=False)

sql_utilities.get_all_series(server, dbname, substr=None, debug=False)
sql_utilities.get_sql_data(server, dbname, seriesname, freq=None, scale=None, scale_label=False, debug=False)
sql_utilities.get_sql_metadata(server, dbname, seriesname=None, substr=None, standard=False, debug=False)

haver_utilities.get_databases()
haver_utilities.get_haver_data(code, scale=None, eop=False, periods=False, debug=False)
haver_utilities.get_haver_metadata(code, debug=False)
haver_utilities.get_all_haver_metadata(database)
```

## World Bank / EDI / data.imf.org / Data Mapper

```python
worldbank_utilities.get_database_info()
worldbank_utilities.get_all_worldbank_metadata(debug=False)
worldbank_utilities.get_worldbank_countries(debug=False)
worldbank_utilities.get_worldbank_data(seriesname, country, counterpart=None, freq='A', longformat=False, dataformat='json', debug=False)
worldbank_utilities.get_worldbank_metadata(seriesname)
worldbank_utilities.search_worldbank_metadata(search_str, debug=False)
worldbank_utilities.get_worldbank_topics(debug=False)

edi_utilities.get_databases(debug=False)
edi_utilities.get_dimensions(database, input_only=True, debug=False)
edi_utilities.get_dimension_values(database, dimension, substr=None, debug=False)
edi_utilities.get_edi_data_from_url(url, add_vintage=False, scale_factor=1, scale_label=False, longformat=False, debug=False)
edi_utilities.get_edi_haver_data(havercode, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_bloomberg_data(ticker, field, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_weo_data(country, indicator, freq='A', vintage='current', add_vintage=False, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_gfs_data(country, classification=None, sector=None, unit=None, freq='A', longformat=False, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_wdi_data(country, indicator, freq='A', longformat=False, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_csd_desk_data(country, indicator, freq='A', vintage='current', vintagetimestamp=None, exercise=None, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_csd_ccx_data(country, indicator, freq='A', vintage='current', exercise=None, longformat=False, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_cf_data(country, indicator, longformat=False, freq=None, scale=None, scale_label=False, get_url=False, debug=False)
edi_utilities.get_edi_metadata(database, country=None, indicator=None, freq=None, seriescode=None, vintage=None, debug=False)

imf_ext_data_utilities.get_databases(debug=False)
imf_ext_data_utilities.get_query_dimensions(database, debug=False)
imf_ext_data_utilities.get_dimension_values(codelist, debug=False)
imf_ext_data_utilities.get_series_codes(database, debug=False)
imf_ext_data_utilities.get_country_codes(database, debug=False)
imf_ext_data_utilities.get_imf_ext_data(database, *params, longformat=False, scale=None, scale_label=False, debug=False)

datamapper_utilities.get_datamapper_data(indicators, country=None, longformat=False, debug=False)
datamapper_utilities.get_datamapper_metadata(debug=False)
datamapper_utilities.get_country_codes(debug=False)
datamapper_utilities.get_region_codes(debug=False)
datamapper_utilities.get_group_codes(debug=False)
datamapper_utilities.get_all_areas(debug=False)
datamapper_utilities.get_var_areas(indicator, debug=False)
```

## Eurostat / BIS / DMXe writer / DataFrame utilities

```python
eurostat_utilities.get_datasets(dataset='all', lang='en')
eurostat_utilities.set_args(timeout=None, cert=None)
eurostat_utilities.get_dimensions(dataset)
eurostat_utilities.get_dimension_values(dataset, dimension)
eurostat_utilities.get_data_structure(dataset, dim=None, full=False)
eurostat_utilities.get_eurostat_data(dataset, dims={}, longformat=False, flags=False)

bis_utilities.get_databases()
bis_utilities.get_dimensions(dataset, refresh=False, debug=False)
bis_utilities.get_dimension_values(dataset, dimension, refresh=False, debug=False)
bis_utilities.get_bis_sdmx_data(db, key={}, params={}, longformat=False, debug=False)
bis_utilities.get_bis_data(db, code, start=None, end=None, longformat=False)

dmxe_writer_utilities.save_dmxe_data(outfilename, df, freq=None, datecol=None, debug=False)
dmxe_writer_utilities.save_dmxe_metadata(outfilename, seriescode, dict_metadata, debug=False)
dmxe_writer_utilities.delete_dmxe_data(filename, series, freq, debug=False)
dmxe_writer_utilities.rename_dmxe_data(filename, series, newseries, debug=False)
dmxe_writer_utilities.check_logs(filename, debug=False)
dmxe_writer_utilities.delete_logs(filename)
dmxe_writer_utilities.read_dmxe_data(infilename, series, freq=None, debug=False)
dmxe_writer_utilities.set_dmxe_libdir(corepath, mappingpath)

dataframe_utilities.merge_dfs(iterable_dfs, how='outer')
```

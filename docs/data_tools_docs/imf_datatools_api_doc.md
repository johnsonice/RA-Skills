---
title: "Documentation for the IMF datatools"
source_pdf: "imf_datatools_doc.pdf"
converted_for: "local coding agent API documentation"
conversion_note: "Converted from the PDF text layer; examples and console output are preserved as extracted."
---

# Documentation for the IMF datatools

*The Datatools Team*

*2025-09-20*

> Converted from the original PDF into Markdown for use as local API/reference documentation by a coding agent. The content is kept close to the source, with headings normalized and many command examples fenced as code blocks.

## API / Command Signature Index

- `get_databases(keyword=None, searchmode='or', refresh=False, debug=False)`
- `get_dimensions(db:str, keyword=None, searchmode='or', refresh=False, debug=False)`
- `get_dimension_values(db, dimension, keyword=None, searchmode='or', refresh=False, debug=False)`
- `get_idata_data(db:str, key, start=None, end=None, params=None, longformat=False, panel=None, debug=False)`
- `get_mapping_data(ecos_db:str, ecos_series:str, force_update=False, debug=False)`
- `get_mapping(ecos_db:str, ecos_series:str, force_update=False, debug=False)`
- `map_db_and_series(ecos_db, ecos_series)`
- `map_bloomberg_ticker(ecos_ticker)`
- `get_countrylist(idata_db='IMF.RES:WEO')`
- `translate_ecos_country(ecos_country, idata_db='IMF.RES:WEO')`
- `get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=None)`
- `get_databases(substr=None, debug=False)`
- `get_weo_databases(debug=False)`
- `get_data_structure(database, debug=False)`
- `get_all_series(dbname, update=True, substr=None, debug=False)`
- `get_countries(dbname, debug=False)`
- `get_ecos_sdmx_metadata(dbname, seriesname=None, substr=None, debug=False)`
- `get_ecos_gfs_metadata(sector, unit, classification, database='ECDATA_GFS_T2_EXPENSE', debug=False)`
- `get_ecos_gfs_metadata(sector, units, classifications)`
- `get_series_attributes(database, country, var, counterpart=None, freq='A',                                  sector=None,`
- `get_ecos_sdmx_data(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None,`
- `get_ecos_gfs_data(country, sector=None, unit=None, classification=None,                   scale=None, scale_label=None,`
- `get_ecos_commodity_data(database, commodity, datatype=None, freq='A', longformat=False, scale=None,`
- `get_ecos_bloomberg_data(ticker, field, freq='D', debug=False)`
- `get_weo_country_codes(save=False)`
- `get_ebv_country_info(save=False)`
- `_get_time_series_attributes(database, country, var,                                                 counterpart=None,`
- `get_all_series(dmxfilename, substr=None, debug=False)`
- `get_dmx_data(dmxfilename, seriesname, freq=None,scale=None, scale_label=False, debug=False)`
- `get_dmx_metadata(dmxfilename, seriesname=None, substr=None, standard=False, debug=False)`
- `get_dmxe_data(dmxfilename, seriesname, freq=None,scale=None, scale_label=False, debug=False)`
- `get_dmxe_metadata(dmxfilename, seriesname=None, substr=None, debug=False)`
- `get_all_series((server, dbname, substr=None, debug=False)`
- `get_sql_data(server, dbname, seriesname, freq=None, scale=None, scale_label=False, debug=False)`
- `get_sql_metadata(server, dbname, seriesname=None, substr=None, standard=False, debug=False)`
- `get_databases()`
- `get_haver_data(code, scale=None, eop=False, periods=False, debug=False)`
- `get_haver_metadata(code, debug=False)`
- `get_all_haver_metadata(database)`
- `get_database_info()`
- `get_all_worldbank_metadata(debug=False)`
- `get_worldbank_countries(debug=False)`
- `get_worldbank_data(seriesname, country, counterpart=None, freq='A', longformat=False, dataformat='json',`
- `get_worldbank_metadata(seriesname)`
- `search_worldbank_metadata(search_str, debug=False)`
- `get_worldbank_topics(debug=False)`
- `get_databases(debug=False)`
- `get_dimensions(database, input_only=True, debug=False)`
- `get_dimension_values(database, dimension, substr=None, debug=False)`
- `get_edi_data_from_url(url, add_vintage=False, scale_factor=1, scale_label=False, longformat=False,`
- `get_edi_haver_data(havercode, scale=None, scale_label=False, get_url=False, debug=False)`
- `get_edi_bloomberg_data(ticker, field, scale=None, scale_label=False, get_url=False, debug=False)`
- `get_edi_weo_data(country, indicator, freq='A', vintage='current', add_vintage=False, longformat=False,`
- `get_edi_gfs_data(country, classification=None, sector=None, unit=None, freq='A', longformat=False,`
- `get_edi_wdi_data(country, indicator, freq='A', longformat=False, scale=none, scale_label=False,`
- `get_edi_csd_desk_data(country, indicator, freq='A', vintage='current', vintagetimestamp=None, exercise=None,`
- `get_edi_csd_ccx_data(country, indicator, freq='A', vintage='current', exercise=None, longformat=False,`
- `get_edi_cf_data(country, indicator, longformat=False, freq=None, scale=none, scale_label=False,`
- `get_edi_metadata(database, country=None, indicator=None, freq=None, seriescode=None, vintage=None,`
- `get_query_dimensions(database, debug=False)`
- `get_dimension_values(codelist, debug=False)`
- `get_series_codes(database, debug=False)`
- `get_country_codes(database, debug=False)`
- `get_imf_ext_data(database, *params,                                                  longformat=False, scale=None,`
- `get_datamapper_data(indicators, country=None,                                                            longformat=False,`
- `get_datamapper_metadata(debug=False)`
- `get_country_codes(debug=False)`
- `get_region_codes(debug=False)`
- `get_group_codes(debug=False)`
- `get_all_areas(debug=False)`
- `get_var_areas(indicator, debug=False)`
- `get_datasets(dataset='all', lang='en')`
- `set_args(timeout=None, cert=None)`
- `get_dimensions(dataset)`
- `get_dimension_values(dataset, dimension)`
- `get_data_structure(dataset, dim=None, full=False)`
- `get_eurostat_data(dataset, dims={}, longformat=False, flags=False)`
- `get_dimensions(dataset, refresh=False, debug=False)`
- `get_dimension_values(dataset, dimension, refresh=False, debug=False)`
- `get_bis_sdmx_data(db, key={}, params={}, longformat=False, debug=False)`
- `get_bis_data(db, code, start=None, end=None, longformat=False)`
- `save_dmxe_data(outfilename, df, freq=None, datecol=None, debug=False)`
- `save_dmxe_metadata(outfilename, seriescode, dict_metadata, debug=False)`
- `delete_dmxe_data(filename, series, freq, debug=False)`
- `rename_dmxe_data(filename, series, newseries, debug=False):`
- `check_logs(filename, debug=False)`
- `delete_logs(filename)`
- `read_dmxe_data(infilename, series, freq=None, debug=False)`
- `set_dmxe_libdir(corepath, mappingpath)`
- `merge_dfs(iterable_dfs, how='outer')`

## Contents

- Abstract

- 1 Introduction

- 2 Installation

- 3 Data Resources

- 4 Further Data Retrieval and Manipulation

- 5 Using with other Applications

- 6 Summary

## Abstract

This document summarizes the goals, use cases, and example commands for the imf_datatools Python library which can be used to retrieve data, metadata, and check available series for many data resources at the IMF. The tools can be called directly from within Stata and R, and instructions are also given for this. For the latest info, check out the datatools website at http://datatools, where a link to the latest version of this document is also available.

# 1 Introduction

This document describes the imf_datatools Python package which can be used to retrieve data from various data sources that are used within the Fund. The goal is to provide an interface that allows users to collect data easily from various resources using the same interface and without consideration for the differences in the underlying data sources. Another goal is to provide users with simple ways to query what kind of series and metadata are available in each database. Section 2 gives a quick installation guide. Section 3 explains each data resource and associated functions in detail, while Section 4 shows further examples of pulling data from multiple sources simultaneously and also applying calculations (frequency conversion, % change, seasonal adjustment using X13, etc.). Section 5 describes how to use the imf_datatools in other languages such as R and Stata. For Python users, the library can easily be used with
```python
# import the library
import imf_datatools
# Get data from EcOS
df_ecos = imf_datatools.get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP')
```

```python
# Get data from SQL
df_sql = imf_datatools.get_sql_data('PRDDMXSQL', 'DMX_WDI', '111.SP.POP.TOTL')
```

```python
# Get data from DMX
df_dmx = imf_datatools.get_dmx_data(
```

r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', '911BF')

```python
# Merge all data
from imf_datatools import dataframe_utilities as idt_utils
df_all = idt_utils.merge_dfs([df_ecos, df_sql, df_dmx])
```

```python
# Print out recent years
print(df_all['2016':'2019'])
```

The library has dependencies on various 3rd-party libraries such as numpy, pandas, requests, BeautifulSoup, but should work with most versions of these libraries as of early 2020. If necessary a requirements.txt file will be created. Note that the DMX libraries cannot be used for the servers maintained by Econometric Support, as the servers do not have the necessary Microsoft Access drivers installed. The imf_datatools has been tested but there is no guarantee they work for every case. If any problems are found please contact Datatools Support. The latest information on the tools can be found at http://datatools.

# 2 Installation

This section describes how to install the imf_datatools on Fund personal machines or in a server environment. To gain access to a server maintained by Econometric Support contact EconometricSupport@imf.org and request access to a server with Python available.

## 2.1 Installation on Workstations

To use the imf_datatools the Python library is necessary, even when using from R or Stata. Python and R users should follow steps in 2.1.1 to install the Python library. R users can then read the instructions on usage in 2.1.2. Stata users can jump to the steps in 2.1.3 which will install both the Python library and the necessary Stata commands.

### 2.1.1 Python Library Installation

1. Make sure to install the latest Python from the Software Center (Version 3.10.9 as of Oct 2023)

2. Open Command Prompt by selecting the Windows button at the bottom left of your screen, and typing “cmd”.
When Command Prompt appears as a suggestion, select it.

3. In the command prompt, type or copy and paste the following1 :
```powershell
python \\ecnswn12p\ems_shared\pub\datatools\installer.py
```

This should install the latest stable release of the imf_datatools Python library. This command can also be used to update the library to the latest version.

Once this has been done, the installation can be checked by typing the following in the same command prompt window, python
```python
import imf_datatools
exit()
```

If no error messages appear the installation is complete, and the library is ready to use. If any problems occur, send an email to Datatools Support. 1 This location used to be \\was.int.imf.org\ecn\ems_shared\pub\datatools\dev\imf_datatools and while this folder still exists, the new

location is recommended.

### 2.1.2 Using datatools with R on your workstation

For R users, there are no further installation steps, and below we show how to call the imf_datatools from within R.2 After following the steps in 2.1.1 above, make sure you have the latest R from the Software Center. Also, using the imf_datatools requires that you have Python installed and have installed the imf_datatools library using the above procedure. For the latest versions of R it is also necessary to set the Python path. Within RStudio, go to Tools, Global Options, and at the bottom there is a tab for Python.

This should be set to C:/ProgramData/Python3/python.exe as shown in the figure above. To use the imf_datatools within R, it is necessary to install the reticulate package (this only needs to be done once). In RStudio, execute:
```python
install.packages("reticulate")
```

Once the package has been installed, load the library and set the Python version to the correct one:
```r
library(reticulate)
# specify the python location.
use_python("C:/ProgramData/Python3", required=TRUE)
```

Import the imf_datatools library:
```r
imf_datatools <- import("imf_datatools")
```

and it should be ready for use:
```r
df <- imf_datatools$get_haver_data("GDP@USECON")
tail(df)
#              GDP@USECON
# 2019-10-01    21747.4
# 2020-01-01    21561.1
# 2020-04-01    19520.1
# 2020-07-01    21170.3
```

2 Contact Econometric Support for general questions on R and how to use the imf_datatools in R.

```python
# 2020-10-01      21494.7
# 2021-01-01      22048.9
```

Diagnosing any problems for R Below are several checks to do if you have problems using the imf_datatools in R.
1. Make sure Python and the imf_datatools Python library are correctly installed by opening Command Prompt and
doing the following:
```python
ipython # start ipython session
import imf_datatools
imf_datatools?
```

Type:        module String form: <module 'imf_datatools' from 'C:\\ProgramData\\Python3\\lib\\site-packages\\imf_datatools\\ File:        c:\programdata\Python3\lib\site-packages\imf_datatools\__init__.py Docstring:   <no docstring>

The above should confirm that the imf_datatools library is installed and in the correct location. If not, please refer to the installation instructions above.
2. Confirm that the Python path is set as above.
3. Check your Python configuration with
```python
py_config()
```

python:            C:/ProgramData/Python3/python.exe libpython:         C:/ProgramData/Python3/python310.dll pythonhome:        C:/ProgramData/Python3 version:           3.10.9 (tags/v3.10.9:1dd9be6, Dec 6 2022, 20:01:21) [MSC v.1934 64 bit (AMD64)] Architecture:      64bit numpy:             C:/ProgramData/Python3/Lib/site-packages/numpy numpy_version:     1.24.4

NOTE: Python version was forced by RETICULATE_PYTHON

and if you have mistakenly installed a different version of Python, please delete it and > make sure that the Python path is set correctly.
4. If you have imported other R libraries such as rio which also have an import function, this may mask the import
function that is part of the reticulate library, resulting in an error like import("imf_datatools") Error in import("imf_datatools") : No such file

In this case you can specify that you want to use the import function from the reticulate library by specifying reticulate::import("imf_datatools") instead of import("imf_datatools"). You can also load the reticulate library after loading all other libraries (in which case the import function from all other libraries are masked).
5. Also see Sec.5.1 as for the latest R, the application of timezones may affect the dates displayed.

### 2.1.3 Stata Installation Instructions for your Workstation

For Stata users it is necessary to install the additional Stata commands that call the imf_datatools. First, make sure you have Stata version 16 or higher, preferably the latest one available in the Software Center. Also make sure you install the latest Python from the Software Center as well.

If you are using Stata 17.1 and not the latest Stata 17 R2 from the Software Center and upgrade to the new Python 3.10.9 available in Fall 2023, your datatools commands will not work. Please make sure to update Stata to version 17 R2 from the Software Center.

#### 2.1.3.1 Setting the Python Path in Stata

If you are using Python for the first time in Stata, or if you have updated Python, you need to update Stata’s Python path. To do this, within Stata, execute
```stata
set python_exec C:\ProgramData\Python3\python.exe, perm
```

and this will set Python to your latest version. This needs to be done only once.

#### 2.1.3.2 Running installdatatools.ado to install the datatools libraries

Note that the following has changed as of June 2024 with the new version of Python. To use the installdatatools Stata command, copy the file installdatatools.ado under \\ecnswn12p\ems_shared\pub\data to your computer’s C:\ado\plus\i folder. Next, issue the following command in Stata to install all necessary libraries for the datatools:
```stata
installdatatools
```

to install both Python and Stata files for datatools. Several black windows may appear and it may take a few minutes to complete. Please do not try to issue any further Stata commands during this time. If you get the error message You must install the latest Python from Software Center. Please install Python first and then install datatoo this means there is an old copy of the file installdatatool.ado in Stata’s path. Run the command sysdir to check Stata’s path and remove any older versions of installdatatools.ado. Currently there is a problem where the first time this command is called it may fail. If this happens, re-issue the command and the install should work. Later on this command can also be run to update the imf_datatools to the latest version, and the command should work on the first try. If there are any problems please contact Datatools-Support@imf.org.

#### 2.1.3.3 Checking installation

Once installation is complete, type the following in Stata to see the help files (all examples are clickable):
```stata
help ediuse
help ecosuse
help dmxsuse
help dmxeuse
help sqlsuse
```

Try running the following command in Stata to test if it works:
```stata
ediuse data, database(weo-published) country(111) indicator(NGDP) vintage(2023-10) clear
```

## 2.2 Installation on Econometric Support Servers

The servers maintained by Econometric Support provide a better computing environment than personal machines issued by the Fund, with more CPU and RAM available. Again, the Python library needs to be installed even if using the
```python
imf_datatools from R or Stata. 2.2.1 shows the installation instructions for Python, followed by instructions for R
```

(2.2.2) and Stata (2.2.3). Note that reading from DMX files is not possible from the servers as the necessary Microsoft Access drivers are not available.

### 2.2.1 Installing the Python Library on a Server

To install/use the imf_datatools Python library on the servers it is easiest to Use a server which already has an environment set up. Send an email to Econometric Support requesting access to a server containing the imf_datatools. Access rights as well as details of how to use the environment will be provided. Pre-built enviornments that are mostly identical to what is/was available in the Software Center are available, for Python 3.6.8, 3.8.10 and 3.10.9. This allows users to execute code that was written for these environments without having to make small changes. To test the environment, do the following in Command Prompt: python
```python
import imf_datatools
exit()
```

If no error messages appear the installation is complete, and the library is ready to use.

### 2.2.2 Using datatools with R on econometric support server

To use the imf_datatools in R on any econometric server, the following steps are needed to correctly set the environment:
1. Make sure that your R location in RStudio is specified using a mapped drive and NOT a network path.
For example, if your R version in Tool -> Global Options... -> General is \\ecnswn02d\app\r\R-4.4.0, you need to map \\ecnswn02d\apps\from the server you are on and set your R location using the mapped drive.
- To map the drive:
  - In your file explorer, choose “This PC” from the left side of the window
  - Click the “Computer” tab then “Map Network Drive” button
  - Choose a drive letter like V and enter \\ecnswn02d\apps in the folder field then press finish.
  - A drive with the letter you chose now shows in your “This PC”
- How to set your R path.
  - In RStudio, go to Tools -> Global Option... -> General and click change... next to the R Version
box.
  - Click browse in the dialog box that pops up and type or navigate to your R location using the newly created
mapped drive location as follows: “V:\r\R-4.4.0\bin\x64” NOTE: A previous version of this documentation had \\ecnswn02d\app\r\r_latest as the R location. The version of the reticulate R library in this folder is incompatible with versions of Python above 3.10. It is now recommended to use the version-numbered R installations like \\ecnswn02d\app\r\R-4.4.0 and not use \\ecnswn02d\app\r\r_latest or \\ecnswn02d\app\r\r_stable.
2. Check HTTPS_PROXY and HTTP_PROXY, using Sys.getenv() and make sure they are NOT set.
```r
Sys.getenv("HTTPS_PROXY")
Sys.getenv("HTTP_PROXY")
```

If the outputs are not empty, use Sys.setenv() to set them to empty.
```r
Sys.setenv("HTTPS_PROXY"="")
Sys.setenv("HTTP_PROXY"="")
```

Once the steps above are completed, run the following commands to import your imf_datatools into your R environment.
```r
library(reticulate)
imf_datatools <- import("imf_datatools")
```

For help, contact Econometric Support requesting access to a server with the imf_datatools installed and instructions on how to use in R.

### 2.2.3 Stata Installation Instructions for Server Users

First, follow the steps above in 2.2.1 using the Simple method (recommended) or the Advanced method to install the
```python
imf_datatools Python library.
```

Set Python Within Stata In the below examples, the Python environment with the imf_datatools library installed is given as D:\Apps\sss_env, modify as necessary. Issue the following two commands so that Stata points to the correct version of Python:
```stata
python set exec "D:\Apps\sss_env\sss_env\python.exe", permanently
python set userpath "D:\Apps\sss_env\sss_env\Lib\site-packages", permanently
```

These commands need to be executed just once, and must be done regardless of whether you are using the Simple method or Advanced method. Install the Stata Command Files This applies only if you are using the Advanced method to create your own environment.     Copy the file \\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\py\imf_stata_utils.py to under D:\data\[username]\_sss_en (change your path based on where your env is). Create the folder D:\data\[username]\ado for Stata files. Within Stata, issue the following commands:
```stata
cd D:\data\[username]\ado
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\ediuse.ado"
```

., replace
```stata
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\ediuse.sthlp" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\ecosuse.ado" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\ecosuse.sthlp" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\dmxuse.ado" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\dmxuse.sthlp" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\dmxeuse.ado" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\dmxeuse.sthlp" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\sqluse.ado" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\sqluse.sthlp" ., replace
copy "\\ecnswn12p\ems_shared\pub\datatools\stable\imfdatause\ecosuse_examples.ado" ., replace
```

This will copy all Stata command files to the D:\data\[username]\ado folder. Finally, for each session of Stata on the server, if you are using the Advanced method, the following command must be executed:
```stata
adopath + D:\data\[username]\ado
```

This adds the folder D:\data\[username]\ado to Stata’s path so that the command files are found, and this command can be put in Stata .do files so it is automatically executed. To test that installation is complete, try python:import imf_datatools

and if no errors are shown you can now execute commands like
```stata
ediuse data, database(weo-published) indicator(NGDP) country(111, 193) clear
```

# 3 Data Resources

This section goes over the available data sources and the associated functions for each resource. In principle the
```python
imf_datatools provides the data and metadata as is from the original resource, without modification. This
```

leads to an inconsistent interface for each resource but instead of trying to modify each resource into a uniform interface we provide users with what is natively available. In all cases the main output of data retrieval will be a pandas.DataFrame, the standard in Python when dealing with tabular data. As the API for the pandas library tends to change over time, there may be some dependencies on the version of pandas used, but for the most part the libraries are written so that they do not use exotic parts of the library and the interface should be rather stable. The current version (as of 2020) is written with version 0.24.2. Many functions have an option debug which is set to False by default, but can be set to True so that more information is printed to screen, and in some cases some results are written out to the local folder where the command was executed.

## 3.1 Notes on Data and Resources

For all retrieved time series data, the data will have a pd.DatetimeIndex at the beginning of the period. For example, monthly data for February 2020 will have a date of 2020-02-01, quarterly data for 20Q2 will have a date of 2020-04-01, and annual data for 2019 will have a date of 2019-01-01. The reason for this is because it allows combining data with different frequencies. Data from Haver allows the option of aligning this date to be the end of period, and if necessary this can be implemented in the future for other resources. The imf_datatools can be expanded to support other data resources. For example, there are many public APIs as well as commercial products/services available. However, to add a data resource, the following considerations are necessary.
1. Accessibility
Some web services/APIs require subscriptions and/or API keys which will be necessary for rapid data retrieval. Any code written would have to read in each user’s API key. While this is possible, it leads to some setup on the user side.
2. item Licensing
Some licenses do not allow for indiscriminate distribution of data even among Fund users, so allowing access to data that is then distributed can lead to legal problems. Some examples of frequently used resources are CEIC 1 , World Integrated Trade Solution (WITS) 2 , BEA 3 , BLS 4 , 1 https://info.ceicdata.com/api-and-data-feed-solution
```python
2 https://wits.worldbank.org/witsapiintro.aspx?lang=en
```

3 https://apps.bea.gov/API/signup/index.cfm 4 https://www.bls.gov/developers/

Federal Reserve 5 , Euro Stat 6 , ECB 7 ,UN Comtrade 8 . Many central banks also host various data services. There are also data aggregation services such as quandl https://www.quandl.com/, dbnomics https://db.nomics.world/ which pull data from various resources and make them available. If there are suggestions for further data resources contact Econometric Support to see if that resource can be added.

## 3.2 iData

The iData system is the new (as of 2025) Fund-wide data system that is planned to replace many of the existing data resources including EcOS (Sec.3.4), EDI (Sec.3.10), the external-facing data.imf.org (Sec.3.11), and Data Mapper (Sec.3.12). Once the transition is complete these systems are scheduled to be decomissioned. Note on Public and Non-public Data in iData iData serves as an interface to both public and non-public data. For public data such as the IMF.STA:CPI dataset, there are no restrictions on access, and the commands below can be used with no additional commands. However, for non-public data it is necessary to obtain a token which requires clicking in a page that opens in your browser. This token is set to expire in an hour and it is necessary to refresh this token after this. Within the imf_datatools setting the flag idata_utilities.PRIVATE to True will check whethre a token has previously been obtained within the session and whether it has not expired. If this is not satisfied, on the next data retrieval the token is obtained by opening a browser window. The equivalent commands for R is
```r
library(reticulate)
datatools <- import("imf_datatools")
datatools$idata_utilities$PRIVATE <- TRUE
```

and for Stata it is idatause private

#### `get_databases(keyword=None, searchmode='or', refresh=False, debug=False)`

Returns a pandas.DataFrame containing the available datasets. Once the set of datasets is obtained this is stored in memory so additional calls will not refresh this unless the optional variable refresh is set to True. This is important
```python
when obtaining non-public datasets as setting idata_utilities.PRIVATE = True will return further datasets. It is
recommended that this command be run after setting idata_utilities.PRIVATE =True.
```

The variable keyword is a str or iterable of strs that allows filtering on dataset names and descriptions (all filters are
```python
case-independent). The default searchmode is or so that for example keyword=['sta', 'res'] will return any database
that contains either “sta” or “res” in its name or description. Setting searchmode="and" will provide only databases that
contain all specified keywords. Setting keyword='sta' will return any database that has the letters “sta” in them.
from imf_datatools import idata_utilities
```

```python
# Get public databases
datasets = idata_utilities.get_databases()
```

```python
# To get non-public datasets, set PRIVATE to True.
idata_utilities.PRIVATE = True
datasets_all = idata_utilities.get_databases(refresh=True)
```

#### `get_dimensions(db:str, keyword=None, searchmode='or', refresh=False, debug=False)`

5 https://research.stlouisfed.org/docs/api/fred/ 6 https://ec.europa.eu/eurostat/web/json-and-unicode-web-services 7 https://sdw-wsrest.ecb.europa.eu/help/ 8 https://comtrade.un.org/data/doc/api/

To query data from iData you must specify the dataset name (the index of the datasets from get_databases()), and a query keyword that combines the dimension values of each dimension of the dataset. For example the IMF.STA:CPI database has five dimensions COUNTRY, INDEX, COICOP_1999, TYPE_OF_TRANSFORMATION and FREQUENCY. To retrieve data you must first know these dimensions, then filter on valid values along each dimension. The function get_dimensions() provides these dimensions and their mnemonics, and the following get_dimension_values() provides the valid candidates for each dimension. For both get_dimensions() and get_dimension_values(), within a single session the values are stored in-memory so
```python
they are not retrieved multiple times. To force a refresh use the refresh=True option.
```

For example for the IMF.STA:CPI dataset,
```python
from imf_datatools import idata_utilities
```

```python
db = 'IMF.STA:CPI'
```

```python
dims = idata_utilities.get_dimensions(db)
```

gives Description      Dimension Order COUNTRY                                   Country                    0 INDEX_TYPE                             Index type                    1 COICOP_1999                  Expenditure Category                    2 TYPE_OF_TRANSFORMATION     Type of Transformation                    3 FREQUENCY                               Frequency                    4

Similar to get_databases(), the optional variables keyword and searchmode allow filtering on the dimension mnemonic
```python
and Description column. Again the default searchmode is “or” so that specifying keyword=['country', 'type'] would
```

match the dimensions COUNTRY, INDEX_TYPE, TYPE_OF_TRANSFORMATION above.
#### `get_dimension_values(db, dimension, keyword=None, searchmode='or', refresh=False, debug=False)`

This function provides the available candidates for a given dimension for a db. The results are stored in-memory and
```python
after initial retrieval use these results unless refresh=True is given.
```

The optional variables keyword and searchmode are the same for get_databases() and get_dimensions(), they allow filtering on the dimension value mnemonics or descriptions.
```python
from imf_datatools import idata_utilities
```

```python
db = 'IMF.STA:CPI'
```

```python
countrylist = idata_utilities.get_dimension_values(db, 'COUNTRY')
```

gives Name Code AFG                      Afghanistan, Islamic Republic of ALB                                               Albania DZA                                               Algeria AGO                                                Angola AIA     Anguilla, United Kingdom-British Overseas Terr... ...                                                   ... WBG                                    West Bank and Gaza YEM                                    Yemen, Republic of ZMB                                                Zambia

ZWE                                                  Zimbabwe G163                                           Euro Area (EA)

[201 rows x 1 columns]

Filtering on the results:
```python
db = 'IMF.STA:CPI'
```

```python
# Filter on "republic"
republics = idata_utilities.get_dimension_values(db, 'COUNTRY', keyword='republic')
```

```python
# Show the first 5
```

republics[:5] Name Code AFG    Afghanistan, Islamic Republic of ARM                Armenia, Republic of AZE             Azerbaijan, Republic of BLR                Belarus, Republic of CAF            Central African Republic

```python
# Filter on "republic" or "kingdom"
republic_kingdom = idata_utilities.get_dimension_values(db, 'COUNTRY', keyword=['republic', 'kingdom'])
```

```python
# Check how many "republic" or "kingdom"s there are
len(idata_utilities.get_dimension_values(db, 'COUNTRY', keyword=['republic', 'democratic'], searchmode='or')
```

```python
# Check how many "republic" AND "kingdom"s there are
len(idata_utilities.get_dimension_values(db, 'COUNTRY', keyword=['republic', 'democratic'], searchmode='and')
```

#### `get_idata_data(db:str, key, start=None, end=None, params=None, longformat=False, panel=None, debug=False)`

To retrieve data from iData, specify the dataset name db from get_databases(), then specify the query key which is a str concatenating the dimension values of each dimension separated by a “.”. To know the dimensions and their valid values use the functions get_dimension(db) and get_dimension_values(db, dim) respectively. To have an open query on a dimension, omit putting any values for that dimension. To specify multiple values, specify with a “+” in between. The parameters start and end specify the start and end periods of the data respectively. Use standard formats like '2020', '2020-01', '2020Q2', etc. Note that if you specify the day of the period, unless you include the final day of the month for end, it will not retrieve the data for that period for monthly and lower frequency data. For example
```python
end='2020-05' will retrieve data up to May 2020, as will end='2020-05-31', but end='2020-05-30' will not include
```

May 2020 data for monthly data.
```python
# Get data from CPI
db = 'IMF.STA:CPI'
# Specify dimensions.
# Here we get data for
# - COUNTRY: USA, JPN
# - INDEX_TYPE: CPI
```

```python
# - COICOP_1999: _T
# - TYPE_OF_TRANSFORMATION: open (any value)
# - FREQUENCY: M
key = 'USA+JPN.CPI._T..M'
```

```python
df = idata_utilities.get_idata_data(db, key=key)
```

JPN.CPI._T.IX.M      JPN.CPI._T.POP_PCH_PA_PT.M        JPN.CPI._T.YOY_PCH_PA_PT.M       USA.CPI._T.IX.M        USA.CPI dates 1955-01-01           16.771486                               NaN                               NaN           12.244589 1955-02-01           16.771486                          0.000000                               NaN           12.244589 1955-03-01           16.663512                         -0.643794                               NaN           12.244589 1955-04-01           16.807480                          0.863973                               NaN           12.244589 1955-05-01           16.645524                         -0.963593                               NaN           12.244589 ...                        ...                               ...                               ...                 ... 2024-12-01          110.700000                          0.636364                          3.651685          144.736088 2025-01-01          111.200000                          0.451671                          4.022451          145.683553 2025-02-01          110.800000                         -0.359712                          3.648269          146.330636 2025-03-01          111.100000                          0.270758                          3.638060          146.659451 2025-04-01          111.500000                          0.360036                          3.528319          147.116216

[844 rows x 6 columns]

Note that in the above example the dimension TYPE_OF_TRANSFORMATION which was kept open returns values for IX, POP_PCH_PA_PT and YOY_PCH_PA_PT.
```python
The option longformat=True will return the data in long format where each query dimension is returned as a column
```

along with a column dates and OBS_VALUES for the values.
```python
db = 'IMF.STA:CPI'
```

'USA+JPN.CPI._T.IX.M'
```python
df = idata_utilities.get_idata_data(db, key=key, longformat=True)
```

COUNTRY INDEX_TYPE COICOP_1999 TYPE_OF_TRANSFORMATION FREQUENCY      dates                  OBS_VALUE 0          JPN        CPI          _T                     IX         M 1955-01-01                  16.771486 1          JPN        CPI          _T                     IX         M 1955-02-01                  16.771486 2          JPN        CPI          _T                     IX         M 1955-03-01                  16.663512 3          JPN        CPI          _T                     IX         M 1955-04-01                  16.807480 4          JPN        CPI          _T                     IX         M 1955-05-01                  16.645524 ...        ...        ...         ...                    ...       ...        ...                        ... 1683       USA        CPI          _T                     IX         M 2024-12-01                 144.736088 1684       USA        CPI          _T                     IX         M 2025-01-01                 145.683553 1685       USA        CPI          _T                     IX         M 2025-02-01                 146.330636 1686       USA        CPI          _T                     IX         M 2025-03-01                 146.659451 1687       USA        CPI          _T                     IX         M 2025-04-01                 147.116216

[1688 rows x 7 columns]

Finally, setting the option panel to a valid dimension name like COUNTRY will set the data in panel format, where the data is organized by the specified dimension and dates with one column grouping together the remaining dimensions:
```python
key = 'USA+JPN.CPI._T..M'
df = idata_utilities.get_idata_data(db, key=key, panel='COUNTRY')
```

COUNTRY         dates   CPI._T.IX.M     CPI._T.POP_PCH_PA_PT.M       CPI._T.YOY_PCH_PA_PT.M

0                  JPN 1955-01-01         16.771486                          NaN                       NaN 1                  JPN 1955-02-01         16.771486                     0.000000                       NaN 2                  JPN 1955-03-01         16.663512                    -0.643794                       NaN 3                  JPN 1955-04-01         16.807480                     0.863973                       NaN 4                  JPN 1955-05-01         16.645524                    -0.963593                       NaN ...                ...        ...               ...                          ...                       ... 1683               USA 2024-12-01        144.736088                     0.035500                  2.888057 1684               USA 2025-01-01        145.683553                     0.654616                  3.000483 1685               USA 2025-02-01        146.330636                     0.444170                  2.821549 1686               USA 2025-03-01        146.659451                     0.224707                  2.390725 1687               USA 2025-04-01        147.116216                     0.311446                  2.311289

[1688 rows x 5 columns]

```python
The option panel is mutually exclusive with longformat=True.
```

Retrieval of non-public is the same as above, make sure to set
```python
idata_utilities.PRIVATE = True
```

and this will allow retrieval of all datasets available to the user.

## 3.3 Mapping EcOS to iData

For the transition from EcOS to iData, there have been several changes:
- The country codes used are now ISO3 instead of IMF codes like “111” for United States.
- The series codes have changed and in many cases have been split from one series code across multiple dimensions.
- Some databases like IFS have been split up into multiple databases.
- Some databases and series codes have been discontinued.
To assist this transition, there is a new module idata_mapper.py which translates the above. It should be noted that this is only usable for “standard” EcOS databases that have as inputs country, series code, frequency and optionally a counterpart country. As a special case Bloomberg tickers can also be translated. For databases like those used in
```python
ecos_sdmx_utilities.get_ecos_commodity_data() that do not have a country, this will not work.
```

Basic usage examples are below. Map EcOS database name and series code to iData equivalents. EcOS database name should be same as what is used to query EcOS data, e.g., “WEO_WEO_PUBLISHED”.
```python
from imf_datatools.idata_mapper import *
from imf_datatools import ecos_sdmx_utilities
from imf_datatools import idata_utilities
```

```python
ecos_db = 'WEO_WEO_PUBLISHED'
ecos_series = 'NGDP'
idata_db, idata_series = map_db_and_series(ecos_db, ecos_series)
# 'IMF.RES.WEO:WEO_LIVE_2025_APR_VINTAGE', 'NGDP'
```

```python
Get full mapping data avaialble for a given EcOS database using option ecos_series=“ALL”:
ecos_db = 'WEO_WEO_PUBLISHED'
mapping = get_mapping_data(ecos_db, ecos_series='all')
```

EcosSeriesCode           IDataSeriesCode      DatabaseId       DatabaseRedirect

Id 38005398           911BG_BP6            ARM.BG_BP6.*             21   IMF.RES.WEO:WEO_LIVE 38005399          911GB_PR.A             ARM.GB_PR.A             21   IMF.RES.WEO:WEO_LIVE 38005400          911GB_PR.Q             ARM.GB_PR.Q             21   IMF.RES.WEO:WEO_LIVE 38005401            911GB_PR             ARM.GB_PR.*             21   IMF.RES.WEO:WEO_LIVE 38005402   911GGXCNL_GDP_M.A      ARM.GGXCNL_GDP_M.A             21   IMF.RES.WEO:WEO_LIVE ...                      ...                     ...            ...                    ... 38035573        316NPGDPXO.A           BRB.NPGDPXO.A             21   IMF.RES.WEO:WEO_LIVE 38035574        316NPGDPXO.Q           BRB.NPGDPXO.Q             21   IMF.RES.WEO:WEO_LIVE 38035575          316NPGDPXO           BRB.NPGDPXO.*             21   IMF.RES.WEO:WEO_LIVE 38035576     316NC_USD_WGT.A        BRB.NC_USD_WGT.A             21   IMF.RES.WEO:WEO_LIVE 38035577     316NC_USD_WGT.Q        BRB.NC_USD_WGT.Q             21   IMF.RES.WEO:WEO_LIVE

[414000 rows x 4 columns]

Map IFS, which is split into multiple databases:
```python
ecos_db = 'ECDATA_IFS_Latest_Published'
ecos_series = 'PCPI_IX'
idata_db, idata_series = map_db_and_series(ecos_db, ecos_series)
# 'IMF.STA:CPI', 'CPI._T.SPR_IX'
```

Map Bloomberg ticker (fields are same as in EcOS):
```python
ecos_ticker = 'VIX Index'
field = 'PX_LAST'
idata_db, idata_ticker = map_bloomberg_ticker(ecos_ticker.upper())
# 'IMF.CSF:BBGDL', 'VIX_INDEX'
```

Translate country from EcOS IMF Codes to ISO3. Note that country groups dependd on database, so if there are any special non-ISO3 country groups, it is necessary to specify the database, default is to use WEO.
```python
ecos_country = '111' # IMF code
idata_country = translate_ecos_country(ecos_country)
# 'USA'
```

Compare data from EcOS and iData by translating EcOS country, series code into iData equivalents:
```python
ecos_db = 'ECDATA_CPI_LATEST_PUBLISHED'
ecos_series = 'PCPI_IX'
ecos_country = '111'
freq = 'Q'
```

```python
# Get EcOS data
df_ecos = ecos_sdmx_utilities.get_ecos_sdmx_data(ecos_db, ecos_country, ecos_series, freq=freq)
df_ecos.columns = [c + '_ecos' for c in df_ecos.columns]
```

```python
# Map to iData db and series
idata_db, idata_series = map_db_and_series(ecos_db, ecos_series)
idata_country = translate_ecos_country(ecos_country)
# Get iData data
from imf_datatools import idata_utilities
idata_utilities.PRIVATE = True
key = idata_country + '.' + idata_series + '.' + freq
df_idata = idata_utilities.get_idata_data(idata_db, key)
# Not recommended
```

```python
# df_idata = get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=None)
df_idata.columns = [c + '_idata' for c in df_idata.columns]
```

```python
# Merge
df = df_ecos.merge(df_idata, left_index=True, right_index=True, how='outer')
```

111PCPI_IX.Q_ecos      USA.CPI._T.IX.Q_idata dates 1955-01-01              12.244589                  12.244589 1955-04-01              12.244589                  12.244589 1955-07-01              12.305736                  12.305736 1955-10-01              12.321022                  12.321022 1956-01-01              12.290449                  12.290449 ...                           ...                        ... 2024-04-01             143.968241                 143.968241 2024-07-01             144.403145                 144.403145 2024-10-01             144.727986                 144.727986 2025-01-01             146.224547                 146.224547 2025-04-01             147.488598                 147.488598

[282 rows x 2 columns]

Below each function is explained in detail.
#### `get_mapping_data(ecos_db:str, ecos_series:str, force_update=False, debug=False)`

This is mostly a utility function to see the internal working of mapping between EcOS and iData. Most users should directly use map_db_and_series. Get mapping between EcOS database and series code to iData equivalents. Specify ecos_db and ecos_series,
```python
these should be the same as inputs into ecos_sdmx_utilities.get_ecos_sdmx_data(). For example, ecos_db =
'WEO_WEO_PUBLISHED' and ecos_series = 'NGDP'. Returns a pandas.DataFrame containing the mapping of EcOS
```

series codes in the given EcOS database for the specified ecos_series.
```python
The argument ecos_series = 'ALL' is a special case where all series for ecos_db will be mapped, this may take time as
```

some of the mapping databases are very large. If possible, the output will be written out to the folder idata_mapper/ in the current working directory.
#### `get_mapping(ecos_db:str, ecos_series:str, force_update=False, debug=False)`

This is mostly a utility function to see the internal working of mapping between EcOS and iData. Most users should directly use map_db_and_series. Returns a str idata_db, dict of series_mapping, and dict of dict_series_idata_db, where idata_db is the corresponding iData database name, series_mapping is dict between the EcOS series code ecos_series and the corresponding iData series code, and dict_series_idata_db is a mapping of each series code in ecos_db to the iData database it has been mapped to. This only applies to databases like IFS which have been split into multiple databases in iData, and if the database has not been split, this will be None. The results are cached so that the first time the function is run within a session, the results are retrieved from a SQL database and stored internally in memory. The second time the function is run on the same code the results are retrieved
```python
from this memory. Using option force_update will update results.
```

In the case of any exceptions, a triplet of (None, None, None) is returned.
#### `map_db_and_series(ecos_db, ecos_series)`

Map a given ecos_db and ecos_series to their iData equivalent. Returns a tuple of strs idata_db and idata_series,

and if something goes wrong returns None, None. In cases where the original EcOS database has been split into multiple databases will correctly identify the new iData database.
#### `map_bloomberg_ticker(ecos_ticker)`

```python
Equivalent of map_db_and_series for ecos_db = 'ECDATA_BLOOMBERG', that is, maps a Bloomberg ticker in EcOS to the
```

equivalent in iData. In most cases this is simply replacing any spaces in the EcOS version into underscores for the iData version. Note that tickers for the input in the the EcOS function ‘get_ecos_sdmx_bloomberg() are case-sensitive, that is only works for example with “VIX Index” and not “VIX INDEX”, whereas it seems for iData and the associated mapping tables tickers are all in upper case. This function will therefore strip any leading or ending white space and convert to upper case internally to find match.
#### `get_countrylist(idata_db='IMF.RES:WEO')`

This is mostly a utility function to see the internal working of mapping country codes. Most users should directly use
```python
translate_ecos_country().
```

Return idata_utilities.get_dimension_values(idata_db, 'COUNTRY') for the specified idata_db.                  This is a pandas.DataFrame containing the country ISO3 values as index and names as values.
#### `translate_ecos_country(ecos_country, idata_db='IMF.RES:WEO')`

Translate a given ecos_country into the corresponding iData equivalent (typically ISO3). Returns a str correspoding to
```python
idata_country. By default uses IMF.RES:WEO as the database to obtain the mapping, but any iData database that has
```

dimension 'COUNTRY' can be used. Note that this function relies on the EBV (Enterprise Business Vocabularies) to match the country names used in iData with the IMF codes used in EcOS. Therefore in some cases like country groups, there is no way to find the corresponding matches if the group code is not in the EBV.
#### `get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=None)`

Not recommended for use, mostly for testing purposes. Allows retrieving data from EcOS by specifying ecos_db, ecos_country, 'ecos_series, and freq. Optionally specify
```python
ecos_counterpart.
# Get DOT data using get_idata_data_using_ecos
ecos_db = 'ECDATA_DOT'
ecos_series = 'TXG_FOB_USD'
ecos_country = '111'
ecos_counterpart = '193'
freq = 'A'
df_ecos = ecos_sdmx_utilities.get_ecos_sdmx_data(ecos_db, ecos_country, ecos_series, freq=freq, counterpart=e
df_ecos.columns = [c + '_ecos' for c in df_ecos.columns]
```

```python
# Get from iData
df_idata = get_idata_data_using_ecos(ecos_db, ecos_country, ecos_series, freq, ecos_counterpart=ecos_counterp
df_idata.columns = [c + '_idata' for c in df_idata.columns]
```

```python
# Merge
df = df_ecos.merge(df_idata, left_index=True, right_index=True, how='outer')
print(df)
```

111TXG_FOB_USD_193.A_ecos       USA.XG_FOB_USD.AUS.A_idata dates 1948-01-01                    1.140000e+08                     1.140000e+08

1949-01-01                        1.430000e+08                            1.430000e+08 1950-01-01                        1.050000e+08                            1.050000e+08 1951-01-01                        1.830000e+08                            1.830000e+08 1952-01-01                        1.940000e+08                            1.940000e+08 ...                                        ...                                     ... 2020-01-01                        2.338644e+10                            2.338644e+10 2021-01-01                        2.646213e+10                            2.646213e+10 2022-01-01                        3.055162e+10                            3.055162e+10 2023-01-01                        3.367853e+10                            3.367853e+10 2024-01-01                        3.459343e+10                            3.459343e+10

[77 rows x 2 columns]

## 3.4 EcOS

The EcOS system has a web interface that allows querying and data/metadata retrieval, and this is also used by the EcXL Excel add-in. The EcOS web interface requires authentication of the user’s Fund credentials, so the initial connection can take 10–20 seconds, depending on the time of day and usage. Once connected, this connection will be active for a while and communication with the server will be fast. The EcOS system has many available databases, notably among them WEO, DOT, IFS, etc. The first thing that is necessary is to understand which databases are available. Note that since the EcOS web service authenticates the user’s Fund credentials, users cannot retrieve data from databases that are not available to them, so the web service has security built into it. For example, access to the WEO Live database (WEO_WEO_LIVE) is only granted by user, and those who do not have permission will not be able to download the data through the web service9 . The names of the EcOS databases are organized such that databases that are owned by RES start with WEO_ and databases owned by other departments start with ECDATA_. The EcOS web service has a limit of 5000 series that can be returned at once. In general it is recommended that inquiries be broken into smaller pieces and looped over, and if a response to a request does exceed 5000 series, the value of 5000 will be returned instead of a pandas.DataFrame. Note on GAS database The GAS (Global Assumptions Data) is a special case where by default the series code used for retrieval is different from the column name returned by the database. See the link above and the Excel files within for further information from RES. As a practical issue, when retrieving data from this database using the datatools, if the user retrieves the data in the usual way
```python
get_ecos_sdmx_data('WEO_GAS_LIVE', '001', 'POILAPSP')
```

the output will have a different series code (in this case PZPIOIL): 001PZPIOIL.A dates 1970-01-01           2.225950 1971-01-01           3.111986 1972-01-01           3.596700 1973-01-01           4.172908 1974-01-01          12.358646 1975-01-01          11.507955 9 It should be noted that all database names will be available to anybody.

```python
If this behavior is to be avoided, add the option use_original_indicator=True so that
get_ecos_sdmx_data('WEO_GAS_LIVE', '001', 'POILAPSP', use_original_indicator=True)
```

gives 001POILAPSP.A dates 1970-01-01           2.225950 1971-01-01           3.111986 1972-01-01           3.596700 1973-01-01           4.172908 1974-01-01          12.358646 1975-01-01          11.507955
#### `get_databases(substr=None, debug=False)`

This function returns a sorted list of available EcOS databases. Without any arguments this function will return all database names, regradless of whether the user has access rights to them. The returned list will be sorted in alphabetical order, so it will be easy to check for databases with similar names such as WEO_WEO_PUBLISHED. If the option substr is used, the list of databases can be narrowed down to those that contain the specified characters.
```python
For example, if substr="WEO" is specified, only databases containing "WEO" will be returned. This option can also be a
list so that if substr=['WEO', '2018'] is specified, databases that contain both "WEO" and "2018" will be returned. The
```

order of the substrs in the list is not relevant for this function. If the option debug is specified, information during execution of the function is shown and if possible, data will be written out to the current folder.
#### `get_weo_databases(debug=False)`

This function returns a df of available WEO vintages in EcOS, sorted in chronological order with index being the vintage name like WEO_WEO_Jan2020Pub. Columns for the year and month are also provided. This function allows searching for and looping over WEO vintages and matching the vintage name with the period easier, as the WEO vintages can be difficult to parse for programs.
```python
weodbs = ecos_sdmx_utilities.get_weo_databases()
print(weodbs[-5:])
```

year month WEO_WEOJan2019Pub   2019      1 WEO_WEOApr2019Pub   2019      4 WEO_WEOJuly2019Pub 2019       7 WEO_WEOOct2019pub   2019     10 WEO_WEOJan2020Pub   2020      1

#### `get_data_structure(database, debug=False)`

This functions will get the structure of a given database and returns a dict containing information including available countries, indicators, and other attributes. Functions like get_all_series, get_countries, get_ecos_sdmx_metadata rely on this to retrieve information on the available series, list of countries, and series metadata, respectively. The entire dict may not be of use to most users but this function allows users to see the underlying structure of each database. If the option debug is specified, the original XML file that contains the information is saved and other information is shown on screen.
#### `get_all_series(dbname, update=True, substr=None, debug=False)`

Uses get_data_structure and returns a sorted list of all series codes in a given database dbname. The option substr can be used to narrow down the series of interest. For example if

```python
get_all_series('WEO_WEO_PUBLISHED', substr='GDP')
```

is specified, only series codes containing 'GDP' will be returned. substr can also be a list so that get_all_series('WEO_WEO_PUBLIS
```python
substr=['GDP', 'TX']) will return series that contain both 'GDP' and 'TX'. The order within the list does not matter,
```

and the search is case-insensitive so specifying 'gdp' and 'GDP' are the same.
```python
The option update (default True) can be specified as False if the function was run before with debug=True and in this
```

case the saved text file will be read in instead of querying the web service. This option is probably not of use to most users since the query does not take more than a few seconds. If the option debug is specified, the list is saved as a text file.
#### `get_countries(dbname, debug=False)`

Uses get_data_structure and returns a sorted pandas.DataFrame of all country names and country codes in a given database dbname. Note that the WEO databases and ECDATA databases may have different country names (e.g., "Korea" in WEO vs. "Korea, Republic of" in ECDATA). The differences are mostly just in the names of the countries and not differences in countries themselves, but some groups/areas may be defined in one database but not in others. If the option debug is specified, the country names and codes are saved as a csv file.
#### `get_ecos_sdmx_metadata(dbname, seriesname=None, substr=None, debug=False)`

Uses get_data_structure and returns a sorted pandas.DataFrame of all series codes and their descriptions in a given database dbname. To allow users to specify the series of interest in more detail, there are two options, seriesname and substr. If the series code of interest are already known, specifying
```python
>>> get_ecos_sdmx_metadata('ECDATA_DOT_LATEST_PUBLISHED', seriesname='TBG_USD')
```

will return results only the series of interest. This can also be a list, >>> get_ecos_sdmx_metadata('ECDATA_DOT_LATEST_PUBLISHED',
```python
seriesname=['TBG_USD', 'TMG_CIF_USD'])
```

will return a pandas.DataFrame for the two specified series. Another option substr will allow matching of substrings of the series code to be specified. For example
```python
>>> get_ecos_sdmx_metadata('ECDATA_DOT_LATEST_PUBLISHED', seriesname='USD')
```

will return all series codes that contain 'USD', and specifying a list will return series codes containing all substrings. The order of the list does not matter, and all matching is case-insensitive. As of early 2020, the WEO databases do not have a description of the series used in the EcOS web service, so the returned results will not have further information than the series codes. If the option debug is specified, the country names and codes are saved as a csv file.
#### `get_ecos_gfs_metadata(sector, unit, classification, database='ECDATA_GFS_T2_EXPENSE', debug=False)`

Function to retrieve metadata for GFS databases, which have different internal structure than others like WEO or IFS. The parameters sector, unit, classification must be specified. The database parameter defaults
```python
toECDATA_GFS_T2_EXPENSE, this can be changed by specifying for example database=ECDATA_GFS etc.
sector = ['S13', 'S1313', 'S1311']
units = ['XDC', 'XDC_R_B1GQ']
classifications = ['W0|S1|G2', 'W0|S1|G21']
```

#### `get_ecos_gfs_metadata(sector, units, classifications)`

SECTOR_CODE                                              SECTOR_FULL_NAME       ... CLASSIFICATION_O S13XDCW0|S1|G2                         S13                                            General government       ...

S13XDCW0|S1|G21                        S13                                   General government             ... S13XDC_R_B1GQW0|S1|G2                  S13                                   General government             ... S13XDC_R_B1GQW0|S1|G21                 S13                                   General government             ... S1313XDCW0|S1|G2                     S1313    Local governments, excluding social security f...             ... S1313XDCW0|S1|G21                    S1313    Local governments, excluding social security f...             ... S1313XDC_R_B1GQW0|S1|G2              S1313    Local governments, excluding social security f...             ... S1313XDC_R_B1GQW0|S1|G21             S1313    Local governments, excluding social security f...             ... S1311XDCW0|S1|G2                     S1311    Central government, excluding social security ...             ... S1311XDCW0|S1|G21                    S1311    Central government, excluding social security ...             ... S1311XDC_R_B1GQW0|S1|G2              S1311    Central government, excluding social security ...             ... S1311XDC_R_B1GQW0|S1|G21             S1311    Central government, excluding social security ...             ...

[12 rows x 23 columns]

#### `get_series_attributes(database, country, var, counterpart=None, freq='A',                                  sector=None,`

```python
counterpart_sector=None, longformat=False, debug=False)
```

Get attributes attached to each series. Some databases like the WEO databases have useful attributes that are returned with the data, this function returns a pandas.DataFrame containing these attributes.
```python
attrs = get_series_attributes('WEO_WEO_PUBLISHED', '111', 'NGDP')
print(attrs)
```

111NGDP.A attributes SCALE                                                                                      Billions SERIESCODE                                                                                111NGDP.A A_HISTORICAL_DATA_SOURCE                                                 National Statistics Office A_LATEST_ACTUAL_DATA                                                                           2020 A_SEASONAL_ADJUSTMENT_OF_QUARTERLY_DATA                                          Yes, by the source A_NATIONAL_ACCOUNTS_MANUAL_USED                              System of National Accounts (SNA) 2008 A_GDP_VALUATION                                                                       Market prices A_GDP_VALUATION_COMMENTS                          Real Gross Domestic Product determined by chai... A_ORIGINAL_SOURCE_IN_CALENDAR_YEAR                                                              Yes A_STARTEND_MONTHS_OF_REPORTING_YEAR                                                January/December TIME_FORMAT                                                                                  Annual

In the above example we see that the series 111NGDP.A has attributes showing the default scale, historical data source, as well as useful information like the latest year for actual data. The actual data as of this writing has years up to 2026 so we are able to infer from this that the years 2021 to 2026 are forecasts. These attributes are only available in some databases, notably the WEO databases. For others, the attributes do not return useful information.
```python
attrs = ecos_sdmx_utilities.get_series_attributes('ECDATA_DOT_LATEST_PUBLISHED', '111', 'TXG_FOB_USD', counte
```

```python
print(attrs)
```

111TXG_FOB_USD_158.A attributes SCALE                      Millions SERIESCODE     111TXG_FOB_USD_158.A TIME_FORMAT                  Annual

This function is a wrapper around the get_ecos_sdmx_data() function with the option get_data set to False so that the returned pandas.DataFrame is for the attributes and not for the actual data. Options such as all can be used to specify retrieval of all countries for a given indicator or all indicators for a given country.

#### `get_ecos_sdmx_data(database, country, var, counterpart=None, freq='A', sector=None, counterpart_sector=None,`

```python
longformat=False, scale=None, scale_label=None, use_original_indicator=False, get_data=True, debug=False)
```

The main function to retrieve data from the EcOS databases. A simple example is >>> get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP')

which will get the GDP for the US (country code 111). For some databases like DOT (ECDATA_DOT_LATEST_PUBLISHED) a counterpart country can be specified, in which case the code will be >>> get_ecos_sdmx_data('ECDATA_DOT_LATEST_PUBLISHED', '111',
```python
'TBG_USD', counterpart='193')
```

and this will retrieve the data for the series "TBG_USD" for US (country code 111) and Australia (country code 193). Note that if a counterpart country is not specified, all counterpart countries will be downloaded, and this may lead to too many series queried and no results returned (see warning at beginning of this section). The variables country and var accept country codes and variables like '111' and 'NGDP', but can also be lists such as ['111', '193'] and ['NGDP', 'PPPPC'], in which case all available combinations will be retrieved. These parameters also take the special values 'ALL' in which case all countries or variables for that database will be retrieved. Note that this will use resources on both the server side and on the user side and is not recommended, it is best to create a loop of small requests. Also, the EcOS web service will only serve up to 5, 000 series at once, so results may be truncated if large series are sent. The imf_datatools will detect when exactly 5, 000 series are returned, and the user will get a warning message without any of the data. The EcOS database stores data of different frequencies under the same series code. For example the series code NGDP for US is available in both annual and quarterly frequency under the same series code 111NGDP, and are stored in the same rows of the underlying EcOS data tables. Each retrieved series code is given a frequency identifier at the end, such as 111NGDP.A. By default the function get_ecos_sdmx_data will try to retrieve annual data if it is available. If other
```python
frequencies are desired, the ‘freq} parameter can be used,
>>> get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP', freq='Q')
```

will retrieve the quarterly series. Multiple frequencies can be specified, for example with
```python
>>> get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP', freq='QA')
```

in which case both frequencies will be combined. In this case since the imf_datatools will always set the date of the data for each period to be the first day, the annual series will only be filled for dates of Jan 1, while the quarterly series will have data for Jan 1, Apr 1, Jul 1, and Oct 1. The option scale will apply the numerical scale of each series if set to a valid value. For example, the series NGDP in
```python
WEO has included in its metadata the scale of "Billions", so if scale='ecos' or scale='default' is specified, this will
```

convert the raw values into these scales:
```python
df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP')
print(df[-5:]) # original raw values
```

111NGDP.A dates 2021-01-01 2.311842e+13 2022-01-01 2.394174e+13 2023-01-01 2.480448e+13 2024-01-01 2.571359e+13 2025-01-01 2.666723e+13

```python
df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP', scale='ecos')
```

```python
print(df[-5:]) # with Billions applied
```

111NGDP.A dates 2021-01-01 23118.423201 2022-01-01 23941.740804 2023-01-01 24804.483969 2024-01-01 25713.589689 2025-01-01 26667.226897

Other options are k, M, B, T which will convert into scales of thousands, millions, billions, and trillions, respectively.
```python
df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP', scale='T')
```

```python
print(df[-5:]) # with Trillions applied
```

111NGDP.A dates 2021-01-01 23.118423 2022-01-01 23.941741 2023-01-01 24.804484 2024-01-01 25.713590 2025-01-01 26.667227

The scale is specified for each different series and can be convenient to align different series to be at the same scale. If the
```python
option scale_label=True is specified, the applied scale will be shown in the variable name.
df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP', scale='T', scale_label=True)
```

```python
print(df[-5:]) # with Trillions applied, and label
```

111NGDP.A (Trillions) dates 2021-01-01              23.118423 2022-01-01              23.941741 2023-01-01              24.804484 2024-01-01              25.713590 2025-01-01              26.667227

```python
Another option that is available for EcOS is to specify long format with option longformat=True. In this case the data
```

will be returned in long format, where the columns are organized so that indices necessary to specify a row (country code, counterpart, etc.) come first, followed by a date column, and then finally columns for variables. The ‘pandas.DataFrame} index will just be a range. As an example,
```python
>>> df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED',
```

['111', '193', '196'], ['NGDP', 'PPPPC'])

>>> print(df[-5:]) 111NGDP.A           111PPPPC.A     ...        196NGDP.A        193NGDP.A dates                                             ... 2020-01-01 2.232176e+13          67426.835263     ...    3.198156e+11     2.029311e+12 2021-01-01 2.318028e+13          69643.835970     ...    3.359503e+11     2.121742e+12 2022-01-01 2.401380e+13          71760.345806     ...    3.521432e+11     2.229370e+12 2023-01-01 2.488141e+13          73953.425079     ...    3.681717e+11     2.343918e+12 2024-01-01 2.579342e+13          76252.108497     ...    3.852210e+11     2.455932e+12

will format the data so that the dates are the index of the pandas.DataFrame, with columns for each combination of

```python
country code and series name. If the option ‘longformat=True} is specified,
>>> df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED',
['111', '193', '196'], ['NGDP', 'PPPPC'], longformat=True)
```

>>> print(df[df['dates'].dt.year > 2019]) COUNTRY      dates          NGDP        PPPPC 70      111 2020-01-01 2.232176e+13 67426.835263 71      111 2021-01-01 2.318028e+13 69643.835970 72      111 2022-01-01 2.401380e+13 71760.345806 73      111 2023-01-01 2.488141e+13 73953.425079 74      111 2024-01-01 2.579342e+13 76252.108497 135     193 2020-01-01 2.029311e+12 54799.037792 136     193 2021-01-01 2.121742e+12 56477.090940 137     193 2022-01-01 2.229370e+12 58238.979664 138     193 2023-01-01 2.343918e+12 60037.523515 139     193 2024-01-01 2.455932e+12 61879.685651 195     196 2020-01-01 3.198156e+11 42044.566681 196     196 2021-01-01 3.359503e+11 43241.164873 197     196 2022-01-01 3.521432e+11 44501.565529 198     196 2023-01-01 3.681717e+11 45806.672359 199     196 2024-01-01 3.852210e+11 47116.024190

the output now has COUNTRY and dates as the first two columns, followed by the series codes. The rows are ordered by all indices necessary to specify the row (in this case only COUNTRY), then dates. The aforementioned scale and scale_label options can be used together with the longformat option:
```python
df = get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111',
['NGDP', 'PPPPC'], scale='ecos', scale_label=True, longformat=True)
```

```python
print(df[-5:]) # long format, with EcOS scales applied, and label
```

COUNTRY      dates NGDP (Billions) PPPPC (Units) 71     111 2021-01-01     23118.423201   69284.853116 72     111 2022-01-01     23941.740804   71282.929032 73     111 2023-01-01     24804.483969   73368.515045 74     111 2024-01-01     25713.589689   75560.002430 75     111 2025-01-01     26667.226897   77849.679792

This function has been tested against the following databases (see Sec. 3.4 for how to get database names).
1. WEO databases such as WEO_WEO_PUBLISHED, vintages such as WEO_WEO_Jan2008Pub. Note that to query databases
like WEO_WEO_LIVE users must contact RES and be included in the group of allowed users.
2. DOT databases like ECDATA_DOT_LATEST_PUBLISHED, ECDATA_DOT_2018M05.
3. The CDIS database ECDATA_CDIS_LATEST_PUBLISHED.
4. The CPIS database ECDATA_CPIS_LATEST_PUBLISHED.
5. The GFS databases ECDATA_GFS_MAIN_AGGREGATES_BALANCES,
ECDATA_GFS_STATEMENT_CASH, ECDATA_GFS_T1_REVENUE, ECDATA_GFS_T2_EXPENSE, ECDATA_GFS_T3_6_9_INTEGRATED_BALANCE_SHEET, ECDATA_GFS_T7_COFOG, ECDATA_GFS_T8_COUNTERPART_SECTOR, ECDATA_FAS_LATEST_PUBLISHED

6. FSI database ECDATA_FSI

7. MFS database ECDATA_MFS

```python
As mentioned in the notes in 3.4 the option use_original_indicator=True can be specified for the GAS database, and
```

the output will use the original input series code instead.

There may be cases of EcOS databases which do not work with this default function, in this case contact Econometric Support and a solution will be provided.

#### `get_ecos_gfs_data(country, sector=None, unit=None, classification=None,                   scale=None, scale_label=None,`

```python
longformat=False,   database='ECDATA_GFS_T2_EXPENSE', debug=False)
```

Function to retrieve data for GFS databases, which have different internal structure than others like WEO or IFS. The parameters sector, unit, classification are optional, in which case all available combinations are retrieved. However, as there can be hundreds or thousands of series for each country, it is strongly recommended that each query be as specific as possible, and loops used. The database parameter defaults toECDATA_GFS_T2_EXPENSE, this can be
```python
changed by specifying for example database=ECDATA_GFS etc.
sector = ['S13', 'S1313', 'S1311']
units = ['XDC', 'XDC_R_B1GQ']
classifications = ['W0|S1|G2', 'W0|S1|G21']
df = get_ecos_gfs_data('111', sector=sector, unit=units, classification=classifications)
df[-5:]
```

111S1311XDCW0|S1|G2.A 111S1313XDCW0|S1|G21.A ... 111S13XDC_R_B1GQW0|S1|G2.A                         111S1313XDCW0|S1| dates                                                      ... 2016-01-01           2.510257e+12                     NaN ...                    35.946776 2017-01-01           2.576004e+12                     NaN ...                    35.643140 2018-01-01           2.730785e+12                     NaN ...                    35.445473 2019-01-01           2.877787e+12                     NaN ...                    35.687250 2020-01-01           4.306570e+12                     NaN ...                    45.401838

[5 rows x 12 columns]

The usual options of freq, scale, scale_label, and longformat work similarly to get_ecos_sdmx_data().

#### `get_ecos_commodity_data(database, commodity, datatype=None, freq='A', longformat=False, scale=None,`

```python
scale_label=False, debug=False) The commodity-type databases have a different structure from typical databases
```

like WEO and IFS in that there is no country variable to be specified. For this reason, data from these databases have their own retrieval function.

The parameters database and commodity are required. The datatype argument can be specified as a str or list, if the default None is used all available datatypes are returned.

An example:
```python
df = get_ecos_commodity_data('ECDATA_COMMODITY_PRICE_SYSTEM', ['PFOOD', 'PMEAT', 'PMETA'], datatype='Index')
df[-5:]
```

PFOODIndex.A PMEATIndex.A PMETAIndex.A dates 2014-01-01    171.242918    160.482890    164.375361 2015-01-01    141.481856    137.437771    126.573735 2016-01-01    145.354121    126.609668    119.730283 2017-01-01    148.589074    139.135792    146.314857 2018-01-01    149.479578    135.854016    152.860336

Example of abbreviating datatype:

```python
df = ecos_sdmx_utilities.get_ecos_commodity_data('ECDATA_COMMODITY_PRICE_SYSTEM', ['PBARL', 'PSUGA', 'PWOOL']
df[-5:]
```

PBARLUSD.A PBARLIndex.A PSUGAIndex.A PWOOLIndex.A dates 2015-01-01 127.865278     134.485842    130.427122    162.843794 2016-01-01 129.387806     136.087203    180.515131    179.076542 2017-01-01 132.016477     138.851981    156.990951    208.564084 2018-01-01 135.227095     142.228837    122.574768    267.616394 2019-01-01 146.386611     153.966167           NaN           NaN

The usual options of freq, scale, scale_label, and longformat work similarly to get_ecos_sdmx_data().
#### `get_ecos_bloomberg_data(ticker, field, freq='D', debug=False)`

Function to retrieve business-day data from the ECDATA_BLOOMBERG database. As of early 2020, this database contains over 17, 000 tickers from Bloomberg. The list of available tickers can be queried using (see Sec. 3.4) >>> get_all_series('ECDATA_BLOOMBERG')

and further series may be requested through the Library. A simple example is
```python
>>> df = get_ecos_bloomberg_data('VIX Index', field='PX_LAST')
```

which will retrieve the ticker "VIX Index" (note that capitalization and spaces must match what is in the database) and for the ticker "PX_LAST". Tickers and fields may also be specified as lists, e.g.,
```python
>>> df = get_ecos_bloomberg_data(['VIX Index', 'CVIX Index'],                ['PX_LAST', 'PX_OPEN'])
```

will retrieve the data for the two tickers "VIX Index", "CVIX Index" and two fields "PX_LAST", "PX_OPEN". The Bloomberg data is only given for business days, but the program will automatically convert this into a daily series so that values for Saturdays and Sundays will be filled with NaN. To remove these values either do >>> df.resample('B').mean()

which will resample to business days, but keep business day values that were originally NaN, or >>> df.dropna()

to drop all NaN values including those for weekends and holidays. As a special case, the field can take "ALL", in which case all available fields for the specified ticker(s) will be returned. Since each series can have thousands of observations, it is recommended that queries be looped over single tickers and fields.
#### `get_weo_country_codes(save=False)`

This function will return a combined table of WEO country names and codes merged together with country information
```python
from the World Bank.
```

The RES department places an Excel file containing current WEO countries and groups10 for each major WEO release. The function first downloads this file and gets the WEO country names and codes from the sheet "All Countries and Country Codes". Next, it uses the function worldbank_utilities.get_worldbank_countries() (see Sec. put wb ref) to download the list of countries used by the World Bank. The World Bank table is left-merged to the RES table using the ISO 2-letter codes. 10 Available at  http://www-intranet.imf.org/departments/RES/Divisions/WEO/Documents/WEO_Data_Tab/WEO/%20Countries/ %20and/%20Country/%20Groups.xlsx.

Finally, the sheet "WEO Country Groups" in the RES Excel file is used to create columns corresponding to groups of countries. If a country belongs in a group it will have value 1 and otherwise 0. If the option save is specified, the RES Excel file will be saved locally.
#### `get_ebv_country_info(save=False)`

This function utilizes the EBV (Enterprise Business Vocabularies) to return a combined table of country information merged with information from the World Bank. If the option save is specified, the output will be saved locally as a csv file. Contact the EBV team for information on the EBV or contents of the data.
#### `_get_time_series_attributes(database, country, var,                                                 counterpart=None,`

```python
sector=None, counterpart_sector=None,                                                 freq='A', debug=False)
```

This function provides attributes of a series in a database for a given country, complementary to the get_ecos_sdmx_metadata() function. For example for WEO:
```python
>>> tsattrs = _get_time_series_attributes('WEO_WEO_PUBLISHED', '111', 'NGDP')
```

```python
print(tsattrs.T)
```

seriescode                                                                                     111NGDP.A scale                                                                                               3530 A_PRIMARY_DOMESTIC_CURRENCY_1                                                                  US dollar N_LATEST_ACTUAL_ANNUAL_DATA                                                                         2022 N_LATEST_ACTUAL_QUARTERLY_DATA                                                                    2023Q2 N_HISTORICAL_DATA_SOURCE                                                      National Statistics Office N_NATIONAL_ACCOUNTS_MANUAL_USED                                   System of National Accounts (SNA) 2008 N_GDP_VALUATION                                                                            Market prices N_GDP_VALUATION_COMMENTS                               Real Gross Domestic Product determined by chai... N_REPORTING_IN_CALENDAR_YEAR                                                                         Yes N_STARTEND_MONTHS_OF_REPORTING_YEAR                                                     January/December N_BASE_YEAR                                                                                         2012 N_REPORTING_BASED_ON_EXPENDITURE_APPROACH                                                            Yes N_CHAINWEIGHTED                                                                           Yes, from 1980 N_FORMULA_USED_TO_DERIVE_VOLUMES                                                                  Fisher N_FORMULA_USED_TO_DERIVE_VOLUMES_COMMENTS              In the NIPAs, the changes in quantities and pr... N_SEASONAL_ADJUSTMENT_OF_QUARTERLY_DATA                                               Yes, by the source N_ANNUALIZATION_OF_QUARTERLY_DATA                                                                    Yes N_ANNUALIZATION_OF_QUARTERLY_DATA_COMMENTS             Annual value equals a simple average of the fo... N_BASIS_OF_QUARTERLY_REAL_GDP_PROJECTIONS              The quarterly projection reflects the expected... DESK_SERIES                                                                                      111NGDP SUBMISSION_DATE                                                                    9/20/2023 12:00:00 AM time_format                                                                                          P1Y scale_factor                                                                                    Billions scale_values                                                                                1000000000.0

As can be seen, useful information such as N_LATEST_ACTUAL_ANNUAL_DATA and N_LATEST_ACTUAL_QUARTERLY_DATA are available to distinguish historical and projection data. This function was initially used only internally within get_ecos_sdmx_data() to retrieve the scale of the series (hence the underscore at the beginning of the function name), but now returns all available attributes in the latest version of the
```python
imf_datatools.
```

Summary

As of early 2020, the EcOS database is set to be replaced through the iData project. As long as the replacement has API access, the imf_datatools should be able to provide access to WEO and other vintages.

## 3.5 DMX

The DMX file format is commonly used by country desks to store data. DMX files are actually Microsoft Access database files, and can be connected to and queried using ODBC drivers. The following functions are available to query and retrieve data, metadata from DMX files. To have the necessary ODBC drivers installed, users must install the Data Management for Excel (DMX) add-in from the Software Center. Since this driver is necessary to connect to Microsoft Access files, DMX-related commands will not work on the Econometric Support servers, as the Windows Office update method is incompatible with the Fund’s security policies.
#### `get_all_series(dmxfilename, substr=None, debug=False)`

This function will retrieve all available series codes in a given DMX file and return a list. For example dmx_utilities.get_all_series(r'\\Data2\apd\Data\AUS\DMX\AUS_MT.dmx')

will retrieve all series codes from the file \\Data2\apd\Data\AUS\DMX\AUS\_MT.dmx. Several notes of caution are necessary regarding the path to the DMX file:
1. As the DMX file is a regular file, you must have access and read permission. Many country desks have DMX files on
their Q drive, users without access to the files will of course not be able to see the contents unless they have access rights.
2. The Q drive of a user depends on which department they are in, so it is recommended to use paths like \\Data2\apd
instead of Q:\ so it is clear where the absolute path is, and does not depend on who is running the command.
3. In Windows the path separator is backslash (\) which is an escape character 11 in many languages, including Python.
For this reason, Python has what are called “raw strings” which will not use the backslash to be an escape character. This is why the file paths in the above example start with r. It is possible to substitute regular slashes and Python will understand the path, for example //Data2/apd/Data/AUS/DMX/AUS/_MT.dmx will work, but this may cause confusion since some applications may represent Windows paths in different ways if using forward slashes. Most users will have the sample file C:\ProgramData\IMF\DMX\Samples\sample.dmx created when they install DMX. Running the function on this file gives
```python
>>> serieslist = dmx_utilities.get_all_series(
```

r'C:\ProgramData\IMF\DMX\Samples\sample.dmx') >>> print(', '.join(serieslist)) 911BCA_GDP, 911BCAXGT_GDP, 911BCAXT, 911BE, 911BEA, 911BEAB, 911BEAI, 911BEAM,911BEAO, 911BEAP, 911BED, 911BER, 911BF, 911BFD, 911BFO, 911BFOA, 911BFOA_MLT, 911BFOA_S, 911BFOAP

#### `get_dmx_data(dmxfilename, seriesname, freq=None,scale=None, scale_label=False, debug=False)`

This function will retrieve data from a given DMX file and return it as a pandas.DataFrame. A simple example is dmx_utilities.get_dmx_data( r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', '911BF')

11 For example \n is associated with a newline, \t is a tab, etc.

which will retrieve the series 911BF from the DMX file C:\ProgramData\IMF\DMX\Samples\sample.dmx. The seriesname can be a list of seriescodes, for example dmx_utilities.get_dmx_data(r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', ['911BF', '911BCA_GDP'])

will retrieve both series. For DMX files it is possible to store the same series with different frequencies. To distinguish between the frequencies, the parameter freq can take on the values "A", "Q", "M", "D" for annual, quarterly, monthly, and daily data. The default value is None and if there is only one available frequency, that series is returned. If no freq is specified but multiple frequencies exist, a SystemExit is raised, while if a freq is specified and that frequency series exists, that series is returned. It is possible to specify a list for seriesname so that many series from the same dmxfilename can be retrieved at once. The result will be a pandas.DataFrame with a column for each series. This will be slightly more efficient than querying each series independently and combining the results afterwards. The dmxfilename and freq must be common to all series, i.e., it is not possible to get data from multiple DMX files with one use of this function. The option scale can be set to values of 'dmx', 'default', 1, 'u', 'k', 'm', 'b', 't'. If the value is 'dmx' or 'default', the scale stored as metadata will be applied, while 1, u will return the original values, and 'k/m/b/t' will correspond to scaling in thousands, millions, billions, and trillions. If the option scale_label is set to True, the scale is shown in the columns.
#### `get_dmx_metadata(dmxfilename, seriesname=None, substr=None, standard=False, debug=False)`

This function will retrieve the metadata of a series or multiple series from a given DMX file. For example
```python
>>> metadata = dmx_utilities.get_dmx_metadata(
```

r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', '911BF') >>> print(metadata) OID SyncID UDP_CreatedBy ... CTS_EXT MAP_SERIES Notes 911BF   14       1       skapoor ...      NaN        NaN   NaN

will retrieve the metadata from the series 911BF from the file C:\ProgramData\IMF\DMX\Samples\sample.dmx. The output will be a pandas.DataFrame containing available information on the series containing 41 columns, some of which are UDP_CreatedBy, UDP_CreatedDate, UDP_UpdatedBy, UDP_UpdatedDate, Source, Sector. These columns can be used to understand which series are of interest. Note that this metadata depends on the creator of the series inputting this information, otherwise the fields will be empty. It is also possible to retrieve the metadata for multiple series at once, for example
```python
>>> serieslist = ['911BF', '911BCA_GDP']
>>> metadata = dmx_utilities.get_dmx_metadata(
```

r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', serieslist) >>> print(metadata) OID SyncID UDP_CreatedBy      UDP_CreatedDate UDP_UpdatedBy UDP_UpdatedDate Documentation ... Source_Series_Location Source_Series_Date_Range Share_Level BYear CTS_EXT MAP_SERIES Notes

911BF         2        1             skapoor 2012-01-20 11:13:01 None             None                  NaN ...                              NaN NaN   Department     NaN            NaN        NaN    NaN

911BCA_GDP       14          1       skapoor 2012-01-20 11:13:01

None                None              NaN    ...                           NaN NaN    Department       NaN        NaN             NaN    NaN

will retrieve the metadata for all series in serieslist at once and the result will be a row for each series. If no seriesname is specified, the metadata will be retrieved for all series in the DMX file. The option subst can be used to get metadata only for series containing specific substrings,
```python
>>> metadata = dmx_utilities.get_dmx_metadata(
r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', substr='911')
```

will retrieve metadata for all series containing the substr "911". The substr can be a list, so that
```python
>>> metadata = dmx_utilities.get_dmx_metadata(
r'C:\ProgramData\IMF\DMX\Samples\sample.dmx', substr=['911', 'BE'])
```

will retrieve metadata for series containing both "911" and "BE". The substrings are case-insensitive, and in the case of DMX the order matters, so that series of the form "911*BE*" where * is any character will match, but "BE*911" will not. Finally, if the option standard is set to True, only the columns for Topic and UDP_UpdatedDate will be returned.

#### 3.5.0.1 Note on DMXe

The current DMX system that uses Microsoft Access files will soon be replaced with DMXe files, which will use sqlite files (https://www.sqlite.org/index.html). Python has no problem connecting to sqlite files, so connecting to this file type should be possible.

## 3.6 DMXe

The DMXe file format is the new version of DMX and internally is a completely different file type based on sqlite files. Usage is very similar to DMX files, the following functions are available to query and retrieve data, metadata from DMXe files. Unlike DMX files, DMXe files should be accessible via the datatools anywhere as long as Python is installed. Internally the sqlite3 library is used to access the file, this library should be widely available.
#### `get_all_series(dmxfilename, substr=None, debug=False)`

This function will retrieve all available series codes in a given DMXe file and return a list. For example dmxe_utilities.get_all_series(r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe')

will retrieve all series codes from the file r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe'. Several notes of caution are necessary regarding the path to the DMXe file:
1. As the DMXe file is a regular file, you must have access and read permission. Many country desks have DMXe files
on their Q drive, users without access to the files will of course not be able to see the contents unless they have access rights.
2. The Q drive of a user depends on which department they are in, so it is recommended to use paths like \\Data2\apd
instead of Q:\ so it is clear where the absolute path is, and does not depend on who is running the command.

3. In Windows the path separator is backslash (\) which is an escape character 12 in many languages, including Python.
For this reason, Python has what are called “raw strings” which will not use the backslash to be an escape character. This is why the file paths in the above example start with r. It is possible to substitute regular slashes and Python will understand the path, for example //Data2/apd/Data/AUS/DMX/AUS/_MT.dmx will work, but this may cause confusion since some applications may represent Windows paths in different ways if using forward slashes.
```python
>>> serieslist = dmxe_utilities.get_all_series(
```

r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe') >>> print(', '.join(serieslist[:5])) 646BCA, 646BCAXGTO, 646BCAXGTXO, 646BCAXGT, 646BGS

#### `get_dmxe_data(dmxfilename, seriesname, freq=None,scale=None, scale_label=False, debug=False)`

This function will retrieve data from a given DMXe file and return it as a pandas.DataFrame. A simple example is
```python
dmxfilename = r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe'
```

dmxe_utilities.get_dmxe_data(dmxfilename, '646BCA')

which will retrieve the series 911BF from the above DMXe file. The seriesname can be a list of seriescodes, for example dmxe_utilities.get_dmxe_data(dmxfilename, ['646BCA', '646BCAXGT'])

will retrieve both series. For DMXe files it is possible to store the same series with different frequencies. To distinguish between the frequencies, the parameter freq can take on the values "A", "Q", "M", "D" for annual, quarterly, monthly, and daily data. The default value is None and if there is only one available frequency, that series is returned. If no freq is specified but multiple frequencies exist, a SystemExit is raised, while if a freq is specified and that frequency series exists, that series is returned. It is possible to specify a list for seriesname so that many series from the same dmxfilename can be retrieved at once. The result will be a pandas.DataFrame with a column for each series. This will be slightly more efficient than querying each series independently and combining the results afterwards. The dmxfilename and freq must be common to all series, i.e., it is not possible to get data from multiple DMXe files with one use of this function. The option scale can be set to values of 'dmxe', 'default', 1, 'u', 'k', 'm', 'b', 't'. If the value is 'dmxe' or 'default', the scale stored as metadata will be applied, while 1, u will return the original values, and 'k/m/b/t' will correspond to scaling in thousands, millions, billions, and trillions. If the option scale_label is set to True, the scale is shown in the columns.
#### `get_dmxe_metadata(dmxfilename, seriesname=None, substr=None, debug=False)`

This function will retrieve the metadata of a series or multiple series from a given DMXe file. For example
```python
>>> metadata = dmxe_utilities.get_dmxe_metadata(
```

r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe', '646BCA') >>> print(metadata) SeriesId CreatedBy ...          FiscalLead LastUpdatedVersion SeriesCode                       ... 646BCA              1 AUmredkar ... Start in January                     4

will retrieve the metadata from the series 646BCA from the above file. The output will be a pandas.DataFrame containing available information on the series containing 41 columns, some of which are CreatedBy, CreatedDate, UpdatedBy, UpdatedDate, Source, Sector. These columns can be used to understand which series are of interest. Note that this metadata depends on the creator of the series inputting this information, otherwise the fields will be empty. It is also possible to retrieve the metadata for multiple series at once, for example 12 For example \n is associated with a newline, \t is a tab, etc.

```python
>>> serieslist = ['646BCA', '646BCAXGT']
>>> metadata = dmxe_utilities.get_dmxe_metadata(
```

r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe', serieslist) >>> print(metadata) SeriesId CreatedBy ...          FiscalLead LastUpdatedVersion SeriesCode                       ... 646BCA             1 AUmredkar ... Start in January                      4 646BCAXGT          4 AUmredkar ... Start in January                      4

will retrieve the metadata for all series in serieslist at once and the result will be a row for each series. If no seriesname is specified, the metadata will be retrieved for all series in the DMXe file. The option subst can be used to get metadata only for series containing specific substrings,
```python
>>> metadata = dmxe_utilities.get_dmxe_metadata(
r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe', substr='BCA')
```

will retrieve metadata for all series containing the substr "BCA". The substr can be a list, so that
```python
>>> metadata = dmxe_utilities.get_dmxe_metadata(
r'\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe', substr=['BCA', 'X'])
```

will retrieve metadata for series containing both "BCA" and "X". The substrings are case-insensitive, and in the case of DMXe the order matters, so that series of the form "BCA*X*" where * is any character will match, but "X*BCA" will not.

## 3.7 SQL

There are several SQL databases within the Fund that store economic time series data. Some examples are the CSD database, the Consensus Forecasts database, and the WDI database. The sql_utilities library will connect to SQL databases that have similar internal structures to DMX files and retrieve data and metadata. Since the internal structure of the SQL databases and DMX files are very similar, the functions available and their behavior are also very similar, the only difference being that for DMX only the DMX file name is required, but for SQL both server name and database name are required. To connect to a SQL database you need to know the server name and the database of interest. There is no good way to figure out the server names, the most common will probably be PRDCSDSQL for the CSD database and PRDDMXSQL for a
```python
server containing Consensus Forecasts, WDI, and others. If using the DMX add-in in Excel, the server being used may
```

be inferred from the information in the retrieval sheet.
#### `get_all_series((server, dbname, substr=None, debug=False)`

This function will query a server and dbname for available series codes. A simple usage would be
```python
>>> metadata = sql_utilities.get_all_series('PRDDMXSQL', 'DMX_CF')
```

which will return over 23, 000 series as of early 2020. The option substr will narrow down the substrings included in the series codes, for example
```python
>>> metadata = sql_utilities.get_all_series('PRDDMXSQL', 'DMX_CF', substr='111')
```

will return only series codes containing "111". The substr can be a list,
```python
>>> metadata = sql_utilities.get_all_series('PRDDMXSQL', 'DMX_CF',
substr=['111', 'GDP'])
```

will return series codes containing "111" and "GDP". The substrings are case-insensitive, and the order matters, so that in the above example, any series code of the form "111*GDP" where * is any character will match, but series codes of the form "GDP*111" will not.
#### `get_sql_data(server, dbname, seriesname, freq=None, scale=None, scale_label=False, debug=False)`

This function will retrieve data from a given SQL server and database. A simple example is sql_utilities.get_sql_data('PRDDMXSQL', 'DMX_WDI', '111.NY.GDP.COAL.RT.ZS')

which will retrieve the series 111.NY.GDP.COAL.RT.ZS} from the SQL serverPRDDMXSQL} and database DMX\_WDI}. Theseriesname} can be a list of seriescodes, for example sql_utilities.get_sql_data('PRDDMXSQL', 'DMX_WDI', ['111.NY.GDP.COAL.RT.ZS', '111.NY.GDP.DISC.KN'])

will retrieve both series. For SQL files it is possible to store the same series with different frequencies. To distinguish between the frequencies, the parameter freq can take on the values "A", "Q", "M", for annual, quarterly, and monthly data. The default value is None and the function will try to return all available frequencies. If a frequency is specified, the function will return the series with that frequency if it exists, otherwise will return None. Since this behavior is inconsistent with dmx_utilities, this behavior will probably change soon. It is possible to specify a list for seriesname so that many series from the same server and dbname can be retrieved at once. The result will be a pandas.DataFrame with a column for each series. This will be slightly more efficient than querying each series independently and combining the results afterwards. The server, dbname and freq must be common to all series, i.e., it is not possible to get data from multiple SQL servers or databases with one use of this function. The option scale can be set to values of "sql", "default", 1, 'u', 'k', 'm', 'b', 't'. If the value is 'sql' or 'default', the scale stored as metadata will be applied, while 1, u will return the original values, and 'k/m/b/t' will correspond to scaling in thousands, millions, billions, and trillions. If the option scale_label is set to True, the scale is shown in the columns.
#### `get_sql_metadata(server, dbname, seriesname=None, substr=None, standard=False, debug=False)`

This function will retrieve the metadata of a series or multiple series from a given server and database. For example
```python
>>> metadata = sql_utilities.get_sql_metadata('PRDDMXSQL',
```

'DMX_WDI', '111.NY.GDP.COAL.RT.ZS') >>> print(metadata) OID Documentation Country_Code   Country_Name Subject_Matter Alias                   ... Observations_Updated_By UDP_CreatedDate UDP_CreatedBy UDP_UpdatedDate UDP_UpdatedBy SyncID

111.NY.GDP.COAL.RT.ZS 67448 None 111 United States None None None None None 2019-04-04 15:13:52.663   IMFNT\TKing                          None

will retrieve the metadata from the series 111.NY.GDP.COAL.RT.ZS from the server PRDDMXSQL and database DMX_WDI. The output will be a pandas.DataFrame containing available information on the series containing 41 columns, some of which are UDP_CreatedBy, UDP_CreatedDate, UDP_UpdatedBy, UDP_UpdatedDate, Source, Sector. These columns can be used to understand which series are of interest. Note that this metadata depends on the creator of the series inputting this information, otherwise the fields will be empty. It is also possible to retrieve the metadata for multiple series at once, for example
```python
>>> serieslist = ['111.NY.GDP.COAL.RT.ZS', '111.NY.GDP.DISC.KN']
>>> metadata = sql_utilities.get_sql_metadata('PRDDMXSQL', 'DMX_WDI', serieslist)
```

>>> print(metadata)

OID Documentation Country_Code   Country_Name Subject_Matter Alias ... Observations_Updated_By UDP_CreatedDate UDP_CreatedBy UDP_UpdatedDate UDP_UpdatedBy SyncID

111.NY.GDP.COAL.RT.ZS 67448  None   111                United States None          None     ... None None None 2019-04-04 15:13:52.663                 IMFNT\TKing   None

111.NY.GDP.DISC.KN   69728    None    111 United States None                         None    ... None None None 2019-04-04 15:13:52.663   IMFNT\TKing  None

will retrieve the metadata for all series in serieslist at once and the result will be a row for each series. If no seriesname is specified, the metadata will be retrieved for all series in the SQL server and database specified. The option substr can be used to get metadata only for series containing specific substrings,
```python
>>> metadata = sql_utilities.get_sql_metadata('PRDDMXSQL', 'DMX_WDI',
substr='193')
```

will retrieve metadata for all series containing the substr "193". The substr can be a list, so that
```python
>>> metadata = sql_utilities.get_sql_metadata('PRDDMXSQL', 'DMX_WDI', substr=['193', 'GDP'])
```

will retrieve metadata for series containing both "193" and "GDP". The substrings are case-insensitive, and in the case of DMX the order matters, so that series of the form "193*GDP*" where * is any character will match, but "GDP*193" will not. Finally, if the option standard is set to True, only the columns for Topic and UDP_UpdatedDate will be returned.

## 3.8 Haver

Haver is a commercial database system that the Fund purchases. It contains approximately 160 databases such as USECON, CANADA, JAPAN, EUNA, INTDAILY and others. Haver also provides some executables which allow programs to query the data and available series. The data for Haver is stored in propietary database files prepared by Haver and are kept locally within the Fund. These files are continuously updated to have the latest data and typically Haver has a very quick turnaround between the release of official statistics and updates. Haver provides its own official Haver library which can be accessed with
```python
import Haver
```

The code to retrieve Haver was originally written independently at the Fund, but for imf_datatools ver 1.2 it was rewritten to rely on the official Haver library. Users can check the source code if they wish to change the behavior of the original library. Documentation can be found at the Haver website’s client area at http://www.haver.com/clientarea/news.html 13 .
#### `get_databases()`

This function returns all available databases, such as USECON, etc. as a list. As of 2021, the IMF is subscribed to 160 databases. Each database can contain several tens of thousands up to several hundreds of thousands of series codes.
```python
get_all_haver_series(database) Deprecated in ver 1.2.
13 See http://www-intranet.imf.org/fundwide/info/EconFinData/Pages/ViewItem.aspx?itemId=2486 for information on how to access the
```

client area.

#### `get_haver_data(code, scale=None, eop=False, periods=False, debug=False)`

This function will retrieve data from Haver in the form of pandas.DataFrames. If a single series code like GDP@USECON is given, the result will be a pandas.DataFrame with one column for this data. If multiple series codes are given as a list, all valid series codes will be retrieved and each will be a column in the pandas.DataFrame.
```python
>>> df = haver_utilities.get_haver_data('GDP@USECON')
```

>>> df[-5:] # print final 5 periods GDP@USECON dates 2018-07-01     20749.8 2018-10-01     20897.8 2019-01-01     21098.8 2019-04-01     21340.3 2019-07-01     21542.5

This is an example of retrieving multiple Haver codes at once:
```python
# Returns a list of series like 'A11101A', 'A11101AE', ...
serieslist = ['GDP@USECON', 'IP@IP']
df = haver_utilities.get_haver_data(serieslist)
df[-5:] # print final 5 periods
```

GDP@USECON     IP@IP 2021-03-01         NaN   99.1237 2021-04-01     22731.4   99.1655 2021-05-01         NaN   99.9870 2021-06-01         NaN 100.1849 2021-07-01         NaN 101.1148

If the option eop is set to True, the dates in the DataFrame’s index will be set to the final date of the period:
```python
>>> df = haver_utilities.get_haver_data('GDP@USECON', eop=True)
```

>>> df[-5:] # print final 5 periods GDP@USECON dates 2018-09-30     20749.8 2018-12-31     20897.8 2019-03-31     21098.8 2019-06-30     21340.3 2019-09-30     21542.5

If the option periods is set to True, the dates in the DataFrame’s index will be a PeriodIndex instead of a DatetimeIndex. Note that in this case trying to retrieve multiple series with different frequencies will result in an error.

By default Haver data will be returned in the scale that is shown in the metadata (use the get_haver_metadata function to retrieve this). If the option scale is set to one of 1, k, M, B, T, the values will be converted to use the specified scales of unit, thousands, millions, billions, trillions.

For example for GDP@USECON, the metadata shows that the scale is Bil. $ and the above code examples show that indeed it is in billions. However, when comparing multiple series, each series may have its own units. To undo these, specify 1 (one) as the scale:
```python
df = haver_utilities.get_haver_data('GDP@USECON', scale=1)
df[-5:] # print final 5 periods
```

2018-07-01 2.074980e+13 2018-10-01 2.089780e+13 2019-01-01 2.109880e+13

2019-04-01      2.134030e+13 2019-07-01      2.154250e+13

If for example T is specified, the values will be converted to trillions:
```python
df = haver_utilities.get_haver_data('GDP@USECON', scale='T')
df[-5:] # print final 5 periods
```

2018-07-01     20.7498 2018-10-01     20.8978 2019-01-01     21.0988 2019-04-01     21.3403 2019-07-01     21.5425

#### `get_haver_metadata(code, debug=False)`

Get metadata from specified code(s) or a full database. Either a valid code as a str or a list of codes must be specified. Returns a pandas.DataFrame is created with each series code as a row. To retrieve metadata for an entire database, see
```python
get_all_haver_metadata function.
```

The Haver database maintains very good metadata, and each series will contain the following 18 columns:
1. database
2. code
3. startdate
4. enddate
5. frequency
6. descriptor
7. numobs
8. datetimemod
9. magnitude
10. decprecision
11. diftype
12. aggtype
13. datatype,
14. group
15. geography1
16. geography2
17. shortsource
18. longsource
#### `get_all_haver_metadata(database)`

Retrieve all metadata for a given database. Typically each database has several tens of thousands of series, so this may take a few tens of seconds. Returns a df with the same 18 columns as get_haver_metadata. for each series contained in database.

## 3.9 World Bank

The World Bank maintains an online web API service 14 This API allows programs to connect and retrieve data, metadata as soon as it becomes available. The worldbank_utilities library connects to this API and parses the available information. Currently the imf_datatools focuses on retrieving economic data, but the World Bank also has an API for other data, such as the Climate Data API 15 . 14 See https://datahelpdesk.worldbank.org/knowledgebase/articles/889392-about-the-indicators-api-documentation for official documenta-

tion. 15 https://datahelpdesk.worldbank.org/knowledgebase/articles/902061-climate-data-api

Contact Econometric Support if other types of data retrieval are necessary and these can be built in.
#### `get_database_info()`

This function will retrieve information on the available databases within the World Bank API and returns as a pandas.DataFrame. The index will be the sorted database names and the columns will be
1. id
2. lastupdated
3. name
4. description
5. dataavailability
6. metadataavailability
7. concepts
See the official documentation on the meaning of these items. As of January 2020 there are 57~databases available. If the option debug is specified, the original downloaded XML data will be attempted to be saved as a local file.
#### `get_all_worldbank_metadata(debug=False)`

Retrieves metadata on all available series and descriptions and returns as a ‘pandas.DataFrame}. The index will be the series names, and the columns will be
1. name
2. source
3. sourceOrganization
4. unit
5. topic_ids
6. topic_values
See the official documentation on the meaning of these items. As of January 2020 there are 17, 328~series codes available. If the option debug is specified, the original downloaded data will be attempted to be saved as a local file.
#### `get_worldbank_countries(debug=False)`

Retrieves a list of World Bank countries and regions and associated information and saves as a pandas.DataFrame. The index will be the ISO 3-letter codes, with columns of
1. name
2. iso2Code
3. region
4. capitalCity
5. incomeLevel
6. latitude
7. longitude
See the official documentation on the meaning of these items. Note that as of January 2020 Kosovo is not assigned a standard code, so while the World Bank uses XK and XKX, this may be different for other organizations. This function is used by ecos_sdmx_utilities.get_weo_country_codes() to combine WEO country code information with the World Bank country information (see Sec. 3.4). If the option debug is specified, the original downloaded XML data and resulting table (csv) will be attempted to be saved as a local file.
#### `get_worldbank_data(seriesname, country, counterpart=None, freq='A', longformat=False, dataformat='json',`

```python
debug=False)
```

Retrieves data from the World Bank API. The countries are ISO 3-letter codes, such as 'CHN', 'USA', 'JPN', etc., or a list of such countries, such as ['CHN', 'USA', 'JPN']. The special keyword all can be used to specify all countries

at once. The seriesname can be a series name such as SP.POP.TOTL or a list of such series such as ['SP.POP.TOTL', 'AG.AGR.TRAC.NO']. The underlying API cannot actually handle multiple series codes unless the source ID is specified, but this function will internally send each series code and merge the results together. Examples:
```python
# Get population data for China
>>> df = worldbank_utilities.get_worldbank_data('SP.POP.TOTL', 'CHN')
```

>>> print(df[-5:]) CHN.SP.POP.TOTL date 2015-01-01     1.371220e+09 2016-01-01     1.378665e+09 2017-01-01     1.386395e+09 2018-01-01     1.392730e+09 2019-01-01              NaN

```python
# Get multiple series and countries
>>> df = worldbank_utilities.get_worldbank_data(['SP.POP.TOTL', 'AG.AGR.TRAC.NO'],
```

['CHN', 'USA']) >>> print(df[-5:]) CHN.SP.POP.TOTL USA.SP.POP.TOTL CHN.AG.AGR.TRAC.NO USA.AG.AGR.TRAC.NO date 2015-01-01     1.371220e+09      320742673.0        NaN                 NaN 2016-01-01     1.378665e+09      323071342.0        NaN                 NaN 2017-01-01     1.386395e+09      325147121.0        NaN                 NaN 2018-01-01     1.392730e+09      327167434.0        NaN                 NaN 2019-01-01              NaN              NaN        NaN                 NaN

If the option longformat is specified as True, the data will be returned in a long format so that each row contains a unique combination of countrycode, countryname, dates and each indicator is a column.
```python
>>> df = worldbank_utilities.get_worldbank_data(['SP.POP.TOTL', 'AG.AGR.TRAC.NO'],
['CHN', 'USA'], long=True)
```

>>> df.head()
```python
countrycode countryname      dates    SP.POP.TOTL AG.AGR.TRAC.NO
```

0         CHN       China 2019-01-01            NaN            NaN 1         CHN       China 2018-01-01 1.392730e+09              NaN 2         CHN       China 2017-01-01 1.386395e+09              NaN 3         CHN       China 2016-01-01 1.378665e+09              NaN 4         CHN       China 2015-01-01 1.371220e+09              NaN >>> df.tail()
```python
countrycode    countryname       dates SP.POP.TOTL AG.AGR.TRAC.NO
```

115         USA United States 1964-01-01 191889000.0         4783000.0 116         USA United States 1963-01-01 189242000.0         4755000.0 117         USA United States 1962-01-01 186538000.0         4730000.0 118         USA United States 1961-01-01 183691000.0         4690000.0 119         USA United States 1960-01-01 180671000.0               NaN

```python
Currently the only supported format for parsing the response is dataformat='json'. If the option debug=True is specified
```

more output is shown on screen and text files containing the response will be saved in the working directory. Starting in Nov 2020, some new series containing counterparts were added (see blog article for details and links to code). By specifying the counterpart argument, data can be retrieved from these series. The counterpart country codes are not consistent with the ISO country codes used for other parts of the API. For this reason this function will return the counterpart countries by name and not ISO code. In previous versions, when specifying a counterpart the return format

was forced to be in long format, now this is relaxed so series names will be [countr].[series].[counterpart]. For the counterpart argument, the options "WLD" for “World” and "all" for all counterparts will be useful.
```python
>>> df = worldbank_utilities.get_worldbank_data('DT.GPA.DPPG', 'AFG', counterpart='all')
```

>>> df.tail() AFG.DT.GPA.DPPG_Asian Dev. Bank     ... AFG.DT.GPA.DPPG_World Bank-IDA dates                                           ... 2018-01-01                                  0.0 ...                                                                       0.0 2019-01-01                                  0.0 ...                                                                       0.0 2020-01-01                                  0.0 ...                                                                       0.0 2021-01-01                                  0.0 ...                                                                       0.0 2022-01-01                                  0.0 ...                                                                       0.0

[5 rows x 19 columns]

```python
>>> df = worldbank_utilities.get_worldbank_data('DT.GPA.DPPG', 'AFG', counterpart='all', longformat=True)
```

>>> df.tail() dates country value          counterpart       series 318 2022-01-01     AFG    0.0             Denmark DT.GPA.DPPG 319 2022-01-01     AFG    0.0             Croatia DT.GPA.DPPG 320 2022-01-01     AFG    0.0               China DT.GPA.DPPG 321 2022-01-01     AFG    0.0            Bulgaria DT.GPA.DPPG 322 2022-01-01     AFG    0.0 Asian Dev. Bank      DT.GPA.DPPG

In some cases the data with counterpart may have both annual and monthly frequencies. The default is to retrieve the
```python
data for annual frequency with option freq='A', this can be changed to freq='M' as needed.
# Default is annual frequency
>>> df = worldbank_utilities.get_worldbank_data('DT.AMT.BLAT.CD', 'AFG', counterpart='WLD')
```

>>> df.tail() AFG.DT.AMT.BLAT.CD_World dates 2019-01-01                 4400000.0 2020-01-01                  500000.0 2023-01-01                50268887.5 2024-01-01                50268887.5 2025-01-01                47615027.5

```python
# Specify monthly freq
>>> df = worldbank_utilities.get_worldbank_data('DT.AMT.BLAT.CD', 'AFG', counterpart='WLD', freq='M')
```

>>> df.tail() AFG.DT.AMT.BLAT.CD_World dates 2025-05-01                       0.0 2025-06-01                 2692006.2 2025-10-01                21394187.5 2025-11-01                       0.0 2025-12-01                 2134646.2

#### `get_worldbank_metadata(seriesname)`

Get metadata for a specific series or list of series. The returned result will be a df with an index of series names, and the columns will be
1. name
2. source

3. sourceOrganization
4. unit 5.topic_ids
5. topic_values
See the official documentation on the meaning of these items. This function uses the same API as get_all_worldbank_metadata and returns the same result for the specified series.
#### `search_worldbank_metadata(search_str, debug=False)`

Searches within the description of series and returns a df of seriesnames and their descriptions that matches search_str1. Thesearch_str1 must be a single ‘str1 and the search is case-insensitive.
```python
>>> df= worldbank_utilities.search_worldbank_metadata('gdp')
```

>>> print(df.shape) (658, 1) >>> print(df[-5:]) description SH.XPD.TOTL.ZS                     Health expenditure, total (% of GDP) SL.GDP.PCAP.EM.KD     Labor productivity is used to assess a country... SL.GDP.PCAP.EM.KD.ZG GDP per person employed (annual % growth)\nAnn...
```python
SL.GDP.PCAP.EM.XD     GDP per person employed, index (2000 = 100)\nG...
```

TG.VAL.TOTL.GD.ZS     Merchandise trade (% of GDP)\nMerchandise trad...

#### `get_worldbank_topics(debug=False)`

Get available topics within World Bank data and return a df of topic information. As of January 2020 there are 21 topics
```python
available. If the option debug=True is specified, more output is shown and the information is written out to the working
```

directory.

## 3.10 EDI

The EDI (Economic Data Interface) is a browser-based data aggregation-dissemination service available within the Fund. The webpage is at https://edi.imf.org/#/ and users can browse data and also download from it. Another feature is that it is available through Pulse Secure so is a convenient way to tap into Fund resources if they are not available that way. The EDI has an API which allows users to use programming languages to connect to it and retrieve the data they choose. The edi_utilities library has been built to connect to this EDI API, and allows users to query the available databases,
```python
country codes, series codes, and download both data and metadata. Technical support requests for the EDI itself should
```

be sent to ITDES-CATS and support for the API should be sent to Econometric Support. For all data retrieval functions, if the option scale is specified this will scale the data values into the specified scale. This can take on values of 'edi' or 'default' which will use the scales stored as metadata, or specifying one of 1, u, k, m, b, t will scale the values by 1, 103 , 106 , 109 , 1012 . There is also an option scale_label for the data retrieval functions, and if this is set to True the output columns will contain additional information on the scales and units. For example not specifying scale gives
```python
df = edi_utilities.get_edi_weo_data('111', 'NGDP', vintage="2023-10")
df[-3:]
```

111NGDP.A dates 2026-01-01 3.022388e+13 2027-01-01 3.142886e+13 2028-01-01 3.269037e+13

```python
but specifying scale='default' will use the stored scale (in this case billions):
df = edi_utilities.get_edi_weo_data('111', 'NGDP', vintage="2023-10", scale='default')
df[-3:]
```

111NGDP.A dates 2026-01-01 30223.880505 2027-01-01 31428.864888 2028-01-01 32690.373203

```python
and specifying scale_label=True will add this to the columns:
df = edi_utilities.get_edi_weo_data('111', 'NGDP', vintage="2023-10", scale='default', scale_label=True)
df[-3:]
```

111NGDP.A (Billions/National Currency) dates 2026-01-01                           30223.880505 2027-01-01                           31428.864888 2028-01-01                           32690.373203

```python
In the above we specified scale='t' for 'trillions'.
```

When applicable the option longformat can be used to transform the output into long format. This option is similar to that of EcOS. Another option get_url is available for the data retrieval functions, this will return the URL for the corresponding data retrieval. This URL can in turn can be turned into a df using the function get_edi_data_from_url(url). All functions to retrieve time series data below admit arguments to slice the returned dataframe by start and end dates that
```python
may be specified by setting for example start='2018-01-01' and end='2019-01-01'. These start and end datestrings
```

are simply passed alongside the other arguments. Note on WEO vintages Due to a change in the EDI, it is now necessary to specify the vintage explicitly when calling get_edi_weo_data(). Specifying the add_vintage option to True will work as well when retrieving all vintages. Otherwise all vintages will be retrieved with column names that do not allow distinguishing them. To get the latest vintage, for Python use max(edi_utilities.get_dimension_values('weo-published', 'vintage'))

or for R
```r
library(reticulate)
imf_datatools <- import("imf_datatools")
```

max(imf_datatools$edi_utilities$get_dimension_values('weo-published', 'vintage'))

or for Stata
```stata
ediuse values, database(weo-published) var(vintage)
```

will provide a list of all vintages. Note on GAS database As noted above in Sec.3.4, the GAS (Global Assumptions Data) is a special case where by default the series code used for retrieval is different from the column name returned by the database. Similar to the get_ecos_sdmx_data() function,
```python
the get_edi_ecos_data() function allows the option use_original_indicator=True to set the output to have the same
```

indicator as what was used in the input.

The default behavior of get_edi_ecos_data('gas-live', '001', 'poilapsp') is the below:

001PZPIOIL.A dates 1970-01-01        2.225950 1971-01-01        3.111986 1972-01-01        3.596700 1973-01-01        4.172908 1974-01-01       12.358646 1975-01-01       11.507955
```python
adding the option use_original_indicator=True will give
get_edi_ecos_data('gas-live', '001', 'poilapsp', use_original_indicator=True)
```

001POILAPSP.A dates 1970-01-01          2.225950 1971-01-01          3.111986 1972-01-01          3.596700 1973-01-01          4.172908 1974-01-01         12.358646 1975-01-01         11.507955
#### `get_databases(debug=False)`

Returns a df containing the name of available database names as the index and columns for shortname, description, environment, primary_keys. The primary_keys column contains the dimensions to filter on for that database when retrieving data. Running this function gives an output like the following shortname   ...                           primary_keys database              ... bloomberg                    Bloomberg   ...                    ticker/field/freq haver                            Haver   ...                           db/varname weo-published                      WEO   ...       vintage/country/indicator/freq

and it can be seen that for example the database bloomberg takes in the filters ticker, field, and freq. Note that for Haver, although the input dimensions are db and varname, to make it easier for users the actual get_edi_haver_data function below uses the combination varname@db like GDP@USECON to make it easier for users.
#### `get_dimensions(database, input_only=True, debug=False)`

Returns a df of the input dimensions of a database to filter on, similar to the column primary_keys in get_databases, but with more description.
#### `get_dimension_values(database, dimension, substr=None, debug=False)`

Returns all available values for a given dimension. For example
```python
import edi_utilities
dims = edi_utilities.get_dimensions('weo-published')
print(dims)
```

description name
```python
country       Country Code
```

indicator        Indicator vintage       Vintage Date
```python
freq       Frequency Code
```

shows that the database weo-published takes in filters country, indicator, vintage, freq and we can query the available
```python
country values with
vals = edi_utilities.get_dimension_values('weo-published', 'country')
len(vals)
```

and this shows that there are 356~countries available in this database.
#### `get_edi_data_from_url(url, add_vintage=False, scale_factor=1, scale_label=False, longformat=False,`

```python
debug=False)
```

Returns the corresponding df for a given URL that specifies EDI data. This URL can be created using the get_url option for the data retrieval options.
#### `get_edi_haver_data(havercode, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieves Haver data from EDI. Input havercode can be a Haver code like 'GDP@USECON' or a list of Haver codes like ['GDP@USECON', 'IP@IP']. Returns a df with the Haver codes as columns.
#### `get_edi_bloomberg_data(ticker, field, scale=None, scale_label=False, get_url=False, debug=False)`

Retrieves Bloomberg data from the EDI. Inputs ticker and field can be a single Bloomberg ticker or field, or can be a list.
#### `get_edi_weo_data(country, indicator, freq='A', vintage='current', add_vintage=False, longformat=False,`

```python
scale=none, scale_label=False, get_url=False, debug=False)
```

As mentioned in the above note in Sec. 3.10, it is necessary to now specify a vintage explicitly. Retrieves WEO data from EDI. For this database, by default the annual data for the current vintage is retrieved. This is for WEO data only but is applied as it is expected that most users expect annual data and the current vintage for WEO. To get quarterly data or previous vintages, use the options freq or vintage. The inputs country and indicator can be single str values or a list of values. The special option 'all' can be specified to retrieve data for all countries for a given set of indicators or all indicators for a given set of countries, but this cannot be specified for both country and indicator together. If the option add_vintage is set to True, the vintage information will be added to the columns to distinguish different
```python
vintages. When specifying vintages, the special option vintage='all' can be used to retrieva all vintages at once.
# Default is to get annual data for current vintage
df = edi_utilities.get_edi_weo_data('111', 'NGDP', vintage="2023-10")
df[-3:]
```

111NGDP.A dates 2026-01-01 3.022388e+13 2027-01-01 3.142886e+13 2028-01-01 3.269037e+13

```python
# Get data for multiple countries, indicators
df = edi_utilities.get_edi_weo_data(['111', '193'], ['NGDP', 'PPPPC'], vintage="2023-10")
df[-3:]
```

111NGDP.A    111PPPPC.A     193NGDP.A    193PPPPC.A dates 2026-01-01 3.022388e+13 88935.380304 2.857887e+12 69909.362176 2027-01-01 3.142886e+13 92051.711123 3.000490e+12 71959.491571 2028-01-01 3.269037e+13 95301.969440 3.148119e+12 74091.063445

```python
# Specify freq, get vintages
df = edi_utilities.get_edi_weo_data('111', 'NGDP', freq='Q', vintage='2020-01')
df[-3:]
```

111NGDP.Q dates 2021-04-01 2.301632e+13 2021-07-01 2.322117e+13 2021-10-01 2.342382e+13

```python
# Add vintage info
df = edi_utilities.get_edi_weo_data('111', 'NGDP', freq='Q',
vintage='2020-01', add_vintage=True)
```

111NGDP.Q@2020-01-01 dates 2021-04-01          2.301632e+13 2021-07-01          2.322117e+13 2021-10-01          2.342382e+13

```python
# Add scale, scale labels, and vintage info
df = edi_utilities.get_edi_weo_data('111', 'NGDP', freq='Q', scale='default',
scale_label=True, vintage='2020-01', add_vintage=True)
df[-3:]
```

111NGDP.Q@2020-01-01 (Billions/National Currency) dates 2021-04-01                                       23016.322724 2021-07-01                                       23221.170234 2021-10-01                                       23423.818907

```python
get_edi_ecos_data(database, country, indicator, freq='A', partner_country=None, sector=None, classification=N
unit=None, longformat=False, scale=none, scale_label=False, use_original_indicator=False, get_url=False,
debug=False)
```

Get EcOS databases that are not WEO or GFS from EDI. The available EcOS databases can be retrieved with the
```python
get_databases() function (Sec. 3.4). The inputs country, indicator, scale, scale_label are the same as for
get_edi_weo_data. For the database GFS, there are no indicators so the inputs sector, classification, and unit
```

can be used to filter the data. Similarly, for the database DOT, the input partner_country can be used to filter partner countries.
```python
As mentioned in the note in Sec.3.10, the use_original_indicator=True option can be used for the GAS-LIVE database
```

to force the output column names use the input indicator names.
#### `get_edi_gfs_data(country, classification=None, sector=None, unit=None, freq='A', longformat=False,`

```python
scale=none, scale_label=False, get_url=False, debug=False)
```

Get EcOS data for database GFS. Same as calling get_edi_ecos_data with database being GFS. At the minimum the
```python
country must be specified, and additional filters for classification, sector, unit can be specified.
```

#### `get_edi_wdi_data(country, indicator, freq='A', longformat=False, scale=none, scale_label=False,`

```python
get_url=False, debug=False)
```

Get World Bank WDI data using EDI.
#### `get_edi_csd_desk_data(country, indicator, freq='A', vintage='current', vintagetimestamp=None, exercise=None,`

```python
longformat=False, scale=none, scale_label=False, get_url=False, debug=False)
```

Get CSD desk data from EDI.

```python
Here, exercise can take the values 'SR' or 'WEO'. If exercise=None then hopefully all exercises that match the criteria
```

are returned.

```python
Vintage refers to a month and year combination, formatted as 'YYYY-MM' for example vintage='2018-05'. If no vintage
```

is specified then all vintages, or the most recent vintage will be returned. It may accept a list of vintages.

```python
The vintagetimestamp refers to a yyyymmdd formatted string, for example vintagetimestamp='20180605'. Note that
```

the vintage and the vintage timestamp may not always have the exact same month since the vintage can be updated at a later date than the vintage.
```python
# example
df = edi_utilities.get_edi_csd_desk_data(country='233',indicator='bop10',exercise='sr',vintage='2018-01',vint
```

#### `get_edi_csd_ccx_data(country, indicator, freq='A', vintage='current', exercise=None, longformat=False,`

```python
scale=none, scale_label=False, get_url=False, debug=False)
```

Get CSD exercise data from EDI.

#### `get_edi_cf_data(country, indicator, longformat=False, freq=None, scale=none, scale_label=False,`

```python
get_url=False, debug=False)
```

Get Consensus Forecasts data from EDI.

Note that for older versions of the code, a single seriescode like 134PCPI_YOY was specified whereas a change in Feb 2023 changed this to specify separate country and indicator like 134 and PCPI_YOY as shown below.
```python
# previous code (deprecated)
# df = edi_utilities.get_edi_cf_data('133PCPI_YOY', freq='M')
# New code (correct)
df = edi_utilities.get_edi_cf_data('133', 'PCPI_YOY', freq='M')
print(df)
```

134PCPI_YOY.M dates 1989-10-01       2.991667 1989-11-01       2.988000 1989-12-01       2.964000 1990-01-01       2.887500 1990-02-01       2.978000 ...                   ... 2022-09-01       7.774000 2022-10-01       8.073163 2022-11-01       8.229809 2022-12-01       8.257233 2023-01-01       6.437487

The older version is now deprecated and should not be used, it is recommended to update the imf_datatools to the latest version.

#### `get_edi_metadata(database, country=None, indicator=None, freq=None, seriescode=None, vintage=None,`

```python
ticker=None, field=None, get_url=False, debug=False)
```

Get metadata from EDI by specifying databases to select from. database can either be a single database or a list of databases. Can filter on the dimensions country, indicator, seriescode, vintage, ticker, field and freq. By default
```python
no filtering is done, so if database='weo-published' and country='111' and indicator='NGDP' are specified, results
```

are returned for all frequencies and vintages.

## 3.11 data.imf.org

The website https://data.imf.org is the Fund’s official external data dissemination platform. The platform includes an API which allows access to the data for anybody with an internet connection. The official documentation is at https://datahelp.imf.org/knowledgebase/articles/838041-sdmx-2-0-restful-web-service. While the API is powerful and generally does a good job of retrieving data, at times the connection is cut off, especially after intense use with the error message Bandwidth Limit Exceeded. In this case the only possible action is to wait for the service to allow you to resume. Obtaining data from the API can be a little tricky. The first step is to understand the dimensions that the database you are querying is expecting. For example for the database BOP the dimensions can be queried with
```python
dbname = 'BOP'
dims = imf_ext_utilities.get_query_dimensions(dbname)
print(dims)
```

conceptref                                            values codelist CL_FREQ                FREQ                                [A, B, Q, M, D, W] CL_AREA_BOP        REF_AREA [AF, AL, DZ, AD, AO, AI, AG, AR, AM, AW, AU, A... CL_INDICATOR_BOP INDICATOR [IAFR_BP6_EUR, IAFR_BP6_XDC, IAFR_BP6_USD, IAC...

From this we see that the database is expecting three dimensions, the frequency, area and indicator. The allowed values of each dimension are shown in the column values. So a valid query in this case is then
```python
series = ['IAPD_BP6_XDC', 'IAPDG_BP6_USD']
df = imf_ext_utilities.get_imf_ext_data(dbname, ['A', 'JP', series])
df[-5:]
```

JP.IAPD_BP6_XDC.A JP.IAPDG_BP6_USD.A dates 2016-01-01       2.772117e+14        3.444450e+09 2017-01-01       2.743704e+14        3.413785e+09 2018-01-01       2.700951e+14        3.622683e+09 2019-01-01       2.871133e+14        3.368279e+09 2020-01-01       3.103983e+14        2.763942e+09

The parameter to pass into get_imf_ext_data is the database name, followed by a list of dimensions. This list of dimensions can include lists, so for example to get more data, the above query can be changed to
```python
series = ['IAPD_BP6_XDC', 'IAPDG_BP6_USD']
df = imf_ext_utilities.get_imf_ext_data(dbname, [['A', 'M'], ['US', 'JP'], series])
df[-5:]
```

JP.IAPD_BP6_XDC.A JP.IAPDG_BP6_USD.A US.IAPDG_BP6_USD.A dates 2016-01-01       2.772117e+14        3.444450e+09                 0.0 2017-01-01       2.743704e+14        3.413785e+09                 0.0 2018-01-01       2.700951e+14        3.622683e+09                 0.0 2019-01-01       2.871133e+14        3.368279e+09                 0.0 2020-01-01       3.103983e+14        2.763942e+09                 0.0

in which case all available combinations are returned. If a dimension is skipped over using the special None variable, all possible combinations for that dimension are returned:
```python
series = IAPD_BP6_XDC'
# Skip frequency
df = imf_ext_utilities.get_imf_ext_data(dbname, [None, 'JP', series])
```

```python
df[-5:]
```

JP.IAPD_BP6_XDC.A     JP.IAPD_BP6_XDC.Q dates 2020-01-01          3.103983e+14          2.906673e+14 2020-04-01                   NaN          2.979669e+14 2020-07-01                   NaN          3.014217e+14 2020-10-01                   NaN          3.103983e+14 2021-01-01                   NaN          3.161939e+14

In this case the frequency was set to None, resulting in both annual and quarterly frequency being retrieved. If the dimension for countries is set to None, all countries are retrieved:
```python
# Get annual data for all countries
df = imf_ext_utilities.get_imf_ext_data(dbname, ['A', None, series])
df[-5:]
```

IS.IAPD_BP6_XDC.A PA.IAPD_BP6_XDC.A MU.IAPD_BP6_XDC.A SN.IAPD_BP6_XDC.A                    ...   KY.IAPD_BP6_XDC. dates                                                                                                  ... 2016-01-01       6.287500e+10       1.095956e+10       3.247870e+11    8.216734e+11                    ...         2.825343e+1 2017-01-01       9.379700e+10       1.165304e+10       5.130490e+11    8.488634e+11                    ...         3.052228e+1 2018-01-01       1.589580e+11       1.288800e+10       4.944290e+11    1.027574e+12                    ...         3.000723e+1 2019-01-01       1.807300e+11       1.230859e+10       5.143550e+11             NaN                    ...         3.622788e+1 2020-01-01       1.836040e+11       1.331234e+10                NaN             NaN                    ...                  Na

[5 rows x 80 columns]

Note that skipping multiple dimensions will consume resources both for data retrieval and network bandwidth, and may lead to the connection being unable for a while. It is recommended that only one dimension is skipped.
#### `get_databases(debug=False)`

Get available databases and return a pandas.DataFrame with the database code and a column providing the description.
#### `get_query_dimensions(database, debug=False)`

Get the query dimensions for a given database. Returns a pandas.DataFrame with the index containing the necessary dimensions to retrieve data. The column values contains a list of all valid values for each dimension.
#### `get_dimension_values(codelist, debug=False)`

Returns the valid parameters for a given input dimension. For example for the BOP database the dimensions are CL_FREQ, CL_AREA_BOP,CL_INDICATOR_BOP‘. The dimension names for each database are unique to that database, so there is no need to specify the database name.
#### `get_series_codes(database, debug=False)`

Quickhand function to retrieve valid series codes for a given database. Searches for a dimension name with indicator in it and returns a pandas.DataFrame with an index of series codes and a column with descriptions.
#### `get_country_codes(database, debug=False)`

Quickhand function to retrieve valid country codes for a given database. Searches for a dimension name with area or countr in it and returns a pandas.DataFrame with an index of country codes and a column with names.
#### `get_imf_ext_data(database, *params,                                                  longformat=False, scale=None,`

```python
scale_label=False,                            debug=False)
```

Function to retrieve data from data.imf.org.          Specify the database name, followed by a list of parameters. The list of parameters may contain individual values as strs, or may be a list of str values.              Use the
```python
get_query_dimensions(database) function to retrieve the dimensions for each database, and the get_dimension_values(codelist
```

function to retrieve valid values for each dimension.

If a dimension is set to None, all possible values of that dimension are searched for. Care is needed as this may lead to trying to retrieve large amounts of data, which will typically lead to the connection becoming unavailable for a while.
```python
# Simple example using BOP.
# The only dimensions necessary are frequency, country, indicator.
dbname = 'BOP'
```

```python
# Get dimensions of this database
dims = imf_ext_utilities.get_query_dimensions(dbname)
```

conceptref                                            values codelist CL_FREQ                FREQ                                [A, B, Q, M, D, W] CL_AREA_BOP        REF_AREA [AF, AL, DZ, AD, AO, AI, AG, AR, AM, AW, AU, A... CL_INDICATOR_BOP INDICATOR [IAFR_BP6_EUR, IAFR_BP6_XDC, IAFR_BP6_USD, IAC...

```python
# Get valid indicators
serieslist = imf_ext_utilities.get_dimension_values('CL_INDICATOR_BOP')
len(serieslist)
serieslist = ['IAFR_BP6_XDC', 'IAFR_BP6_USD']
```

```python
# Get data for a single annual series
series = 'IAFR_BP6_USD'
df = imf_ext_utilities.get_imf_ext_data(dbname, ['A', 'JP', series])
```

JP.IAFR_BP6_USD.A dates 2016-01-01       8.444119e+12 2017-01-01       8.975693e+12 2018-01-01       9.185265e+12 2019-01-01       9.992715e+12 2020-01-01       1.105603e+13

```python
# Get data for multiple frequencies, countries
df = imf_ext_utilities.get_imf_ext_data(dbname, [['A', 'Q'], ['JP', 'CH'], series])
```

CH.IAFR_BP6_USD.A JP.IAFR_BP6_USD.A CH.IAFR_BP6_USD.Q JP.IAFR_BP6_USD.Q dates 2020-01-01       6.044633e+12       1.105603e+13       5.390063e+12       1.033164e+13 2020-04-01                NaN                NaN       5.473039e+12       1.051040e+13 2020-07-01                NaN                NaN       5.711973e+12       1.074877e+13 2020-10-01                NaN                NaN       6.044633e+12       1.105603e+13 2021-01-01                NaN                NaN                NaN       1.082070e+13

```python
# Skip a dimension with None, in this for countries
df = imf_ext_utilities.get_imf_ext_data(dbname, ['A', None, series])
```

```python
# Retrieved for 176 countries
df[-5:]
```

CI.IAFR_BP6_USD.A        HN.IAFR_BP6_USD.A      XK.IAFR_BP6_USD.A     BI.IAFR_BP6_USD.A      ...   ME.IAFR_BP6_USD. dates                                                                                                    ... 2016-01-01       2.131779e+10              8.004554e+09           4.793741e+09          5.964244e+08     ...         2.229762e+0 2017-01-01       1.315939e+10              9.443878e+09           5.802145e+09          6.738612e+08     ...         2.815810e+0 2018-01-01       1.315316e+10              9.654496e+09           5.457292e+09          6.910459e+08     ...         3.034391e+0 2019-01-01       1.486926e+10              1.051853e+10           5.799472e+09                   NaN     ...         3.291983e+0

2020-01-01                    NaN        1.351133e+10          6.514710e+09                     NaN   ...                     Na

[5 rows x 176 columns]

```python
# Specify options for output format
df = imf_ext_utilities.get_imf_ext_data(dbname, ['A', ['US', 'JP'], 'TXG_FOB_USD', ['UK', 'FR']], scale='B',
df[-5:]
```

dates values (US Dollars/Billions) ref_area     indicator counterpart_area 141 2016-01-01                      6.247867       JP TXG_FOB_USD                FR 142 2017-01-01                      6.279942       JP TXG_FOB_USD                FR 143 2018-01-01                      7.072807       JP TXG_FOB_USD                FR 144 2019-01-01                      6.841118       JP TXG_FOB_USD                FR 145 2020-01-01                      5.639124       JP TXG_FOB_USD                FR

```python
get_imf_ext_metadata(database, values,                                                 concept='INDICATOR'
debug=False)
```

Get metadata from data.imf.org. The metadata stored corresponds to each dimension. Provide the database name, list of dimension values to inspect, and optionally the dimension name. The dimension name defaults to INDICATOR which for most databases is the name for series codes. To check the dimension names, use the get_query_dimensions() function and check the column conceptref.
```python
dbname = 'DOT'
# Get metadata for a single series code
meta = imf_ext_utilities.get_imf_ext_data(dbname, 'TXG_FOB_USD')
```

meta INDICATOR_ALTERNATE_PUBLICATION_CODES INDICATOR_CODE                         INDICATOR_CONCEPT      ... INDICATOR                                                                                                       ... TXG_FOB_USD                    70..DZF|US Dollars    TXG_FOB_USD            Goods, Value of Exports, FOB        ...     Goods, V

```python
# Get metadata for multiple series
meta = imf_ext_utilities.get_imf_ext_metadata(dbname, ['TXG_FOB_USD', 'TMG_FOB_USD'])
```

meta INDICATOR_ALTERNATE_PUBLICATION_CODES INDICATOR_CODE             INDICATOR_CONCEPT                  ... INDICATOR                                                                                                       ... TXG_FOB_USD                    70..DZF|US Dollars    TXG_FOB_USD Goods, Value of Exports, FOB                   ...     Goods, V TMG_FOB_USD                    71.VDZF|US Dollars    TMG_FOB_USD Goods, Value of Imports, FOB                   ...     Goods, V

```python
# Get metadata for all series
dbname = 'BOP'
meta = imf_ext_utilities.get_imf_ext_metadata(dbname, None)
```

meta INDICATOR_ALTERNATE_PUBLICATION_CODES INDICATOR_CODE INDICATOR_CTS_CODE               ... INDICATOR                                                                                          ... BMTR_BP6_XDC                       .6099EX.D.A.N.2   BMTR_BP6_XDC       BMTR_BP6_XDC               ...      Supplementary Item BMTR_BP6_USD                       .6099EX.D.A.N.1   BMTR_BP6_USD       BMTR_BP6_USD               ...      Supplementary Item I_BP6_EUR                          .809999.N.A.A.6      I_BP6_EUR          I_BP6_EUR               ... I_BP6_XDC                          .809999.N.A.A.2      I_BP6_XDC          I_BP6_XDC               ... I_BP6_USD                          .809999.N.A.A.1      I_BP6_USD          I_BP6_USD               ...

[5 rows x 12 columns]
```python
# Gets metadata for > 5,000 series
len(meta)
```

The default is to query the metadata of INDICATORS, but this can be changed to query the FREQ, REF_AREA, and other dimensions.
```python
dbname = 'IFS'
```

```python
# Check the dimensions available
dims = imf_ext_utilities.get_query_dimensions(dbname)
# The relevant concept names are contained in the column "conceptref"
```

dims conceptref                                             values codelist CL_FREQ                FREQ                                 [A, B, Q, M, D, W] CL_AREA_IFS        REF_AREA [AF, AL, DZ, AD, AO, AI, AG, 5M, AR, AM, AW, A... CL_INDICATOR_IFS INDICATOR [NFIAXD_XDC, NFIAXD_SA_XDC, NFIAXD_NSA_XDC, NF...

```python
# Check metadata on annual FREQ
freqmeta = imf_ext_utilities.get_imf_ext_metadata(dbname, 'A', concept='FREQ')
freqmeta
```

FREQ_ID FREQ_MNEMO FREQ_NAME FREQ 1        YEAR         A    Annual

```python
# Get metadata on all FREQ
freqmeta = imf_ext_utilities.get_imf_ext_metadata(dbname, None, concept='FREQ')
freqmeta
```

FREQ_ID FREQ_MNEMO FREQ_NAME FREQ 1        YEAR         A     Annual 3      QUART          Q Quarterly 4      MONTH          M    Monthly

```python
# Get metadata on all countries
countrymeta = imf_ext_utilities.get_imf_ext_metadata(dbname, None, concept='REF_AREA')
countrymeta[-5:]
```

REF_AREA_CODE REF_AREA_FULL_NAME REF_AREA_ISO__CODE ... REF_AREA_SDMX_CODE REF_AREA                                                      ... 1C_SRF             SRF                NaN                NaN ...              1C_SRF F6                 603                NaN                NaN ...                  F6 7A                 759                NaN                NaN ...                  7A WAEMU (West African Eco A10                205                NaN                NaN ...                 A10 W00                001                NaN                NaN ...                 W00                  All Co

[5 rows x 8 columns]
```python
len(countrymeta)
```

## 3.12 Data Mapper

The IMF Data Mapper https://www.imf.org/external/datamapper/ is a relatively new external-facing public website that provides core data as well as an API for data retrieval. The official documentation for the API is at https://www.imf. org/external/datamapper/api/ and the imf_datatools allows retrieval from this API. The API itself is relatively simple and straightforward, providing metadata for the available series, a list of abbreviations for available countries, regions and

analytical groups and their names, and data retrieval. As of March 2023, all data seems to be annual series.

#### `get_datamapper_data(indicators, country=None,                                                            longformat=False,`

```python
debug=False)
```

Retrieve data for the provided indicators which is a str if a single indicator, or an iterator over multiple indicators. By default this will return all combinations of available indicators and countries, but by specifying the country to be a str for a single country or an iterable for multiple countries, the results will be filtered to show only the specified countries. The countries are specified using ISO-3, although the regions and groups are not official ISO-3.
```python
# Get data for series "rev" for all countries
df = datamapper_utilities.get_datamapper_data('rev')
df[-5:]
```

USA.rev       GBR.rev      AUT.rev       BEL.rev       DNK.rev       FRA.rev      DEU.rev    ...      HUN.rev    MN dates                                                                                                         ... 2017-01-01     30.804607    36.430611     48.482773     51.346433    52.335793     53.545034     45.511239    ...    44.251211   28.4 2018-01-01     30.142743    36.279399     48.908775     51.390747    51.308761     53.355596     46.270900    ...    44.033137   31.2 2019-01-01     30.269822    36.038315     49.175824     49.935827    53.799360     52.287155     46.521712    ...    43.879887   31.8 2020-01-01     30.804202    36.160429     48.953411     50.170800    53.750990     52.545067     46.075268    ...    43.408033   27.8 2021-01-01     31.457877    36.888300     50.051910     49.387916    53.415074     52.622474     47.525425    ...    41.144710   32.7

[5 rows x 144 columns]

```python
# Filter on countries for series "NGDP_RPCH"
df = datamapper_utilities.get_datamapper_data('NGDP_RPCH', country=['USA', 'JPN'])
df[-5:]
```

JPN.NGDP_RPCH USA.NGDP_RPCH dates 2023-01-01            1.6            1.0 2024-01-01            1.3            1.2 2025-01-01            0.9            1.8 2026-01-01            0.5            2.1 2027-01-01            0.4            1.9

```python
# Get multiple series for one country
df = datamapper_utilities.get_datamapper_data(['BCA', 'NGDP_RPCH'], country='CHN')
df[-5:]
```

CHN.BCA CHN.NGDP_RPCH dates 2023-01-01 279.289             4.4 2024-01-01 249.784             4.5 2025-01-01 227.469             4.6 2026-01-01 175.958             4.6 2027-01-01 149.562             4.6

```python
# Specify long format
df = datamapper_utilities.get_datamapper_data(['BCA', 'NGDP_RPCH'], country=['USA', 'CHN'], longformat=True)
df
country      dates     BCA NGDP_RPCH
```

0       CHN 1999-01-01 21.114         NaN 1       CHN 2000-01-01 20.432         NaN 2       CHN 2001-01-01 17.405         NaN 3       CHN 2002-01-01 35.422         NaN

4        CHN 2003-01-01     43.052          NaN ..       ...        ...        ...          ... 187      USA 1982-01-01        NaN         -1.8 188      USA 1983-01-01        NaN          4.6 189      USA 1984-01-01        NaN          7.2 190      USA 1985-01-01        NaN          4.2 191      USA 1986-01-01        NaN          3.5

[192 rows x 4 columns]

#### `get_datamapper_metadata(debug=False)`

Get metadata for all indicators. The result will be a pd.DataFrame with the indicator name as the column.
```python
meta = datamapper_utilities.get_datamapper_metadata()
```

meta label   ... indicator                                                                 ... BCA                        Current account balance\nU.S. dollars          ...                World Economic Outlook (Octo BCA_GDP         External Current Account, Incl.Grants (% of GDP)          ...         AFR Regional Economic Outlook (Octo BCA_NGDPD                Current account balance, percent of GDP          ...                World Economic Outlook (Octo BFD_GDP                 Net Foreign Direct Investment (% of GDP)          ...         AFR Regional Economic Outlook (Octo BM_GDP                  Imports of Goods and Services (% of GDP)          ...         AFR Regional Economic Outlook (Octo ...                                                          ...          ... ka_ret         Real estate capital transaction openness index...          ...                                    Wang-Ja pb                    Government primary balance, percent of GDP          ...   Public Finances in Modern History Databa prim_exp          Government primary expenditure, percent of GDP          ...   Public Finances in Modern History Databa rev                           Government revenue, percent of GDP          ...   Public Finances in Modern History Databa total_theil                         Export Diversification Index          ...   IMF Board Policy Paper "Sustaining Long-

[110 rows x 5 columns]

#### `get_country_codes(debug=False)`

Get list of available countries. The output will be a pd.DataFrame with the code for each country as the column, and a column providing the name.
```python
countrylist = datamapper_utilities.get_country_codes()
countrylist
```

label code ABW          Aruba AFG    Afghanistan AGO         Angola AIA       Anguilla ALB        Albania ...            ... WSM          Samoa YEM          Yemen ZAF   South Africa ZMB         Zambia ZWE       Zimbabwe

[239 rows x 1 columns]

#### `get_region_codes(debug=False)`

Get list of available regions. The output will be a pd.DataFrame with the code for each region as the column, and a column providing the name.
```python
regionlist = datamapper_utilities.get_region_codes()
```

regionlist label code AFQ                            Africa (Region) AFRREO       African Regional Economic Outlook AFR_SSQ           Sub-Saharan Africa (Region) APQ                           Asia and Pacific AZQ                  Australia and New Zealand CAQ              Central Asia and the Caucasus CBQ                                  Caribbean CMQ                            Central America EAQ                                  East Asia EEQ                            Eastern Europe EUQ                                     Europe MEQ                       Middle East (Region) NAQ                               North Africa NMQ                              North America PIQ                           Pacific Islands SAQ                                 South Asia SEQ                             Southeast Asia SMQ                              South America SPR_GD_AFR                              Africa SPR_GD_Asia                               Asia SPR_GD_CPI       Caribbean and Pacific Islands SPR_GD_EUR                              Europe SPR_GD_MECA       Middle East and Central Asia SPR_GD_WHD                  Western Hemisphere SSQ               Sub-Saharan Africa (Region) WEQ                             Western Europe WHQ                Western Hemisphere (Region)

#### `get_group_codes(debug=False)`

Get list of available analytical groups. The output will be a pd.DataFrame with the code for each group as the column, and a column providing the name.
```python
grouplist = datamapper_utilities.get_group_codes()
```

grouplist label code ADVEC                                            Advanced economies AEEUEJ                                Adv econ excl US, Euro, Japan AFR                                             Africa (Analytical) ARAWORLD                                                      World AS5                                                         ASEAN-5 ...                                                             ... WEOWORLD                                                      World gb_othersource                                      Other countries gbcasestudy       Identified as gender budgeting country in IMF ...

gbtier_1           Prominent gender budgeting countries covered i... gbtier_2           Other gender budgeting countries covered in th...

[128 rows x 1 columns]

#### `get_all_areas(debug=False)`

Get list of all available countries, regions, analytical groups together. The output will be a pd.DataFrame with the code for each country/region/group as the index, and a column providing the name.
```python
arealist = datamapper_utilities.get_all_areas()
```

arealist label code ABW                                                            Aruba AFG                                                      Afghanistan AGO                                                           Angola AIA                                                         Anguilla ALB                                                          Albania ...                                                              ... WEOWORLD                                                       World gb_othersource                                       Other countries gbcasestudy        Identified as gender budgeting country in IMF ... gbtier_1           Prominent gender budgeting countries covered i... gbtier_2           Other gender budgeting countries covered in th...

[394 rows x 1 columns]

#### `get_var_areas(indicator, debug=False)`

Get a list of all available countries, regions, analytical groups for a given indicator. The output will be a pd.DataFrame containing the code for each country/region/group that is available for that indicator as the index, and a column providing the name.
```python
areas = datamapper_utilities.get_var_areas('rev')
```

areas label code USA        United States GBR       United Kingdom AUT              Austria BEL              Belgium DNK              Denmark ...                  ... HRV              Croatia SVN             Slovenia MKD     North Macedonia POL               Poland ROU              Romania

[144 rows x 1 columns]

## 3.13 EuroStat

Get data from EuroStat, official documentation at https://ec.europa.eu/eurostat. See also official API documentation at https://wikis.ec.europa.eu/display/EUROSTATHELP/API+-+Getting+started. The functions below are based on the eurostat library, documentation at https://pypi.org/project/eurostat/, and customized to be consistent with other datatools libraries. To use this file, it may be necessary to install the eurostat library with: pip install eurostat
#### `get_datasets(dataset='all', lang='en')`

Get all avialable datasets. The EuroStat database is organized at the top level as datasets, with each dataset containing one or multiple series and various other dimensions.
```python
Default of dataset='all' will return all available datasts and descriptions. Specify a dataset if limiting to a specific
dataset.
```

Can also specify languages ‘en’, ‘fr’, ‘de’, defaults to ‘en’.
#### `set_args(timeout=None, cert=None)`

For most cases should not be necessary but if needed can set parameters for requests. Default timeout is 120 sec, can change and also specify a cert file. Returns a pandas.DataFrame showing the new arguments.
#### `get_dimensions(dataset)`

Get query dimensions for a given dataset and return a list of dimensions to specify the data.
```python
dims = eurostat_utilities.get_dimensions('DEMO_R_D2JAN')
```

['freq', 'unit', 'sex', 'age', 'geo']

#### `get_dimension_values(dataset, dimension)`

Get available values for a given dataset and dimension.
```python
vals = eurostat_utilities.get_dimension_values('NASQ_10_F_BS', 'unit')
```

['MIO_EUR', 'MIO_NAC', 'PC_GDP']

#### `get_data_structure(dataset, dim=None, full=False)`

Get the data structure of a given dataset. If dim is None (default), will return a pandas.DataFrame with descriptions of each dimension without values. If dim is specified, returns a pandas.DataFrame with valid values and descriptions for that dimension.
```python
If full=True, return all possible values, not just the ones used (default False).
# No dim specified
data_struct = eurostat_utilities.get_data_structure('NASQ_10_F_BS')
```

name                                                   descr dim
```python
freq                                      Time frequency         This code list contains the periodicity that r...
```

unit                                     Unit of measure                                                      None sector                                            Sector                                                      None

finpos                         Financial position                                                       None na_item    National accounts indicator (ESA 2010)                                                       None geo               Geopolitical entity (reporting)          This code list defines the reporting geopoliti...

```python
# With dim specified
data_struct = eurostat_utilities.get_data_structure('NASQ_10_F_BS', 'na_item')
```

descr val F                             Total financial assets/liabilities F_FDI          Total financial assets/liabilities, of which f... F1               Monetary gold and special drawing rights (SDRs) F11                                                Monetary gold F12                                Special drawing rights (SDRs) F2                                         Currency and deposits F21                                                     Currency F22_F29                    Transferable deposits; other deposits F22                                        Transferable deposits F29                                               Other deposits F3                                               Debt securities F3_FDI         Debt securities, of which foreign direct inves... F31                                   Short-term debt securities F32                                    Long-term debt securities F4                                                         Loans F4_FDI                 Loans, of which foreign direct investment F41                                           Short-term - Loans F42                                            Long-term - Loans F5                             Equity and investment fund shares F51                                                       Equity F51M_FDI       Unlisted shares and other equity, of which for... ...

#### `get_eurostat_data(dataset, dims={}, longformat=False, flags=False)`

Main function to get EuroStat data. By default will get all data within a given dataset, otherwise specify dict for filtering params with dims.
```python
Setting flags=True will return flags associated with each observation. If not longformat (default), two pandas.DataFrames
```

will be returned, one containing the data and the other containing the flags. These two DataFrames should have the
```python
same index and columns. If longformat=True, the flags will be placed in their own column “flags” in the long format
```

DataFrame. The filter dims should use the other functions get_dimensions(dataset) and get_dimension_values(dataset, dim) to specify keywords and values. For example in the following a filter is done to retrieve data only for specific countries and units.
```python
dataset = 'NASQ_10_F_BS'
```

```python
# Get valid dimensions
dims = eurostat_utilities.get_dimensions(dataset)
# ['freq', 'unit', 'sector', 'finpos', 'na_item', 'geo']
```

```python
# Get dimension values
# Using get_data_structure(dataset, dim) will provide descriptions of the
# values of each dimension.
```

```python
sectors = eurostat_utilities.get_dimension_values(dataset, 'sector')
# ['S1', 'S11', 'S12', 'S121_S122_S123', 'S121', 'S125_S126_S127',
# 'S124', 'S125', 'S126', 'S127', 'S128', 'S129', 'S13', 'S14_S15',
# 'S14', 'S15', 'S2']
# Can similarly get values for other dimensions.
```

```python
# Create filter
dims = {'geo' : 'BE',
```

'unit' : 'PC_GDP', 'na_item' : 'F',
```python
# specify multiple items in a dimension with a list
```

'sector' : ['S1', 'S12'], }

```python
# Get data
df = eurostat_utilities.get_eurostat_data(dataset, dims)
```

Q.PC_GDP.S1.ASS.F.BE   Q.PC_GDP.S1.LIAB.F.BE   Q.PC_GDP.S12.ASS.F.BE   Q.PC_GDP.S12.LIAB.F.BE dates 1998-10-01                      NaN                     NaN                     NaN                      NaN 1999-01-01                    984.0                   907.7                   467.8                    456.0 1999-04-01                    991.0                   907.8                   465.6                    455.8 1999-07-01                    992.3                   912.7                   472.1                    463.3 1999-10-01                   1032.7                   928.7                   484.7                    469.9 ...                             ...                     ...                     ...                      ... 2022-10-01                   1108.7                  1055.8                   497.7                    506.6 2023-01-01                   1116.6                  1058.0                   505.1                    511.2 2023-04-01                   1095.2                  1036.4                   497.7                    503.8 2023-07-01                   1079.0                  1022.3                   488.5                    495.4 2023-10-01                   1078.8                  1019.2                   481.6                    484.7

[101 rows x 4 columns]

```python
# Get data in long format and with flags
df = eurostat_utilities.get_eurostat_data(dataset, dims, longformat=True, flags=True)
```

```python
freq     unit sector finpos na_item geo flags      dates     value
```

0        Q   PC_GDP     S1    ASS       F BE        1999-01-01     984.0 1        Q   PC_GDP     S1   LIAB       F BE        1999-01-01     907.7 2        Q   PC_GDP    S12    ASS       F BE        1999-01-01     467.8 3        Q   PC_GDP    S12   LIAB       F BE        1999-01-01     456.0 4        Q   PC_GDP     S1    ASS       F BE        1999-04-01     991.0 ..     ...      ...    ...    ...     ... ..    ...        ...       ... 395      Q   PC_GDP    S12   LIAB       F BE        2023-07-01     495.4 396      Q   PC_GDP     S1    ASS       F BE        2023-10-01    1078.8 397      Q   PC_GDP     S1   LIAB       F BE        2023-10-01    1019.2 398      Q   PC_GDP    S12    ASS       F BE        2023-10-01     481.6 399      Q   PC_GDP    S12   LIAB       F BE        2023-10-01     484.7

[400 rows x 9 columns]

## 3.14 BIS

The Bank for International Settlements hosts data and this is accessible through an API, official documentation is at https://stats.bis.org/api-doc/v1/. The bis_utilities provide functions to access data and metadata, both through the pandaSDMX library and also through direct queries to the API.
#### `get_databases()`

Get all avialable datasets. Returns a pandas.DataFrame with the database name as the index.
#### `get_dimensions(dataset, refresh=False, debug=False)`

Get query dimensions for a given dataset and return a list of dimensions to specify the data.
```python
dims = bis_utilities.get_dimensions('WS_NA_SEC_DSS')
```

['FREQ', 'ADJUSTMENT', 'REF_AREA', 'COUNTERPART_AREA', 'REF_SECTOR', 'COUNTERPART_SECTOR', 'CONSOLIDATION', ' 'EXPENDITURE', 'UNIT_MEASURE', 'CURRENCY_DENOM', 'VALUATION', 'PRICES', 'TRANSFORMATION', 'CUST_BREAKDOWN']

The function retrieves the dimensions and also the available values of each dimension. This is then stored as a dict for this session so that future calls for this information (and calls to get_dimension_values) do not repeat the query for the
```python
same database. To force an update, use the option refresh=True.
```

#### `get_dimension_values(dataset, dimension, refresh=False, debug=False)`

Get available values for a given dataset and dimension. Returns a pandas.DataFrame with the index set to available values.
```python
vals = bis_utilities.get_dimension_values('WS_NA_SEC_DSS', 'REF_AREA')
```

name                  parent CL_BIS_IF_REF_AREA 00                                                                 Others            CL_BIS_IF_REF_AREA 11                      Technical residual (Non-residents / Cross-border)            CL_BIS_IF_REF_AREA 1A                                           US banks in offshore centres            CL_BIS_IF_REF_AREA 1B                                       International banking facilities            CL_BIS_IF_REF_AREA 1C                                            International organisations            CL_BIS_IF_REF_AREA ...                                                                   ...                           ... ZA                                                           South Africa            CL_BIS_IF_REF_AREA ZM                                                                 Zambia            CL_BIS_IF_REF_AREA ZR                                                                  Zaire            CL_BIS_IF_REF_AREA ZW                                                               Zimbabwe            CL_BIS_IF_REF_AREA _Z                                                         Not applicable            CL_BIS_IF_REF_AREA

[432 rows x 2 columns]

#### `get_bis_sdmx_data(db, key={}, params={}, longformat=False, debug=False)`

Get BIS data using pandaSDMX. By default will get all data within a given dataset, otherwise specify dict for filtering params with key. The dict params allows specifying startPeriod, endPeriod.
```python
If not longformat (default), a pandas.DataFrames will be returned with the dates as the index. If longformat=True,
```

each dimension of the dataset will be its own column.
```python
db = 'WS_NA_SEC_DSS'
```

```python
key = {'FREQ' : 'Q',
```

'ADJUSTMENT' : 'N', 'REF_AREA' : 'AR',

'COUNTERPART_AREA' : 'XW', 'REF_SECTOR' : 'S1+S13', 'COUNTERPART_SECTOR' : 'S1', 'CONSOLIDATION' : 'N', 'ACCOUNTING_ENTRY' : 'L', 'STO' : 'LE', 'INSTR_ASSET' : 'F3', 'MATURITY' : 'T', 'EXPENDITURE' : '_Z', 'UNIT_MEASURE' : 'USD', 'CURRENCY_DENOM' : '_T', 'VALUATION' : 'N', 'PRICES' : 'V', 'TRANSFORMATION' : 'N', 'CUST_BREAKDOWN' : '_T'}
```python
params = {'startPeriod' : 2000, 'endPeriod' : '2023-06'}
```

```python
df = get_bis_sdmx_data(db, key=key, params=params, debug=False)
```

Q.N.AR.XW.S1.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T           Q.N.AR.XW.S13.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T dates 2018-04-01                                               272.276059                                                 NaN 2018-07-01                                               240.062311                                                 NaN 2018-10-01                                               239.874817                                                 NaN 2019-01-01                                               236.950934                                                 NaN 2019-04-01                                               241.963724                                                 NaN 2019-07-01                                               208.480027                                                 NaN 2019-10-01                                               200.195167                                                 NaN 2020-01-01                                               203.900941                                                 NaN 2020-04-01                                               208.396845                                                 NaN 2020-07-01                                               214.932335                                                 NaN 2020-10-01                                               214.533246                                                 NaN 2021-01-01                                               233.672621                                          192.210904 2021-04-01                                               244.217507                                          199.809332 2021-07-01                                               249.627316                                          204.964572 2021-10-01                                               255.009723                                          212.250929 2022-01-01                                               279.992746                                          220.581546 2022-04-01                                               296.087258                                          224.361338 2022-07-01                                               308.310803                                          233.198126 2022-10-01                                               311.728939                                          238.958269 2023-01-01                                               315.429912                                          242.940868 2023-04-01                                               327.583617                                          251.903298

```python
# Get data in long format
df = get_bis_sdmx_data(db, key=key, params=params, longformat=True, debug=False)
```

#### `get_bis_data(db, code, start=None, end=None, longformat=False)`

Get BIS data using direct queries to the API, not through SDMX. Specify the database name db as well as a str code that specifies the series code(s). This will take a form like 'Q.N..XW.S1+S11+S12+S13.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T+C01+C02' where each dimension is separated by a .. To specify multiple values, separate by + as in the above for S1+S11+S12+S13, and to allow all values, leave empty as in the above third dimension. If longformat is specified, each dimension of the query will be put in its own column.

```python
db = 'WS_NA_SEC_DSS'
code = 'Q.N.AR.XW.S1+S13.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T'
df = get_bis_data(db, code)
```

Q.N.AR.XW.S1.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T            Q.N.AR.XW.S13.S1.N.L.LE.F3.T._Z.USD._T.N.V.N._T dates 2018-04-01                                                272.276059                                                        NaN 2018-07-01                                                240.062311                                                        NaN 2018-10-01                                                239.874817                                                        NaN 2019-01-01                                                236.950934                                                        NaN 2019-04-01                                                241.963724                                                        NaN 2019-07-01                                                208.480027                                                        NaN 2019-10-01                                                200.195167                                                        NaN 2020-01-01                                                203.900941                                                        NaN 2020-04-01                                                208.396845                                                        NaN 2020-07-01                                                214.932335                                                        NaN 2020-10-01                                                214.533246                                                        NaN 2021-01-01                                                233.672621                                                 192.210904 2021-04-01                                                244.217507                                                 199.809332 2021-07-01                                                249.627316                                                 204.964572 2021-10-01                                                255.009723                                                 212.250929 2022-01-01                                                279.992746                                                 220.581546 2022-04-01                                                296.087258                                                 224.361338 2022-07-01                                                308.310803                                                 233.198126 2022-10-01                                                311.728939                                                 238.958269 2023-01-01                                                315.429912                                                 242.940868 2023-04-01                                                327.583617                                                 251.903298 2023-07-01                                                305.675820                                                 234.388816 2023-10-01                                                236.740514                                                 207.440018 2024-01-01                                                267.115846                                                 237.911544

```python
# Get data in long format
df = get_bis_data(db, code, longformat=True)
```

## 3.15 Troubleshooting

For all resources, the imf_datatools return data only if you have access to it. Please consult the appropriate parties for these permissions. The imf_datatools and its authors do not grant permissions to anything. In case a resource does not return data, check that the data can be accessed using conventional methods such as the various Excel add-ins that are available within the Fund. If the data is not retrieved it may be a permission issue. For trouble accessing data with:
1. EcOS
Check permission for the database requested. Use the EcOS application or the ECXL add-in in Excel to see that data of interest exists.
2. DMX
Check access permission to the DMX file and that it exists. Use the DMX add-in in Excel to see that data of interest exists.
3. SQL server
Check permission for the database requested.

SQL databases are monitored for failed login attempts. Trying to a access databases that you do not have access to will trigger alarms to the database teams which may lead to warnings.
4. Haver
Use the Haver DLXVG3 tool (available from the Software Center) to check that series codes exist. There is no userdependent permission for Haver.
5. World Bank
Check the World Bank website that data of interest is available. There are no user-dependent permissions.
6. OECD
Check the OECD website that data of interest is available. There are no user-dependent permissions.
# 4 Further Data Retrieval and Manipulation

## 4.1 Writing to DMXe Files

A new feature as of Jun 2024 is the ability to write to DMXe files. This is done by using the same executable files that Excel uses when running the DMXe add-in, so that the behavior should be exactly the same as using through Excel. To install the DMXe writer, make sure the library pythonnet is installed. Check with the command import pythonnet in a python session, and if this gives an error, run pip install pythonnet in a Command Prompt window. The commands can also be called from Stata via the command dmxewriter. Use the Stata command
```stata
help dmxewriter
```

to get further info and examples, and this is also shown in Sec. 5.2.6. A very simple example of Stata is shown below. // Get annual data from EcOS.
```stata
ecosuse data, database(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) f(ecos_A, replace)
```

// Write data to a DMXe file. dmxewriter data , dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_A) indicator(_111NGDP_A, _193PCPI_A) t

// Modify column Descriptor. Descriptor can take any string value. dmxewriter metadata, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(111NGDP.A) column(Descriptor) value(

// Delete values of indicators from a DMXe file. dmxewriter delete, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(111NGDP.A) freq(A)

Below the available commands and examples are provided.
#### `save_dmxe_data(outfilename, df, freq=None, datecol=None, debug=False)`

Save DMXe data for a pandas.DataFrame df into a DMXe file outfilename. df should be in the standard format for imf_datatools with an Index corresponding to the dates/periods, and each column providing a different series. If
```python
freq=None is given, the frequency of each column is determined by the imf_datatools and saved in the DMXe file,
```

otherwise specify a frequency like A, Q, M, D and B. For cases (such as when using through R) when an index is not given, specify the column for dates using the argument datecol.

```python
import imf_datatools
from imf_datatools import dmxe_writer_utilities
# Get data
df = imf_datatools.get_haver_data('IP@IP')
```

```python
# Save to DMXe file
filename = 'out.dmxe'
```

dmxe_writer_utilities.save_dmxe_data(filename, df)

#### `save_dmxe_metadata(outfilename, seriescode, dict_metadata, debug=False)`

Save DMXe metadata for a given series seriescode into a DMXe file outfilename. The attributes are stored in dict_metadata which is a dictionary between the metadata header like “Notes” and the corresponding text. Note that DMXe places restrictions on some metadata headers so that only a pre-specified set of values are valid, and other fields like “Country_Code” are automatically generated so cannot be specified. See the documentation for details.
```python
import imf_datatools
from imf_datatools import dmxe_writer_utilities
# Get data
df = imf_datatools.get_haver_data('IP@IP')
```

```python
# Save to DMXe file
filename = 'out.dmxe'
```

dmxe_writer_utilities.save_dmxe_data(filename, df)

```python
# Update metadata
dict_metadata = {'Notes' : 'Downloaded from Haver'}
```

dmxe_writer_utilities.save_dmxe_metadata(filename, 'IP@IP', dict_metadata)

#### `delete_dmxe_data(filename, series, freq, debug=False)`

Delete a series from the DMXe file filename. freq can take on a frequency like A, Q, M, D, and two special cases:
1. all will delete all frequencies.
2. series will delete the series itself.
#### `rename_dmxe_data(filename, series, newseries, debug=False):`

Rename a series in the DMXe file filename to another name newseries.
#### `check_logs(filename, debug=False)`

Check and return how many rows of access logs there are in a DMXe file filename.
#### `delete_logs(filename)`

Delete the access logs in the DMXe file filename. These access logs can take up substantial space, especially after batch operations, so cleaning periodically is recommended.
#### `read_dmxe_data(infilename, series, freq=None, debug=False)`

Utility function to retrieve DMXe data using same executables as used in Excel add-in. Same functionality as dmxe_utilities.get_dmxe_data(), but also allows calculation based on expressions. If freq is None and multiple
```python
frequencies exist, the lowest available frequency is returned.
```

An example of reading the data as-is and applying a DMXe calculation is shown below. For details of DMXe functions see the documentation available at http://www-intranet.imf.org/departments/ITD/DigitalProducts/DAE/Pages/DMXeHome-Page-.aspx

```python
import imf_datatools
from imf_datatools import dmxe_writer_utilities
# Get data
df = imf_datatools.get_haver_data('IP@IP')
```

```python
# Save to DMXe file
filename = 'out.dmxe'
```

dmxe_writer_utilities.save_dmxe_data(filename, df)

```python
# Read out data as-is
df2 = dmxe_writer_utilities.read_dmxe_data(filename, 'IP@IP')
```

```python
# Do calculation using DMXe.
# In this example we calculate the %yoy.
# The additional parameters are to specify the lag and to use percentage.
df_yoy = dmxe_writer_utilities.read_dmxe_data(filename, 'calc(TsPCH(IP@IP, 12, 1))')
```

```python
# Calculate moving average over 12 months
df_mavg = dmxe_writer_utilities.read_dmxe_data(filename, 'calc(TsMAvg(IP@IP, 12))')
```

```python
# If changing the frequency of the output from the original, specify the freq
df_q = dmxe_writer_utilities.read_dmxe_data(filename, 'calc(TsConsolidate(IP@IP, average))', freq='Q')
```

#### `set_dmxe_libdir(corepath, mappingpath)`

The default path for the necessary DMXe libraries is C:\Program Files\International Monetary Fund\DMXe\Core. If for whatever reason this path needs to be changed set using the arguments corepath and mappingpath. This should only be relevant on the servers where the DMXe libraries are not installed by default to a fixed location. To run on the server, copy the two folders Core and Template under C:\Program Files\International Monetary Fund\DMXe to the server for example to E:\data\[user]\DMXe', then edit the filedmxe_writer_utilities.py‘ which you are importing to have the lines
```python
# Add this line to dmxe_writer_utilities.py before
# set_dmxe_libdir() is called.
DMXECOREDIR = r'E:\data\kmoriya\DMXe\Core'
```

```python
# This line already exists.
MAPPINGFILE = DMXECOREDIR + '/../Template/Mapping.dmxe'
```

## 4.2 Data Retrieval Scripts

Each library in section 3 retrieves data from a single source like EcOS, DMX, or Haver. For Python users it should be relatively easy to write a script that will get the data of interest from these sources. However, for some users it may be convenient to be able to specify the necessary data in an Excel file and have a single command retrieve the data for them. For this purpose there is a script datacollector.py in the imf_datatools/scripts folder. The complete documentation is here. The script requires two arguments, the input Excel file name and the output Excel file name. The simplest use case would be
```python
python datacollector.py path/to/input.xlsx output/path/output.xlsx
```

which will read in the contents of path/to/input.xlsx and write out to output/path/output.xlsx. These paths can be relative to where the command is run, or an absolute path like:

C:\Users\jdoe\Desktop\input.xlsx.

Note that if the path contains spaces, the entire path must be put in double quotes:
```python
python datacollector.py "input (1).xlsx" "output/path/output file.xlsx"
```

The output file will be overwritten each time the script is run. Users should be careful not to overwrite existing files.

In the case that the input Excel file contains multiple sheets, the sheet can be specified via input.xlsx::sheet1 so that in this case the sheet named sheet1 will be used.

The input Excel file must have the following structure.

1. Valid input rows will specify a series to retrieve. Column A will be an optional alias of the series, which will
become the column name for that series. The alias cannot contain special characters or start with a numerical value. Column B will be the resource name, which can be one of EcOS, DMX, SQL, Haver, World Bank, OECD, or imf_ext. This column is case-insensitive, so dmx for example will work. In column C onwards are the necessary parameters to specify the series, and these follow the get_[resource]_data functions explained in section 3. For example for EcOS the corresponding function would be get_ecos_sdmx_data (see Sec. 3.4 so columns C, D, E would be the database name, country code, and seriescode. For this script, all input rows can specify only one series.

2. A further option is to apply calculations to series. To do this, use a row to specify the alias (necessary for
calculation rows) and the expression. For example, if series with aliases gdp_USA and gdp_AUS‘ have been defined in rows after that calculations using those aliases can be specified:

In this example the calculations are

1. period-over-period % change of a series (applying function calc_pop, . All functions from dataframe utilities can
be applied using the name of the function but without the calc_ part. Each alias of a series must be put in square brackets like pop(gdp_USA).

2. Sum of two series. Similarly, the sum, difference, product and division of two series can be done.

3. Apply the year-over-year % change of a series (applygin function calc_yoy) to the sum of two series.

In this way, almost any new series can be derived from series that are already defined.

3. If a hash mark (#) is specified at the beginning of a cell, that cell and all further cells in that row will not be
included in the input. This is an easy way to add comments to the input sheet. Empty rows are also ignored.

4. If in column A END is specified (case-insensitive), further input rows are ignored. This is an easy way to cut off a
long input and test it up to a certain row.

The example file input_dc.xlsx which is included in the imf_datatools/scripts folder shows examples of retrieving data from various sources and calculations among them.

The script takes in several options, listed below. To see the available options, try python datacollector.py -h or
```python
python datacollector.py --help.
```

1. -f or --freq Allows specifying the frequency of the data and ensuring that all retrieved data is of that frequency. If
data is specified that does not match this frequency, an error is raised. Specify one of A, Q, M, D for annual, quarterly, monthly, or daily data, respectively.
2. -s or --separate By default all data will be merged together regardless of frequency into one df. This is possible
because for each frequency, the data takes on the date of the first day of each period. If this option is specified, the results will be written out in separate sheets for each frequency.
3. -l or --log Allows a log file to be created showing what the program did. This may be useful if trying to understand
why the program is not working.
4. -v or --verbose Show more output of what the program is doing.
Examples:
```python
# Specify input sheet as data
python datacollector.py input.xlsx::data output.xlsx
```

```python
# Retrieve data from 1990 to 2015 only
python datacollector.py input.xlsx output.xlsx -t 1990,2015
```

```python
# Retrieve only annual data, raise error if non-annual data is specified
python datacollector.py input.xlsx output.xlsx -f A
```

```python
# Specify output is split by frequency
python datacollector.py input.xlsx output.xlsx -s
```

```python
# Specify output sheet and that output split by frequency.
# In this case each sheet name will have the frequency appende
python datacollector.py input.xlsx output.xlsx::out -s
```

```python
# Create log file. This log file will be in a folder log
# where the user is running the code
python datacollector.py input.xlsx output.xlsx::out -s -l
```

## 4.3 dataframe_utilities

The imf_datatools comes with a utility library dataframe_utilities.py which contains many utility functions to apply calculations such as percent changes and frequency conversions to pandas.DataFrames created by the datatools. Users familiar with the pandas library can of course write their own versions of these functions on the fly but having a common set of functions can be useful. Below each available function is documented with available options.
#### `merge_dfs(iterable_dfs, how='outer')`

This function takes in an iterable of pandas.DataFrames and merges them into one pandas.DataFrame. It is assumed that each df has a pandas.Timestamp as an index and by default the function will do an outer join so that any date that was in the original index values will be in the output. Since the function operates on pandas.Timestamps, it is possible to merge dfs of different frequencies, then apply ffill and other functions so that all rows have a value.
```python
# merge two quarterly series
df = haver_utilities.get_haver_data('GDP@USECON')
df2 = haver_utilities.get_haver_data('J025PCW@EUNA')
df3 = dataframe_utilities.merge_dfs([df, df2])
print(df3[-3:])
```

J025PCW@EUNA     GDP@USECON dates 2019-01-01                0.20       21098.8 2019-04-01                0.12       21340.3 2019-07-01                0.27       21542.5
```python
# merge montly and quarterly series
df = haver_utilities.get_haver_data('IP@IP') # monthly
df2 = haver_utilities.get_haver_data('GDP@USECON') # quarterly
df3 = dataframe_utilities.merge_dfs([df, df2])
# quarterly series only has values at beginning of each quarter,
# 19Q4 value was not available at this time.
print(df3[-8:])
```

GDP@USECON     IP@IP dates 2019-04-01     21340.3 108.9888 2019-05-01         NaN 109.2264 2019-06-01         NaN 109.2774 2019-07-01     21542.5 109.0852 2019-08-01         NaN 109.9634 2019-09-01         NaN 109.4437 2019-10-01         NaN 108.8532 2019-11-01         NaN 109.7573 2019-12-01         NaN 109.4330

Functions to calculate time series These functions apply transformations that are common to time series, such as percent changes, shifts, and differences. The output of these functions is a pandas.DataFrame (or a pandas.Series if the input was a pandas.Series), so the functions can be chained together to calculate various expressions such as
- %yoy of a moving 3-month average
```python
calc_yoy(calc_rolling(df, method='mean'))
```

- contribution of one series to the growth of another
calc_diff(df, 4) / calc_shift(df2, 4)
- Calculate an index series normalized to 100 at a given period for the ratio of two series
calc_rebase(df[col1] / df2[col2], '2020-01') # will set the value at 2020 Jan to be 100 (default) The functions assume by default that there is an index for the input DataFrame that is a pd.DatetimeIndex with name dates, but the option indexcol allows specifying a column to use as the date index. This is useful for example if calling these functions from R where the index information may be lost.
```python
1. calc_pop(df, nshift=1, datecol=None)
Calculates percent change from previous period (period-over-period). Default is to calculate percent change from nshift=1
```

period ago, but this can be adjusted.
```python
2. calc_yoy(df, datecol=None)
```

Calculates percentage change from previous year (year-over-year).
```python
3. calc_shift(df, n=1, datecol=None)
```

Shifts values against index of df. Positive values of shift result in values moving to future dates, while negative shift values move values to past dates. Original dates in the index where values no longer exist will be given NaN values. This function

can be useful when combined with other functions to calculate contributions to growth and other values.
```python
# Get monthly data
df = haver_utilities.get_haver_data('IP@IP')
# First values
print(df[:3])
```

IP@IP dates 1921-01-01 4.0985 1921-02-01 4.0155 1921-03-01 3.9047
```python
# Final values
print(df[-3:])
```

IP@IP dates 2019-10-01 108.8532 2019-11-01 109.7573 2019-12-01 109.4330
```python
# Apply shift (default of 1).
# Original first month's value has become NaN
print(df.shift()[:3])
```

IP@IP dates 1921-01-01      NaN 1921-02-01 4.0985 1921-03-01 4.0155
```python
# Final period has been added
print(df.shift()[-3:])
```

IP@IP dates 2019-11-01 108.8532 2019-12-01 109.7573 2020-01-01 109.4330

```python
4. calc_diff(df, shifts=1, datecol=None)
```

Calculates the difference of a series for a number of shifts. For positive shifts of n the difference is with n previous periods.
```python
5. calc_ana(df, datecol=None)
```

Calculate annualized percent change with formula

𝑝 𝑦(𝑡) 𝑦𝑎𝑛𝑎 (𝑡) = 100 × ((          ) − 1) 𝑦(𝑡 − 1)

where 𝑦(𝑡) is the original time series and 𝑝 is 4 for quarterly series and 12 for monthly series.
```python
6. calc_rolling(df, nperiods=1, method='mean', datecol=None)
Calculate rolling mean or sum of a series. Specify number of periods and method with how='mean' or how='sum'. Result
```

will have the rolling mean or sum of nperiods ending at that period. If there are less than nperiods before that period, values will be NaN.
```python
# Monthly data
df = haver_utilities.get_haver_data('IP@IP')
print(df[-3:])
```

IP@IP dates 2019-10-01 108.8532 2019-11-01 109.7573 2019-12-01 109.4330
```python
# Calculate rolling mean of 3 months
print(calc_rolling(df, 3, 'mean')[-3:])
```

dates 2019-10-01 109.420100 2019-11-01 109.351400 2019-12-01 109.347833
```python
# Calculate rolling sum of 3 months
print(calc_rolling(df, 3, 'sum')[-3:])
```

IP@IP dates 2019-10-01 328.2603 2019-11-01 328.0542 2019-12-01 328.0435
```python
# First 2 periods will become NaN
print(calc_rolling(df, 3, 'sum')[:3])
```

IP@IP dates 1921-01-01      NaN 1921-02-01      NaN 1921-03-01 12.0187

```python
7. calc_ytd(df, start='Jan', datecol=None, debug=False)
```

Calculate year-to-date sums for a given series. By default, for monthly and quarterly series, the output will be the cumulative sum of the series starting in January or Q1 of that year. The starting period can be changed with the option
```python
start, for monthly series specifying start='Apr' will give the cumulative sum of each year starting in April.
df = haver_utilities.get_haver_data('IP@IP')
print(df[-3:])
```

IP@IP dates 2019-10-01 108.8532 2019-11-01 109.7573 2019-12-01 109.4330
```python
# Calculate ytd starting in Jan
print(calc_ytd(df)[-3:])
```

IP@IP dates 2019-10-01 1094.2008 2019-11-01 1203.9581 2019-12-01 1313.3911
```python
# Calculate ytd starting in Oct
print(calc_ytd(df, start='Oct')[-3:])
```

IP@IP dates 2019-10-01 108.8532 2019-11-01 218.6105 2019-12-01 328.0435
```python
# quarterly series
```

```python
df_q = haver_utilities.get_haver_data('GDP@USECON')
# Calculate ytd starting in Q1
print(calc_ytd(df_q)[-5:])
```

GDP@USECON dates 2018-07-01     61423.2 2018-10-01     82321.0 2019-01-01     21098.8 2019-04-01     42439.1 2019-07-01     63981.6
```python
# Calculate ytd starting in Q2
print(calc_ytd(df_q, start='Q2')[-5:])
```

GDP@USECON dates 2018-07-01     41260.0 2018-10-01     62157.8 2019-01-01     83256.6 2019-04-01     21340.3 2019-07-01     42882.8

```python
8. calc_diffytd(df, start='Jan', datecol=None, debug=False)
```

Undo year-to-date sums for a given series. By default, for monthly and quarterly series, the output will take January or Q1 of that year to be the starting period. The starting period can be changed with the option start, for monthly series
```python
specifying start='Apr' will undo the cumulative sum for each year starting in April.
# A series that already has YTD applied
df = haver_utilities.get_haver_data('Y238IXD@EMERGELA')
print(df[-6:])
```

Y238IXD@EMERGELA dates 2020-10-01            9531.8 2020-11-01           10586.9 2020-12-01           11625.7 2021-01-01             950.5 2021-02-01            2050.4 2021-03-01            3310.5
```python
# Unravel the YTD starting in Jan
print(calc_diffytd(df)[-6:])
```

Y238IXD@EMERGELA dates 2020-10-01            1046.8 2020-11-01            1055.1 2020-12-01            1038.8 2021-01-01             950.5 2021-02-01            1099.9 2021-03-01            1260.1

If the same start period is used, applying ytd and diffytd in succession should yield the original series.

```python
9. calc_pow(df, p=1, datecol=None)
```

Calculate power of a series for any real number.

```python
10. calc_rebase(df, startdatestr, col=None, rebase_val=100, datecol=None, enddatestr=None, debug=False)
```

Rebase a time series to a given period or range of periods and value. By default the value for the date specified by datestr will be rebased to 100, but this value can be changed with option rebase_val. If enddatestr is provided, the normalization will be the average value between startdatestr and enddatestr.
```python
df = haver_utilities.get_haver_data('IP@IP')
print(df[-3:])
```

IP@IP dates 2023-08-01 103.2927 2023-09-01 103.3643 2023-10-01 102.7081

```python
# Rebase at 2023-09
print(calc_rebase(df, '2023-09')[-3:])
```

IP@IP dates 2023-08-01   99.930730 2023-09-01 100.000000 2023-10-01   99.365158

```python
# Rebase to different value
print(calc_rebase(df, '2023-09', rebase_val=1)[-3:])
```

IP@IP dates 2023-08-01 0.999307 2023-09-01 1.000000 2023-10-01 0.993652

```python
# Rebase to average over 2010-2019
print(calc_rebase(df, '2010-01', enddatestr='2019-12')[-3:])
```

IP@IP dates 2023-08-01 104.299694 2023-09-01 104.371992 2023-10-01 103.709395

```python
# Print the mean between 2010-2019 to confirm.
print(calc_rebase(df, '2010-01', enddatestr='2019-12').loc['2010' : '2019'].mean())
```

IP@IP    100.0 dtype: float64

```python
11. calc_ffill(df, nperiods=1, datecol=None, debug=False)
```

Forward-fill data for nperiods using the latest value. This is NOT the same as the pandas.DataFrame ffill function, it is not for filling NA values but for extending the DataFrame by nperiods with the last available value.
```python
12. calc_vol(df, nperiods, datecol=None, debug=False)
```

Calculate the volatility of a DataFrame for nperiods. Volatility is defined as standard deviation of the last nperiods divided by the average in that period.
```python
13. calc_unpop(df, init_val=100, ffill=True, datecol=None, debug=False)
```

Undo a %pop calculation, useful if the series was provided as such. init_val specifies the initial period value. Since the calculation is a cumulative product of series value, if there are any NA values in the input df the values will all be NA after that value. By default if any NA values exist after reindexing to a full index, the function will fill missing

values with NA. If this behavior is not wanted and to return only the last part of the series without any NA values, set
```python
ffill=False.
14. calc_cumsum(df, datecol=None, debug=False)
```

Calculate the simple cumulative sum of a DataFrame or Series. Functions to apply frequency conversion The below functions can be used to convert the frequency of a time series to another. As the imf_datatools will always return the index of a DataFrame as the beginning date of each period, it is necessary to use these functions when combining time series with different frequencies. For downsampling, where the new frequency is lower than the original, the basic choices are to take the mean or sum of the subperiods that create the new period, or to take the first or last available values within the new period. In the
```python
case that output for only complete periods are wanted, specify complete=True and this will remove incomplete periods.
```

The complete option is not available for functions calc_d2m and calc_w2m since it can be difficult to determine whether a day or week completes a month or not. For upsampling, where the new frequency is higher than the original, the two choices are to take the level so that the original value for a period is given to each subperiod that is included, or the ‘mean} where the original value of a period is distributed evenly among the subperiods.
```python
1. calc_d2w(df, method='mean', day='Sun', datecol=None, debug=False)
```

Convert a daily time series to weekly. The default will be to take the mean over the week and set the index to Sundays. Options are mean, average, sum, first, last.
```python
2. calc_d2m(df, method='mean', datecol=None)
```

Convert a daily time series to monthly. By default will take the mean over each month. Other options are sum, first, last.
```python
3. calc_d2q(df, method='mean', datecol=None)
```

Convert a daily time series to quarterly. By default will take the mean over each quarter. Other options are sum, first, last.
```python
4. calc_w2m(df, method='mean', datecol=None)
```

Convert a weekly time series to monthly. By default will take the mean over each month. Other options are sum, first, last.
```python
5. calc_m2q(df, method='mean', complete=False, datecol=None)
```

Convert a monthly time series to quarterly. By default will take the mean over each quarter. Other options are sum,
```python
first, last, middle. If middle is specified, the value of the middle month is used. If complete=True is specified, only
```

values for complete quarters are returned.
```python
6. calc_m2a(df, method='mean', complete=False, datecol=None)
```

Convert a monthly time series to annual. By default will take the mean over each year. Other options are sum, first, last, ytdcurrent, or the first three characters of a month name like Jan or Apr to return the value of that month for each year. If ytdcurrent is specified, the year-to-date sum is calculated for each year ending at the last month of the series. That is, if the series ends in August, the year-to-date sum from the previous year’s July to the current year’s August is
```python
calculated for each year. If complete=True is specified, only values for complete years are returned.
7. calc_q2a(df, method='mean', complete=False, datecol=None)
```

Convert a quarterly time series to annual. By default will take the mean over each year. Other options are sum, first,
```python
last, or Q1, Q3, etc., to return the value of that quarter for each year. If complete=True is specified, only values for
```

complete years are returned.

```python
8. calc_q2m(df, method='level', datecol=None)
```

Convert a quarterly series to monthly, defaults to level so that all months within a quarter are given the original quarter’s value, or can also specify mean which will split the quarter value by 3.
```python
9. calc_a2m(df, method='level', datecol=None)
```

Convert an annual series to monthly, defaults to level so that all months within a year are given the original year’s value, or can also specify mean which will split the annual value by 12.
```python
10. calc_a2q(df, method='level', datecol=None)
```

Convert an annual series to quarterly, defaults to level so that all quarters within a year are given the original year’s value, or can also specify mean which will split the annual value by 4.
# 5 Using with other Applications

For applications (programs or language) that can use system commands, the imf_datatools can be called as Python scripts to create output that the application can read, for example Excel or csv files using the data retrieval scripts from Sec. 4.2. Applications like MatLab and Mathematica could use the imf_datatools in this way, or could be used in workflow scripts. Note that it is possible to have scheduled tasks that can periodically update data which can then be fed into various dashboards, reports, and other systems so that the whole process can be automated from data retrieval to output. Below are some applications where the imf_datatools can be used directly without incurring system commands and writing out/reading in the output.

## 5.1 R

The imf_datatools can be used to get data directly loaded into a R data frame without having to write out and read in through an intermediate format. See the installation instructions in Chapter 2 on how to invoke the imf_datatools in R. The following sections show some examples of how data retrieval can be done directly within R. This is not meants as a comprehensive guide about the imf_datatools, but just examples of how Python commands will be translated into their R counterparts. Warning for timezones R The table of data retrieved in Python is automatically translated into an R data frame by the reticulate pakcage. However, when translating columns containing datetime values from Python to R, the reticulate package will automatically interpret the datetimes as being in UTC time and convert to local time. It seems that with the new version of Python
### 3.10.9 and R 4.4.0 as of June 2024, this applies to index datetimes as well.

The simplest solution is to set the local timezone to UTC with the command
```r
Sys.setenv(TZ="UTC")
```

Be warned however that if the local time is used by Sys.time() and other commands to show for example the time that a document was created, this will also be shown in UTC.
```r
Sys.time()
# "2021-05-11 21:44:22 EDT"
```

```python
# Set time zone to UTC
Sys.setenv(TZ="UTC")
```

```python
# Time is now shown in UTC
Sys.time()
# "2021-05-12 01:45:58 UTC"
```

```python
In cases where longformat=TRUE is used, that is, all dates are contained in columns of the DataFrame and not in the
```

index, there is the option to use the function with_tz from the lubridate package to force the times to be interpreted as UTC. An exmaple of the problem is shown below:
```python
# In longformat dates are now converted to local time zone!
tail(imf_datatools$get_edi_weo_data("111", "NGDP", vintage="2023-10", longformat=TRUE))
#       vintage country               dates       NGDP.A
# 74 2023-10-01     111 2022-12-31 19:00:00 2.694964e+13
# 75 2023-10-01     111 2023-12-31 19:00:00 2.796655e+13
# 76 2023-10-01     111 2024-12-31 19:00:00 2.904889e+13
# 77 2023-10-01     111 2025-12-31 19:00:00 3.022388e+13
# 78 2023-10-01     111 2026-12-31 19:00:00 3.142886e+13
# 79 2023-10-01     111 2027-12-31 19:00:00 3.269037e+13
```

In the below the with_tz function is applied so the dates are correctly set:
```r
library(lubridate)
```

```python
# Now times are correct:
tail(with_tz(imf_datatools$get_edi_weo_data("111", "NGDP", vintage="2023-10", longformat=TRUE), tzone="UTC"))
#       vintage country      dates       NGDP.A
# 74 2023-10-01     111 2023-01-01 2.694964e+13
# 75 2023-10-01     111 2024-01-01 2.796655e+13
# 76 2023-10-01     111 2025-01-01 2.904889e+13
# 77 2023-10-01     111 2026-01-01 3.022388e+13
# 78 2023-10-01     111 2027-01-01 3.142886e+13
# 79 2023-10-01     111 2028-01-01 3.269037e+13
```

Get EcOS data in R Below are commands to retrieve information or data from EcOS:
```python
# Get EcOS data
df <- imf_datatools$get_ecos_sdmx_data('WEO_WEO_PUBLISHED', '111', 'NGDP')
```

```python
# Get multiple EcOS data
df <- imf_datatools$get_ecos_sdmx_data('WEO_WEO_PUBLISHED',
```

c('111', '193'), c('NGDP', 'PPPPC'))

```python
# Get DOT data
df <- imf_datatools$get_ecos_sdmx_data('ECDATA_DOT_LATEST_PUBLISHED',
c('111', '193'), 'TXG_FOB_USD', counterpart<-c('158', '134'))
```

```python
# Get Bloomberg data
df <- imf_datatools$get_ecos_bloomberg_data('VIX Index', 'PX_LAST')
```

```python
# Get all series for USA
serieslist <- imf_datatools$ecos_sdmx_utilities$get_all_series(
'WEO_WEO_PUBLISHED', substr<-'111')
```

```python
# Get all databases
dbnames <- imf_datatools$ecos_sdmx_utilities$get_databases()
```

```python
# Get metadata for series
metadata <- imf_datatools$ecos_sdmx_utilities$get_ecos_sdmx_metadata(
```

'ECDATA_DOT_LATEST_PUBLISHED')

```python
# Get WEO country codes and groups
countrydata <- imf_datatools$ecos_sdmx_utilities$get_weo_country_codes()
```

Get DMX data in R

Below are commands to retrieve information or data from DMX files:
```python
# Get single series
dmxfilename <- "C:/ProgramData/IMF/DMX/Samples/sample.dmx"
df <- imf_datatools$dmx_utilities$get_dmx_data(dmxfilename, '911BF')
```

```python
# Get metadata
df <- imf_datatools$dmx_utilities$get_dmx_metadata(dmxfilename,
```

c('911BF', '911BCA_GDP', '911BFD'))

```python
# Get all series
serieslist <- imf_datatools$dmx_utilities$get_all_series(dmxfilename)
```

```python
# Get all series containing substr
serieslist <- imf_datatools$dmx_utilities$get_all_series(dmxfilename,
substr<-'GDP')
```

Get SQL data in R

Below are commands to retrieve information or data from economic SQL servers:
```python
# Get single series
df <- imf_datatools$sql_utilities$get_sql_data('PRDDMXSQL',
```

'DMX_WDI', '111.SP.POP.TOTL')

```python
# Get metadata
df <- imf_datatools$sql_utilities$get_sql_metadata('PRDDMXSQL',
```

'DMX_WDI', '111.SP.POP.TOTL')

```python
# Get metadata for all series including substr
df <- imf_datatools$sql_utilities$get_sql_metadata('PRDDMXSQL',
'DMX_WDI', substr<-'111')
```

```python
# Get available databases
df <- imf_datatools$sql_utilities$get_all_databases('PRDDMXSQL')
```

```python
# Get all series
serieslist <- imf_datatools$sql_utilities$get_all_series('PRDDMXSQL', 'DMX_WDI')
```

```python
# Get all series containing substr
serieslist <- imf_datatools$sql_utilities$get_all_series('PRDDMXSQL',
'DMX_WDI', substr<-'GDP')
```

Get Haver data in R Below are commands to retrieve information or data from economic Haver: 1
```python
# Get single series
df <- imf_datatools$get_haver_data('GDP@USECON')
```

```python
# Get metadata
metadata <- imf_datatools$haver_utilities$get_haver_metadata('GDP@USECON')
```

```python
# Get databases
metadata <- imf_datatools$haver_utilities$get_databases()
```

```python
# Get all series in a database
metadata <- imf_datatools$haver_utilities$get_all_series('USECON')
```

```python
# Get all metadata in a database
metadata <- imf_datatools$haver_utilities$get_all_metadata('USECON')
```

Get World Bank data in R Below are commands to retrieve information or data from the World Bank API:

```python
# Get data
df <- imf_datatools$get_worldbank_data('NY.GDP.MKTP.CD', 'CHN')
```

```python
# Get all countries
countrydata <- imf_datatools$worldbank_utilities$get_worldbank_countries()
```

```python
# Get available series
metadata <- imf_datatools$worldbank_utilities$get_all_worldbank_series()
```

```python
# Get info on a database
info <- imf_datatools$worldbank_utilities$get_datbase_info()
```

```python
# Get metadata
metadata <- imf_datatools$worldbank_utilities$get_worldbank_metadata(
```

'NY.GDP.MKTP.CD')

Get data.imf.org data in R Below are commands to retrieve information or data from data.imf.org:
```python
# Get data
dbname <- 'AFRREO'
df_afr <- imf_datatools$get_imf_ext_data(dbname, c('A', 'ZA','NGDP_R_PC_PP_PT'))
```

```python
# Get data for multiple countries
freq <- 'A'
countrylist <- c('ZA', 'GH', 'NG')
1 There is a R library for Haver called Haver (documentation at http://dm-edms.imf.org/cyberdocs/viewdocument.asp?doc=6734588&lib=
```

DMSDR1S). Users can use this directly instead of calling through Python, although available functions, formatting of data frames, etc. may be different. 2 There is a R library for the World Bank API called wbstats (documentation at https://cran.r-project.org/web/packages/wbstats/vignettes/

Using_the_wbstats_package.html). Users can use this directly instead of calling through Python, although available functions, formatting of data frames, etc. may be different.

```r
varlist <- 'NGDP_R_PC_PP_PT'
df_afr <- imf_datatools$get_imf_ext_data(dbname, freq, countrylist, varlist)
```

```python
# Get databases
dbnames <- imf_datatools$imf_ext_utilities$get_dataflow()
```

```python
# Get country codes in a database
countrydata <- imf_datatools$imf_ext_utilities$get_country_codes('APDREO')
```

```python
# Get series codes in a database
serieslist <- imf_datatools$imf_ext_utilities$get_series_codes('DOT')
```

```python
# Get metadata
```

```r
metadata <- imf_datatools$imf_ext_utilities$get_imf_ext_metadata(dbname,
freq,countrylist,varlist)
```

Combine multiple sources using python script in R To combine data from multiple sources, users need to copy imf_datatools/scripts/datacollector.py and input.xlsx
```python
from the datatools folder to current folder then read in series info from input.xlsx and write out to outname.xlsx
datacollector <- import("datacollector")
# Call the main function in datacollecto
datacollector$main(c("input.xlsx", "outname.xlsx"))
```

## 5.2 Stata

Starting with Stata 16, released in late 2019, Stata has Python built into it3 . This allows Stata to rely on Python to do tasks like data collection that Stata cannot do. Stata offers Python packages that allow integration of data and variables retrieved in Python to be transferred to Stata4 , and there is a set of Stata .ado and Stata help files developed by the Datatoolsteam to allow the usage of the imf_datatools. In R the syntax of running commands is similar to those of Python. However, Stata requires a different syntax for issuing
```python
imf_datatools commands, so we provide wrapper Stata commands to easily access the data.
```

### 5.2.1 ecosuse

The information below can alse be obtained by typing
```stata
help ecosuse
```

Syntax
```stata
ecosuse databases, [substr(keywords)] [clear | frame(framename[,replace])]
```

```stata
ecosuse metadata, database(database) [indicator(indicators) | substr(key words)] [clear |
```

frame(framename[,replace])]

```stata
ecosuse data, database(database) indicator(indicator) [country(country code) counterpart(country
```

code) sector(sector code) counterpart_sector(sector code) long scale(unit) freq(frequency) 3 https://www.stata.com/new-in-stata/python-integration/ 4 https://www.stata.com/python/api16/index.html

tin(date1,date2)] [clear | frame(framename[,replace])]

```stata
ecosuse bloomberg, ticker() field() [tin(date1,date2)] [clear | frame(framename[,replace])]
```

```stata
ecosuse commodity, database(database) commodity() datatype() [long scale(unit) freq(frequency)
```

tin(date1,date2)] [clear | frame(framename[,replace])]

```stata
ecosuse seriesnames, database(database) [substr(key words)] [clear | frame(framename[,replace])]
```

```stata
ecosuse countrycodes, [database(database)] [clear | frame(framename[,replace])]
```

```stata
ecosuse weocountryinfo, [clear | frame(framename[,replace])]
```

options                         Description ---------------------------------------------------------------------------------------------------Main databases                     dowloands names of the databases
```python
metadata                      dowloands metadata
```

data                          downloads data bloomberg                     dowloands Bloomberg data commodity                     dowloands commodity data
```python
seriesnames                   dowloands series names
countrycodes                  downloads country code
```

weocountryinfo                downloads information on WEO countries, various codes and groups

Options database()                    database indicator()                   indicator series, can be separated by commas substr()                      key word to search for series
```python
country()                     IFS code, can be separated by commas
```

counterpart()                 counterpart IFS code, can be separated by commas sector()                      sector code, can be separated by commas counterpart_sector()          counterpart sector code, can be separated by commas long                          imports data in long format scale(unit)                   scales data by specifieid units
```python
freq()                        frequency of data
```

tin()                         time range ticker()                      Bloomberg ticker field()                       Bloomberg field
```stata
clear                         replaces data in memory
```

frame(framename[,replace])    creates new data frame and save the data in the frame ---------------------------------------------------------------------------------------------------Description
```stata
ecosuse retrieves data and metadata from EcOS.
```

Main functions databases downloads database names

```python
metadata downloads metadata of indicator series or series which contain the keywords as specified in
```

option substr().

data downloads data as specified.

bloomberg downloads Bloomberg data.

commodity downloads commodity data. The available databases are WEO_COMMODITY_FORECAST_LIVE, WEO_OLD_COMMODITY_FORECAST_LIVE, WEO_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE, WEO_PRIMARY_COMMODITY_PRICE_SYSTEM_ARCHIVE, WEO_OLD_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE, ECDATA_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE, and ECDATA_COMMODITY_PRICE_SYSTEM.

```python
seriesnames only downloads names of the entire series or series which contain the keywords as
```

specified in option substr().

```python
countrycodes downloads countrycodes from ECOS database. The default is WEO_WEO_PUBLISHED.
```

weocountryinfo downloads information on WEO countries (such as country ISO 2-digit code, ISO 3-digit code, capital city, income level, geographic information, and etc.) and country grouping (such as advanced economies, emerging and developi mies, G7, Euro area, LAC, MENA, and etc.).

+---------+ ----+ Options +-------------------------------------------------------------------------------------

database() specifies the database. For example, WEO_WEO_PUBLISHED, ECDATA_DOT_LATEST_PUBLISHED. This option is required for ecosuse metadata and ecosuse data.

indicator() selects indicator series. Multiple series can be separated by commas. For example, indicator(ALL) will return all series, and indicator(NGDP, NGDP_R) will return both series. This option is required for ecosuse data. indicator() or substr() is required for ecosuse
```python
metadata.
```

substr() allows for searching for sereis by keywords. Multiple keywords can be separated by commas. For example, substr(GDP, TX) will return series containing both GDP and TX. indicator() or substr() is required for ecosuse metadata.

```python
country() selects country. Only 3-digit IFS country code is allowed, and country code can be
```

separated by commas. For example, country(ALL) will return all countries, and country(111,193) will return both countries. This option is required for ecosuse data.

counterpart() selects counterpart country. Only 3-digit IFS country code is allowed, and country code can be separated by commas.

sector() selects sector code. Multiple sector codes can be separated by commas.

counterpart_sector() selects counterpart sector code. Multiple sector codes can be separated by commas

long imports data in long format. The default option is to import the data in the wide format.

scale(unit) scales data by specified units. Variable labels contains the units and/or currency for reference. scale(default) or scale(ecos) scales to what the default scale is in EcOS. For example, NGDP is in "Billions" in EcOS. If scale(ecos) is specified, NGDP will be divided by 1,000,000,000. Other options for scale() are U/K/M/B/T. If any of these are specified, the values are divided by 1, 1000, 1,000,0000, 1,000,0000, 000, 1,000,0000,000,000. ecos/U/K/M/B/T are case-insensitive. The default is scale(default) or scale(ecos).

```python
freq() specifies frequency of imported data. It can be A for annual, Q for quarterly, or M for
```

monthly, or D for daily. A/Q/M/D are case-insensitive. Multiple frequencies can be specified if available. For example, freq(AQ). The default is A.

```python
tin(date1,date2) allows for time range selection. date1 = minimum date or blank to indicate no
minimum date; date2 = maximum date or blank to indicate no maximum date. The default is the
```

whole series. Here are examples of acceptable date forms: tin(1980,2010), tin(1980q1,2010q1), tin(1980m1,2010m1), tin(2015,), tin(2015-01,), tin(2015-01-15, 2015-12-15).

ticker() selects Bloomberg ticker. For example, VIX Index, VXN Index.

field() selects Bloomberg field. For example, PX_LAST, PX_HIGH.

```stata
clear replaces data in memory.
```

frame(framename[, replace]) creates new data frame and saves the downloaded data in the frame. If there is no frame named framename in memory, a new frame named framename is created. If framename does exist in memory, you can replace the frame. replace clears framename before the data are read to it.

Examples

+-----+ ----+ WEO +-----------------------------------------------------------------------------------------

Get data. . ecosuse data, database(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) f(ecos_weo1, replace)

Get data in long format. . ecosuse data, d(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) long clear Declare the data to be panel data.
```python
. gen IFS_code = real(COUNTRY)
. gen year = yofd(dates)
```

. order IFS_code year . xtset IFS_code year . drop COUNTRY dates

Get data in specified time range. . ecosuse data, d(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) tin(2000,2015)
```stata
clear
```

Use options long and tin. . ecosuse data, d(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) long tin(2000,2015) clear

Can declare the data to be panel as in the example before.

Get data from WEO vintage, all series for country 111 (USA). . ecosuse data, d(WEO_WEO_PUBLISHED) country(111) indicator(ALL) clear

Get all quarterly data for series NGDP. . ecosuse data, d(WEO_WEO_PUBLISHED) country(ALL) indicator(NGDP) freq(Q) long f(ecos_weo6) Declare the data to be panel data.

```python
. gen IFS_code = real(COUNTRY)
. gen quarter = qofd(dates)
```

. format quarter %tq . order IFS_code quarter . xtset IFS_code quarter . drop COUNTRY dates

Scale by units. . ecosuse data, d(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, LP) scale(M) clear

. ecosuse data, d(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) scale(ecos) long
```python
freq(AQ) clear
```

+-----+ ----+ DOT +-----------------------------------------------------------------------------------------

Get data. . ecosuse data, d(ECDATA_DOT_LATEST_PUBLISHED) country(111, 193, 196) indicator(TXG_FOB_USD) counterpart(158, 134, 156) clear

Get data in long format. . ecosuse data, d(ECDATA_DOT_LATEST_PUBLISHED) country(111, 193, 196) indicator(TXG_FOB_USD) counterpart(158, 134, 156) long clear Declare the data to be panel data.
```python
. gen year = yofd(dates)
. gen country_pair = COUNTRY + "-" + COUNTERPART_COUNTRY
```

. encode country_pair, gen(country_pair_id) . order COUNTRY COUNTERPART_COUNTRY country_pair_id year . xtset country_pair_id year . drop country_pair dates

+-----+ ----+ BOP +-----------------------------------------------------------------------------------------

Get data. . ecosuse data, d(ECDATA_BOP) country(111) indicator(IAFR_BP6_USD) clear

Get vintage data. . ecosuse data, d(ECDATA_BOP_2018M10) country(111) indicator(IAFR_BP6_USD) clear

+-----+ ----+ GEE +-----------------------------------------------------------------------------------------

Get vintage data. . ecosuse data, d(WEO_GEEOCT2018Pub) country(111) indicator(TXGSN) clear

Get live data. (It may require access right.) . ecosuse data, d(WEO_GEE_LIVE) country(111) indicator(TXG_PT) clear

+-----------+ ----+ Bloomberg +-----------------------------------------------------------------------------------

Get data.

. ecosuse bloomberg, ticker(VIX Index, VXN Index) field(PX_LAST, PX_HIGH) clear

Get data for all fields. . ecosuse bloomberg, ticker(VIX Index) field(ALL) clear

Get data in specified time range. . ecosuse bloomberg, ticker(VIX Index) field(ALL) tin(2000-01-15,2019-12-15) clear

+-----------+ ----+ Commodity +-----------------------------------------------------------------------------------

Get data. . ecosuse commodity, d(ECDATA_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE) commodity(PCOAL, PGASO, PFOOD, PDAP, PCPI, PCOIL) datatype(CYuan, Euro, Real, SDR, USD) clear

Get data in long format. . ecosuse commodity, d(ECDATA_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE) commodity(PCOAL, PGASO, PFOOD, PDAP, PCPI, PCOIL) datatype(CYuan, Euro, Real, SDR, USD) long clear

Get quarterly and annual data. . ecosuse commodity, d(ECDATA_PRIMARY_COMMODITY_PRICE_SYSTEM_LIVE) commodity(PCOAL, PGASO, PFOOD, PDAP, PCPI, PCOIL) datatype(CYuan, Euro, Real, SDR, USD) long freq(QA) clear

+----------------------+ ----+ Get info on datasets +------------------------------------------------------------------------

Get names of all ECOS databases. . ecosuse databases, f(ecos_db, replace)

Get databases containing substr WEO. . ecosuse databases, substr(WEO) f(ecos_db_weo, replace)

Get all metadata in a database. . ecosuse metadata, d(WEO_WEO_PUBLISHED) f(ecos_weo_metadata, replace)

Get all metadata in a database with substr. . ecosuse metadata, d(WEO_WEO_PUBLISHED) substr(GDP, TX) f(ecos_weo_metadata, replace)

Get all metadata in a database with indicators. . ecosuse metadata, d(ECDATA_DOT_LATEST_PUBLISHED) indicator(TXG_FOB_USD) f(ecos_dot_metadata, replace)

Get all series in a database. . ecosuse seriesnames, d(WEO_WEO_PUBLISHED) f(ecos_weo_series, replace)

Get all Bloomberg tickers. . ecosuse seriesnames, d(ECDATA_BLOOMBERG) f(ecos_bloomberg_tickers, replace)

Get all series in a database with substrings. . ecosuse seriesnames, d(WEO_WEO_PUBLISHED) substr(GDP, TX) f(ecos_weo_series, replace)

Get all country codes (defaults to WEO_WEO_PUBLISHED). . ecosuse countrycodes, f(ecos_countrycodes, replace)

Get country codes from ECDATA_DOT_LATEST_PUBLISHED. . ecosuse countrycodes, d(ECDATA_DOT_LATEST_PUBLISHED) f(ecos_countrycodes_dot, replace)

Get full info on WEO countries and groups. . ecosuse weocountryinfo, f(ecos_full_weo_countrycodes, replace)

### 5.2.2 ediuse

The information below can also be obtained by typing in stata:
```stata
help ediuse
```

Syntax
```stata
ediuse databases, [clear | frame(framename[,replace])]
```

```stata
ediuse dimensions, database(database) [clear | frame(framename[,replace])]
```

```stata
ediuse values, database(database) var(dimension) [substr(key words)] [clear |
```

frame(framename[,replace])]

```stata
ediuse data, database(database) query_options [long scale(unit) tin(date1,date2) clear |
```

frame(framename[,replace])]

```stata
ediuse metadata, database(database) query_options clear | frame(framename[,replace])]
```

options                         Description ---------------------------------------------------------------------------------------------------Main databases                     dowloands names of the databases dimensions                    dowloands dimensions of a database values                        downloads values of one dimension of a database data                          downloads data
```python
metadata                      downloads metadata
```

Options database()                    database var()                         dimension of database substr()                      key word to search for series long                          imports data in long format scale()                       scales data by specifieid units tin()                         time range
```stata
clear                         replaces data in memory
```

frame([,replace])             creates new data frame and save the data in the frame query_options                 query options vary by database ---------------------------------------------------------------------------------------------------Description
```stata
ediuse queries and retrieves data from EDI via API.
```

Options

+------+ ----+ Main +----------------------------------------------------------------------------------------

databases downloads names of the database.

dimensions downloads dimensions of a database. For example, "weo-published" database contains the following dimensions: country, indicator, vintage and freq.

values downloads values of one dimension of a database.

data downloads data as queried.

```python
metadata downloads metadata as queried.
```

+---------+ ----+ Options +-------------------------------------------------------------------------------------

database() specifies the database. For example, weo-published, bloomberg, consensus-forecasts.   This option is required for ediuse dimensions, ediuse values and ediuse data.

var() specifies one dimension of a database and downloads its values. The values can be used to query and retrieve specific series in the options of ediuse data. This option is required for
```stata
ediuse values.
```

substr() allows for searching for sereis by keywords.

1. Multiple keywords can be separated by commas. For example, substr(GDP, TX) will return
series containing both GDP and TX.
2. Wildcard asterisk (*) can be used in the search. The logic is as follows:
1) If the substr does NOT contain a *, a search of *substr* is done so substr is contained. 2) If the substr is a list like the above, a search of *gdp*bp6* is done so that all subparts are contained in order. 3) If the substr contains any *s, then this is passed in directly so that if for example *gdp is passed in, results will end with gdp, while gdp* will return results starting with gdp, and *gdp* will return anything containing gdp.

long imports data in long format. The default option is to import the data in the wide format. long is not available for time series data. For example, Bloomberg data.

scale(unit) scales data by specified units. Variable labels contains the units and/or currency for reference. scale(default) scales to the original scale stored in the database. Other options for scale() are U/K/M/B/T. If any of these are specified, the values are divided by 1, 1000, 1,000,0000, 1,000,0000, 000, 1,000,0000,000,000. ecos/U/K/M/B/T are case-insensitive. The default is scale(default).

```python
tin(date1,date2) allows for time range selection. date1 = minimum date or blank to indicate no
minimum date; date2 = maximum date or blank to indicate no maximum date. The default is the
```

whole series. For example, tin(1980,2010), tin(1980q1,2010q1), tin(1980m1,2010m1), tin(2015,)

```stata
clear replaces data in memory.
```

frame(framename[, replace]) creates new data frame and saves the downloaded data in the frame. If there is no frame named framename in memory, a new frame named framename is created. If

framename does exist in memory, you can replace the frame. replace clears framename before the data are read to it.

query_options vary by databases. They generally are database dimensions. See below for examples on how to specify the query options.

Examples

Get list of databases available in EDI. . ediuse databases, clear

+---------------+ ----+ WEO published +-------------------------------------------------------------------------------

To query WEO published, first get dimensions. . ediuse dimensions, d(weo-published) clear

Four dimensions are listed in variable name: country indicator vintage freq. Those four dimensions will be query_options of edi data.

Specifically, the syntax to query and retrieve WEO published database is:

```stata
ediuse data, d(weo-published) country() indicator() [vintage() freq()] [long scale() tin()]
```

[clear | frame(framename[,replace])]

Options country() indicator() are required. all can be specified to download all indicators or all countries. But all cannot be used in both options at the same time. The default for vintage() is most recent publication and for freq() is annual.

The following command retrieve values of dimension indicator. . ediuse values, d(weo-published) var(indicator) clear

The following command retrieve values of dimension indicator which contains key words gdp and bp6. . ediuse values, d(weo-published) var(indicator) substr(gdp, bp6) clear

Wildcard asterisk (*) can be specified in substr. . ediuse values, database(weo-published) var(indicator) substr(*gdp*bp6*) clear

The values of indicator can be used to select data using option indicator(). Other dimension can be used to select data in the same way. . ediuse data, d(weo-published) indicator(NGDP, PPPPC) country(111, 193) clear

Get multiple vintages in long format. . ediuse data, d(weo-published) indicator(NGDP, PPPPC) country(111, 193) vintage(2020-01-01, 2020-04-01) long clear

Get multiple frequencies, scale data by trillions, and download data since 2010. For consistency, all parameters are separated by comma. For exmample, freq(A,Q) instead of freq(AQ). . ediuse data, d(weo-published) indicator(NGDP, PPPPC) country(111, 193) freq(A,Q) scale(t) tin(2010,) clear

Wildcard asterisk (*) can be specified in country() and indicator(). . ediuse data, d(weo-published) country(11*) indicator(*GDP) long clear

More examples on getting multiple vintages.

1. Matches all vintages which contain 200*.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(200*) long clear

2. Matches all vintages which contain 200*-04.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(A) vintage(200*-04) long clear

3. Matches any vintage in range 2000 � 2015. Note the double dash.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(A) vintage(2000--2015) long clear

4. Matches any vintage in range 201[5-9] which is 2015 to 2019.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(201[5-9]) long clear

5. Matches any vintage in range 201[136-9] which is 2011, 2013, 2016, 2017, 2018, 2019.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(201[136-9]) long clear

6. Returns all 2019 vintages.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(2019) long clear

7. Returns all 2018, 2019 vintages.
. ediuse data, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(2018, 2019) long clear

+-----------+ ----+ Bloomberg +-----------------------------------------------------------------------------------

Bloomberg database contains three dimensions: field ticker freq. The syntax to query Bloomberg database is:
```stata
ediuse data, d(bloomberg) field() ticker() freq() [tin()] [clear | frame(framename[,replace])]
```

Get data. . ediuse data, d(bloomberg) field(PX_LAST) ticker(VIX Index) clear

+---------------------+ ----+ Consensus Forecasts +-------------------------------------------------------------------------

Consensus Forecasts database contains two dimensions: seriescode freq. The syntax to query Consensus Forecasts database is:
```stata
ediuse data, d(consensus-forecasts) seriescode() freq() [scale() tin()] [clear |
```

frame(framename[,replace])]

Get data. . ediuse data, d(consensus-forecasts) seriescode(111NYPCP_YOY, 111NYPCP_YOY_1Y) clear

Get data in long format. . ediuse data, d(consensus-forecasts) seriescode(111NGDP_R_YOY, 193NGDP_R_YOY) long clear

Wildcard asterisk (*) can be specified in seriescode(). . ediuse data, d(consensus-forecasts) seriescode(*TMG_YOY*) long clear

+----------+

----+ Metadata +------------------------------------------------------------------------------------

query_options follow ediuse data. Below are some examples.

WEO. . ediuse metadata, d(weo-published) country(111) indicator(NGDP) clear

. ediuse metadata, d(weo-published) country(111) indicator(NGDP) freq(Q) vintage(2020-01-01, 2020-04-01) clear

. ediuse metadata, d(weo-published) country(11*) indicator(*GDP) freq(Q) clear

Multiple databases can be used for metadata search. Note that vintage format is different for each database in output. . ediuse metadata, d(weo-published, csd-forecasts-desk) country(111) indicator(NGDP) freq(Q) vintage(201*) clear

### 5.2.3 dmxuse

The information below can also be obtained by typing into stata
```stata
help dmxuse
```

Syntax
```stata
dmxuse metadata, dmxpath(path) [indicator(indicator)| substr(key words)] [clear |
```

frame(framename[,replace])]

```stata
dmxuse seriesnames, dmxpath(path) substr(key words) [clear | frame(framename[,replace])]
```

```stata
dmxuse data, dmxpath(path) indicator(indicator) [scale(unit) freq(frequency) tin(date1,date2)]
```

[clear | frame(framename[,replace])]

options                         Description ---------------------------------------------------------------------------------------------------Main
```python
metadata                      dowloands metadata
seriesnames                   dowloands series names
```

data                          downloads data

Data Specification dmxpath()                     path to DMX file indicator()                   indicator substr()                      key word to search for series scale(unit)                   scales data by specifieid units
```python
freq()                        frequency of data
```

tin()                         time range
```stata
clear                         replaces data in memory
```

frame(framename[,replace])    creates new data frame and save the data in the frame ---------------------------------------------------------------------------------------------------Description
```stata
dmxuse imports data from DMX file.
```

Options

+------+ ----+ Main +----------------------------------------------------------------------------------------

```python
metadata downloads metadata that give information about the DMX file.
```

```python
seriesnames only downloads names of the entire series or series which contain the keywords as
```

specified in option substr().

data downloads data as specified.

+--------------------+ ----+ Data Specification +--------------------------------------------------------------------------

dmxpath() specifies the location of the DMX file. This option is required.

indicator() selects indicators. This option is required for dmxuse data.

substr() allows for searching for sereis by keywords. Multiple keywords can be separated by commas. For example, substr(GDP, TX) will return series containing both GDP and TX.

scale(unit) scales data by specified units. Variable labels contains the units and/or currency for reference. scale(default) scales to the original scale stored in the database. Other options for scale() are U/K/M/B/T. If any of these are specified, the values are divided by 1, 1000, 1,000,0000, 1,000,0000, 000, 1,000,0000,000,000. default/U/K/M/B/T are case-insensitive. The default is scale(default).

```python
freq() specifies the frequency of the imported data. It can be A for annual, Q for quarterly, or M
```

for monthly, or W for weekly, or D for daily. A/Q/M/W/D are case-insensitive. The default is A.

```python
tin(date1,date2) allows for time range selection. date1 = minimum date or blank to indicate no
minimum date; date2 = maximum date or blank to indicate no maximum date. The default is the
```

whole series. For example, tin(1980,2010), tin(1980q1,2010q1), tin(1980m1,2010m1), tin(2015,)

```stata
clear replaces data in memory.
```

frame(framename[, replace]) creates new data frame and saves the downloaded data in the frame. If there is no frame named framename in memory, a new frame named framename is created. If framename does exist in memory, you can replace the frame. replace clears framename before the data are read to it.

Examples

Get metadata of all series in a DMX file. . dmxuse metadata, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) clear

Get metadata of series using keywords search. . dmxuse metadata, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) substr(GDP) f(dmx_metadata, replace)

Get metadata of specified indicators. . dmxuse metadata, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) indicator(911BE) f(dmx_metadata_series)

Get all series names. . dmxuse seriesnames, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) f(dmx_serieslist)

Get available series names and narrow down with substr(). . dmxuse seriesnames, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) substr(911, GDP) f(dmx_serieslist_str)

Get data of specified indicators. . dmxuse data, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) indicator(911BE, 911BCA_GDP) frame(dmx_data)

Get annual data. . dmxuse data, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) indicator(911BE, 911BCA_GDP)
```python
freq(A) f(dmx_data_annual)
```

Get data in specified time range. . dmxuse data, dmxpath(C:\ProgramData\IMF\DMX\Samples\sample.dmx) indicator(911BE, 911BCA_GDP) tin(2000,) clear

### 5.2.4 dmxeuse

The information below can also be obtained by typing in stata:
```stata
help dmxeuse
```

Syntax
```stata
dmxeuse metadata, dmxepath(path) [indicator(indicator)| substr(key words)] [clear |
```

frame(framename[,replace])]

```stata
dmxeuse seriesnames, dmxepath(path) substr(key words) [clear | frame(framename[,replace])]
```

```stata
dmxeuse data, dmxepath(path) indicator(indicator) [scale(unit) freq(frequency) tin(date1,date2)]
```

[clear | frame(framename[,replace])]

options                         Description ---------------------------------------------------------------------------------------------------Main
```python
metadata                      dowloands metadata
seriesnames                   dowloands series names
```

data                          downloads data

Data Specification dmxepath()                    path to DMXe file indicator()                   indicator substr()                      key word to search for series scale(unit)                   scales data by specifieid units
```python
freq()                        frequency of data
```

tin()                         time range
```stata
clear                         replaces data in memory
```

frame(framename[,replace])    creates new data frame and save the data in the frame ----------------------------------------------------------------------------------------------------

Description

```stata
dmxeuse imports data from DMXe file.
```

Options

+------+ ----+ Main +----------------------------------------------------------------------------------------

```python
metadata downloads metadata that give information about the DMXe file.
```

```python
seriesnames only downloads names of the entire series or series which contain the keywords as
```

specified in option substr().

data downloads data as specified.

+--------------------+ ----+ Data Specification +--------------------------------------------------------------------------

dmxepath() specifies the location of the DMXe file. This option is required.

indicator() selects indicators. This option is required for dmxeuse data.

substr() allows for searching for sereis by keywords. Multiple keywords can be separated by commas. For example, substr(GDP, TX) will return series containing both GDP and TX.

scale(unit) scales data by specified units. Variable labels contains the units and/or currency for reference. scale(default) scales to the original scale stored in the database. Other options for scale() are U/K/M/B/T. If any of these are specified, the values are divided by 1, 1000, 1,000,0000, 1,000,0000, 000, 1,000,0000,000,000. default/U/K/M/B/T are case-insensitive. The default is scale(default).

```python
freq() specifies the frequency of the imported data. It can be A for annual, Q for quarterly, or M
```

for monthly, or W for weekly, or D for daily. A/Q/M/W/D are case-insensitive. The default is A.

```python
tin(date1,date2) allows for time range selection. date1 = minimum date or blank to indicate no
minimum date; date2 = maximum date or blank to indicate no maximum date. The default is the
```

whole series. For example, tin(1980,2010), tin(1980q1,2010q1), tin(1980m1,2010m1), tin(2015,)

```stata
clear replaces data in memory.
```

frame(framename[, replace]) creates new data frame and saves the downloaded data in the frame. If there is no frame named framename in memory, a new frame named framename is created. If framename does exist in memory, you can replace the frame. replace clears framename before the data are read to it.

Examples

Get metadata of all series in a DMXe file. . dmxeuse metadata, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) clear

Get metadata of series using keywords search. . dmxeuse metadata, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) substr(BCA) clear

Get metadata of specified indicators. . dmxeuse metadata, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) i(646BCA_BP6) clear

Get all series names. . dmxeuse seriesnames, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe)
```stata
clear
```

Get available series names and narrow down with substr(). . dmxeuse seriesnames, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) substr(BCA) clear

Get data of specified indicators. . dmxeuse data, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) i(646BCA_BP6, 646BXG) clear

Get annual data. . dmxeuse data, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) i(646BCA_BP6) freq(A) clear

Get data in specified time range. . dmxeuse data, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) i(646BCA_BP6) tin(2010,) clear

Get data in specified scale unit. . dmxeuse data, dmxepath(\\was.int.imf.org\ecn\ems_shared\pub\datatools\samples\gab.dmxe) i(646BCA_BP6) scale(B) clear

### 5.2.5 sqluse

The information below can also be obtained by typing in stata:
```stata
help sqluse
```

Syntax
```stata
sqluse databases, server(server name) [clear | frame(framename[,replace])]
```

```stata
sqluse metadata, server(server name) database(database) [indicator(indicators) |
```

substr(keywords)] [clear | frame(framename[,replace])]

```stata
sqluse seriesnames, server(server name) database(database) [substr(keywords)] [clear |
```

frame(framename[,replace])]

```stata
sqluse data, server(server name) database(database) indicator(indicator) [scale(unit)
freq(frequency) tin(date1,date2)]] [clear | frame({it:framena dab:replace}])]
```

options                         Description ---------------------------------------------------------------------------------------------------Main databases                     dowloands names of the databases resid on the server
```python
metadata                      dowloands the metadata of the database
metadata                      dowloands the series names of the database
```

data                          downloads data

Options
```python
server()                      server where data resides
```

database()                    database within the server indicator()                   indicator series, can be separated by commas substr()                      keyword to search for series scale(unit)                   scales data by specifieid units
```python
freq()                        frequency of data
```

tin()                         time range
```stata
clear                         replace data in memory
```

frame(framename[,replace])    creates new data frame and save the data in the frame ---------------------------------------------------------------------------------------------------Description
```stata
sqluse imports data from internal SQL server.
```

Options +------+ ----+ Main +----------------------------------------------------------------------------------------

databases downloads database names

```python
metadata downloads metadata of indicator series or series which contain the keywords as specified in
```

option indicator() or substr().

```python
seriesnames only downloads names of the entire series or series which contain the keywords as
```

specified in option substr().

data downloads data as specified.

+---------+ ----+ Options +-------------------------------------------------------------------------------------

```python
server() specifies the server where data resides. For example, PRDDMXSQL, PRDCSDSQL. This option is
```

required for all commands.

database() specifies the database within the server. For example, DMX_WDI, CSD_FORECAST. This option is required for sqluse metadata and sqluse data.

indicator() selects indicator series. Multiple series can be separated by commas. For example, indicator(111.SP.POP.TOTL,193.SP.POP.TOTL) will return both series. This option is required for
```stata
sqluse data. indicator() or {op ()} is required for sqluse metadata.
```

substr() allows for searching for sereis by keywords. Multiple keywords can be separated by commas. For example, substr(111, TAX) will return series containing both 111 and TAX. indicator() or substr() is required t sqluse metadata}.

scale(unit) scales data by specified units. Variable labels contains the units and/or currency for reference. scale(default) scales to the original scale stored in the database. Other options for scale() are U/K/M/B/T. If any of these are specified, the values are divided by 1, 1000, 1,000,0000, 1,000,0000, 000, 1,000,0000,000,000. default/U/K/M/B/T are case-insensitive. The default is scale(default).

```python
freq() specifies the frequency of the imported data. It can be A for annual, Q for quarterly, or M
```

for monthly. A/Q/M are case-insensitive. The default is A.

```python
tin(date1:date2) allows for time range selection. date1 = initial date; date2 = final date. The
```

default is the whole series.

```stata
clear replaces data in memory.
```

frame(framename[, replace]) creates new data frame and saves the downloaded data in the frame. If there is no frame named framename in memory, a new frame named framename is created. If framename does exist in memory, you can replace the frame. replace clears framename before the data are read to it. Examples Get available databases. . sqluse databases, server(PRDDMXSQL) clear

Get available databases and narrow down with substr(). . sqluse databases, server(PRDDMXSQL) substr(DMX, VE) f(sql_databasese_substr)

Get metadata of all series in a database. (NOT RECOMMENDED, MAY TAKE TIME.) . sqluse metadata, server(PRDDMXSQL) database(DMX_WDI)f(sql_metadata_all)

Get metadata of series using keywords search. . sqluse metadata, server(PRDDMXSQL) database(DMX_WDI) substr(111, TAX) f(sql_metadata_substr)

Get metadata of indicators. . sqluse metadata, server(PRDDMXSQL) database(DMX_WDI) indicator(111.SP.POP.TOTL, 193.SP.POP.TOTL) f(sql_metadata)

Get all series names. . sqluse seriesnames, server(PRDDMXSQL) database(DMX_WDI) f(sql_seriesnames)

Get available series names and narrow down with substr(). . sqluse seriesnames, server(PRDDMXSQL) database(DMX_WDI) substr(111, GDP) f(sql_seriesnames_substr)

Get data of specified indicators. . sqluse data, server(PRDDMXSQL) database(DMX_WDI) indicator(111.SP.POP.TOTL, 193.SP.POP.TOTL) f(sql_data)

Get annual data. . sqluse data, server(PRDDMXSQL) database(DMX_WDI) indicator(111.SP.POP.TOTL, 193.SP.POP.TOTL)
```python
freq(A) f(sql_data_annual)
```

Get data in specified time range. . sqluse data, server(PRDDMXSQL) database(DMX_WDI) indicator(111.SP.POP.TOTL, 193.SP.POP.TOTL) tin(2000,) clear

### 5.2.6 dmxewriter

The information below can also be obtained by typing in stata:
```stata
help dmxewriter
```

Syntax

dmxewriter data, dmxepath(path) [frame(framename) indicator(indicator) timevar(time variable) name(name)
```python
freq(frequency) tin(date1,date2)]
```

dmxewriter metadata, dmxepath(path) frame(framename) indicator(indicator)

dmxewriter values, column(column name)

dmxewriter rename, dmxepath(path) indicator(indicator) newindicator(new indicator)

dmxewriter delete, dmxepath(path) indicator(indicator)

dmxewriter deletelogs, dmxepath(path)

options                         Description ------------------------------------------------------------------------------------------------------------Main data                          write data to a DMXe file
```python
metadata                      write metadata to a DMXe file
```

values                        extract valid metadata values of a column/field
```stata
rename                        renames an indicator in a DMXe file
```

delete                        deletes the values of indicators from a DMXe file deletelogs                    deletes logs of a DMXe file

data Specification dmxepath()                       path to the DMXe file frame()                          specifies the frame which contains the data to write to the DMXe file indicator()                      indicators timevar()                        name of the date or time varible which can be used to identify the data to be series or a panel data name()                        name of the columns to be written out in the DMXe file
```python
freq()                        frequency of data
```

tin()                         time range column()                      column/field name

```stata
rename Specification
```

newindicator()                new indicator name -------------------------------------------------------------------------------------------------------------

Description

dmxewriter Write data and metadata from a Stata data frame to a DMXe file. It can also modify a DMXe file.

Options +——+ —-+ Main +———————————————————————————————————-

data writes data from a Stata data frame to a DMXe file.

```python
metadata writes metadata from Stata to a DMXe file.
```

values extracts valid metadata values of a column/field

```stata
rename renames an indicator in a DMXe file.
```

delete deletes values of indicators from a DMXe file. It doesn't selete the holder of the indicators. freq()

required.

deletelogs deletes logs of a DMXe file.

+--------------------+ ----+ Data Specification +-----------------------------------------------------------------------------------

dmxepath() specifies the location of the DMXe file. This option is required.

frame() the frame which contains the data to write to the DMXe file. If frame() is not specific, the default current frame.

indicator() specifies indicators to be written out. Indicators are seperated by comma. If indicator() is not speicified for dmxewriter data, the default is all variables in Stata data frame. This option is required dmxe ename} and dmxewriter delete.

timevar() identifies the date or time varible which can be used to identify the data to be a time series or a data. If timevar() is not speicified, the default is variable dates.

name() specifies the name of the columns to be written out in the DMXe file. If name() is not speicified, the is the variable name in Stata data frame.

```python
freq() specifies the frequency of the data to be written out. It can be A for annual, Q for quarterly, or M f
```

monthly, or W for weekly, or D for daily. A/Q/M/W/D are case-insensitive. If the same indica vailable for different frequencies, the default is annual, i.e., A. For example, NGDP is available for annual and quar quarterly NGDP is requested instead of annual, freq(Q) must be specified. freq() is required for dmxewri delete.

```python
tin(date1,date2) allows for time range selection. date1 = minimum date or blank to indicate no minimum date;
```

maximum date or blank to indicate no maximum date. The default is the whole series. For example, tin(198 tin(1980q1,2010q1), tin(1980m1,2010m1), tin(2015,)

column() specifies the name of the column/field. This option is requied for dmxewriter values.

Examples

+-----+ ----+ WEO +--------------------------------------------------------------------------------------------------

1. Get annual data from EcOS.
. ecosuse data, database(WEO_WEO_PUBLISHED) country(111, 193, 196) indicator(NGDP, PCPI) f(ecos_A, replace) (click to run) Write data to a DMXe file. . dmxewriter data , dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_A) indicator(_111NGDP_A, _193PCPI_A) timevar(dates) name(111NGDP.A, 193PCPI.A) (click to run)

2. Get quarterly data from EcOS.
. ecosuse data, database(WEO_WEO_PUBLISHED) country(111) indicator(NGDP) freq(Q) f(ecos_Q, replace) (click to run) Write data to a DMXe file. . dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_Q) indicator(_111NGDP_Q) timevar(date name(111NGDP.Q) (click to run)

3. Get monthly data from EcOS.
. ecosuse data, database(ECDATA_IFS) country(111) indicator(ENEER_IX) freq(M) frame(ecos_M, replace) (click to run) Write data to a DMXe file. . dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_M) indicator(_111ENEER_IX_M) timevar( name(111ENEER_IX.M) (click to run)

4. Get daily data from EcOS.
. ecosuse bloomberg, ticker(VIX Index) field(PX_LAST) frame(ecos_D, replace) (click to run) Write data to a DMXe file. . dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_D) indicator(VIX_IndexPX_LAST_D) timevar(dates) name(VIX_IndexPX_LAST.D) (click to run)

5. Specify option tin() to restrict the time range of the data to be written out.
. dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(ecos_A) indicator(_111PCPI_A) timevar(date name(111PCPI.A) tin(1990, 2020) (click to run)

+-------+ ----+ Haver +------------------------------------------------------------------------------------------------

1. Get annual data from Haver.
. frame create haver_A (click to run) . frame change haver_A (click to run) . import haver gdpa@usecon, clear (click to run) Write data to a DMXe file. . dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(haver_A) indicator(gdpa_usecon) timevar(ti name(GDPA@USECON) (click to run)

2. Get daily data from Haver.
. frame create haver_D (click to run) . frame change haver_D (click to run) . import haver ffed@daily, clear (click to run) Write data to a DMXe file. . dmxewriter data, dmxepath(C:/temp/dmxewriter_example.dmxe) frame(haver_D) indicator(ffed_daily) timevar(tim name(FFED@DAILY) (click to run)

+-----------------+ ----+ Modify metadata +--------------------------------------------------------------------------------------

Write metadata to a DMXe file.

1. Modify column Descriptor. Descriptor can take any string value.
. dmxewriter metadata, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(111NGDP.A) column(Descriptor) valu domestic product, current prices") (click to run)

2. Modify column Scale. Scale can take only pre-specified values.
. dmxewriter metadata, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(111NGDP.A) column(Scale) value("Billions")") (click to run)

3. Previous example shows that Scale can take only pre-specified values. dmxewriter values can extract value
values for a field. . dmxewriter values, column(Scale) (click to run)

Please note that not all columns can be modified. If a column is not a valid writable DMXe field, the action ignored, and Stata will report a warning.

+--------------------+ ----+ Modify a DMXe file +-----------------------------------------------------------------------------------

1. Rename an indicator in a DMXe file.
. dmxewriter rename, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(FFED@DAILY) newindicator(FFED) (click to run)

2. Delete values of indicators from a DMXe file.
. dmxewriter delete, dmxepath(C:/temp/dmxewriter_example.dmxe) indicator(FFED, VIX_IndexPX_LAST.D) freq(D) (click to run)

3. Delete log file of a DMXe file.
. dmxewriter deletelogs, dmxepath(C:/temp/dmxewriter_example.dmxe) (click to run)
# 6 Summary

This document provided an overview of the imf_datatools Python library. Topics such as installation, available resources and functions were covered, as well as usage through R and Stata. At this time there is no support for Matlab or EViews. For Matlab users, it is recommeneded that Python and the imf_datatools library be used as a system command to save any data in csv format and then reading that csv file in using Matlab. This way the imf_datatools can be used seamlessly
```python
from within Matlab.
```

Further planned enhancements include
- better handling of exceptions so they can be raised in Stata and R
- better handling of frequency of series
- distinguish between data not available and connection failures
- enhancements to the datacollector scripts and further output
The latest info on the project is available at the datatools website: http://datatools, and a link to the latest version of this document is also available.

## 6.1 Acknowledgements

The imf_datatools were developed while providing support to users as part of the Econometric Support team, starting around July 2018. Many thanks are due to everybody who provided support and feedback. The first step in adding true value was connecting to EcOS, many thanks to Jerry Chaves, Jobin Maliakal and Rajesh Nilawar and the EcOS/DMX team for their technical support. The possible outreach of the tools increased significantly with the introduction of Python integration in Stata 16, many thanks to Li Tang (Econometric Support) for her support, wisdom and knowledge of what Fund users want. Adeleke Adeyemi (Econometric Support) was kind enough to write the R part of this documentation and provide support for R users. Max Yarmolinski was kind enough to take on much of the underappreciated work of documentation and testing. Thanks to my economist friends Romain Lafarguette and Futoshi Narita for much-appreciated feedback and encouragement, and to the Automation Project team members who provided support as part of an iLabsponsored project. Many thanks to the following users for their interest and providing feedback:
- Ryan Yost
- Antoine Arnoud
- Chengyu Huang
- Di Yang
- Shiyao Wang

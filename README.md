# California Water Quality Analytics

If you're anything like I am, there is only 1 time of the year that is more exciting than any holiday: the release of the water quality reports! This project will be looking into the different facets of water quality throughout the state of California to provide insights on how to better utilize our most precious resource.  



## Project Pipeline: 
Milestone 1: Python - Decontaminate the Water Standards Table

Milestone 2: SQL - Add standards table, and fix the units in the raw data 

Milestone 3: Power BI/Tableau - Look at relative levels compared to the safety standards throughout the state

Milestone 4: Determine where True Crime fanatics may find false positives of attempted murder by poisoning their drinking water.

Milestone 5: Flask/Render - Deploy website with findings 

---


Data Source: https://data.ca.gov/dataset/water-quality-data
California Open Data Portal
California Department of Water Resources
Water Quality Data

Tables: 
1. Stations
2. Period of Record by Station and Parameter
3. Lab Results
4. Field Results
5. ArcGIS Map Service - https://gis.water.ca.gov/arcgis/rest/services/Geoscientific/i08_Stations_Discrete_Grab_Water_Quality/MapServer
6. ArcGIS Feature Service - https://gis.water.ca.gov/arcgis/rest/services/Geoscientific/i08_Stations_Discrete_Grab_Water_Quality/FeatureServer


Issue 1:  longitude is mostly positive, only 2 values were originally negative, but this plots the stations of California in China. All longitude values must be negative. 
Fix 1: -ABS(longitude) to all SQL tables in Power BI

---
# Milestone 1: The Water Standards
## Decontaminate.py

**Decontaminate.py** is a function with a series of subroutines to clean different aspects of the data, starting with the input of the raw pdf file, and outputting a csv to be input into a SQL server.

The output from the tabulated pdf is a list of lists. Each list represents a different class of pollutants in the water, such as radioactive, organics, disinfectants... 
Each list has a different length, three of them have columns that have been augmented, some list the number 0 as a string 'zero', and many of the NaN are represented as --

The column headings are not consistent and non-intuitive, so the first function will standardize the names of the columns to a meaningful measure.

## Decontaminate_Lables 
This identifies: 
- Contaminant 
- State Maximum Containment Level {State_MCL}
- State Detection Limit for reporting {State_DLR}
- State Public Health Goals (often smells and tastes) {State_PHG}
- Public Health Goal Date {PHG_Date}
- Federal Maximum Containment Level {Federal_MCL}
- Federal Maximum Containmnet Goal {Federal_MCLG}

## Decontaminate_Nulls
**Functionality:**
Decontaminate_Nulls() changes all '--' values in each list to a numpy NaN


## Decontaminate Rows
Looking through each of the tables from the original documentation and the tabulated data, the rows that do not call a contaminant will have one of the following issues in the 'State_MCL' column:
- It will be NaN
- It will say 'MCL'
- It may say 'mrem/yr' in the case of radioactive material

Some of the known contaminants truly have a NaN value for the State_MCL. 
This raises two question: 
- Is there an overarching Federal MCL that must already be met?
- Is this contaminant only a goal? 

If there is a Federal_MCL, the State_MCL will be set equal to the Federal_MCL, since it MUST be met. 
If there is NO Federal_MCL or State_MCL, the contaminant will not be included in this study. 

It was true in all tables that when there was no State_MCL, there was never a case where a Federal_MCL was present. The opposite was not the case. Because this remained true for all 14 categories, I was able to use the State_MCL column with anything containing a Null to remove that column, as it is either a header or a contaminant that is not applicable to the scope of the project. 

### Units
One thing that is missing from this table is the unit of measure of these specifications. Because the reporting is in different units at different sites, it will be important to convert the units to those which can be compared to the regulations. 
The default, as specified in the documentation, is mg/L unless otherwise specified. Since this is the case, this function will add an additional column 'Units' which will all be set to 'mg/L'. 


**Functionality:** 
Decontaminate_Rows() drops all rows that are subheaders in the invdivitual tables or with NULL values in the required columns. 
Although the units of this table are mostly in mg/L, most of the lab measurements were collected in ug/L, so this adjustment has been made to the units of all rows where the unit wasn't in mrem/yr or MCL. Since this column didn't exist in the original table, the units column was added with these considerations. 


## Decontaminate_Lists
Each of these were examined, paying attention to the PHG_Date and any NaN values, the best indicators of where the shifts occurred. Each of these tables were adjusted by dropping the column that contained all NaN values, and then using a dictionary to rename the other columns to the appropriate names. 

For those that are specified differently, their values will be adjusted on a case-by-case basis in the next function

### Column Discrepancies
There were discrepancies in the number of columns in three of the lists: 4, 7, and 11. Each of these were augmented in one of the earlier columns, changing the values to something incorrect, and then adding an additional Federal\rMCLG column at the end. 

**Functionality:**
Decontaminate_Lists() shifts the aberrant 3 tables within the list of tables and removes the additional augmenting column so that all tables are aligned properly



## Decontaminate_Values
This function addresses the issues that are specific to each list, and cannot be standardized across the rest of the documentation. 
Not all of the tables needed modifications, so those are not included here, such as 12 and 14.

**Functionality:**
Decontaminate_Values() is the workhorse of this function, making adjustments and corrections to dissimilarities in the naming, units, and value conversions when necessary to match the units and naming conventions of the lab data. Numerous chemicals were entered in the state regulations under a different chemical naming convention than those in the lab results. Similarly the units were not all in ug/L, so for each of these that were not, the values had to be converted and units adjusted. Furthermore, there were changes from character entries to numerical in this function. 

## Decontaminate_Datatypes
This has now fixed the issues within each of the tables, adjusting the units, changing any additional missing or unknown values to NaN, and changing any strings to numerical values when appropriate.
This function will be applied to the full dataframe after the individuals have been concatenated. 

**Functionality:** 
Decontaminate_Datatypes() ensures that each column has a single data type, converting any that is supposed to be numeric to that type, allowing for calculations and futher adjustments

## Decontaminate_Unit_Conversion
This function was implemented later in the process, after the discovery that most of the lab data is in ug/L rather than mg/L. Rather than going through every single row of the table and correcting each value by hand, this function multiplies the numerical values by 1000, the appropriate conversion from mg to ug to all applicable fields. Since this will also adjust the numeric 'corrected' values from the Decontaminate_Values function, those values were adjusted to meet the mg/L standard, thus expecting the conversion to ug/L.

**Functionality:**
Decontaminate_Unit_Conversion() multiplies all numeric standards (not the year) by 1000 to adjust for the conversion from mg to ug

## Decontaminate_Names
There was an issue when looking at the lab data in that almost all measurements included both dissolved and total amounts of each collected material. Upon further investigation of the state regulatory measures, the dissolved contaminant is the more appropriate measure for most, only with Total Chromium, which was explicitly stated in the table. Therefore, all contaminants were re-named to meet the naming convention of the lab results, adjusting to Dissolved ___ and the appropriate chemical naming conventions. 

**Functionality:** 
Changes the names of each contaminant that doesn't already match the naming convention of the lab results

## Decontaminate
The final function calls each of the subroutines in the order that was followed above. This function will take the filename of the pdf instead of having to previously perform that step. It concatenates all of the lists into a single dataframe before performing the calculations and renaming. 

**Functionality:**
Decontaminate() reads a .pdf file of the CA state regulations regarding water quality, processes this making adjustments to the units, naming, fixes problematic values and nulls, concatenates the lists and returns a .csv file with cleaned data that can be loaded into a SQL database. 



```
def Decontaminate(filename):
    from tabula import read_pdf
    from tabulate import tabulate
    import pandas as pd

    df_list = read_pdf(filename, pages='all')
    Decontaminate_Labels(df_list)
    Decontaminate_Nulls(df_list)
    Decontaminate_Rows(df_list)
    Decontaminate_Lists(df_list)
    Decontaminate_Values(df_list)
    df = pd.concat(df_list, ignore_index=True)
    Decontaminate_Datatypes(df)
    Decontaminate_Unit_Conversion(df)
    Decontaminate_Names(df)
    return df
```

This returns a cleaned dataframe with appropriate units, data types, and in a single concatenated table. 
### Milestone 1: Complete

--- 
# Milestone 2: SQL - Add standards table and fix units in the existing raw data

As I have been running queries to look at the lab data in concert with the state regulations, the initial 'completion' of milestone 1 was retracted a bit, since I discovered that there were different chemical naming conventions used in the lab data, unit differences, etc. (all mentioned above). So as the queries have been performed, the Decontaminate function has also been modified to allow for minimal processing of the lab_results table. 

## Where things currently stand:
The discrepancies in the lab_results table are those in which different labs collected data with different units of measure. These are listed in the file Mismatch_Results.md in the 02_State_Regulation_Processing folder. Most of them contain labs that measured in either ug/L or mg/L for the same contaminant. Mercury was measured with 3 different units, also adding ng/mL. 

Since I do NOT want to acutally modify anything in the actual results, I can use calculated tables in SQL Server to make the appropriate conversions, and create a new table that can be used in Tableau. 

Furthermore, upon investigation, only 1/7th of the lab results are regulated in the state_regulations table. Since the purpose of this project is to look at the regions that near or exceed the regulatory limits, I have created a truncated table from the results of a Join of the state regulations with the results of the lab findings. This will allow for faster processing with the calculated tables and such. 
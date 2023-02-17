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
## The File

The output from the tabulated pdf is a list of lists. Each list represents a different class of pollutants in the water, such as radioactive, organics, disinfectants... 
Each list has a different length, three of them have columns that have been augmented, some list the number 0 as a string 'zero', and many of the NaN are represented as --

The column headings are not consistent and non-intuitive, so the first function will standardize the names of the columns to a meaningful measure.

## Decontaminate Lables 
This identifies: 
- Contaminant
- State Maximum Containment Level
- State Detection Limit for reporting
- State Public Health Goals (often smells and tastes)
- Public Health Goal Date
- Federal Maximum Containment Level
- Federal Maximum Containmnet Goal

## Decontaminate_Nulls
This next function aims to change all '--' values in each list to a numpy NaN

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

For those that are specified differently, their values will be adjusted on a case-by-case basis in the next function

### Column Discrancies
There were discrepancies in the number of columns in three of the lists: 4, 7, and 11. Each of these were augmented in one of the earlier columns, changing the values to something incorrect, and then adding an additional Federal\rMCLG column at the end. 


## Decontaminate Lists
Each of these were examined, paying attention to the PHG_Date and any NaN values, the best indicators of where the shifts occurred. Each of these tables were adjusted by dropping the column that contained all NaN values, and then using a dictionary to rename the other columns to the appropriate names. 


## Decontaminate Values
This function addresses the issues that are specific to each list, and cannot be standardized across the rest of the documentation. 

Not all of the tables needed modifications, so those are not included here, such as 12 and 14.

## Decontaminate_Datatypes
This has now fixed the issues within each of the tables, adjusting the units, changing any additional missing or unknown values to NaN, and changing any strings to numerical values when appropriate.
This function will be applied to the full dataframe after the individuals have been concatenated. 

## Decontaminate
The final function calls each of the subroutines in the order that was followed above. This function will take the filename of the pdf instead of having to previously perform that step. It will finally concatenate all of the lists into a single output. 


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
    return df
```

This returns a cleaned dataframe with appropriate units, data types, and in a single concatenated table. 
### Milestone 1: Complete

--- 
# Milestone 2: SQL - Add standards table and fix units in the existing raw data
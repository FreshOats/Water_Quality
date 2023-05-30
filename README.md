# I Think I'm Being Poisoned...
## [An Investigation of Contaminants Present in California's Drinking Water](https://public.tableau.com/views/IThinkImBeingPoisoned-AWaterQualityAnalysis/TitlePage?:language=en-US&:display_count=n&:origin=viz_share_link)

If you're anything like I am, there is only 1 time of the year that is more exciting than any holiday: the release of the annual water quality report! This project looks into the past and present chemical contamination in the state of California to provide insights on how to better understand the safety of our most precious resource.  

The project was broken down into several phases, starting with the data acquisition and exploratory data analysis. The next phase was the ETL, which was the bulk of the project - the contaminated water data were unclean on a level that rivals some of the counties' water supplies. After the cleaned data were loaded to a SQL server, a series of queries were used to find relationships and patterns with safe, unsafe, and dangerous levels of contaminants. The third phase was creating a series of dashboards to showcase the findings using Tableau. And finally the final deployment of the visualizations, programming, and overall assessment of the water quality. 

Data were acquired from the California Open Data Portal, which provided drinking water reports back as far as 1909. There were very comprehensive data covering field results and lab results, but most of the measures and standards set don't reflect the safety of the water, for example the pH and turbidity of the water. Similarly the amount of sediment, smells, and flavors in the water have goals by the California State Water Board, but these do not impact the health and safety of the drinking water. 

The standards that were used for this project came from the California Water Board in a file last updated on January 3, 2023, titled 'MCLs, DRLs, PHGs, for Regulated Drinking Water Contaminants', set by the Office of Environmental Health Hazard Assessment (OEHHA) in California as well as including the federal regulations set by the United States Envioronmental Protection Agency (USEPA). In all cases considered, the OEHHA regulations were stricter than the USEPA regulations. At this point I would like to note that all of the contaminants in the regulatory documentation were chemical contaminants. These did not include biological contaminants such as e. coli, salmonella, etc. Therefore the scope of this project and findings are limited to chemical contaminants in California's drinking water during the years when such contaminants were measured. 


## Project Pipeline: 
Milestone 1: Python - Decontaminate the Water Standards Table

Milestone 2: SQL - Add standards table, and fix the units in the raw data 

Milestone 3: Tableau - Look at relative levels compared to the safety standards throughout the state

Milestone 4: Deploy with findings 

---

Data Source: [data.ca.gov](https://data.ca.gov/dataset/water-quality-data)
California Open Data Portal
California Department of Water Resources
Water Quality Data

The tables provided with the original data from the Open Data Portal: 
1. Stations
2. Period of Record by Station and Parameter
3. Lab Results
4. Field Results
5. ArcGIS Map Service
6. ArcGIS Feature Service

---
# Milestone 1: The Water Standards
The first phase of the project involved the data acquisition, exploratory data analysis, and ETL (extract, transform, load). The files from the EDA remain in the 01_EDA folder in the Repository, and utilized a combination of Jupyter files to look at the data as well as uploading to SQL server to do a series of queries to get a better understanding of what these data contained. 

Following this, the next hurdle was extracting the OEHHA and USEPA standards from the regulatory guide, which was only available in .pdf format, broken into numerous tables, not all with matching dimensions. The files related to this processing are in the folder 02_State_Regulation_Processing. The result of the data processing was the file Decontaminate.py, which reamins in the MAIN. The following outlines the program Decontaminate.py and the subroutines used to clean the data and what cleaning processes were needed to organize and provide matching cases to the data that would be joined in the lab_results of the raw data.

It must be noted at this time, that this was a very iterative process, since there were many conventions, units, and naming discrepancies between the standards and the acquired data in the lab_results, even across different water stations. Since the standards table is unlikely to add many new fields, I opted to make the changes in convention and units to this table.

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

This returns a cleaned dataframe with appropriate units, data types, and in a single concatenated table. To ensure the fidelity of the raw data from Lab Results, any modifications or calculations to these data will be done with the addition of calculated tables in either SQL or Tableau, which will add additional columns to make such adjustments, and not actually change the data. Thus, this concludes the processing for the first mileston. 

### Milestone 1: Complete

--- 
# Milestone 2: SQL - Add standards table and fix units in the existing raw data

As I have been running queries to look at the lab data in concert with the state regulations, the initial 'completion' of milestone 1 was retracted a bit, since I discovered that there were different chemical naming conventions used in the lab data, unit differences, etc. (all mentioned above). So as the queries have been performed, the Decontaminate function has also been modified to allow for minimal processing of the lab_results table. 

## Cleaning the lab_results data
To maintain the fidelity of the original data, this table was not altered in Python, and rather these data were adjusted using SQL to create a new output table that could reduce the processing power and time needed to perform the necessary queries as well as import into Tableau for the creating of visualizations. 

### Units and Conversions
The first minor hurdle was adjusting the units from either ug/L or mg/L, and because some of the labs measured the same contaminants with different units, I used the CASE clause to filter and multiply the value from the results column and output this value in a new column named "Fixed_Result". Furthermore, there were issues with the measurements of the Nitrates. There are 2 different methods to measure nitrate and nitrite concentrations - the direct concentration in mg/L, and the free nitrogen ion concentration, which, after doing some quick chemistry, requires multiplication by a factor to change the concentration of nitrate to the concentration of free nitrogen by how much nitrogen is present in the nitrate or nitrite. The only potentially problematic calculation would be the nitrate + nitrate, since there is no measure of the relative concentrations of each, but, fortunately, all of these measurements were made in mg/L as N, so no adjustments or assumptions needed to be made. 

### Creating the New Truncated Table
After each of the conversions and unit adjustments were made, I used the SELECT * INTO () to create a new table named regulated_contaminants. This table joined the state_regulations table with the lab results using a LEFT JOIN; thus, none of the contaminants that were measured by the lab that did not have regulatory standards were not included in the query output. This query applied the CASE changes for the unit conversions and such. As a result, this output table included all of the original data from the state_regulations and the lab_results, but it also included the additional column with the fixed_result, including the calculations made to the results column in the CASE clause. 

## Investigating the Data
Using SQL, I wanted to look at the contaminants over time, but I really wanted to focus on the results from the past 5 years, so anything since January 1, 2018. Through a series of queries, I used both WITH clauses (common table expressions) and window functions to investigate the contaminants and their relative levels with regard to the state maximums. Ultimately, from these analyses, I had a good sense of what I wanted to show in the Tableau visualizations, only I was able to run these queries very quickly and identify potential relationships to look into. 


The creation of the regulated_contaminants table in conjunction with the queries that led to an outline of what I need to show in visualizations completes milestone 2.
### Milestone 2: Complete


--- 
# Milestone 3: Tableau
[I Think I'm Being Poisoned...](https://tinyurl.com/2mef2b97)
Tableau was used to create a completely interactive multi-page site to showcase the contaminants that have exceeded the current state levels for safe water going back 75 years as well as only considering the past 5  years. It provides information by station and county. Each map and graph can be observed using 75 or 5 years of data. After the assembly of the EPA and the discovery of the dangers of different fertilizers and pesticides, the acceptible levels of these toxins were reduced, so while the data from the past 75 years show high averages, the past five years may yield an average of 0.0% in the drinking water. It is important to see the history of the contaminants in the water, because while it may no longer be present in drinking water, it may still have persistent contamination in the soil.

Individual pages were created for the 8 most prevalent or dangerous contaminants in California: Antimony, Arsenic, Chromium, Lead, Mercury, Nitrate and Nitrite, and Strontium. Facts about these contaminants can be accessed on a page that shows their county-wide distribution and concentration, the history by county, and a bar graph showing the counties with a non-zero measure of that contaminant compared to the safe concentration set by the CA-EPA. On these pages, the user can also select the county on the map to see specific information on the timeline and bar graphs - the y-axis automatically adjusts to the highest level prior to selection, but upon selection it automatically adjusts to the maximum on that county. 

The other pages show the 2022 state audit of safe water in California, showing that 2.6% of Californians, just less than 1 million residents, do not have access to safe water and are receiving contaminated water. That being said, not all contaminants are equal. The threat of a low-concentration exposure to arsenic or lead is substantially more concerning than an unsafe concentration of antimony, strontium, or nitrate. Following this analysis, all contaminants investigated are presented, also showing the difference between unsafe and dangerous. Continuing, there is a page that provides information to people who may live in an are with potentially contaminated water, with links and resources to determine whether this is the case.

Additional concerns by the CA State Auditor was that there were over 370 failing water systems in the state, providing 920,000 residents, but even more concerning are the over 450 additional water systems that are nearing failing levels that do serve over 1,000,000 additional residents. While this information is very concerning, again I have to return to the fact that all contaminants are not equal. Having unsafe water isn't the same as having dangerous water, and long-term exposure to strontium may have no effect on adults, whereas long-term exposure of arsenic will. 

Two final pages provide resources and solutions for dealing with contaminated water. Since most of the regions with contaminated water are located in the Central Valley, and the majority of consumers without access to safe water tend to be in lower-income regions, the majority of solutions are provided with renters in mind. An expensive installation of a top-of-the-line reverse osmosis system is not only out of the price-range, but also likely not something that a renter can even install. There is a broad range of renter-friendly solutions including pitchers with specialized filters, faucet filters with specialized filters, and even counter-top Reverse Osmosis and Distillation filtration systems that attach to a faucet but can be removed if necessary. The caveat to the cheaper solutions of the pitchers and faucet filters, specialized filters must be purchased to ensure that they are filtering out the contaminants that are present - Arsenic is not removed by most over-the-counter filters, but there are available filters by PUR and ZeroWater that remove such. 

### Color Scheme
Since these measurements are continuous and each of the contaminants is measured on a different scale for their detrimental effects, the colors have been adapted to normalize the contaminants. The colors range on the maps from white to red. The maximum in the color scale is 2x the state maximum concentration. 

In the charts and graphs, the color scale is a diverging scale, which is yellow in the safe region, and then gets redder as it approaches and passes the state maximum. The maximum on the scale has also been set to 2x the state maximum. The center of the scale was set to 1/5 of the maximum in each of them, to ensure fidelity of the color scheme and easier interpretation when comparing the contaminants. Since the Y-scaling of the graphs are so different, they have not been normalized to the state maximum, as many of the tables would not be visible. The tables only include entries that contained at least one measurement above 0. 

### Map backgrounds
To achieve the effect of the danger and maintain a dark background for the vis, I'm using the Dark map. It's as not necessary to see the streets and cities as it is to see the distribution of locations, and upon hover-over, the county names and relative levels are shown. I have only included the city names on the timeline map, since this is the only one that isn't covered such that it would be difficult to impossible to see the city names, as they would be covered by the data elements. 


### Animations and Buttons
The title page utilizes and animation that walks through 75 years of contamination data that exceeds the threshold. Each page has a set of Navigation buttons that redirect to different pages like a website, and in addition has buttons that show or hide either text, a menu, or images.

### Individual Contaminants
The 8 contaminants that are either exceeding limits in California or are just known as particularly dangerous each have their own dashboard. These dashboards show a map broken up by county with the level of contaminant, and the color scheme going from gray - benign to red - toxic. Linked to the counties on the map are two graphs, one bar graph to show all of the counties' levels of that contaminant in relation to the state maximum level, and another that shows a timeline from the earliest measurements through 2022. For the first 2 visuals, there is a page selection that allows the user to look at the differences between the results of the past 75 years and the past 5 years alone. 

The Tableau visualization was publised on Tabluea Public as 'I think I'm Being Poisoned', which can be found with the link:
[I Think I'm Being Poisoned...](https://tinyurl.com/2mef2b97)

This completes the 3rd milestone. 

### Milestone 3: Complete

--- 
# References
Data Source: https://data.ca.gov/dataset/water-quality-data <br>
Standards Source: https://www.waterboards.ca.gov/drinking_water/certlic/drinkingwater/documents/mclreview/mcls_dlrs_phgs.pdf <br>
https://www.cdph.ca.gov/
https://calepa.ca.gov/
https://www.epa.gov/sdwa/chromium-drinking-water
https://www.waterboards.ca.gov/lahontan/water_issues/projects/pge/
https://www.who.int/news-room/fact-sheets/detail/arsenic
https://www.knowyourh2o.com

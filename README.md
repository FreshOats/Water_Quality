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

## Cleaning the lab_results data
To maintain the fidelity of the original data, this table was not altered in Python, and rather these data were adjusted using SQL to create a new output table that could reduce the processing power and time needed to perform the necessary queries as well as import into Tableau for the creating of visualizations. 

### Units and Conversions
The first minor hurdle was adjusting the units from either ug/L or mg/L, and because some of the labs measured the same contaminants with different units, I used the CASE clause to filter and multiply the value from the results column and output this value in a new column named "Fixed_Result". Furthermore, there were issues with the measurements of the Nitrates. There are 2 different methods to measure nitrate and nitrite concentrations - the direct concentration in mg/L, and the free nitrogen ion concentration, which, after doing some quick chemistry, requires multiplication by a factor to change the concentration of nitrate to the concentration of free nitrogen by how much nitrogen is present in the nitrate or nitrite. The only potentially problematic calculation would be the nitrate + nitrate, since there is no measure of the relative concentrations of each, but, fortunately, all of these measurements were made in mg/L as N, so no adjustments or assumptions needed to be made. 

### Creating the New Truncated Table
After each of the conversions and unit adjustments were made, I used the SELECT * INTO () to create a new table named regulated_contaminants. This table joined the state_regulations table with the lab results using a LEFT JOIN; thus, none of the contaminants that were measured by the lab that did not have regulatory standards were not included in the query output. This query applied the CASE changes for the unit conversions and such. As a result, this output table included all of the original data from the state_regulations and the lab_results, but it also included the additional column with the fixed_result, including the calculations made to the results column in the CASE clause. 

## Investigating the Data
Using SQL, I wanted to look at the contaminants over time, but I really wanted to focus on the results from the past 5 years, so anything since January 1, 2018. Through a series of queries, I used both WITH clauses (common table expressions) and window functions to investigate the contaminants and their relative levels with regard to the state maximums. Ultimately, from these analyses, I had a good sense of what I wanted to show in the Tableau visualizations, only I was able to run these queries very quickly and identify potential relationships to look into. 

---

The creation of the regulated_contaminants table in conjunction with the queries that led to an outline of what I need to show in visualizations completes milestone 2.
### Milestone 2: Complete




--- 
# Milestone 3: Tableau
https://public.tableau.com/views/Water_Quality_16833247481940/StrontiumCountyAvg?:language=en-US&publish=yes&:display_count=n&:origin=viz_share_link

I have started creating dashboards containing both maps as well as bar graphs showing the relative levels, maximums and averages of the typical offenders - Chromium, Lead, and Mercury, and then looked at the contaminants that are higher than the state standards for California. Since these data go back nearly 80 years for some of the measures, there are some HUGE differences over time, which have definitely impacted the averages. That being said, most of the graphs and analyses in Tableau restrict the data to the beginning of 2018 through 2022. This way there is a better measure of the recent levels of these contaminants.

I have organized the data such that we can see the individual stations, and where they are located on the map along with maximum levels, and then following that with county average levels. I also have a by-county selectable chart in each that allows the user to investigate the levels over time. I think that it would make the most sense to put all of these in the same dash, since the user can then scroll through all of the counties at once, seeing the changes in chemicals over time. It is not currently organized this way, but will be in the future. 

Finally, there is a map that only looks at the contaminants that still hold concentrations that are at least 2x the state maximum allowable. This map shows the individual stations. 
Each of the graphs and maps contain both the state maximum and federal (if it exists) in addition to the measured concentration and county.

### Color Scheme
Since these measurements are continuous and each of the contaminants is measured on a different scale for their detrimental effects, the colors have been adapted to normalize the contaminants. The colors range on the maps from white to red. The maximum in the color scale is 2x the state maximum concentration. 

In the charts and graphs, the color scale is a diverging scale, which is yellow in the safe region, and then gets redder as it approaches and passes the state maximum. The maximum on the scale has also been set to 2x the state maximum. The center of the scale was set to 1/5 of the maximum in each of them, to ensure fidelity of the color scheme and easier interpretation when comparing the contaminants. Since the Y-scaling of the graphs are so different, they have not been normalized to the state maximum, as many of the tables would not be visible. The tables only include entries that contained at least one measurement above 0. 

### Map backgrounds
I really like the maps that show the cities and streets because they give a better reference as to where in the state the stations are, but they make it very difficult to interpret the data. Perhaps I can create 2 pages, one with the street map and the second with the normal or dark for better contrast of where in the state the contaminants are - that way the user can look at familiar locations on the street map and then see how many measurements were taken in the other map or vice versa. 

### Updates to Animations and First 2 pages on Tableau
I've added maps that show 113 years of all contamination over 100%, which can be a little misleading, so there is a button to go to the same map looking at the yearly change in an animation. 

The next page created has been the changes over year of the 8 main contaminants... I'm not sure how impactful this is, given that the contaminants that go really high are way off the charts. 

I'm thinking for the next set of pages, I'll run through each of the chemicals on their own 'page', which I think I can make into something that can just be filtered. This may be a better place to put the county charts, the map with the county averages and then talk about the dangers and impacts of each of the contaminants. 

I should probably list all of the contaminants that have ever been found to exceed the state maximum level on the last page? Maybe briefly discuss the impact each of them had? 

#### Buttons
I've figured out how to make buttons, which are really useful for making it more like a website. I need to make sure that there is enough space on each page for some text. 


--- 
## Now has several pages for reports and contaminants
- I have organized the "Investigate Contaminants" so that there is a nav button that links to each contaminant. Each of these pages will show a map that can be clicked on to look at the specific county. There is a graph that updates with the county selection to show the avg. concentration of that contaminant over time from 1947 to 2022. Additionally, I've included two time points, one investigating the past 75 years, and the other looking at the past 5. 
- The title page still shows the scare-map with the Max Levels since 1947 per station, but with the button click will go to an automation that allows the user to see station maximums each year
- The next page has information from the california audit in 2022, assessing the number of failing water treatment systems and addressing how many people (about 1 million) do not have accesss to water that meets state regulations, and the number of failing stations per county
- Another page will show the worst counties from the past 5 years only - these only report counties that are at least 100%, but I think I'm going to reduce it to 90% of the maximum
- There is a page that shows all of the contaminants that were reported - not sure if this is necessary
- The last page is all about what you can do, with solutions both for homeowners capable of installing a system, or for those who can only use a counter-top or faucet solution. 

The last major steps will be to add the written content for each of the pages, then format the content on each page for consistency. 

I did look into poisonings, but it was a dead end. I think what's more important at this point is to aim to help people find the resources to get water tested, find water reports, and get access to safe water if they live in a questionable area. 



--- 
DB 1: I think I'm being poisoned
This contains the maps with all Max and Timeline
Navigation Links across the top
Button to change from 75 to timeline
Currently Contains "Investigate Contaminants" button

Text: 
This is an investigation of chemical contaminants in California's drinking water. The data were acquired from the CA government lab analyses from each water station in the state. The state standards set by the EPA were used as the reference to determine whether levels exceed the safe level or not. To be clear, 'safe' is used per the determination by the state's determination. In other words, if the level exceeds the safe level, it is not necessarily 'dangerous', it just exceeds the pre-determined safe level. Certain contaminants will be discussed more throroughly, including levels considered 'dangerous' by the CDC.

--- 
DB 2: State Auditor 2022 on the drinking water situation
Two maps of CA showing # of people without safe water, # of failing water systems
Contains all buttons

Text: Nearly 1 million residents of California live in areas that fail to meet the safety regulations for one or more contaminant. 
Most of these places are located in the central valley, and the residents who are impacted the most live in areas of lower socioeconomic status. There are about 30 million residents of California, so roughly 1/30th of the state's population is impacted by unsafe water. 

While these data show where the water systems are failing, they do not show which contaminants are above the state levels. Not all contaminants are created equally: the long-term health impacts of exposure to higher levels of nitrates is substantially different from long-term exposure to metals like lead or arsenic. 

---
DB 3: COntaminants
This shows a list of the contaminants that were both listed in the state regulatory information and tested for by at least one of the stations. All null values were excluded in these analyses, as they indicated that no data were collected at that site or time. These contaminants come from several sources: naturally occurring contaminants, pesticides, and fertilizers are the most common sources that introduce these contaminants into the water. it should be noted that the presence of these contaminants in the data shows the level after water treatment - this is the water that will be provided to consumers. 

Click on the "Investigate Contaminants" Button to find links to the contaminants that are either infamous or measured as unsafe in at least one county. Each of these pages will give historical information as well as a recent subset of the data. Furthermore, the health impact of these contaminants will be provided.  

--- 
DB 4: Dangerous Places
The table shows the maximum concentration of a particular contaminant from a station within the counties presented. The value shown is only from a single station, and it represents the worst source of water from within that county. The maximum was included here, as many of the stations measure 0 ug/L of these contaminants, so an average or median measurement doesn't demonstrate the safety concerns of the residents receiving water from that source. There is at least one station within these counties that yields the values presented. 

The two contaminants that have the highest measurements are arsenic and strontium. The impact of strontium is minimal compared to that of arsenic. Strontium can be considered dangerous to very young children, as with constant exposure to strontium, the metal can interfere with natural bone development. Arsenic is usually thought of as a poison - and it can be lethal at high doeses. At a low concentration, the body metabolizes arsenic within 48 hours. This is not the concern we need to consider. The long-term exposure to low doses of arsenic can cause _____, and these effects occur in people of all ages. 

# Maybe list these in order from dangerous to least dangerous? 
Arsenic
Mercury
Strontium
Antimony
Nitrate?

---
DB 5: Help!
Copy test from Tableau. 
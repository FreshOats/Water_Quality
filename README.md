# California Water Quality Analytics

If you're anything like I am, there is only 1 time of the year that is more exciting than any holiday: the release of the water quality reports! This project will be looking into the different facets of water quality throughout the state of California to provide insights on how to better utilize our most precious resource.  


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
CREATE DATABASE WaterQuality;

-- DROP TABLE dbo.lab_results
CREATE TABLE lab_results (
    station_id INT, 
    station_name VARCHAR(500), 
    full_station_name VARCHAR(500), 
    station_number VARCHAR(250), 
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    status_ VARCHAR(250),
    county_name VARCHAR(250),
    sample_code VARCHAR(250),
    sample_date DATETIME,
    sample_depth VARCHAR(50),
    sample_depth_units VARCHAR(250),
    parameter VARCHAR(250), 
    result FLOAT,
    reporting_limit FLOAT,
    units VARCHAR(250),
    method_name VARCHAR(250)
);

SELECT * 
FROM dbo.lab_results;

BULK INSERT dbo.lab_results
FROM "C:\Users\justi\OneDrive\Desktop\Analytics\Water_Quality\Data\lab_results.csv"
WITH 
(
	FORMAT = 'CSV',
	FIRSTROW = 2
)
GO
;

-- Verify that these rows match
SELECT COUNT(station_id) AS Station_ID, COUNT(latitude) AS Lat, COUNT(longitude) AS Lon
FROM dbo.lab_results;
-- There are more station ids than coordinates, but the lat/long match

--DROP TABLE period_of_record;
CREATE TABLE period_of_record (
    station_id INT, 
    station_name VARCHAR(250), 
    full_station_name VARCHAR(250), 
    station_number VARCHAR(250), 
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    county_name VARCHAR(250),
    parameter VARCHAR(250),
    sample_count INT,
    sample_date_min DATETIME,
    sample_date_max DATETIME
);

BULK INSERT dbo.period_of_record
FROM "C:\Users\justi\OneDrive\Desktop\Analytics\Water_Quality\Data\period_of_record.csv"
WITH 
(
	FORMAT = 'CSV',
	FIRSTROW = 2
)
GO
;

SELECT COUNT(station_id) AS Station_ID, COUNT(latitude) AS Lat, COUNT(longitude) AS Lon
FROM dbo.period_of_record
-- Again, a few hundred station IDs don't have coordinates

--DROP TABLE dbo.field_results;

CREATE TABLE field_results (
    station_id INT, 
    station_name VARCHAR(500),
    station_number VARCHAR(250),
    full_station_name VARCHAR(500), 
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    status_ VARCHAR(250),
    county_name VARCHAR(250),
    sample_code VARCHAR(250),
    sample_date DATETIME,
    sample_depth VARCHAR(50),
    sample_depth_units VARCHAR(250),
    anl_data_type VARCHAR(50),
    parameter VARCHAR(500), 
    fdr_result FLOAT,
    fdr_text_result VARCHAR(500),
    fdr_date_result VARCHAR(250),
    fdr_reporting_limit FLOAT, 
    uns_name VARCHAR(50),
    mth_name VARCHAR(50),
    fdr_footnote VARCHAR(MAX)
);

BULK INSERT dbo.field_results
FROM "C:\Users\justi\OneDrive\Desktop\Analytics\Water_Quality\Data\field_results.csv"
WITH 
(
	FORMAT = 'CSV',
	FIRSTROW = 2
)
GO
;

SELECT COUNT(station_id) AS Station_ID, COUNT(latitude) AS Lat, COUNT(longitude) AS Lon
FROM dbo.field_results
-- There are 30 station IDs without coordinates

-- DROP TABLE dbo.stations;
CREATE TABLE stations (
    station_id INT, 
    station_name VARCHAR(500),
    full_station_name VARCHAR(500), 
    station_number VARCHAR(250),
    station_type VARCHAR(250),
    latitude FLOAT,
    longitude FLOAT,
    county_name VARCHAR(250),
    sample_count INT,
    sample_date_min DATETIME,
    sample_date_max DATETIME
);


BULK INSERT dbo.stations
FROM "C:\Users\justi\OneDrive\Desktop\Analytics\Water_Quality\Data\stations.csv"
WITH 
(
	FORMAT = 'CSV',
	FIRSTROW = 2
)
GO
;

SELECT COUNT(station_id) AS Station_ID, COUNT(latitude) AS Lat, COUNT(longitude) AS Lon
FROM dbo.stations
-- Same situation as before

-- DROP TABLE dbo.state_regulations
CREATE TABLE state_regulations (
	contaminant VARCHAR(250) NOT NULL, 
	state_max FLOAT NOT NULL, 
	state_det_limit FLOAT, 
	state_health_goal FLOAT, 
	state_health_date INT, 
	federal_max FLOAT,
	federal_max_goal FLOAT, 
	reg_units VARCHAR(50)
);

BULK INSERT dbo.state_regulations
FROM "C:\Users\justi\OneDrive\Desktop\Analytics\Water_Quality\Data\state_regulations.csv"
WITH 
(
	FORMAT = 'CSV',
	FIRSTROW = 2
)
GO
;

SELECT *
FROM dbo.state_regulations
;

-- This will create the subset of lab results that contains only the contaminants found on the regulatory table
SELECT * INTO regulated_contaminants
FROM
    (SELECT s.Contaminant,
            s.State_MCL AS State_Max,
            s.Federal_MCL AS Federal_Max,
            s.Units AS Reg_Units,
            l.*
     FROM state_regulations s
     INNER JOIN lab_results l ON l.parameter = s.Contaminant) AS regulated_contaminants;